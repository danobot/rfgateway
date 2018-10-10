import argparse
import signal
import sys
import time
import logging

from rpi_rf import RFDevice

# A small helper class implementing a dictionary with expiring items. This class might cause memory leaks because items are deleted only when tick() is called with the key.
# Calling class is responsible for calling clear() periodically to remove stale entries.
class ExpiringDict(dict):
  
    def __init__(self, *args):
        dict.__init__(self, args)

    def __getitem__(self, key):
        return dict.__getitem__(self, key)[1]
        
        

    def __setitem__(self, key, val):
        #logging.info("SET %s['%s'] = %s" % (str(dict.get(self, 'name_label')), str(key), str(val)))

        dict.__setitem__(self, key, (val,time.time()))

    def tick(self, key):
        try: 
            item = dict.__getitem__(self, key)
            item_age = time.time() - item[1]

            if item_age < 3: # age less than (still valid)
                #logging.info("Item still valid")
                return 1
            else: # age older than (it expired, delete the record)
                #logging.info("item expired, deleting item")
                del self[key]
                return 0
        except KeyError:
            return 0 # same as if the record was there and it was deleted as a result of the tick call


import paho.mqtt.publish as publish


GPIO_PIN = 15
rfdevice = None
MQTT_HOST = 'ubuntu'
TOPIC = '/rf/'

# RF GPIO :: defines and registered exist handler to clean up GPIO when closing
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, exithandler)

# Logging
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s [%(levelname)s] %(module)s: %(message)s' )

# Argument Parsing
parser = argparse.ArgumentParser(description='Receives a decimal code via a 433/315MHz GPIO device')
parser.add_argument('-g', dest='gpio', type=int, default=GPIO_PIN,
                    help="GPIO pin (Default: 27)")
args = parser.parse_args()

# Set up RF
rfdevice = RFDevice(args.gpio)
rfdevice.disable_tx()
rfdevice.enable_rx()

timestamp = None
logging.info("Listening for codes on GPIO " + str(args.gpio))

codeCache = ExpiringDict() # Tracks recent codes, stops duplicate MQTT messages per RF code

count = 0

# Continuously process RF signals
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        if rfdevice.rx_proto == 1: # ignore other RF protocols
            # Filter by pulsewidth
            pulsewidth_range = 350 <= rfdevice.rx_pulselength <= 480 or 300 <= rfdevice.rx_pulselength <= 310 or 200<=rfdevice.rx_pulselength <= 290
            
            # Filter by code range
            code_range = rfdevice.rx_code > 10000
            string = ""

            if pulsewidth_range and code_range:
                count = count +1
                string = "**************************** #" + str(count)+"\n"

            if code_range:
                if codeCache.tick(rfdevice.rx_code) == 0: # Checks if code was processed already, if not:
                    logging.info(str(rfdevice.rx_code) +
                        " [pulselength " + str(rfdevice.rx_pulselength) +
                        ", protocol " + str(rfdevice.rx_proto) + ", pulsewidth_range="+str(pulsewidth_range)+", code_range="+str(code_range)+"] " + string)
                    #client.publish(TOPIC + str(rfdevice.rx_code), "ON")
                    #client.publish(TOPIC + 'all', str(rfdevice.rx_code))
                    publish.single(TOPIC+ 'all', str(rfdevice.rx_code), hostname=MQTT_HOST)
                    codeCache[rfdevice.rx_code] = rfdevice.rx_code
                    
            # else, we ignore because the RF device sent out multiple codes and we do not want multiple MQTT messages

    #client.loop()
    time.sleep(0.007)

rfdevice.cleanup()

