#!/usr/bin/env python3

import argparse
import logging
import time
from rpi_rf import RFDevice
DATA_PIN = 17
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)

parser = argparse.ArgumentParser(description='Sends a decimal code via a 433/315MHz GPIO device')
#parser.add_argument('code', metavar='CODE', type=int,
#                    help="Decimal code to send")
parser.add_argument('-g', dest='gpio', type=int, default=17,
                    help="GPIO pin (Default: 17)")
parser.add_argument('-p', dest='pulselength', type=int, default=None,
                    help="Pulselength (Default: 350)")
parser.add_argument('-t', dest='protocol', type=int, default=None,
                    help="Protocol (Default: 1)")
args = parser.parse_args()

rfdevice = RFDevice(DATA_PIN)
rfdevice.enable_tx()

if args.protocol:
    protocol = args.protocol
else:
    protocol = "default"
if args.pulselength:
    pulselength = args.pulselength
else:
    pulselength = "default"

#rfdevice.tx_code(args.code, args.protocol, args.pulselength)
while True:
    code = 2011696976
    pulselength = 260
    rfdevice.tx_code(code, 1, pulselength)
    time.sleep(0.5)

    logging.info(str(code) +
    " [protocol: " + str(1) +
    ", pulselength: " + str(pulselength) + "]")
    # code =2011694936
    # rfdevice.tx_code(code, 1, pulselength)
    # time.sleep(0.01)
    # rfdevice.tx_code(code, 1, pulselength)
    # time.sleep(0.01)
    # rfdevice.tx_code(code, 1, pulselength)
    # time.sleep(0.01)
    # rfdevice.tx_code(code, 1, pulselength)
    # time.sleep(0.01)
    # rfdevice.tx_code(code, 1, pulselength)
    # time.sleep(0.01)
    # rfdevice.tx_code(code, 1, pulselength)
    # time.sleep(0.01)
    # rfdevice.tx_code(code, 1, pulselength)
    # time.sleep(0.01)
    # logging.info(str(code) +
    # " [protocol: " + str(1) +
    # ", pulselength: " + str(pulselength) + "]")
rfdevice.cleanup()
