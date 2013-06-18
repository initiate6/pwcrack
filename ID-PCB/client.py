#!/usr/bin/python
# -*- coding: utf8 -*-
############################################

import socket, string, time, ssl
import urllib, re, os

def main():
     
    network = 'irc.init6.me'
    chan = 'pwcrack'
    port = 16667
    sysinfo = readsysinfo()
    for line in sysinfo:
        if re.match("^CID_",line):
            nick = line 
        if re.match("^system\.",line):
            system = line.split('.')[1]
        if re.match("^bits\.",line):
            bits = line.split('.')[1]
        if re.match("^cpuCount\.",line):
            threads = int(line.split('.')[1])
        if re.match("^gpu\.",line):
            gpu = line.split('.')[1]
            
    chan1 = 'pwc'+ '_'.join(nick.split('_')[1:])
    print chan1
    print nick
    print system
    print bits
    print threads
    print gpu

    connect(network, nick, chan, chan1, port, system, bits, threads, gpu)
    
def readsysinfo():
    try:
        sysinfo = [line.strip('\n') for line in open('sysinfo', 'r')]
        return sysinfo

    except IOError as e:
        print("({0})".format(e))
        
def connect(network, nick, chan, chan1, port, system, bits, threads, gpu):
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
    irc.send('JOIN #%s\r\n' % chan1)
    msg = '!ready.'+nick+'.'+system+'.'+bits+'.'+str(threads)+'.'+gpu
    irc.send('PRIVMSG #%s %s\r\n' % (chan,msg))
	
    while True:
        data = irc.recv(4096)
        print data

	if data.find('PING') != -1:
            irc.send('PONG '+data.split()[1]+'\r\n')
	if data.find('!gtfo\r\n') != -1:
            irc.send('QUIT\r\n')
            exit()#exits python. 
	if data.find('!CID') != -1:
            cmd = data.split()[3:]
            command(cmd)
        print data

def command(cmd):
    clientID = cmd[0].strip(':')
    cmdline = ' '.join(cmd[1:])
    print cmdline
    #excute command on PC     
    
main()
