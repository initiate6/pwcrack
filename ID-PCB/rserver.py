#!/usr/bin/python
# -*- coding: utf8 -*-

import socket, string, time, ssl
import urllib, re, os, sqlite3


def main():
    import socket, string, time, ssl
    import urllib, re, os, sqlite3
    
    #some functions to help repetitive task in connect()
    def msg(ircCMD, channel, msg):
        irc.send(ircCMD +'#'+ msg + '\r\n')
    def join(channel):
        irc.send('JOIN #%s \r\n' % channel)
        
    network = 'irc.init6.me'
    chan = 'pwcrack'
    port = 16667
    nick = 'TPSreport'
    
        
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
            addclient(clientID, system, bits, cpuCores, gpuType)
        
        print data
        msg('PRIVMSG', chan, ".update")
    
def createDB():
       
    conn = sqlite3.connect('pwcrack.db')
    c = conn.cursor()

    #create table clients and data names/types 
    c.execute('''CREATE TABLE IF NOT EXISTS clients
                 (clientID text, system text, bits text, Threads text, gpuType text)''') 

    #create table algorithms and data names/types 
    c.execute('''CREATE TABLE IF NOT EXISTS algorithms
                 (algorithm text, AMD-accel text, AMD-loops text, NV-accel text, NV-loops text)''')

    #create a table completed. track all clients and the command they excuted and if it finished or cutoff.
    #Add support down the line for how many recoverd. 
    c.execute('''CREATE TABLE IF NOT EXISTS completed
                 (clientID text, completed text, command text)''')

    conn.commit()
    c.close()
    conn.close()
        
    
def addclient(clientID, system, bits, cpuCores, gpuType):
        
    conn = sqlite3.connect('pwcrack.db')
    c = conn.cursor()
    #lookup clientID in database to see if it exist if not add client.

    for row in c.execute("SELECT * FROM clients"):
        if clientID not in row[0]:
            

    


    
    c.execute("INSERT INTO clients VALUES (clientID, system, bits, cpuCores, gpuType)")
    



def LoadAlgorithms():
    

















    
main()
