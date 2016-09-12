#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Sat Messenger tools
#
#
#  Display Antenna serial number, Antenna model, next outbound message number (momsn), Signal (0-5), Network time and GPS position.
# v0.1
# 
##

import time
import rockBlock
from rockBlock import rockBlockProtocol
import arrow
import serial

serialport = "/dev/tty.usbserial"


class Infos(rockBlockProtocol):
    
    def main(self):
        global signal
        
        signal = -1
        
        rb = rockBlock.rockBlock(serialport, self)

        # get signal 
        print ""
        
        print 'Antenna serial number : ' + str(rb.getSerialIdentifier())
        print 'Antenna model : ' + str(rb.model())
        #print 'Antenna revision : ' + str(rb.revision())
        
        momsn = rb.momsn().split(',')
        print 'Momsn : ' + momsn[1]
        
        signal = rb.requestSignalStrength() 
        print "Signal (0-5) : " + str(signal) 
        
        if signal > -1:
        
              a = arrow.get(rb.networkTime())
              print 'UTC Time : ' + str(a.datetime)
              print 'GPS position : ' + str(rb.geo())



        rb.close()
        
        
           
    def rockBlockRxStarted(self):
        print "rockBlockRxStarted"
        
    def rockBlockRxFailed(self):
        print "rockBlockRxFailed"
        
    def rockBlockRxReceived(self,mtmsn,data):
        print "rockBlockRxReceived " + str(mtmsn) + " " + data
        
    def rockBlockRxMessageQueue(self,count):
        print "rockBlockRxMessageQueue " + str(count)
             
        
        
if __name__ == '__main__':

    # Check Serial comm 
    ser = serial
    
    print ''
    print "Satmessenger toolsv0.1"
    print "Rockblock infos"
    print "Checking serial communication..."
    try:
       ser = serial.Serial(serialport, 19200, timeout=5)

       if(ser == None or ser.isOpen() == False):
            print 'Communication problem with antenna'
       else:
            ser.close()
            print "OK"
            print 'getting infos...'
            Infos().main()


    except serial.serialutil.SerialException:
        print 'Communication problem with antenna'
  
   
        
    