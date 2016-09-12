#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Sat Messenger Web interface
# v0.1
# 
# Forward a text message to destination email
# Web Interface->rockblock->satellite->rockblock servers->sat messenger server->email
#
# author: Sam Neurohack
#
#
# Features :
#
# - Change buttons texts according to serial port availability
# - Rockblock device info page
# - builtin fonts, no online requests
# 
# todo : 
# - Display mt messages bug
# - 
#
# CHANGE the serialport line before use if needed.
#


from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.web import static
from twisted.web.template import flattenString
from twisted.internet import reactor
#from twisted.internet import task
#from twisted.web import server

import cgi
import time
import os
import binascii

import serial
import arrow

import rockBlock
from rockBlock import rockBlockProtocol

#
# Ok for OS X. Change me for /dev/ttyUSB0 style for Linux
#

serialport = "/dev/tty.usbserial"



class MoExample(rockBlockProtocol):
  
    
    def rockBlockTxStarted(self):
        global MoDisplay
        
        print "rockBlockTxStarted"
        MoDisplay = "rockBlockTxStarted..."
        
    def rockBlockTxFailed(self):
        global MoDisplay
        
        print "rockBlockTxFailed"
        MoDisplay += "rockBlockTxFailed... "

    def rockBlockTxSuccess(self,momsn):
        global MoDisplay
        
        print "rockBlockTxSuccess " + str(momsn)
        MoDisplay +=  "rockBlockTxSuccess... message number : " + str(momsn)
        
        
        

class MtExample (rockBlockProtocol):
    
    
           
    def rockBlockRxStarted(self):
        global MtDisplay
        global MtData
        
        print "rockBlockRxStarted"
        MtDisplay = "rockBlockRxStarted..."
        MtData = ""
        
    def rockBlockRxFailed(self):
        global MtDisplay
        
        print "rockBlockRxFailed"
        MtDisplay += "rockBlockRxFailed..."
        
    def rockBlockRxReceived(self,mtmsn,data):
        global MtDisplay
        global MtData
        
        print "rockBlockRxReceived " + str(mtmsn) + " " + data
        MtData += "rockBlockRxReceived Number : " + str(mtmsn) + " " + data + " "
        
       
    def rockBlockRxMessageQueue(self,count):
        global MtDisplay
        print "rockBlockRxMessageQueue " + str(count)
        MtDisplay += "rockBlockRxMessageQueue..." + str(count) + "..."


class InfoDisplay(rockBlockProtocol):
    
           
    def rockBlockRxStarted(self):
        global InfoDisplay
    
        print "rockBlockRxStarted"
        InfoDisplay = "rockBlockRxStarted..."
        
    def rockBlockRxFailed(self):
        global InfoDisplay
        
        print "rockBlockRxFailed"
        InfoDisplay += "rockBlockRxFailed..."
        
    def rockBlockRxReceived(self,mtmsn,data):
        global InfoDisplay
        
        print "rockBlockRxReceived " + str(mtmsn) + " " + data
        InfoDisplay += "rockBlockRxReceived Number : " + str(mtmsn) + " " + data + " "
        
       
    def rockBlockRxMessageQueue(self,count):
        global InfoDisplay
        print "rockBlockRxMessageQueue " + str(count)
        InfoDisplay +=  "rockBlockRxMessageQueue..." + str(count) + "..."


#
# Send Page
#


