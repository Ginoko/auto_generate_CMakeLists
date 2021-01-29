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


class LanguageConfiguration:
    __type_value_map = {
        "c": ["90", "99", "11"],
        "c++": ["98", "11", "14", "17", "20"]
    }

    def __init__(self, language_type: str, language_version: str):
        """

        :param language_type:
        :param language_version:
        """
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
        try:
            path_list = path.split("\\")
            if len(path_list) == 1:
                path_list = path.split("/")
                if len(path_list) == 1:
                    raise ValueError
            trim = path_list[-1]
        except ValueError:
            trim = "my_project"
        return trim

    def generate(self) -> None:
        count = 1
        for root, dirs, files in os.walk("E:\\CODE\\NacCode\\trunk_xczy\\nac"):
            print("----------LOOP %d----------" % count)
            print("1. root")
            print(root)
            print("2. dirs")
            for name in dirs:
                print(name)
            print("3. files")
            for name in files:
                print(name)
            count += 1


def main(argv) -> None:
    options, args = getopt.getopt(argv, "ro:m:", ["recv", "opcode=", "msg="])
    project_root = None
    project_name = 0x00
    msg = "test"
    for option, value in options:
        if option in ("-r", "--root"):
            project_root = str(value)
        elif option in ("-o", "--opcode"):
            code = int(value)
        elif option in ("-m", "--msg"):
            msg = value


if __name__ == '__main__':
    main(sys.argv[1:])
