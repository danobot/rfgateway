/*
  RFSniffer

  Usage: ./RFSniffer [<pulseLength>]
  [] = optional

  Hacked from http://code.google.com/p/rc-switch/
  by @justy to provide a handy RF code sniffer
*/

#include "../rc-switch/RCSwitch.h"
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
using namespace std;

#include <RH_ASK.h>
#include <SPI.h> // Not actualy used but needed to compile
RH_ASK driver;
// RH_ASK driver(2000, 2, 4, 5); // ESP8266 or ESP32: do not use pin 11

int main(int argc, char *argv[]) {
  Serial.begin(9600); // Debugging only
  if (!driver.init())
    Serial.println("init failed");

     while(1) {
       uint8_t buf[RH_ASK_MAX_MESSAGE_LEN];
       uint8_t buflen = sizeof(buf);
       if (driver.recv(buf, &buflen)) // Non-blocking
       {
           int i;
           // Message with a good checksum received, dump it.
           driver.printBuffer("Got:", buf, buflen);
       }


  }

  exit(0);


}
