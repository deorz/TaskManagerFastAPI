FROM python:3.8.9

LABEL author='deorz' version=1 project='task_manager'

WORKDIR backend/

COPY requirements.txt requirements.txt

COPY . .

RUN pip3 install -U pip && pip3 install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/"

CMD ["gunicorn", "main:task_manager", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0:8000"]