FROM python:3-alpine

COPY . /app
WORKDIR /app

RUN pip install \
    Flask==1.1.1 \
    Flask-Bootstrap==3.3.7.1 \
    Flask-Login==0.4.1 \
    Flask-Mobility==0.1.1 \
    Flask-WTF==0.14.2

ENV PORT=8080
ENV IP=0.0.0.0

CMD python run_server.py
