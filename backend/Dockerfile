FROM python:3.10-bullseye

LABEL author='deorz' version=1 project='task_manager'

RUN apt update && apt install openssh-client

WORKDIR backend/

COPY requirements.txt requirements.txt

COPY . .

RUN pip3 install -U pip && pip3 install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/"

CMD ["uvicorn", "main:task_manager", "--host", "0.0.0.0", "--port", "8000"]