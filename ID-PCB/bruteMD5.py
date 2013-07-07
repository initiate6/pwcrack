#!/usr/bin/python
# -*- coding: utf8 -*-

import socket, string, time, ssl
import urllib, re, os, sqlite3

def main():
    
    #some functions to help repetitive task in connect()
    def msg(ircCMD, channel, msg):
        irc.send('%s #%s %s\r\n' % (ircCMD, channel, msg))
    def join(channel):
        irc.send('JOIN #%s \r\n' % channel)
        
    network = 'irc.init6.me'
    chan = 'pwcrack'
    port = 16667
    nick = 'bruteMD5'
      
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
	if data.find('!<replace>') != -1:

        print data

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
            if gpuType == "ocl":
                command = "oclHashcat-plus32.exe -m 0 -a 3 --remove --markov-hcstat=hashcat.hcstat -t 100  \
                            -o outputfile.txt --outfile-format=3 --disable-potfile -n 80 -u 1000 \
                            --gpu-temp-retain=70 example500.hash a?a?a?a?a?a?a?a "
            elif gpuType == "cuda":
                command = "cudaHashcat-Plus32.exe --help"

             
        elif bits == "64bit":
            if gpuType == "ocl":
                command = "oclHashcat-plus64.exe --help"
            elif gpuType == "cuda":
                command = "cudaHashcat-plus64.exe --help"

        
    elif system == 'Linux':
        if bits == "32bit":
            if gpuType == "ocl":
                command = "./oclHashcat-plus32.bin --help"
            elif gpuType == "cuda":
                command = "./cudaHashcat-Plus32.bin --help"

             
        elif bits == "64bit":
            if gpuType == "ocl":
                command = "./oclHashcat-plus64.bin --help"
            elif gpuType == "cuda":
                command = "./cudaHashcat-plus64.bin --help"
      

    if system == 'Darwin':
        print "Darwin"
    
main()