class Send(Resource):

    
    def render_GET(self, request):
        global MoDisplay
        global status
        
        ser = serial
        print ""
        print ""
        print "Checking antenna communication : "

        try:
           ser = serial.Serial(serialport, 19200, timeout=5)

           if(ser == None or ser.isOpen() == False):
                print 'Communication problem with antenna'
                status = "No Satellite communication available. Check connections"
                buttontext = "NoSatelliteDeviceError"
                ser.close()
           else:
              ser.close()   
              print "OK"
              status = "Satellite communication available"
              buttontext = "Send"



        except serial.serialutil.SerialException:
           print 'Communication problem with antenna'
           status = "No Satellite communication available. Check connections"
           buttontext = "NoSatelliteDeviceError"
        
        return """
<!DOCTYPE HTML>
<!--
	Prologue by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>Sat Messenger</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
		<link rel="stylesheet" href="assets/css/main.css" />
		<!--[if let IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
		<!--[if let IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
	</head>
	<body>

		<!-- Header -->
			<div id="header">

				<div class="top">

					<!-- Logo -->
						<div id="logo">
							<span class="image avatar48"><img src="images/avatar.png" alt="" /></span>
							<h1 id="title">Sat Messenger</h1>
							<p>choose you action</p>
						</div>

					<!-- Nav -->
						<nav id="nav">
							<!--

								Prologue's nav expects links in one of two formats:

								1. Hash link (scrolls to a different section within the page)

								   <li><a href="#foobar" id="foobar-link" class="icon fa-whatever-icon-you-want skel-layers-ignoreHref"><span class="label">Foobar</span></a></li>

								2. Standard link (sends the user to another page/site)

								   <li><a href="http://foobar.tld" id="foobar-link" class="icon fa-whatever-icon-you-want"><span class="label">Foobar</span></a></li>

							-->
							<ul>
								<li><a href="index.html" id="top-link" class="skel-layers-ignoreHref"><span class="icon fa-home">Intro</span></a></li>
								<li><a href="about.html" id="portfolio-link" class="skel-layers-ignoreHref"><span class="icon fa-cog">About</span></a></li>
								<li><a href="send.html" id="contact-link" class="skel-layers-ignoreHref"><span class="icon fa-cloud-upload">Send</span></a></li>
								<li><a href="check.html" id="about-link" class="skel-layers-ignoreHref"><span class="icon fa-cloud-download">Check </span></a></li>
								<li><a href="rockblock.html" id="about-link" class="skel-layers-ignoreHref"><span class="icon fa-signal">Rockblock</span></a></li>
								
							</ul>
						</nav>

				</div>

			</div>

		<!-- Main -->
			<div id="main">

				<!-- Send -->
					<section id="send" class="four">
						<div class="container">
<header>
                                <h2>Send Message</h2>
                            </header>

                            <p>Because Satellite messages are quite expensive.<br />
                            Your message + destination email must me less than 50 characters.</p>

                           <form method="post" action="#">
								<div class="row">
									<div class="12u$"><input type="text" name="to" placeholder="Destination email" /></div>
									<div class="12u$">
										<textarea name="message" placeholder="Message"></textarea>
									</div>
									<div class="12u$">
										<input type="submit" value=%s />
									</div>
								</div>
							</form>

                        </div>
                    </section>

            </div>


		<!-- Footer -->
			<div id="footer">

				<!-- Copyright -->
					<ul class="copyright">
					<br />%s<br />
					</ul>

			</div>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/jquery.scrollzer.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
			<script src="assets/js/main.js"></script>

	</body>
</html>"""% (buttontext, status)



    def render_POST(self, request):
