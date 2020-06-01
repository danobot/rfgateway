import argparse
import signal
import sys
import time
import logging
import os
from rpi_rf import RFDevice
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# A small helper class implementing a dictionary with expiring items. This class might cause memory leaks because items are deleted only when tick() is called with the key.
# Calling class is responsible for calling clear() periodically to remove stale entries.
class ExpiringDict(dict):
  
    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.debounce = float(kwargs.get('debounce', 3.0))
    def __getitem__(self, key):
        return dict.__getitem__(self, key)[1]
        
        

    def __setitem__(self, key, val):
        #logging.info("SET %s['%s'] = %s" % (str(dict.get(self, 'name_label')), str(key), str(val)))

        dict.__setitem__(self, key, (val,time.time()))

    def tick(self, key):
        try: 
            item = dict.__getitem__(self, key)
            item_age = time.time() - item[1]

            if item_age < self.debounce: # age less than (still valid)
                #logging.info("Item still valid")
                return 1
            else: # age older than (it expired, delete the record)
                #logging.info("item expired, deleting item")
                del self[key]
                return 0
        except KeyError:
            return 0 # same as if the record was there and it was deleted as a result of the tick call



GPIO_PIN = os.getenv('GPIO_PIN') if os.getenv('GPIO_PIN') else 15
MQTT_HOST = os.getenv('MQTT_HOST') if os.getenv('MQTT_HOST') else "tower.local"
TOPIC = os.getenv('TOPIC') if os.getenv('TOPIC') else 'home/gw/433toMQTT'
TEST_TOPIC = os.getenv('TEST_TOPIC') if os.getenv('TEST_TOPIC') else '/rftest'




# Logging
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s [%(levelname)s] %(module)s: %(message)s' )
client = mqtt.Client()

client.connect(MQTT_HOST, 1883, 60)
def on_connect(client, userdata, flags, rc):
    logging.info("Connected to MQTT broker with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic
    if topic == MQTT_TEST_TOPIC:
        client.publish(TEST_TOPIC  + "/result", payload=msg.payload, qos=0, retain=False)
        return

client.on_connect = on_connect
client.on_message = on_message


rfdevice = None


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

codeCache = ExpiringDict(debounce=0.3) # Deduplicate:  Tracks recent codes, stops duplicate MQTT messages per RF code

count = 0
# Continuously process RF signals
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        if rfdevice.rx_proto == 1: # ignore other RF protocols
            # Filter by pulsewidth
            pulsewidth_range = True #350 <= rfdevice.rx_pulselength <= 480 or 300 <= rfdevice.rx_pulselength <= 310 or 200<=rfdevice.rx_pulselength <= 290
            code_range = rfdevice.rx_code > 10000
            
            if code_range:
                if codeCache.tick(rfdevice.rx_code) == 0: # Checks if code was processed already, if not:
                    count = count + 1
                    logging.info('{:<8} [pulselength {:<3}, protocol {}]'.format(rfdevice.rx_code, rfdevice.rx_pulselength,rfdevice.rx_proto))
                    publish.single(TOPIC, "{\"value\":" + str(rfdevice.rx_code)+"}", hostname=MQTT_HOST)
#                    publish.single(TOPIC + str(rfdevice.rx_code), "ON", hostname=MQTT_HOST)
                    codeCache[rfdevice.rx_code] = rfdevice.rx_code

            # else, we ignore because the RF device sent out multiple codes and we do not want multiple MQTT messages

    #client.loop()
    time.sleep(0.007)



## Test endpoint




# RF GPIO :: defines and registered exist handler to clean up GPIO when closing
def exithandler(signal, frame):
    rfdevice.cleanup()
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, exithandler)
