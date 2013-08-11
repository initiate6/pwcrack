#!/usr/bin/python
# -*- coding: utf8 -*-
##
#Copyright 2013 (Jason Wheeler INIT6@INIT6.me) and DC214.org
#
#This file is part of ID-PCB (IRC distributed password cracking bot.)
#
#    ID-PCB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License.
#
#    ID-PCB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    To receive a copy of the GNU General Public License
#    see <http://www.gnu.org/licenses/>.
##

import socket, string, time, ssl
import urllib, re, os, sqlite3, sys


def main():
    import socket, string, time, ssl
    import urllib, re, os, sqlite3
    
    #some functions to help repetitive task in connect()
    def msg(ircCMD, channel, msg):
        irc.send('%s #%s %s\r\n' % (ircCMD, channel, msg))
    def join(channel):
        irc.send('JOIN #%s \r\n' % channel)

    #initialize the database with tables.
    createDB()
    
        
    network = 'irc.init6.me'
    chan = 'pwcrack'
    port = 16667
    nick = 'regServer'
    
        
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
	if data.find('!register') != -1:
            clientData = data.split('.')[1:]
            clientID = clientData[1]
            state = clientData[2]
            system = clientData[3]
            bits = clientData[4]
            cpuCores = clientData[5]
            gpuType = clientData[6]
            password = clientData[7]
            email = str('.'.join(clientData[8:10])).strip('\r\n')
            register(clientID, state, system, bits, cpuCores, gpuType, password, email)
        if data.find('!update') != -1:
            clientData = data.split('.')[1:]
            clientID = clientData[1]
            state = clientData[2]
            system = clientData[3]
            bits = clientData[4]
            cpuCores = clientData[5]
            gpuType = clientData[6]
            password = clientData[7]
            email = str('.'.join(clientData[8:10])).strip('\r\n')
            updateClient(clientID, state, system, bits, cpuCores, gpuType, email)
            
        
        #print data

    
def createDB():
       
    conn = sqlite3.connect('pwcrack.db')
    cur = conn.cursor()

    #create table clients and data names/types 
    cur.execute('''CREATE TABLE IF NOT EXISTS clients
                 (clientID text, state text, system text, bits text, Threads text, gpuType text, auth text, email text)''') 

    #create a table completed. track all clients and the command they excuted and if it finished or cutoff.
    #Add support down the line for how many recoverd. 
    cur.execute('''CREATE TABLE IF NOT EXISTS completed
                 (clientID text, status text, command text, foundCount text)''')

  
    conn.commit()
    cur.close()
    conn.close()
        
    
def updateClient(clientID, state, system, bits, cpuCores, gpuType, email):       
        try:
            
            conn = sqlite3.connect('pwcrack.db')

            with conn:

                cur = conn.cursor()
                cur.execute("SELECT * FROM clients")
                rows = cur.fetchall()
                    
                for row in rows:
                    if re.match(clientID,row[0]) and row[6] == 'Y': #If client is found in database and has been authicated update state
                        cur.execute("UPDATE clients SET state=? WHERE clientID=?",(state, clientID))
                        print row

        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:
            if conn:
                conn.close()

def checkPassword(password, system, bits, gpuType, clientID):
    #pull this out into a new fuction and return "clear for landing"
    if password[0] == 'W':
        if re.match('[Windo]{1,5}', password[1]) and system == 'Windows':
            if re.match('3|6', password[2]) and bits[0] == password[2]:
                if re.match('o|c|n', password[3]) and re.match('o|c|n', gpuType[0]):
                    if re.match('\d\d\d', password[4:7]):
                        if password[7:] == 'DC214':
                            print "password is a okay"
                            return True
                        else:
                            print "you're not legit"
                            return False
                            #send kill job. 
            

    elif password[0] == 'L':
        print "pass 1"
        if re.match('[Linux]{1,5}', password[1]) and system == 'Linux':
            print "pass 1"
            if re.match('3|6', password[2]) and bits[0] == password[2]:
                print "pass 2"
                if re.match('o|c|n', password[3]) and re.match('o|c|N', gpuType[0]):
                    print "pass 3"
                    if re.match('\d\d\d', password[4:7]):
                        print "pass 4"
                        if password[7:] == 'DC214':
                            print "Password is a okay TUX"
                            return True
                        else:
                            print "you're not legit"
                            return False
                            #send kill job.
    #else:
        #print "you're not legit"
        #return False
        #send kill job. 


def register(clientID, state, system, bits, cpuCores, gpuType, password, email):
    if checkPassword(password, system, bits, gpuType, clientID) == True:
        auth = "Y"
        try:                            
            clients = []
            conn = sqlite3.connect('pwcrack.db')

            with conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM clients")
                rows = cur.fetchall()
                #if table is empty no clients have been added go ahead and add client. 
                if not rows:
                   cur.execute("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (clientID, state, system, bits, cpuCores, gpuType, auth, email)) 

                #Creates a list of all clients then it checks to see if current client is in database if not adds it. if so prints error msg.
                else:
                    for row in rows:
                        clients.append(row[0])
                        
                    if clientID not in clients:
                        cur.execute("INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (clientID, state, system, bits, cpuCores, gpuType, auth, email))

                    else:
                        print "Client already in registered in database" 

        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:
            if conn:
                conn.close()
    


 
main()
