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

import string, time, sys
import urllib, re, os, sqlite3

def main():
    import socket, ssl
    
    def sendMsg(channel, msg):
        irc.send('PRIVMSG #%s %s\r\n' % (channel, msg))
        
    def join(channel):
        irc.send('JOIN #%s \r\n' % channel)

    def controller():
        #how many clients do you want working on this program and power level.
        clients = 5
        lPowerLvl = 1  #1-11  1 being crappy and 11 being really good.
        HPowerLvl = 11

        users = {}

        #, 'raw-md4', 'mysql-sha1', 'ntlm', 'nsldap', 'raw-md5u'
        hashes = [ 'nsldaps', 'mysql-sha1.hash' ]
        for hashName in hashes:
            createRuleTable(hashName)
        
            for client in range(clients):

                clientID, state, system, bits, gpuType = getClientInfo(lPowerLvl, HPowerLvl)
                program = getProgram(system, bits, gpuType)
                users[client] = []
                users[client].append(clientID)
                users[client].append(state)
                users[client].append(system)
                users[client].append(bits)
                users[client].append(gpuType)
                users[client].append(program)
            
            while True:
                data = irc.recv(768)
                print data

                if data.find('PING') != -1:
                    irc.send('PONG '+data.split()[1]+'\r\n')

                if data.find('!TRACK') != -1:
                    TrackOutput = '!'.join(data.split('!')[2:])
                    tClientID = TrackOutput.split('.')[1]
                    status = TrackOutput.split('.')[2]
                    foundCount = TrackOutput.split('.')[3]
                    
                    updateTrackClient(tClientID, status, foundCount)

                

                for user in range(len(users)):
                    name = int(user)
                    if checkClientState(users[name][0]) == 'ready':
                        clientID, command = buildcmd(users[name], hashName)
                        updateClient(clientID, 'busy')
                        

                        chan1 = 'pwc'+'_'.join(clientID.split('_')[1:])
                        msg = '!%s' % clientID
                        for cmd in command:
                            msg += '..'
                            msg += re.sub(' ', '..', cmd)
                        
                        join(chan1)
                        sendMsg(chan1, msg)
                        trackClient(clientID, msg)

        #When finished with all hashes need to reset the clients back to standby so they can be picked up again.
        for user in range(len(users)):
            name = int(user)
            if checkClientState(users[name][0]) == 'ready':
                updateClient(users[name][0], 'standby')
                
            

        
    network = 'irc.init6.me'
    chan = 'pwcrack'
    port = 16667
    nick = 'GpuRules'


    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
	if data.find('!start') != -1:
            controller()
            
        print data


def buildcmd(user, hashName):
    command = []
    gpuSettings = []
    attackmode = '-a 0'
    staticOptions = ['--remove', '--outfile-format=3', '--disable-potfile']

    hashFile, mcode, nvAccel, nvLoops, amdAccel, amdLoops = '', '', '', '', '', ''
    
    clientID = user[0]
    state = user[1]
    system = user[2]
    bits = user[3]
    gpuType = user[4]
    program = user[5]

    if gpuType == "ocl":
        staticOptions.append('--gpu-temp-retain=70')
        hashFile, mcode, amdAccel, amdLoops = getGPUSettings(gpuType, hashName)
        gpuSettings.append(amdAccel)
        gpuSettings.append(amdLoops)
    if gpuType == "cuda":
        hashFile, mcode, nvAccel, nvLoops = getGPUSettings(gpuType, hashName)
        gpuSettings.append(nvAccel)
        gpuSettings.append(nvLoops)
    
    ruleCMD = getRules(hashName)

    outfile = getOutFile(clientID, hashName)
    
    command.append(program)
    command.append(mcode)
    command.append(attackmode)
    for option in staticOptions:
        command.append(option)
    command.append(outfile)
    for gpuOption in gpuSettings:
        command.append(gpuOption)
    command.append(hashFile)
    
    command.append(ruleCMD)
    return clientID, command

