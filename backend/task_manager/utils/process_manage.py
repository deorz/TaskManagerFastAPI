import requests


def on_terminate(output: bytes, errors: bytes, exitcode: int,
                 pid: int, id_task: int) -> None:
    """Функция обработки результата выполнения таски"""
    requests.post(
        url=f'http://127.0.0.1:8000/v1/tasks/{id_task}/result',
        json={
            'process_id': pid,
            'output': output.decode('UTF-8'),
            'errors': errors.decode('UTF-8'),
            'exitcode': exitcode
        },
        headers={'content-type': 'application/json'}
    )


def run_process(arglist: list, id_task: int) -> None:
    """Функция запуска откреплённого процесса"""
    import subprocess
    import threading
    def threadfunc(id_task: int):
        p = subprocess.Popen(
            arglist,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = p.communicate()
        on_terminate(
            output=out, errors=err, exitcode=p.returncode,
            pid=p.pid, id_task=id_task
        )

    t = threading.Thread(target=threadfunc, args=[id_task])
    t.start()
