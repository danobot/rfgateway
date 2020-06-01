FROM arm32v7/python:3.6.4-slim-jessie

RUN apt-get update && apt-get install -y python-dev python3-dev build-essential pkg-config libfreetype6-dev libpng12-dev
RUN pip3 install RPi.GPIO rpi-rf paho-mqtt

RUN mkdir app

WORKDIR /app
# COPY ./receive-cached.py ./script.py

CMD ["python", "./script.py"]