def createRuleTable(hashName):
    hashName = ''.join(hashName.split('-'))
    tableName = hashName+'ruleTable'

    rules = ['best64.rule', 'best80.rule', 'Hash-IT_Insert_Space.rule', \
		'Hash-IT_Most_Common_Suffix.rule', 'Hash-IT_Most_Common_Prefix.rule', \
		'insert_overwrite.rule', 'npass.rule', 'passwordspro.rule', 'perfect.rule', \
		'PrependNumSpecial-3.rule']
    
    wordlist = 'wordlist/rockyou.txt'

    ruletable = []
    for rule in rules:
        ruletable.append( (rule, wordlist, 'incomplete') )
        
    try:
        conn = sqlite3.connect('RuleTable.db')

        with conn:
            cur = conn.cursor()
            
            #BruteForce Table. Start=one char for client to start on. charset full charset.
            #status can be incomplete, inprogress, completed
            #commented this out to preserv database across starts.
            #cur.execute("DROP TABLE IF EXISTS %s" % tableName)
            cur.execute('''CREATE TABLE IF NOT EXISTS %s
                         (rule text, wordlist text, status text)''' % tableName)    

            cur.executemany("INSERT INTO "+tableName+" VALUES(?, ?, ?)", ruletable)

    except sqlite3.Error, e:
        print "Error create rule table %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            
def getRules(hashName):
    hashName = ''.join(hashName.split('-'))
    tableName = hashName+'ruleTable'
    
    try:
        conn = sqlite3.connect('RuleTable.db')

        with conn:
            cur = conn.cursor()

            cur.execute("SELECT * FROM %s" % tableName)
            rows = cur.fetchall()

            for row in rows:
                if re.match('incomplete', row[2]):
                    rule = row[0]
                    wordlist = row[1]
                    ruleupdate(hashName, rule, 'inprogress')
                    ruleCMD = "%s -r rules/%s" % (wordlist, rule)
                    return ruleCMD

    except sqlite3.Error, e:
        print "Error get rule %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            
def ruleupdate(hashName, rule, status):
    hashName = ''.join(hashName.split('-'))
    tableName = hashName+'ruleTable'
    try:
        conn = sqlite3.connect('RuleTable.db')

        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM %s" % tableName)
            rows = cur.fetchall()

            for row in rows:
                if re.match(re.escape(rule),row[0]):
                    cur.execute("UPDATE "+tableName+" SET status=? WHERE rule=?",(status, rule))

                    conn.commit()

    except sqlite3.Error, e:
        print "Error ruleupdate %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()

def getClientInfo(lPowerLvl, HPowerLvl):
    try:
        conn = sqlite3.connect('pwcrack.db')

        with conn:
            #state = 'standby'
            cur = conn.cursor()
            cur.execute("SELECT * FROM clients WHERE state='standby'")
            rows = cur.fetchall()
            for row in rows:
                if row[5] != "None":
                    lvl = row[0].split('_')[1]
                    if checkPowerlvl(int(lvl), lPowerLvl, HPowerLvl):
                        state = 'ready'
                        clientID = row[0]
                        system = row[2] #system
                        bits = row[3] #bits
                        gpuType = row[5] #gpuType
                        updateClient(row[0], state )   
                        return clientID, state, system, bits, gpuType
                    
                #else:
                    #print "no clients in database within that powerlvl %s - %s. \
                            #Adjust power level and run again" % (lPowerLvl, HPowerLvl)
    
    except sqlite3.Error, e:
        print "Error getClientInfo %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            
def updateClient(clientID, state):       
        try:
            
            conn = sqlite3.connect('pwcrack.db')

            with conn:

                cur = conn.cursor()
                cur.execute("SELECT * FROM clients")
                rows = cur.fetchall()
                    
                for row in rows:
                    if re.match(clientID,row[0]):
                        cur.execute("UPDATE clients SET state=? WHERE clientID=?",(state, clientID))

        except sqlite3.Error, e:
            print "Error updateClient %s:" % e.args[0]
            sys.exit(1)

        finally:
            if conn:
                conn.close()
                
