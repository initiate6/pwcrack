#!/usr/bin/python
# -*- coding: utf8 -*-
############################################

import socket, string, ssl
import urllib, re, os
import shlex

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
        if re.match("^pass\.", line):
            password = line.split('.')[1]
        if re.match("^email\.",line):
            email = '.'.join(line.split('.')[1:])
            
    chan1 = 'pwc'+ '_'.join(nick.split('_')[1:])
    print chan1, nick, system, bits, threads, gpu, password, email

    connect(network, nick, chan, chan1, port, system, bits, threads, gpu, password, email)
    
def readsysinfo():
    try:
        sysinfo = [line.strip('\n') for line in open('sysinfo', 'r')]
        return sysinfo

    except IOError as e:
        print("({0})".format(e))
        
def connect(network, nick, chan, chan1, port, system, bits, threads, gpu, password, email):
    import socket, string, time, ssl
    import urllib, re, os
    from async_subprocess import AsyncPopen, PIPE

    def ircmsg(ircCMD, channel, msg):
        irc.send('%s #%s %s\r\n' % (ircCMD, channel, msg))
    def join(channel):
        irc.send('JOIN #%s \r\n' % channel)
        
    def command(cmd):
        import time
        import datetime as dt
        
	#excute command on PC
	
	args = shlex.split(cmdline)
        print "This is the args: %s" % args
        
	process = AsyncPopen(args,
                            stdin=PIPE,
                            stdout=PIPE,
                            stderr=PIPE
                            )
	retcode = process.poll()
	while retcode == None:
<<<<<<< HEAD
		stdoutdata, stderrdata = process.communicate(updateKey)
		#if stderrdata:
			#print stderrdata # switch to irc.send(stderrdata) and throw error
		if stdoutdata:
			print stdoutdata # switch to irc.send(stdoutdata) to update room. 
		time.sleep(5) #in seconds
		#Check if Saturday 8/3/2013 if so Check hour >= 23:35 to kill process and upload found files and exit. 
                date = dt.date.today().isoformat()
                timeMinSec =  '.'.join(str(dt.datetime.today()).split()[1].split(':')[:2])
                if date == '2013-08-03':
                    if float(timeMinSec) >=  23.35:
                        print "Time is up, closing and uploading what we have done so far"
                        #excute upload stuff. maybe just do a break.
                    else:
                        pass
=======
            time.sleep(1) #in seconds
	    stdoutdata, stderrdata = process.communicate('s')
	    if stderrdata:
                print stderrdata # switch to irc.send(stderrdata) and throw error
	    if stdoutdata:
                #ircmsg('PRIVMSG', chan1, stdoutdata)
                print stdoutdata # switch to irc.send(stdoutdata) to update room. 
		
	    #Check if Saturday 8/3/2013 if so Check hour >= 23:35 to kill process and upload found files and exit. 
            #date = dt.date.today().isoformat()
            #timeMinSec =  '.'.join(str(dt.datetime.today()).split()[1].split(':')[:2])
            #if date == '2013-08-03':
		#if float(timeMinSec) >=  23.35:
		#print "Time is up, closing and uploading what we have done so far"
                #excute upload stuff. maybe just do a break.
                #stdoutdata, stderrdata = process.communicate('q')
            #else:
                #pass
>>>>>>> a few changes to client and initalbrute
                        
	    retcode = process.poll()

	#upload found file to FTP server.
	#fileUpload(foundfile)
		#if fileUplod doesn't work return False
    
	return True 

    
    	
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.connect((network,port))
    irc = ssl.wrap_socket(socket)
    irc.send('NICK %s\r\n' % nick)
    print irc.recv(4096)
    irc.send('USER %s %s %s :My bot\r\n' % (nick,nick,nick))
    print irc.recv(4096)
    join(chan)
    print irc.recv(4096)
    join(chan1)
    
    state = 'standby'
    msg = '!register.'+nick+'.'+state+'.'+system+'.'+bits+'.'+str(threads)+'.'+gpu+'.'+password+'.'+email
    ircmsg('PRIVMSG', chan, msg)
	
    while True:
        data = irc.recv(4096)
        print data

	if data.find('PING') != -1:
            irc.send('PONG '+data.split()[1]+'\r\n')
	if data.find('!gtfo\r\n') != -1:
            irc.send('QUIT\r\n')
            exit()#exits python.
            
	if data.find('!%s' % (nick) ) != -1:
            cmd = '!'.join(data.split('!')[2:])
            cmdline = ' '.join(cmd.split('..')[1:])
<<<<<<< HEAD
            #cmdline = re.sub('[\.]{2}', ' ', re.escape(str(cmd)))
            print "command before fuction: %s " % cmdline
            if command(cmdline):
                msg1 = '!update.'+nick+'.'+'ready'+'.'+system+'.'+bits+'.'+str(threads)+'.'+gpu+'.'+password+'.'+email
                ircmsg('PRIVMSG', chan1, msg1)
            else:
                msg2 = '!update.'+nick+'.'+'error'+'.'+system+'.'+bits+'.'+str(threads)+'.'+gpu+'.'+password+'.'+email
                ircmsg('PRIVMSG', chan1, msg2)
                
=======
            command(cmdline)
>>>>>>> a few changes to client and initalbrute
            
        if data.find('!GITHASHES') != -1:
            if dlHashes() == 'Successful':
                break
            elif dlHashes() == 'Successful':
                break
            else:
                print "something went wrong downloading hash files "
                
        if data.find('!GITWORDLIST') != -1:
            if dlWordlist() == 'Successful':
                break
            elif dlwordlist() == 'Successful':
                break
            else:
                print "something went wrong downloading hash files "
                
        print data

def fileUpload(foundfile):
    print "file has been uploaded"
    #upload found file to FTP site
    
def dlHashes():
    return 'Successful'

def dlWordlist():
    return 'Successful'

    
main()
