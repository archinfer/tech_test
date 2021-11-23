FROM python:latest

RUN mkdir -p /logs

COPY data data

COPY requirements.txt ./

COPY app app

RUN pip install -r requirements.txt

CMD [ "python", "/app/src/code_csv_json.py"]