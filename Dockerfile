FROM python:3.9.1

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip3 install -r requirements.txt

ENTRYPOINT uvicorn main:app --reload --host 0.0.0.0 --port 8000