#        loopmin.stop()
        dest = cgi.escape(request.args["to"][0])
        data = cgi.escape(request.args["message"][0])

        satmessage = dest  + ' ' + data 
        print "Raw Sat Message : " + satmessage
        
        
       
        # If no crypto
        
        encrypted_msg = satmessage
        
        #
        # message is too long ?
        #
        
        if len(encrypted_msg) >= 50:
              encrypted_msg = "Votre message est trop long."
       
        
        #
        # Send to Rockblock
        #
        
        else:
              mo = MoExample()
              rb = rockBlock.rockBlock(serialport, mo)
              rb.sendMessage(encrypted_msg)      
              rb.close()


        time.sleep(1)

        return """
<!DOCTYPE HTML>
<!--
	Prologue by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>Sat Messenger</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
		<link rel="stylesheet" href="assets/css/main.css" />
		<!--[if let IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
		<!--[if let IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
		<meta http-equiv="refresh" content="5; URL=index.html">
	</head>
	<body>

		<!-- Header -->
			<div id="header">

				<div class="top">

					<!-- Logo -->
						<div id="logo">
							<span class="image avatar48"><img src="images/avatar.png" alt="" /></span>
							<h1 id="title">Sat Messenger</h1>
							<p>choose you action</p>
						</div>

					<!-- Nav -->
						<nav id="nav">
							<!--

								Prologue's nav expects links in one of two formats:

								1. Hash link (scrolls to a different section within the page)

								   <li><a href="#foobar" id="foobar-link" class="icon fa-whatever-icon-you-want skel-layers-ignoreHref"><span class="label">Foobar</span></a></li>

								2. Standard link (sends the user to another page/site)

								   <li><a href="http://foobar.tld" id="foobar-link" class="icon fa-whatever-icon-you-want"><span class="label">Foobar</span></a></li>

							-->
							<ul>
								<li><a href="index.html" id="top-link" class="skel-layers-ignoreHref"><span class="icon fa-home">Intro</span></a></li>
								<li><a href="about.html" id="portfolio-link" class="skel-layers-ignoreHref"><span class="icon fa-cog">About</span></a></li>
								<li><a href="send.html" id="contact-link" class="skel-layers-ignoreHref"><span class="icon fa-cloud-upload">Send</span></a></li>
								<li><a href="check.html" id="about-link" class="skel-layers-ignoreHref"><span class="icon fa-cloud-download">Check </span></a></li>
								<li><a href="rockblock.html" id="about-link" class="skel-layers-ignoreHref"><span class="icon fa-signal">Rockblock  </span></a></li>
								
							</ul>
						</nav>

				</div>

			</div>

	<!-- Main -->
			<div id="main">

				<!-- Send -->
					<section id="send" class="four">
						<div class="container">
 							
 							<header>
                            <h2>Transmission results</h2>
                            </header>
                            
  							<p>%s</p>
  			            </div>
                    </section>

            </div>


		<!-- Footer -->
			<div id="footer">

				<!-- Copyright -->
					<ul class="copyright">
					<br />%s<br />
					</ul>
			</div>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/jquery.scrollzer.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
			<script src="assets/js/main.js"></script>

	</body>
</html>
""" % (MoDisplay,status)


#
# Check Messages
#


class Check(Resource):
    
    

    def render_GET(self, request):
        global MtDisplay
        global status
        
        ser = serial
        print ""
        print ""
        print "Checking antenna communication : "

        try:
           ser = serial.Serial(serialport, 19200, timeout=5)

           if(ser == None or ser.isOpen() == False):
                print 'Communication problem with antenna'
                status = 'No Satellite communication available. Check connections'
                buttontext = "NoSatelliteDeviceError"
                ser.close()
           else:
              ser.close()
              print "OK"
              buttontext = "Check"
              status = 'Satellite communication available'



        except serial.serialutil.SerialException:
           print 'Communication problem with antenna'
           status = 'No Satellite communication available. Check connections'
           buttontext = "NoSatelliteDeviceError"
        return """
<!DOCTYPE HTML>
<!--
	Prologue by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>Sat Messenger</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
		<link rel="stylesheet" href="assets/css/main.css" />
		<!--[if let IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
		<!--[if let IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
	</head>
	<body>

		<!-- Header -->
			<div id="header">

				<div class="top">

					<!-- Logo -->
						<div id="logo">
							<span class="image avatar48"><img src="images/avatar.png" alt="" /></span>
							<h1 id="title">Sat Messenger</h1>
							<p>choose you action</p>
						</div>

					<!-- Nav -->
						<nav id="nav">
							<!--

								Prologue's nav expects links in one of two formats:

								1. Hash link (scrolls to a different section within the page)

								   <li><a href="#foobar" id="foobar-link" class="icon fa-whatever-icon-you-want skel-layers-ignoreHref"><span class="label">Foobar</span></a></li>

								2. Standard link (sends the user to another page/site)

								   <li><a href="http://foobar.tld" id="foobar-link" class="icon fa-whatever-icon-you-want"><span class="label">Foobar</span></a></li>

							-->
							<ul>
								<li><a href="index.html" id="top-link" class="skel-layers-ignoreHref"><span class="icon fa-home">Intro</span></a></li>
								<li><a href="about.html" id="portfolio-link" class="skel-layers-ignoreHref"><span class="icon fa-cog">About</span></a></li>
								<li><a href="send.html" id="contact-link" class="skel-layers-ignoreHref"><span class="icon fa-cloud-upload">Send</span></a></li>
								<li><a href="check.html" id="about-link" class="skel-layers-ignoreHref"><span class="icon fa-cloud-download">Check </span></a></li>
								<li><a href="rockblock.html" id="about-link" class="skel-layers-ignoreHref"><span class="icon fa-signal">Rockblock  </span></a></li>
								
							</ul>
						</nav>

				</div>

			</div>

		<!-- Main -->
			<div id="main">

				<!-- Send -->
					<section id="send" class="four">
						<div class="container">
							<header>
                                <h2>Check Message</h2>
                            </header>
                            
  							<p>You can receive messages sent through satellite to you. <br />
  							Here you can query for waiting messages and read them.</p>


                           <form method="post" action="#">
								<div class="row">
									<div class="12u$">
										<input type="submit" value=%s />
									</div>
								</div>
							</form>

                        </div>
                    </section>

            </div>


		<!-- Footer -->
			<div id="footer">

				<!-- Copyright -->
					<ul class="copyright">
					<br />%s<br />
					</ul>

			</div>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/jquery.scrollzer.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
			<script src="assets/js/main.js"></script>

	</body>
</html>"""% (buttontext,status)


