FROM arm32v7/gcc:5.5.0

RUN apt-get update

# Install wiringpi
RUN apt-get install -y git-core sudo


RUN mkdir app
WORKDIR /app
#RUN git clone --recursive git://github.com/ninjablocks/433Utils.git utils
#RUN git clone git://git.drogon.net/wiringPi wiring

#RUN cd wiring && bash ./build

# Build 433Utils
#RUN rm /app/utils/RPi_utils/RFSniffer.cpp
COPY ./RFSniffer.cpp /app/utils/RPi_utils/RFSniffer.cpp
#RUN cd /app/utils/RPi_utils && make RFSniffer && ls -l


CMD ["/app/utils/RPi_utils/RFSniffer"]
