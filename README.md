Dockerfile that runs Python scripts that interact with Raspberry Pi's GPIO pins.

Use docker compose to load in your script via volume mapping.

The container listens to RF traffic and converts any signals received on RF protocol 1 to MQTT messages on the following topics:
* `/rf/all` with a message containing the RF code
* `/rf/<code>` with a message containing `"ON"` and another message 2 seconds later containing `"OFF"`.
* `/rftest` will return the payload on `/rftest/result` for status testing purposes.