#
# Check Messages Results
#


    def render_POST(self, request):
        global MtDisplay
        global status
        global MtData
        
        MtDisplay = ""
        
        
        if status == 'Satellite communication available':
          
             mt = MtExample()
    
             rb = rockBlock.rockBlock(serialport, mt)           
                                                                        
             rb.messageCheck()
             rb.close()

             time.sleep(1)

        else:
             MtDisplay = "NoSatelliteDevice"
             
        return """

<!DOCTYPE HTML>
<!--
	Prologue by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>Sat Messenger</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
		<link rel="stylesheet" href="assets/css/main.css" />
		<!--[if let IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
		<!--[if let IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
		<meta http-equiv="refresh" content="5; URL=index.html">
	</head>
	<body>

		<!-- Header -->
			<div id="header">

				<div class="top">

					<!-- Logo -->
						<div id="logo">
							<span class="image avatar48"><img src="images/avatar.png" alt="" /></span>
							<h1 id="title">Sat Messenger</h1>
							<p>choose you action</p>
						</div>

					<!-- Nav -->
						<nav id="nav">
							<!--

								Prologue's nav expects links in one of two formats:

								1. Hash link (scrolls to a different section within the page)

								   <li><a href="#foobar" id="foobar-link" class="icon fa-whatever-icon-you-want skel-layers-ignoreHref"><span class="label">Foobar</span></a></li>

								2. Standard link (sends the user to another page/site)

								   <li><a href="http://foobar.tld" id="foobar-link" class="icon fa-whatever-icon-you-want"><span class="label">Foobar</span></a></li>

							-->
							<ul>
								<li><a href="index.html" id="top-link" class="skel-layers-ignoreHref"><span class="icon fa-home">Intro</span></a></li>
								<li><a href="about.html" id="portfolio-link" class="skel-layers-ignoreHref"><span class="icon fa-cog">About</span></a></li>
								<li><a href="send.html" id="contact-link" class="skel-layers-ignoreHref"><span class="icon fa-cloud-upload">Send</span></a></li>
								<li><a href="check.html" id="about-link" class="skel-layers-ignoreHref"><span class="icon fa-cloud-download">Check </span></a></li>
								<li><a href="rockblock.html" id="about-link" class="skel-layers-ignoreHref"><span class="icon fa-signal">Rockblock  </span></a></li>
								
							</ul>
						</nav>

				</div>

			</div>

		<!-- Main -->
			<!-- Main -->
			<div id="main">

				<!-- Send -->
					<section id="send" class="four">
						<div class="container">
 							
 							<header>
                            <h2>Transmission results</h2>
                            </header>
                            
  							<p>%s<br />
  							Messages : %s<br />
  							</p>

                        </div>
                    </section>

            </div>


		<!-- Footer -->
			<div id="footer">

				<!-- Copyright -->
					<ul class="copyright">
					<br />%s<br />
					</ul>
			</div>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/jquery.scrollzer.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
			<script src="assets/js/main.js"></script>

	</body>
</html>
""" % (MtDisplay, MtData,status)

