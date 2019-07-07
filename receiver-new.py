import argparse
import signal
import sys
import time
import logging

from rpi_rf import RFDevice
import paho.mqtt.publish as mqtt
import paho.mqtt.client as mqtt_client
GPIO_PIN = 15
rfdevice = None
MQTT_HOST = '10.1.1.130'
TOPIC = '/rf/'


logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] rx: %(message)s', )

parser = argparse.ArgumentParser(description='Receives a decimal code via a 433/315MHz GPIO device')
parser.add_argument('-g', dest='gpio', type=int, default=GPIO_PIN,
                    help="GPIO pin (Default: 27)")
args = parser.parse_args()

rfdevice = RFDevice(args.gpio)
rfdevice.disable_tx()
rfdevice.enable_rx()
timestamp = None
logging.info("New Version")
logging.info("Listening for codes on GPIO " + str(args.gpio))


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt_client.Client()
client.on_connect = on_connect
client.connect(MQTT_HOST, 1883)
count = 0
c = ""
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        if True: #rfdevice.rx_proto == 1:
            pulsewidth_range = 350 <= rfdevice.rx_pulselength <= 480 or 300 <= rfdevice.rx_pulselength <= 310 or 200<=rfdevice.rx_pulselength <= 290
            code_range = rfdevice.rx_code > 10000
            string = ""
            
            if not code_range:
                c = c + "."
            if pulsewidth_range and code_range:
                count = count +1

                string = "**************************** #" + str(count)+"\n" + str(c)
                c = ""

                
            logging.info(str(rfdevice.rx_code) +
                         " [pulselength " + str(rfdevice.rx_pulselength) +
                         ", protocol " + str(rfdevice.rx_proto) + ", pulsewidth_range="+str(pulsewidth_range)+", code_range="+str(code_range)+"] " + string)


            if pulsewidth_range and code_range:
                client.publish(TOPIC + str(rfdevice.rx_code), "ON")
                client.publish(TOPIC + 'all', str(rfdevice.rx_code))
                #time.sleep(2)
                #client.publish(TOPIC + str(rfdevice.rx_code), "OFF") # for RF devices that can only be triggered and do not have state (such as motion sensors). This line sets Home Assistants binary_sensor state back to off.
                #else:
                    #logging.info("\t\t\t\t\t\t\t\t\t\t\t"+str(rfdevice.rx_code) + " [pulselength " + str(rfdevice.rx_pulselength) +                         ", protocol " + str(rfdevice.rx_proto) + "]")

    client.loop()
    time.sleep(0.007)

import atexit

def exithandler(signal, frame):
    loggin.info("Cleaning up...")
    rfdevice.cleanup()
    client.disconnect()
    sys.exit(0)
atexit.register(exithandler)
