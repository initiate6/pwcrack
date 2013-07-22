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
        
        charset1 = "?l?u?d?s"
        charset2 = "?l?u?d?s?h"
        charset3 = "?l?u?d?s?D"
        charset4 = "?l?u?d?s?F"
        charset5 = "?l?u?d?s?R"
        charset6 = "?l?u?d?s?h?D?F?R"
        
	#split up string into arguments.
	args = shlex.split(cmdline)
        statusKey = '\n'

        #Get the file name for the found passwords, and change the status key to 's' if gpu based.
        for arg in args:
            if re.search('found', arg):
                foundfile = arg
            if re.search('plus', arg):
                statusKey = 's'
            if re.search('charset', arg):
                if arg == 'charset1':
                    charset = charset1
                    index = args.index(arg)
                    args.remove(arg)
                    args.insert(index, charset)
            
                elif arg == 'charset2':
                    charset = charset2
                    index = args.index(arg)
                    args.remove(arg)
                    args.insert(index, charset)
                    
                elif arg == 'charset3':
                    charset = charset3
                    index = args.index(arg)
                    args.remove(arg)
                    args.insert(index, charset)
                    
                elif arg == 'charset4':
                    charset = charset4
                    index = args.index(arg)
                    args.remove(arg)
                    args.insert(index, charset)

                elif arg == 'charset4':
                    charset = charset4
                    index = args.index(arg)
                    args.remove(arg)
                    args.insert(index, charset)
                    
                elif arg == 'charset5':
                    charset = charset5
                    index = args.index(arg)
                    args.remove(arg)
                    args.insert(index, charset)
                    
                elif arg == 'charset6':
                    charset = charset6
                    index = args.index(arg)
                    args.remove(arg)
                    args.insert(index, charset)
                    
                    
        print "This is the args: %s" % args        
                
        #excute command
	process = AsyncPopen(args,
                            stdin=PIPE,
                            stdout=PIPE,
                            stderr=PIPE
                            )
	retcode = process.poll()
	
	while retcode == None:
            time.sleep(5) #in seconds
	    stdoutdata, stderrdata = process.communicate(statusKey)
	    if stderrdata:
                print stderrdata
	    if stdoutdata:
                outdata = re.sub(' ', '..', stdoutdata)
                ircmsg('PRIVMSG', chan1, outdata)
                print outdata
		
	    #Check if Saturday 8/3/2013 if so Check hour >= 23:35 to kill process and upload found files and exit. 
            date = dt.date.today().isoformat()
            timeMinSec =  '.'.join(str(dt.datetime.today()).split()[1].split(':')[:2])
            if date == '2013-08-03':
		if float(timeMinSec) >=  23.35:
                    print "Time is up, closing and uploading what we have done so far"
                    if statusKey == 's':
                        stdoutdata, stderrdata = process.communicate('q')
                        ftpUpload(foundfile, system)
                        return True
                    else:
                        process.terminate()
                        ftpUpload(foundfile, system)
                        return True
            else:
                pass
                        
	    retcode = process.poll()

	#upload found file to FTP server.
	ftpUpload(foundfile, system)
	
    
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
            
            if command(cmdline):
                msg1 = '!update.'+nick+'.'+'ready'+'.'+system+'.'+bits+'.'+str(threads)+'.'+gpu+'.'+password+'.'+email
                ircmsg('PRIVMSG', chan1, msg1)
            else:
                msg2 = '!update.'+nick+'.'+'error'+'.'+system+'.'+bits+'.'+str(threads)+'.'+gpu+'.'+password+'.'+email
                ircmsg('PRIVMSG', chan1, msg2)

            
        if data.find('!GET') != -1:
            output = '!'.join(data.split('!')[2:])
            filename = '.'.join(output.split('.')[1:]).strip('\r\n')
            ftpDownload(filename, system)
                
        if data.find('!PUSH') != -1:
            output = '!'.join(data.split('!')[2:])
            filename = '.'.join(output.split('.')[1:]).strip('\r\n')
            ftpUpload(filename, system)
            
        print data



def ftpUpload(filename, system):
    
    from ftplib import FTP_TLS
    import os

    zipFilename = compressit(filename, system)
    
    ftps = FTP_TLS()
    ftps.connect('pwcrack.init6.me', '21')
    ftps.auth()
    ftps.login('DC214', 'passwordcrackingcontest')
    ftps.prot_p()
    ftps.set_pasv(True)
    local_file = open(zipFilename, 'rb')
    ftps.storbinary('STOR '+zipFilename, local_file)

    print "file %s has been uploaded." % zipFilename
    
def ftpDownload(filename, system):
    from ftplib import FTP_TLS
    import os

    ftps = FTP_TLS()
    ftps.connect('pwcrack.init6.me', '21')
    ftps.auth()
    ftps.login('DC214', 'passwordcrackingcontest')
    ftps.prot_p()
    ftps.set_pasv(True)
    local_filename = filename
    with open(local_filename, 'wb') as f:
        def callback(data):
            f.write(data)
        ftps.retrbinary('RETR %s' % filename, callback)
    f.close()

    file_extension = str(filename.split('.')[1])
    
    if file_extension == '7z':
        status = decompressit(local_filename, system)
        if status:
            print "file %s hash been downloaded." % local_filename
    

def compressit(filename, system):
    from subprocess import Popen, PIPE
    
    zipFilename = str(filename.split('.')[0]) + '.7z'

    if system == 'Windows':
        args = '7za.exe', 'a', zipFilename, filename
    elif system == 'Linux':
        args = './7za', 'a', zipFilename, filename

    compressFile = Popen(args, stdout=PIPE)
    output = compressFile.communicate()[0]

    if re.search("Everything is Ok", output):
        return zipFilename
    else:
        print "something went wrong compressing %s" % filename
        
def decompressit(zipFilename, system):
    from subprocess import Popen, PIPE

    if system == 'Windows':
        args = '7za.exe', 'x', '-y', zipFilename
    if system == 'Linux':
        args = './7za', 'x', '-y', zipFilename
        
    decompressFile = Popen(args, stdout=PIPE)
    output = decompressFile.communicate()[0]
    
    if re.search("Everything is Ok", output):
        return True
    else:
        print "something went wrong decompressing %s" % zipFilename
        
main()
