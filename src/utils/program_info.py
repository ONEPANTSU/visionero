import ctypes
import os

import psutil


class ProgramInfo:
    def get_running_program_list(self):
        return [
            program
            for program in self.get_program_list()
            if self.is_program_running(program)
        ]

    def get_program_list(self):
        program_list = []
        for desktop_path in self.get_desktop_paths():
            desktop_files = os.listdir(desktop_path)
            for file_name in desktop_files:
                if file_name.endswith(".lnk"):
                    program_name = file_name.replace(".lnk", "")
                    program_list.append(program_name)
        return program_list

    def get_program_path_list(self):
        program_list = []
        for desktop_path in self.get_desktop_paths():
            desktop_files = os.listdir(desktop_path)
            for file_name in desktop_files:
                if file_name.endswith(".lnk"):
                    program_name = file_name.replace(".lnk", "")
                    program_path = os.path.join(desktop_path, file_name)
                    program_list.append((program_name, program_path))
        return program_list

    @staticmethod
    def get_desktop_paths():
        desktop_paths = []
        users_directories = (0x0000, 0x0019)

        for user_directory in users_directories:
            path = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(
                None, ctypes.c_int(user_directory), None, ctypes.c_int(0), path
            )
            desktop_paths.append(path.value)

        return desktop_paths

    @staticmethod
    def is_program_running(program_name):
        for process in psutil.process_iter():
            if process.name().lower() == f"{program_name.lower()}.exe":
                return True
        return False
