#!/usr/bin/python
# -*- coding: utf8 -*-

import string, time, sys
import urllib, re, os, sqlite3

def main():
    import socket, ssl
    
    def sendMsg(channel, msg):
        print "inside send msg"
        print channel, msg
        irc.send('PRIVMSG #%s %s\r\n' % (channel, msg))
        print irc.recv(4096)
        
    def join(channel):
        irc.send('JOIN #%s \r\n' % channel)

    def controller():
        #how many clients do you want working on this program and power level.
        clients = 3
        lPowerLvl = 5  #1-11  1 being crappy and 11 being really good.
        HPowerLvl = 8

        users = {}

        
        hashes = [ 'raw-md5', 'raw-sha1', 'raw-md4', 'mysql-sha1', 'ntlm', 'nsldap', 'raw-md5u' ]
        for hashName in hashes:
            createBFtable(hashName)
        
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
                for user in range(len(users)):
                    name = int(user)
                    if checkClientState(users[name][0]) == 'ready':
                        clientID, command = buildcmd(users[name], hashName)
                        updateClient(clientID, 'busy')
                        #sendCMD(clientID, command)

                        chan1 = 'pwc'+'_'.join(clientID.split('_')[1:])
                        msg = '!%s' % clientID
                        for cmd in command:
                            msg += '..'
                            msg += re.sub(' ', '..', cmd)
                            
                            
                        #print "this is the command being sent to the client: %s" % msg
                        #print "this is the channel sending to: %s" % chan1
                        #irccmd = 'PRIVMSG'
                        join(chan1)
                        sendMsg(chan1, msg)
                        #irc.send('PRIVMSG #'+str(chan1)+' '+str(msg)+' \r\n')
                        

        
        
    network = 'irc.init6.me'
    chan = 'pwcrack'
    port = 16667
    nick = 'InitalBrute'


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
    attackmode = '-a 3'
    staticOptions = ['--remove', '--outfile-format=3', '--disable-potfile']
    markovSettings = '--markov-hcstat=hashcat.hcstat'

    hashFile, mcode, nvAccel, nvLoops, amdAccel, amdLoops = '', '', '', '', '', ''
    
    #change these options for different rounds.
    CL = 'CL1-7'
    staticOptions.append('-i --increment-min=1 --increment-max=7')
    markovThreshold = '-t 0'
    
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
    bfstart, bruteforce = getBruteForce(hashName)
    outfile = getOutFile(clientID, hashName, bfstart, CL)
    
    command.append(program)
    command.append(mcode)
    command.append(attackmode)
    for option in staticOptions:
        command.append(option)
    command.append(markovSettings)
    command.append(markovThreshold)
    command.append(outfile)
    for gpuOption in gpuSettings:
        command.append(gpuOption)
    command.append(hashFile)
    command.append(bruteforce)
    return clientID, command


def getClientInfo(lPowerLvl, HPowerLvl):
    try:
        conn = sqlite3.connect('pwcrack.db')

        with conn:
            #state = 'standby'
            cur = conn.cursor()
            cur.execute("SELECT * FROM clients WHERE state='standby'")
            rows = cur.fetchall()
            for row in rows:
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
    

def createBFtable(hashName):
    hashName = ''.join(hashName.split('-'))
    tableName = hashName+'bftable'
    
    charset1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#$%^&*()_-+=[]{}\\|<>\"\':;,.\? /"
    #charset2 = u"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#$%^&*()_-+=[]{}\\|<>\"\':;,.\? /\ñ"
    
    charset = 'charset1'
    #charset = 'charset2'

    bftable = []
    for char in charset1:
        bftable.append( (char, charset, 'incomplete') )
        
    try:
        conn = sqlite3.connect('BFTable.db')

        with conn:
            cur = conn.cursor()
            
            #BruteForce Table. Start=one char for client to start on. charset full charset.
            #status can be incomplete, inprogress, completed
            cur.execute("DROP TABLE IF EXISTS %s" % tableName)
            cur.execute('''CREATE TABLE IF NOT EXISTS %s
                         (start text, charset text, status text)''' % tableName)    

            cur.executemany("INSERT INTO "+tableName+" VALUES(?, ?, ?)", bftable)

    except sqlite3.Error, e:
        print "Error create bf table %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            
def getBruteForce(hashName):
    hashName = ''.join(hashName.split('-'))
    tableName = hashName+'bftable'
    
    try:
        conn = sqlite3.connect('BFTable.db')

        with conn:
            cur = conn.cursor()

            cur.execute("SELECT * FROM %s" % tableName)
            rows = cur.fetchall()

            for row in rows:
                if re.match('incomplete', row[2]):
                    bfstart = row[0]
                    charset = row[1]
                    bfupdate(hashName, bfstart, 'inprogress')
                    bfCMD = "-1 %s -2 %s ?1?2?2?2?2?2?2?2?2" % (bfstart, charset)
                    return bfstart, bfCMD
                
                
    except sqlite3.Error, e:
        print "Error getbf %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            
def bfupdate(hashName, bfstart, status):
    hashName = ''.join(hashName.split('-'))
    tableName = hashName+'bftable'
    try:
        conn = sqlite3.connect('BFTable.db')

        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM %s" % tableName)
            rows = cur.fetchall()

            for row in rows:
                if re.match(bfstart,row[0]):
                    cur.execute("UPDATE "+tableName+" SET status=? WHERE start=?",(status, bfstart))

                    conn.commit()
    except sqlite3.Error, e:
        print "Error bfupdate %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()


    
def getOutFile(clientID, hashName, bfstart, CL):
    #cmd clientID bfstart HashName attack mode
    outfile = "-o %s.%s.%s.%s.a3.found" % (clientID, bfstart, hashName, CL)
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
