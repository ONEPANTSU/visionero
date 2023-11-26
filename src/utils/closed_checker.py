import threading
import time

alert_messages = list()


class ClosedChecker:
    threads = dict()

    def __init__(self, program_info):
        self.program_info = program_info

    def run(self, program_name):
        self.threads[program_name] = True
        track_thread = threading.Thread(
            target=self.track_application, args=(program_name,)
        )
        track_thread.start()

    def stop(self, program_name):
        self.threads[program_name] = False

    def track_application(self, program_name):
        while self.threads[program_name]:
            if not self.is_running(program_name):
                if self.threads[program_name]:
                    alert_messages.append(
                        f"Приложение {program_name} закрыто пользователем"
                    )
                    self.threads[program_name] = False
                break

    def is_running(self, program_name):
        return program_name in self.program_info.get_running_program_list()
