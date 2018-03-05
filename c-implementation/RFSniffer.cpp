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

RCSwitch mySwitch;



int main(int argc, char *argv[]) {
     cout << "Saying hello for no reason!\n";
     // This pin is not the first pin on the RPi GPIO header!
     // Consult https://projects.drogon.net/raspberry-pi/wiringpi/pins/
     // for more information.
     int PIN = 2;

     if(wiringPiSetup() == -1) {
       cout << "wiringPiSetup failed, exiting...\n";
       return 0;
     }

     int pulseLength = 0;
     if (argv[1] != NULL) pulseLength = atoi(argv[1]);

     mySwitch = RCSwitch();
     if (pulseLength != 0) mySwitch.setPulseLength(pulseLength);
     mySwitch.enableReceive(PIN);  // Receiver on interrupt 0 => that is pin #2


     while(1) {

      if (mySwitch.available()) {

        int value = mySwitch.getReceivedValue();

        if (value == 0) {
        cout << "Unknown encoding\n";
        } else {

          cout << "Received " << mySwitch.getReceivedValue() << "\n";
        }

        mySwitch.resetAvailable();

      } else {
        cout << "Switch not available\n";

      }


  }

  exit(0);


}