#
# Rockblock page
#

class Rockblock(Resource):
    
    

    def render_GET(self, request):
        global MtDisplay
        global status
        buttontext = "Check"
              
        status = 'Satellite communication available'
        
        
        ser = serial
        print ""
        print ""
        print "Checking antenna communication : "

        try:
           ser = serial.Serial(serialport, 19200, timeout=5)

           if(ser == None or ser.isOpen() == False):
                print 'Communication problem with antenna'
                status = 'No Satellite communication available. Check connections'
                buttontext = "NoSatelliteDeviceError"
                ser.close()
           else:
              ser.close()
              print "OK"
              buttontext = "Check"
              status = 'Satellite communication available'



        except serial.serialutil.SerialException:
           print 'Communication problem with antenna'
           status = 'No Satellite communication available. Check connections'
           buttontext = "NoSatelliteDeviceError"
       
        return """
<!DOCTYPE HTML>
<!--
	Prologue by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>Sat Messenger</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
		<link rel="stylesheet" href="assets/css/main.css" />
		<!--[if let IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
		<!--[if let IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
	</head>
	<body>

		<!-- Header -->
			<div id="header">

				<div class="top">

					<!-- Logo -->
						<div id="logo">
							<span class="image avatar48"><img src="images/avatar.png" alt="" /></span>
							<h1 id="title">Sat Messenger</h1>
							<p>choose you action</p>
						</div>

					<!-- Nav -->
						<nav id="nav">
							<!--

								Prologue's nav expects links in one of two formats:

								1. Hash link (scrolls to a different section within the page)

								   <li><a href="#foobar" id="foobar-link" class="icon fa-whatever-icon-you-want skel-layers-ignoreHref"><span class="label">Foobar</span></a></li>

								2. Standard link (sends the user to another page/site)

								   <li><a href="http://foobar.tld" id="foobar-link" class="icon fa-whatever-icon-you-want"><span class="label">Foobar</span></a></li>

							-->
							<ul>
								<li><a href="index.html" id="top-link" class="skel-layers-ignoreHref"><span class="icon fa-home">Intro</span></a></li>
								<li><a href="about.html" id="portfolio-link" class="skel-layers-ignoreHref"><span class="icon fa-cog">About</span></a></li>
								<li><a href="send.html" id="contact-link" class="skel-layers-ignoreHref"><span class="icon fa-cloud-upload">Send</span></a></li>
								<li><a href="check.html" id="about-link" class="skel-layers-ignoreHref"><span class="icon fa-cloud-download">Check </span></a></li>
								<li><a href="rockblock.html" id="about-link" class="skel-layers-ignoreHref"><span class="icon fa-signal">Rockblock  </span></a></li>
								
							</ul>
						</nav>

				</div>

			</div>

		<!-- Main -->
			<div id="main">

				<!-- Send -->
					<section id="send" class="four">
						<div class="container">
							<header>
                                <h2>Rockblock Infos</h2>
                            </header>
                            
  							<p>Here you can get basic information from your Rockblock<br />
  							Useful also to check Iridium Satellites Signal</p>


                           <form method="post" action="#">
								<div class="row">
									<div class="12u$">
										<input type="submit" value=%s />
									</div>
								</div>
							</form>

                        </div>
                    </section>

            </div>


		<!-- Footer -->
			<div id="footer">

				<!-- Copyright -->
					<ul class="copyright">
					<br />%s<br />
					</ul>

			</div>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/jquery.scrollzer.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
			<script src="assets/js/main.js"></script>

	</body>
</html>"""% (buttontext,status)

