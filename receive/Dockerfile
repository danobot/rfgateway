FROM arm32v7/python:3.6.4-slim-jessie

RUN apt-get update
RUN apt-get install -y python-dev python3-dev
RUN apt-get install -y build-essential

RUN pip3 install RPi.GPIO

RUN apt-get install -y pkg-config
RUN pip3 install rpi-rf
RUN apt-get install -y libfreetype6-dev libpng12-dev

#RUN pip3 install matplotlib
RUN pip3 install paho-mqtt

#COPY blink.py ./

RUN mkdir app

WORKDIR /app

CMD ["python", "./receive.py"]
