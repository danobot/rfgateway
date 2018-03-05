Dockerfile that runs Python scripts that interact with Raspberry Pi's GPIO pins.

Use docker compose to load in your script via volume mapping.

`docker-compose up` will create two containers.
`gateway-tx` is created with the `send.py` script andlistens to MQTT messages sent on `/rf/send` and transmit a matching RF signal.
The other container `gateway-rx`, listens to RF traffic and converts any signals received on RF protocol 1 to MQTT messages on the following topics:
* `/rf/all` with a message containing the RF code
* `/rf/<code>` with a message containing `"ON"` and another message 2 seconds later containing `"OFF"`.

You can use the blink.py script to test that GPIO works with your docker installation.
