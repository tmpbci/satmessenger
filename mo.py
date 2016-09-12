#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Sat Messenger tools
#
#
# Send a message through Iridium satellites ('Mobile Originated')
# 
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
        print "Send a message from rockblock"
        
        


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
                print "Provide the text message : "
                message = raw_input()
                rb = rockBlock.rockBlock(serialport, self)      
                                                                      
                rb.sendMessage(message)
        
                rb.close()


        except serial.serialutil.SerialException:
            print 'Communication problem with antenna'
    

        rb = rockBlock.rockBlock(serialport, self)        
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
