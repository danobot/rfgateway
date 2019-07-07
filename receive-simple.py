import argparse
import signal
import sys
import time
import logging

from rpi_rf import RFDevice
import paho.mqtt.publish as publish

GPIO_PIN = 15
rfdevice = None
MQTT_HOST = 'ubuntu'
TOPIC = '/rf/'

# pylint: disable=unused-argument
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

parser = argparse.ArgumentParser(description='Receives a decimal code via a 433/315MHz GPIO device')
parser.add_argument('-g', dest='gpio', type=int, default=GPIO_PIN,
                    help="GPIO pin (Default: 27)")
args = parser.parse_args()

signal.signal(signal.SIGINT, exithandler)
rfdevice = RFDevice(args.gpio)
rfdevice.disable_tx()
rfdevice.enable_rx()
timestamp = None
logging.info("Listening for codes on GPIO " + str(args.gpio))



count = 0
countTotal = 0
c = ""
expireCache = time.time()
cache = {}
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        if rfdevice.rx_proto == 1:
            pulsewidth_range = True #350 <= rfdevice.rx_pulselength <= 480 or 300 <= rfdevice.rx_pulselength <= 310 or 200<=rfdevice.rx_pulselength <= 290
            code_range = rfdevice.rx_code > 10000
            
            if code_range:            
                if time.time() - expireCache > 2:
                    cache.clear()
                    expireCache = time.time()
                    #logging.info("Clearing cache for ya'll")
                countTotal = countTotal+1
                if not rfdevice.rx_code in cache:

                    if pulsewidth_range and code_range:
                        count = count + 1

                        logging.info('#{:>3} {:<8} [pulselength {:<3}, protocol {}] {:.2%}'.format(count, rfdevice.rx_code, rfdevice.rx_pulselength,rfdevice.rx_proto, count/countTotal))
                        
                        publish.single(TOPIC+ 'all', str(rfdevice.rx_code), hostname=MQTT_HOST)
                        publish.single(TOPIC + str(rfdevice.rx_code), "ON", hostname=MQTT_HOST)
                        cache[rfdevice.rx_code] = 1
                        
               
    time.sleep(0.007)

rfdevice.cleanup()
