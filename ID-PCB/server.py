#!/usr/bin/python
# -*- coding: utf8 -*-

import socket, string, time, ssl
import urllib, re, os

def main():
     
    network = 'irc.init6.me'
    chan = 'pwcrack'
    port = 16667
    nick = 'yourMaster'

    connect(network, nick, chan, port)
    

        
def connect(network, nick, chan, port):
    #not sure why I needed to included the import socket here as well??
    import socket, string, time, ssl
    import urllib, re, os
        
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.connect((network,port))
    irc = ssl.wrap_socket(socket)
    irc.send('NICK %s\r\n' % nick)
    print irc.recv(4096)
    irc.send('USER %s %s %s :My bot\r\n' % (nick,nick,nick))
    print irc.recv(4096)
    irc.send('JOIN #%s\r\n' % chan)
    print irc.recv(4096)
    #irc.send('JOIN #%s\r\n' % chan1)
	
    while True:
        data = irc.recv(4096)
        print data

	if data.find('PING') != -1:
            irc.send('PONG '+data.split()[1]+'\r\n')
	if data.find('!safeword\r\n') != -1:
            irc.send('QUIT\r\n')
            exit()#exits python. 
	if data.find('!ready') != -1:
            clientData = data.split('.')[1:]
            clientID = clientData[1]
            system = clientData[2]
            bits = clientData[3]
            cpuCores = clientData[4]
            gpuType = clientData[5]
            #add an options for brute force and call different buildcmd()
            amode = 3 #bruteforce
            algorithm = 0 #MD5
            ofile = 'found.3.md5' #outputFileName() #create a output file name based on attack mode and algorithm
            hashfile = 'left.md5' #getHashfile() #depending on algorithm get hashfile
            bruteforce = '-1 abcABC ?1?1?1?1?1?1?1?1' #getBruteforce() #depending gpu/cpu/rating
            command = buildcmd(clientID, system, bits, cpuCores, gpuType, amode, algorithm, ofile, hashfile, bruteforce)
            chan1 = 'pwc'+'_'.join(clientID.split('_')[1:])
            print "clientID: " +clientID+"\nthis is the command to run " + command + '\n'
            irc.send('JOIN #%s\r\n' % chan1)
            msg = '!'+clientID+''+str(command)
            irc.send('PRIVMSG #%s %s\r\n' % (chan1, msg))


                 
        print data

def buildcmd(clientID, system, bits, cpuCores, gpuType, amode, algorithm, ofile, hashfile, bruteforce):
    command = ''
    if system == 'Windows':
        if bits == "32bit":
            if gpuType == "ATI" or gpuType == "AMD":
                command = "oclHashcat-plus32.exe --help"
                

            else: #build hashcat cpu command see http://hashcat.net/wiki/doku.php?id=hashcat
                command = "hashcat-cli32.exe --remove --disable-potfile -n "+cpuCores+" -a "+str(amode)+" -m "+str(algorithm)+" -o "+ofile+" "+hashfile+" "+bruteforce
                
        if bits == "64bit":
            if gpuType == "ATI" or gpuType == "AMD":
                command = "oclHashcat-plus64.exe --help"

            else: #build hashcat cpu command see http://hashcat.net/wiki/doku.php?id=hashcat
                command = "hashcat-cli64.exe --remove --disable-potfile -n "+cpuCores+" -a "+str(amode)+" -m "+str(algorithm)+" -o "+ofile+" "+hashfile+" "+bruteforce
    

    return command

        
    if system == 'Linux':
        print "Linux"

    if system == 'Darwin':
        print "Darwin"
    
main()
