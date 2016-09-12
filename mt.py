#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Sat Messenger tools
#
#
# Query Iridium satellites for waiting messages ('Mobile Terminated')
# and display if any.
# v0.1
# 
#


import rockBlock
from rockBlock import rockBlockProtocol
import serial

serialport = "/dev/tty.usbserial"

class mtExample (rockBlockProtocol):
    
    def main(self):

        
        # Get Arguments
        
        print ''
        print "Satmessenger tools v0.1"
        print "Check and display queued messages."


        # Check Serial comm 
        
        ser = serial
    
        print "Checking antenna communication : "

        try:
           ser = serial.Serial(serialport, 19200, timeout=5)

           if(ser == None or ser.isOpen() == False):
                print 'Communication problem with antenna'
           else:
                ser.close()
                print "OK"
            
                rb = rockBlock.rockBlock(serialport, self)                                                                        
                rb.messageCheck()
        
                rb.close()


        except serial.serialutil.SerialException:
            print 'Communication problem with antenna'
    

        rb = rockBlock.rockBlock(serialport, self)           # "/dev/cu.usbserial" for os x 
                                                                      # "/dev/ttyUSB0" for Linux
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
    mtExample().main()
