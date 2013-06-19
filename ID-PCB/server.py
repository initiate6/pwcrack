#!/usr/bin/python
# -*- coding: utf8 -*-

import socket, string, time, ssl
import urllib, re, os, sqlite3

def main():
    
    #some functions to help repetitive task in connect()
    def msg(ircCMD, channel, msg):
        irc.send(ircCMD +'#'+ msg + '\r\n')
    def join(channel)
        irc.send('JOIN #%s \r\n' % channel)
        
    network = 'irc.init6.me'
    chan = 'pwcrack'
    port = 16667
    nick = 'yourMaster'
    
    conn = sqlite3.connect('pwcrack.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE clients
                 (clientID text, system text, bits text, Threads text, gpuType text, options text)''')    
        
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.connect((network,port))
    irc = ssl.wrap_socket(socket)
    irc.send('NICK %s\r\n' % nick)
    print irc.recv(4096)
    irc.send('USER %s %s %s :My bot\r\n' % (nick,nick,nick))
    print irc.recv(4096)
    join(chan)
    print irc.recv(4096)
	
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
            c.execute("INSERT INTO clients VALUES (clientID, system, bits, cpuCores, gpuType, '')")
        
        print data
        msg('PRIVMSG', chan, ".update")

def something():
        command = buildcmd(clientID, system, bits, cpuCores, gpuType, amode, algorithm, ofile, hashfile, bruteforce)
        chan1 = 'pwc'+'_'.join(clientID.split('_')[1:])
        join(chan1)
        msg = '!'+clientID+''+str(command)
        irc.send('PRIVMSG #%s %s\r\n' % (chan1, msg))

def options():

    #hashfile name
    #charset and bruteforce
    ofile = 'found.3.md5' #outputFileName() #create a output file name based on attack mode and algorithm
    amode = 3 #bruteforce
    algorithm = 0 #MD5
    hashfile = 'left.md5'
    charset =
    rules1 =
    

    
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