def checkClientState(clientID):
        try:
            conn = sqlite3.connect('pwcrack.db')

            with conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM clients")
                rows = cur.fetchall()
                    
                for row in rows:
                    if re.match(clientID,row[0]):
                        state = row[1]
                        return state

        except sqlite3.Error, e:
            print "Error checkClientState %s:" % e.args[0]
            sys.exit(1)

        finally:
            if conn:
                conn.close()
                
def trackClient(clientID, command):
    status = 'working'
    foundCount = 0
    try:
            
        conn = sqlite3.connect('pwcrack.db')

        with conn:

            cur = conn.cursor()
            cur.execute("INSERT INTO completed VALUES(?, ?, ?, ?)", (clientID, status, command, foundCount))

    except sqlite3.Error, e:
        print "Error updating completed %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            
def updateTrackClient(clientID, status, foundCount):
    try:

        conn = sqlite3.connect('pwcrack.db')

        with conn:

            cur = conn.cursor()

            cur.execute("UPDATE completed SET status=?,foundCount=? WHERE clientID=? AND status='working'", (status, foundCount, clientID))


    except sqlite3.Error, e:
        print "Error updating completed %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()

def checkPowerlvl(lvl, lPowerLvl, HPowerLvl):
    if lvl <= 1000:
        level = 1
    elif lvl > 1000 and lvl <= 2000:
        level = 2
    elif lvl > 2000 and lvl <= 3000:
        level = 3
    elif lvl > 3000 and lvl <= 4000:
        level = 4
    elif lvl > 4000 and lvl <= 5000:
        level = 5
    elif lvl > 5000 and lvl <= 6000:
        level = 6
    elif lvl > 6000 and lvl <= 7000:
        level = 7
    elif lvl > 7000 and lvl <= 8000:
        level = 8
    elif lvl > 8000 and lvl <= 9000:
        level = 9
    elif lvl > 9000 and lvl <= 10000:
        level = 10
    elif lvl > 10000:
        level = 11

    if level >= lPowerLvl and level <= HPowerLvl:
        return True
    else:
        return None

    
def getOutFile(clientID, hashName):
    import random
    rand = random.randint(0000,9999)

    outfile = "-o %s.%s.%s..a0.found" % (clientID, hashName, str(rand).rjust(4, '0'))
    return outfile

    
def getGPUSettings(gpuType, hashName):
    try:
        conn = sqlite3.connect('algorithm.db')

        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM algorithms")
            rows = cur.fetchall()
            
            for row in rows:
                if re.match(hashName,row[0]):
                    hashFile = row[1] #return hashFile here to make it easy.
                    mcode = row[2]
                    if gpuType == "ocl":
                        amdAccel = row[3]
                        amdLoops = row[4]
                        return hashFile, mcode, amdAccel, amdLoops
                    if gpuType == "cuda":
                        nvAccel = row[5]
                        nvLoops = row[6]
                        return hashFile, mcode, nvAccel, nvLoops
                        
                else:
                    print "%s not in Algorithm database. \
                            Please add and rerun algorithmTable.py" % hashName

    except sqlite3.Error, e:
        print "Error gpusettings %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()

def getProgram(system, bits, gpuType):
    if system == 'Windows':
        if bits == "32bit":
            if gpuType == "ocl":
                program = "oclHashcat-plus32.exe"        
            elif gpuType == "cuda":
                program = "cudaHashcat-Plus32.exe"
        elif bits == "64bit":
            if gpuType == "ocl":
                program = "oclHashcat-plus64.exe"
            elif gpuType == "cuda":
                program = "cudaHashcat-plus64.exe"
    elif system == 'Linux':
        if bits == "32bit":
            if gpuType == "ocl":
                program = "./oclHashcat-plus32.bin"
            elif gpuType == "cuda":
                program = "./cudaHashcat-Plus32.bin"   
        elif bits == "64bit":
            if gpuType == "ocl":
                program = "./oclHashcat-plus64.bin"
            elif gpuType == "cuda":
                program = "./cudaHashcat-plus64.bin"
    
    return program

  
main()
