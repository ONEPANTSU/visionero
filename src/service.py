import datetime
import subprocess

import psutil
import win32com.client
from sqlalchemy.exc import IntegrityError

from src.repository import HistoryRepository
from src.utils.closed_checker import ClosedChecker
from src.utils.program_info import ProgramInfo


class ProgramService:
    def __init__(self):
        self.repository = HistoryRepository()
        self.program_info = ProgramInfo()
        self.closed_checker = ClosedChecker(self.program_info)

    def get_programs(self) -> dict[str, str]:
        program_list = self.program_info.get_program_list()
        program_status = {}
        for program_name in program_list:
            status = (
                "вкл."
                if self.program_info.is_program_running(program_name)
                else "выкл."
            )
            program_status[program_name] = status
        return program_status

    async def start_program(self, program_name) -> str:
        if program_name not in self.program_info.get_program_list():
            return (
                f"Программа '{program_name}' не установлена "
                f"или отсутствует на рабочем столе"
            )
        else:
            program_list = self.program_info.get_program_path_list()
            for name, path in program_list:
                if name == program_name:
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(path)
                    subprocess.Popen(shortcut.Targetpath)
                    self.closed_checker.run(name)
                    message = f"Запущена программа: {program_name}"
                    try:
                        await self.repository.add_running(
                            program_name=program_name,
                            time=datetime.datetime.now(),
                        )
                    except IntegrityError as error:
                        message += (
                            f"\nПроизошла ошибка "
                            f"при добавление записи в историю. "
                            f"({str(error)})"
                        )
                    return message

    def stop_program(self, program_name) -> str:
        self.closed_checker.stop(program_name)
        programs = self.get_programs()
        if program_name not in programs:
            return (
                f"Программа '{program_name}' "
                f"не установлена или отсутствует на рабочем столе"
            )
        elif programs[program_name] != "вкл.":
            return f"Программа '{program_name}' не запущена."
        else:
            processes = [
                p
                for p in psutil.process_iter()
                if p.name().lower() == f"{program_name.lower()}.exe"
            ]
            for process in processes:
                process.kill()
            return f"Программа '{program_name}' остановлена."

    def stop_all_programs(self) -> str:
        programs = [
            program.lower() + ".exe"
            for program in self.program_info.get_running_program_list()
        ]
        processes = [
            p for p in psutil.process_iter() if p.name().lower() in programs
        ]
        for process in processes:
            process.kill()
        return (
            f"Все запущенные программы остановлены. Программы: {str(programs)}"
        )

    async def get_history(self) -> list[dict[str, str]]:
        history = await self.repository.get_all()
        return [
            {
                "program": running.program,
                "time": str(running.time)
            }
            for running in history
        ]
