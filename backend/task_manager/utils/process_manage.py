from pathlib import Path

import requests

from backend.task_manager.database.models import File, System, Task
from backend.task_manager.settings import settings
from backend.task_manager.utils.file_manage import FileType
from backend.task_manager.utils.ssh_client import RemoteClient


def on_terminate(output: bytes, errors: bytes, exitcode: int, id_task: int) -> None:
    """Функция обработки результата выполнения таски"""
    port: str = ':8000' if settings.DEBUG_ else ''
    requests.post(
        url=f'http://127.0.0.1{port}/v1/tasks/{id_task}/result',
        json={
            'output': output.decode('UTF-8'),
            'errors': errors.decode('UTF-8'),
            'exitcode': exitcode
        },
        headers={'content-type': 'application/json'}
    )


def run_process(task: Task, file: File, system: System, id_task: int) -> None:
    """Функция запуска откреплённого процесса"""
    import threading

    def threadfunc():
        ssh_client = RemoteClient(
            host=system.host,
            user=settings.SSH_USER,
            passphrase=settings.SSH_PASSPHRASE
        )

        ssh_client.upload_file(filepath=file.file_path, remote_path='./tasks/')

        if file.type == FileType.python.value:
            execute_command = '/usr/bin/python3'
            num_threads = ''
            path_to_file = f'tasks/{Path(file.file_path).name}'
            execute_params = task.params if task.params else ''

        else:
            execute_command = 'mpiexec'
            num_threads = f'-n {task.num_threads}'
            path_to_file = f'./tasks/{Path(file.file_path).name}'
            execute_params = task.params if task.params else ''
            ssh_client.execute_commands(command=f'chmod u+x {Path(file.file_path).name}')

        stdin, stdout, stderr = ssh_client.execute_commands(
            command=' '.join(
                target for target in (execute_command, num_threads, path_to_file, execute_params) if target
            )
        )

        on_terminate(
            output=stdout.read(), errors=stderr.read(), exitcode=stdout.channel.recv_exit_status(),
            id_task=id_task
        )

        ssh_client.disconnect()

    t = threading.Thread(target=threadfunc)

    t.start()