#
# Rockblock results
#


    def render_POST(self, request):
        global MtDisplay
        global status
        
        MtDisplay = ""
        
        if status == "No Satellite communication available. Check connections":
      
             return """
        <!DOCTYPE HTML>
<html>
	<head>
		<title>Sat Messenger</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
		<link rel="stylesheet" href="assets/css/main.css" />
		<!--[if let IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
		<!--[if let IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
		<meta http-equiv="refresh" content="1; URL=rockblock.html">
	</head>
	<body>
	"""  
        else:
          
             inf = InfoDisplay()
    
             rb = rockBlock.rockBlock(serialport, inf)           

             
             rockserial = str(rb.getSerialIdentifier())
             print 'Antenna serial number : ' + rockserial
                
             rockmodel = str(rb.model())
             print 'Antenna model : ' + str(rb.model())
             #print 'Antenna revision : ' + str(rb.revision())
        
             momsn = rb.momsn().split(',')
             print 'Momsn : ' + momsn[1]
        
             signal = rb.requestSignalStrength() 
             print "Signal (0-5) : " + str(signal) 
        
             if signal > -1:
        
                      a = arrow.get(rb.networkTime())
                      print 'UTC Time : ' + str(a.datetime)
                      rockgps =  str(rb.geo())
                      print 'GPS position : ' + rockgps

             rb.close()

             time.sleep(1)

             
             return """

<!DOCTYPE HTML>
<!--
	Prologue by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>Sat Messenger</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
		<link rel="stylesheet" href="assets/css/main.css" />
		<!--[if let IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
		<!--[if let IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
	</head>
	<body>

		<!-- Header -->
			<div id="header">

				<div class="top">

					<!-- Logo -->
						<div id="logo">
							<span class="image avatar48"><img src="images/avatar.png" alt="" /></span>
							<h1 id="title">Sat Messenger</h1>
							<p>choose you action</p>
						</div>

					<!-- Nav -->
						<nav id="nav">
							<!--

								Prologue's nav expects links in one of two formats:

								1. Hash link (scrolls to a different section within the page)

								   <li><a href="#foobar" id="foobar-link" class="icon fa-whatever-icon-you-want skel-layers-ignoreHref"><span class="label">Foobar</span></a></li>

								2. Standard link (sends the user to another page/site)

								   <li><a href="http://foobar.tld" id="foobar-link" class="icon fa-whatever-icon-you-want"><span class="label">Foobar</span></a></li>

							-->
							<ul>
								<li><a href="index.html" id="top-link" class="skel-layers-ignoreHref"><span class="icon fa-home">Intro</span></a></li>
								<li><a href="about.html" id="portfolio-link" class="skel-layers-ignoreHref"><span class="icon fa-cog">About</span></a></li>
								<li><a href="send.html" id="contact-link" class="skel-layers-ignoreHref"><span class="icon fa-cloud-upload">Send</span></a></li>
								<li><a href="check.html" id="about-link" class="skel-layers-ignoreHref"><span class="icon fa-cloud-download">Check </span></a></li>
								<li><a href="rockblock.html" id="about-link" class="skel-layers-ignoreHref"><span class="icon fa-signal">Rockblock  </span></a></li>
								
							</ul>
						</nav>

				</div>

			</div>

		<!-- Main -->
			<div id="main">

				<!-- Send -->
					<section id="send" class="four">
						<div class="container">
 							
 							<header>
                            <h2>Rockblock Infos</h2>
                            </header>
                            
  							<p>Signal (0-5) : %s<br />
  							Message counter : %s<br />
  							Rockblock serial number : %s<br />
  							Rockblock model : %s<br />
  							Network time : %s<br />
  							GPS position : %s<br />
  							</p>

                        </div>
                    </section>

            </div>


		<!-- Footer -->
			<div id="footer">

				<!-- Copyright -->
					<ul class="copyright">
					<br />%s<br />
					</ul>
			</div>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/jquery.scrollzer.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
			<script src="assets/js/main.js"></script>

	</body>
</html>
""" % (signal,  momsn[1], rockserial, rockmodel, str(a.datetime), rockgps, status)

#
# Main Twisted
#

root = Resource()
root.putChild('', static.File("index.html"))
root.putChild('index.html', static.File("index.html"))
root.putChild('about.html', static.File("about.html"))
root.putChild('check.html', Check())
root.putChild('send.html', Send())
root.putChild('rockblock.html', Rockblock())
root.putChild('assets', static.File("./assets"))
root.putChild('images', static.File("./images"))
factory = Site(root)

reactor.listenTCP(8080, factory)
#loopmin = task.LoopingCall(everyMin())
#loopmin.start(300.0)

reactor.run()




