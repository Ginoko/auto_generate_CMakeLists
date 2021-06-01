"""
====================
CMakeLists Generator
====================

:Date: 2021-01-26
:Version: 1.0.0
:Author: Ginoko
:Contact: ginorasakushisu666@gmail.com
"""
import sys
import os
import getopt
import platform
import re
import traceback

is_windows = True


class LanguageConfiguration:
    __type_value_map = {
        "c": ["90", "99", "11"],
        "c++": ["98", "11", "14", "17", "20"]
    }

    def __init__(self, language_type: str, language_version: str):
        self.type = language_type.lower()
        self.version = language_version

    def check_valid(self) -> bool:
        """

        :returns: True -> valid, False -> invalid
        """
        if self.type not in self.__type_value_map or \
                self.version not in self.__type_value_map[self.type]:
            return False
        else:
            return True


class CMakeListsGenerator:
    __cmake_minimum_version = "2.8.0"
    __ignore_list = [
        ".svn",
        ".idea",
        "cmake-build-debug"
    ]

    def __init__(self,
                 project_root: str = None,
                 project_name: str = None,
                 language_type: str = "c",
                 language_version: str = "90"):
        if not project_root:
            self.root = os.getcwd()
        else:
            if not os.path.exists(project_root):
                print("**project root parsing error!**")
                raise ValueError
            self.root = project_root

        if not project_name:
            self.name = self.__get_path_last_trim(self.root)
        else:
            self.name = project_name

        self.language = LanguageConfiguration(language_type, language_version)
        if not self.language.check_valid():
            print("**language configuration parsing error!**")
            raise ValueError

    @staticmethod
    def __get_path_last_trim(path: str) -> str:
        """

        :param path: directory path
        :return:
        """
        if is_windows:
            path_list = path.split("\\")
        else:
            path_list = path.split("/")
        trim = path_list[-1]
        if len(path_list) == 1 or trim == "":
            trim = "my_project"
        return trim

    @staticmethod
    def __is_code_file(file_name: str) -> bool:
        ext = file_name.split('.')[-1].lower()
        if ext == "c" or ext == "cc" or ext == "cpp" or ext == "cu" or ext == "h":
            return True
        else:
            return False

    @staticmethod
    def __generate_minimum_version(version: str) -> str:
        return "cmake_minimum_required(VERSION %s)\n" % version

    @staticmethod
    def __generate_project_name(name: str) -> str:
        return "project(%s)\n" % name

    @staticmethod
    def __generate_language_standard(config: LanguageConfiguration) -> str:
        if config.type == "c":
            output = "set(CMAKE_C_STANDARD %s)\n" % config.version
        else:
            output = "set(CMAKE_CXX_STANDARD %s)\n" % config.version
        return output

    @staticmethod
    def __generate_include_dir(dir_path_list: list) -> str:
        output = ""
        for dir_path in dir_path_list:
            output += "include_directories(%s)\n" % dir_path
        return output

    @staticmethod
    def __generate_source_file(project_name: str, file_path_list: list) -> str:
        output = "add_executable(" + project_name + '\n'
        for file_path in file_path_list:
            output += "        " + file_path + '\n'
        output += ')'
        return output

    def __check_ignore_dir(self, dir_path: str):
        for ignore_path in self.__ignore_list:
            if ignore_path in dir_path:
                return True
        return False

    def __absolute_path_to_relative_path(self, path: str) -> str:
        if is_windows:
            if re.match('^[A-Za-z]:', path, re.I):
                return path.split(self.root)[-1].strip('\\')
        else:
            if path[0] == '/':
                return path.split(self.root)[-1].strip('/')

    def print_config(self):
        print("using config:")
        print("\t[project root]: %s" % self.root)
        print("\t[project name]: %s" % self.name)
        print("\t[language type]: %s" % self.language.type)
        print("\t[language version]: %s" % self.language.version)

    def generate(self) -> None:
        count = 1
        exist_code_file = False
        dir_queue = []
        file_queue = []

        print("*************GENERATOR*STARTING*************")

        for root, dirs, files in os.walk(self.root):
            if self.__check_ignore_dir(root):
                continue
            print("[GENERATOR]located in dir: " + root)

            relative_root_list = root.split(self.root)
            relative_root = relative_root_list[1] if len(relative_root_list) > 1 else ""
            relative_root = relative_root.strip('\\').strip('/').replace('\\', '/')

            for name in files:
                if self.__is_code_file(name):
                    print("[GENERATOR]read code file: " + name)
                    if relative_root == "":
                        name_with_path = name
                    else:
                        name_with_path = relative_root + '/' + name
                    file_queue.append(name_with_path)
                    exist_code_file = True
                    count += 1
            if exist_code_file and relative_root != "":
                dir_queue.append(relative_root)
            exist_code_file = False

        with open("CMakeLists.txt", "w") as cmake_file:
            cmake_file.write(self.__generate_minimum_version(self.__cmake_minimum_version))
            cmake_file.write(self.__generate_project_name(self.name))
            cmake_file.write('\n')
            cmake_file.write(self.__generate_language_standard(self.language))
            cmake_file.write('\n')
            cmake_file.write(self.__generate_include_dir(dir_queue))
            cmake_file.write('\n')
            cmake_file.write(self.__generate_source_file(self.name, file_queue))

        print("*************GENERATOR*ENDING*************")


def relative_path_to_absolute_path(path: str) -> str:
    if is_windows:
        if re.match('^[A-Za-z]:', path, re.I) is None:
            return (os.getcwd() + path).strip('\\')
    else:
        if path[0] != '/':
            return (os.getcwd() + path).strip('/')
    return path


def main(argv) -> None:
    options, args = getopt.getopt(argv, "r:n:t:v:d:", ["root=", "name=", "type=", "version="])
    project_root = None
    project_name = None
    language_type = "c"
    language_version = "90"
    for option, value in options:
        if option in ("-r", "--root"):
            project_root = str(value)
            print("config-read: root[%s]" % project_root)
        elif option in ("-n", "--name"):
            project_name = str(value)
            print("config-read: name[%s]" % project_name)
        elif option in ("-t", "--type"):
            language_type = str(value)
            print("config-read: type[%s]" % language_type)
        elif option in ("-v", "--version"):
            language_version = str(value)
            print("config-read: version[%s]" % language_version)
    project_root = relative_path_to_absolute_path(project_root)
    generator = CMakeListsGenerator(project_root,
                                    project_name,
                                    language_type,
                                    language_version)
    generator.print_config()
    generator.generate()


def check_platform() -> None:
    global is_windows
    system = platform.system()
    if system != "Windows":
        is_windows = False


if __name__ == '__main__':
    try:
        check_platform()
        main(sys.argv[1:])
    except Exception as e:
        print("repr(e): %s" % repr(e))
        print("traceback.format_exc(): %s" % traceback.format_exc())
