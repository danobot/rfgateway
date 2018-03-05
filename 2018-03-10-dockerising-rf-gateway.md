---
  title: Dockerising the RF to MQTT gateway
  excerpt:
---

I'm writing this post as the `docker build` command compiles the `Dockerfile` into an image. This is the second attempt at dockerizing a RF signal sniffer. I wrote a post a few months ago about creating an [RF to MQTT Gateyway](), which would allow Home Assistant to receive and control radio-frequency devices. The post is about using an arduino (dedicated hardware) to accomplish this. It works fine but it runs on a dedicated device which consumes power[^1]. I love Docker and [dockerizing applications]().

One of the benefits of Docker is that it allows you to virtualize a dedicated device, such as an arduino, and run it on a shared host. Why run this gateway on physical hardware when I can run it as another software container on my home automation hub (Raspberry Pi 3)?

## RF to MQTT Python Script (using rpi_rf)
The first attempt was based on Python, the `arm32v7/python docker` image and the `rpi_rf` python package.

I included a C++ test docker image below. As i got the Python implementation to work after all, I did not bother completing the C++ implementation. If you make any progress please let me know so I can check it out. I am interested in a C++ version because Python's garbage collection is supposedly very slow, which impacts the timing of RF signals.
{. :notice--info}

```Dockerfile
FROM arm32v7/python:3.6.4-slim-jessie

RUN apt-get update
RUN apt-get install -y python-dev python3-dev
RUN apt-get install -y build-essential

RUN pip3 install RPi.GPIO

RUN pip3 install rpi-rf

#COPY blink.py ./

RUN mkdir app

WORKDIR /app

CMD ["python", "./receive.py"]
```
Download [this RF sniffer program](https://github.com/milaq/rpi-rf/blob/master/scripts/rpi-rf_receive) and save it as `receive.py`. Then wire your RF receiver to your Raspberry Pi. The data pin is on [pin 27](http://laoblogger.com/rpi-3-gpio-pinout-clipart.html#gal_post_162917_rpi-3-gpio-pinout-clipart-1.jpg) by default.

The `docker-compose.yaml` file follows:

```yaml
version: "3"
services:
  gateway:
    build: .
    container_name: gateway
    volumes:
      - ./receive.py:/app/receive.py
    privileged: true
```

You can test this setup by running `com up`.


[^1: It's power supply may actually consume more power than the micro controller itself.]

Have a second docker image for sending commands (reverse MQTT to RF)
 ## C++ implementation
