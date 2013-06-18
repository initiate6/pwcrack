Name: IRC distributed password cracking bot. ID-PCB

Verify.py Check to see if python 2.7 is installed. Check if all libraries can be found on computer if not install them. Check to see if hashcat  is located on computer if not download it.

ginfo.py gather info on computer. OS type and version, 32bit/64bit, how many cores, how much memory, Video cards, driver versions. If something is wrong notify how to fix it. create client ID. Save to file. 

Client.py Connect to IRC server and give clientID and status of computer. Wait for command.Excute command and grab a stats upadte every 5mins and post to its personal irc channel. 



server.py Connect to IRC server. Wait to see .ready ClientID computer info.   Gives next payload to ready client.

BuildPayload.py Creates all the different payloads for the different algrothems and keeps track what has been done and what to do next. 
