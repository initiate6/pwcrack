def controller(charset):

    
    #how many clients do you want working on this program and power level.
    clients = 2
    lPowerLvl = 5  #1-11  1 being crappy and 11 being really good.
    HPowerLvl = 8

    users = {}

    
    hashes = [ 'raw-md5', 'raw-sha1', 'raw-md4', 'mysql-sha1', 'ntlm', 'nsldap', 'raw-md5u' ]
    for hashName in hashes:
        createBFtable(hashName, charset)
    
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
                if checkClientState(user[name][0]) == 'ready':
                    clientID, command = buildcmd(user[name], hashName)
                    updateClient(users[name][0], 'busy')
                    print clientID, command


def buildcmd(user, hashName):
    #change these options for different rounds.
    CL = 'CL1-7'
    staticOptions.append('-i --increment-min=1 --increment-max=7')
    markovThreshold = '-t 0'
    
    command = []
    gpuSettings = []
    attackmode = '-a 3'
    staticOptions = ['--remove', '--outfile-format=3', '--disable-potfile']
    markovSettings = '--markov-hcstat=hashcat.hcstat'

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





        
    



  
