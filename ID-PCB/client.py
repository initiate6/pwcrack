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
        if re.match("^gpuType\.",line):
            gpu = line.split('.')[1]
        if re.match("^email\.",line):
            email = '.'.join(line.split('.')[1:])
            
    chan1 = 'pwc'+ '_'.join(nick.split('_')[1:])
    print chan1
    print nick
    print system
    print bits
    print threads
    print gpu
    print email

    connect(network, nick, chan, chan1, port, system, bits, threads, gpu, email)
    
def readsysinfo():
    try:
        sysinfo = [line.strip('\n') for line in open('sysinfo', 'r')]
        return sysinfo

    except IOError as e:
        print("({0})".format(e))
        
def connect(network, nick, chan, chan1, port, system, bits, threads, gpu, email):
    #not sure why I needed to included the import socket here as well??
    import socket, string, time, ssl
    import urllib, re, os
    from async_subprocess import AsyncPopen, PIPE
        
    def command(cmd):
	clientID = cmd[0].strip(':')
	cmdline = ' '.join(cmd[1:])
	print cmdline
	#send irc.send(!busy to update server with client status)
	#excute command on PC
	#Need to repace the args with the vars.  
	args = ("hashcat-cli32.exe", "-m 100", "-a 3", "-n 2", "A0.M100.hash", "?a?a?a?a?a")
	process = AsyncPopen(args,
                            stdin=PIPE,
                            stdout=PIPE,
                            stderr=PIPE
                            )
	retcode = process.poll()
	while retcode == None:
		stdoutdata, stderrdata = process.communicate('\n')
		if stderrdata:
			print stderrdata # switch to irc.send(stderrdata) and throw error
		if stdoutdata:
			print stdoutdata # switch to irc.send(stdoutdata) to update room. 
		time.sleep(5) #in seconds
		retcode = process.poll()

    
    	
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
    msg = '!ready.'+nick+'.'+system+'.'+bits+'.'+str(threads)+'.'+gpu+'.'+email
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

    
    
main()
