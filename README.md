#
# Sat Messenger/RBS
# v0.2
#

Sat Messenger and RBS (Recovery Base Station) 
A satellite gateway for short messages (SBD), that uses Rockblock hardware


For extensive description : 

- RBS wiki : http://www.tmplab.org/wiki/index.php/Sat_Messenger_/_RBS
- Rockblock serial communication wiki : http://www.tmplab.org/wiki/index.php/Raw_sat


v0.2 : 
- Webui to handle rockblock operations : rockblock infos like signal quality,... send and check messages 
- Forwards received messages to some email 
- Command line tools
- Remember there is no crypto at all. All encrypt version will be here soon.



Install all dependancies you'll need.
i.e : pip install twisted



#
# Web Interface :
#
# Forward a text message to destination email
# Web Interface->rockblock->satellite->rockblock servers->sat messenger server->email
# 


1. Launch with : python mainnocrypto.py
2. Browse to http://127.0.0.1:8080

3. Install and run mainservernocrypto.py on some online server that can handle connexion (default is port 8888, check your firewall rules)
4. Configure in your account at http://rockblock.rock7.com a 'destination' like http://themachinethatrunmainserver:8888




#
# Command lines for basic rockblock operations with no encryption whatsoever :
# 


- infos : Display Antenna serial number, Antenna model, next outbound message number (momsn), Signal (0-5), Network time and GPS position.

       ./infos.py or python infos.py
       

- mo : Send a message to rockblock account destination through satellite in clear text. Ask the message text. MO means mobile originated. ->rockblock->satellite->email.

       python mo.py

- mt : Check for queued messages for the rockblock and display if any are available. MT means mobile terminated. satellite waiting->rockblock->

       python mt.py

- httpmt : send a message to the rockblock ->Internet->satellite->rockblock

       python httpmt.py
