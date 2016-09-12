#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Sat Messenger tools
#
# Send (MT) some text to Rockblock through rockblock POST API
# v0.1
#
# CHANGE THE IMEI VARIABLE WITH YOUR OWN
#
	
import urllib
import urllib2
from getpass import getpass
import binascii
# Gather information

print ""
print "Satmessenger tools v0.1"
print "Send some text to a rockblock through Web API."

print "Please your Rockblock account username : "
username = raw_input()
print "Provide your Rockblock account password : "
password = getpass()
print "Text message to send ? "
message = binascii.hexlify(raw_input())


imei = 'CHANGEME'
values = {'imei':imei, 'username':username, 'password':password, 'data':message}
url = 'https://rockblock.rock7.com/rockblock/MT'

# Send

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
responseString = response.read()
print responseString
