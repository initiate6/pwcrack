#!/usr/bin/python
# -*- coding: utf8 -*-

import string, time, ssl, sys
import urllib, re, os, sqlite3


def main():
    import socket
    #some functions to help repetitive task in connect()
    def msg(ircCMD, channel, msg):
        irc.send('%s #%s %s\r\n' % (ircCMD, channel, msg))
    def join(channel):
        irc.send('JOIN #%s \r\n' % channel)

    charset = u""
    
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
        if data.find('!charset\.') != -1:
            charset = data.split('.')[1:].strip('\r\n')
            
	if data.find('!start') != -1:
            controller(charset)

        print data

def something():
        command = buildcmd(clientID, system, bits, cpuCores, gpuType, amode, algorithm, ofile, hashfile, bruteforce)
        chan1 = 'pwc'+'_'.join(clientID.split('_')[1:])
        join(chan1)
        msg = '!'+clientID+''+str(command)
        irc.send('PRIVMSG #%s %s\r\n' % (chan1, msg))

def getUsers():
    user = {}
    #how many clients do you want working on this program and power level.
    clients = 2
    lPowerLvl = 5  #1-10  1 being crappy and 10 being really good.
    HPowerLvl = 8

    for client in range(clients):

        clientID, state, system, bits, gpuType = getClientInfo(lPowerLvl, HPowerLvl)
        program = getProgram(system, bits, gpuType)
        user[client] = []
        user[client].append(clientID)
        user[client].append(state)
        user[client].append(system)
        user[client].append(bits)
        user[client].append(gpuType)
        user[client].append(program)

    return user
    

def getClientInfo(lPowerLvl, HPowerLvl):
    clientInfo = []
    try:
        conn = sqlite3.connect('pwcrack.db')

        with conn:
            state = 'standby'
            cur = conn.cursor()
            cur.execute("SELECT * FROM clients WHERE state='standby'")
            rows = cur.fetchall()
            for row in rows:
                lvl = row[0].split('_')[1]
                print lvl
                if checkPowerlvl(lvl, lPowerLvl, HPowerLvl):
                    state = 'ready'
                    clientID = row[0]
                    system = row[2] #system
                    bits = row[3] #bits
                    gpuType = row[5] #gpuType
                        
                    return clientID, state, system, bits, gpuType
                    updateClientState(row[0], state )

                else:
                    print "no clients in database within that powerlvl %s - %s. \
                            Adjust power level and run again" % (lPowerLvl, HPowerLvl)
    
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

def checkPowerlvl(lvl, powerlvl):
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


    if level == powerlvl:
        return True
    
def controller(charset):
    users = getUsers()
    print users
    while True:
        for user in len(users):
            if checkClientState(user[int(user)][0]) == 'ready':
                buildcmd(user[int(user)], charset)
            

def buildcmd(user, charset):
    clientID = user[0]
    state = user[1]
    system = user[2]
    bits = user[3]
    gpuType = user[4]
    
    command = []
    attackmode = '-a 3'
    staticOptions = ['--remove', '--outfile-format=3', '--disable-potfile']
    markovSettings = '--markov-hcstat=hashcat.hcstat'


    rounds = getrounds()
    for r in rounds:
        CL = r[0]
        staticOptions.append(r[1])
        markovThreshold = r[2]
        
        mcode, staticOptions, outfile, gpuSettings, hashFile, bruteforce = stage2build(clientID, charset, gpuType, CL)

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
    print command


def stage2build(clientID, staticOptions, charset, gpuType, CL):
    gpuSettings = []
    hashes = [ 'raw-md5', 'raw-sha1', 'raw-md4', 'mysql-sha1', 'ntlm', 'nsldap', 'raw-md5u' ]
    
    for hashName in hashes:
        createBFtable(hashName, charset)
        if gpuType == "ocl":
            staticOptions.append('--gpu-temp-retain=70')
            hashFile, mcode, amdAccel, amdLoops == getGPUSettings(gpuType, hashName)
            gpuSettings.append(amdAccel)
            gpuSettings.append(amdLoops)
        if gpuType == "cuda":
            hashFile, mcode, nvAccel, nvLoops == getGPUSettings(gpuType, hashName)
            gpuSettings.append(nvAccel)
            gpuSettings.append(nvLoops)
        bfstart, bruteforce = getBruteForce(hashName)
        outfile = getOutFile(clientID, hashName, bfstart, CL)
        return mcode, staticOptions, outfile, gpuSettings, hashFile, bruteforce
        
    
def getRounds():
    rounds = []

    round1 = ['CL1-7', '-i --increment-min=1 --increment-max=7', '-t 0']
    round2 = ['CL8', '-i --increment-min=8 --increment-max=8', '-t 70']
    round3 = ['CL9', '-i --increment-min=9 --increment-max=9', '-t 40']
    #round4 = ['CL10', '-i --increment-min=10 --increment-max=10', '-t 20']
    #round5 = ['CL11', '-i --increment-min=10 --increment-max=10', '-t 15']
    #round6 = ['CL12', '-i --increment-min=10 --increment-max=10', '-t 10']
    

    rounds.append(round1)
    rounds.append(round2)
    rounds.append(round3)
    #rounds.append(round4)
    #rounds.append(round5)
    #rounds.append(round6)

    return rounds
    
def getBruteForce(hashName):
    try:
        conn = sqlite3.connect('BFTable.db')

        with conn:
            cur = conn.cursor()

            cur.execute("SELECT * FROM %sbftable" % hashName)
            rows = cur.fetchall()

            for row in rows:
                if row[2] == 'incomplete':
                    bfstart = row[0]
                    charset = row[2]
                    status = 'inprogress'
                    bfupdate(hashName, bfstart, status)
                    bfCMD = "-1 %s -2 %s ?1?2?2?2?2?2?2?2?2" % (bfstart, charset)
                    return bfstart, bfCMD
                    
    except sqlite3.Error, e:
        print "Error getbf %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            
def bfupdate(hashName, bfstart, status):
    try:
        conn = sqlite3.connect('BFTable.db')

        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM %sbftable" % hashName)
            rows = cur.fetchall()

            for row in rows:
                if re.match(bfstart,row[0]):
                    #if this doesn't work create update line and pass that in.
                    cur.execute("UPDATE %sbftable SET status=? WHERE bfstart=?",(status, bfstart) % hashName)

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
        conn = sqlite3.connect('algorithmTable.db')

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

 
def createBFtable(hashName, charset):
    if not charset:
        charset = u"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#$%^&*()_-+=[]{}\\|<>\"\':;,.? /ñ"

    bftable = []
    for char in charset:
        bftable.append( (char, charset, 'incomplete') )
        
    try:
        conn = sqlite3.connect('BFTable.db')

        with conn:
            cur = conn.cursor()
            
            #BruteForce Table. Start=one char for client to start on. charset full charset.
            #status can be incomplete, inprogress, completed
            cur.execute("DROP TABLE IF EXISTS %sbftable" % hashName)
            cur.execute('''CREATE TABLE IF NOT EXISTS %sbftable
                         (start text, charset text, status text)''' % hashName)    

            cur.executemany("INSERT INTO bftable VALUES(?, ?, ?)", bftable)

    except sqlite3.Error, e:
        print "Error create bf table %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()





        
main()
