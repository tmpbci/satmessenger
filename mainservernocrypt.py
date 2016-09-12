#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Sat Messenger Server 
# v0.1
#
# Forward a text message to destination email
# Webui->satellite->rockblock servers->sat messenger server->email
#
# author: Sam Neurohack
# 
# CHANGE ALL THE EMAIL and MAIL SERVER SETTINGS ( 5x 'CHANGEME' )
# 



from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web import static
from twisted.web.template import flattenString
from twisted.internet import reactor

import cgi
import time
import os

from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import binascii

import smtplib
from getpass import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import syslog

class Get(Resource):
	
    def render_GET(self, request):
        return """
<!DOCTYPE HTML>
<html>
	<head>
		<title>Sat Messenger</title>
	</head>
	<body>

	</body>
</html>"""
    
    
    def render_POST(self, request):
 
         imei = cgi.escape(request.args["imei"][0])
         momsn = cgi.escape(request.args["momsn"][0])
         transmit_time = cgi.escape(request.args["transmit_time"][0])
         iridium_latitude = cgi.escape(request.args["iridium_latitude"][0])
         iridium_longitude = cgi.escape(request.args["iridium_longitude"][0])
         iridium_cep = cgi.escape(request.args["iridium_cep"][0])
         encodedhex = cgi.escape(request.args["data"][0])
         satmessage_e = encodedhex.decode("hex")
 
         print "message : " + satmessage_e
         print "message : " + encodedhex
         print "Hexlified message : " + binascii.hexlify(satmessage_e)
         print "imei : " + str(imei)
         print "momsn : " + str(momsn)
         print "transmit_time : " + str(transmit_time)
         print "iridium_latitude : " + str(iridium_latitude)
         print "iridium_longitude : " + str(iridium_longitude)
         print "iridium_cep : " + str(iridium_cep)
         
                
         satmessage = satmessage_e
         print ""
         print satmessage
         print ""
         
         #
         # Forward message to provided email
         #

         
         syslog.syslog('sat messenger')
        
         syslog.syslog(satmessage)

         syslog.syslog(satmessage.split(' ', 1 )[0])
         
         username = 'CHANGEME'                                   # SMTP account username
         sender = 'CHANGE%E'                                     # 'From' email                   
         recipient = satmessage.split(' ', 1 )[0]
         title = 'CHANGEME'                                      # will be as 'Subject' 
         password = 'CHANGEME'                                   # SMTP account password             
         
         # Create message container - the correct MIME type is multipart/alternative.
         msg = MIMEMultipart('alternative')
         msg['Subject'] = title
         msg['From'] = sender
         msg['To'] = recipient
         
         msg.attach(MIMEText(satmessage))
    
    
         try:
            smtpserver = smtplib.SMTP("CHANGEME", 25)            # SMTP server like smtp.foo.bar
            smtpserver.set_debuglevel(0)
            smtpserver.ehlo()
            #smtpserver.starttls()
            #smtpserver.ehlo
            # getpass() prompts the user for their password (so it never appears in plain text)
            smtpserver.login(username, password)
            # sendmail function takes 3 arguments: sender's address, recipient's address
            # and message to send - here it is sent as one string.
            smtpserver.sendmail(sender, recipient, msg.as_string())
            print "Message sent to '%s'." % recipient
            smtpserver.quit()
         except smtplib.SMTPAuthenticationError as e:
            print "Unable to send message: %s" % e

         
          
          
         return """
Content-Type:text/html\n\n
print "OK"
"""
root = Resource()
root.putChild('', Get())

factory = Site(root)

reactor.listenTCP(8888, factory)
#loopmin = task.LoopingCall(everyMin())
#loopmin.start(300.0)

reactor.run()
