# Gather info about the computer and save to file for client.py.
# Only have to run setup.py one time on each computer. 

import platform
import sys
import string
import struct
import re
import random

system = platform.system()
if system == 'Windows':
    import _winreg
if system == 'Linux':
    import subprocess

def main():
    
    #email = raw_input("What is your e-mail address incase your client disconnects? ")
    email = "init6@init6.me"
    
    if system == 'Windows':
        bits = checkBits()
        cpuInfo = winGetCPUinfo()
        gpuType, gpuDesc, gpuDriver, gpuMem = winGetGPUinfo()
        ramInfo = winGetRAMinfo()
        ClientID = getClientID( system, bits, cpuInfo, gpuType, gpuDesc, gpuDriver, gpuMem, ramInfo )
        password = getPassword( ClientID, system, bits, gpuType )
        writeit(ClientID, system, bits, cpuInfo, gpuType, gpuDesc, gpuDriver, ramInfo, password, email)
        #downloads don't work because I haven't uploaded all the packages yet
	#download(ClientID, system, bits, gpuType)
        
    if system == 'Linux':
        bits = checkBits()
	cpuInfo = linGetCPUinfo()
        ramInfo = linGetRAMinfo()
	gpuType, gpuDesc, gpuDriver, gpuMem = linGetGPUinfo()  
	ClientID = getClientID( system, bits, cpuInfo, gpuType, gpuDesc, gpuDriver, gpuMem, ramInfo )
        password = getPassword( ClientID, system, bits, gpuType )
	writeit(ClientID, system, bits, cpuInfo, gpuType, gpuDesc, gpuDriver, ramInfo, password, email)
	#downloads don't work because I haven't uploaded all the packages yet
	#download(ClientID, system, bits, gpuType
	      

    if system == 'Darwin':
        print "Not supported at this time"

#write info to a file for client.py to read later.
def writeit( ClientID, system, bits, cpuInfo, gpuType, gpuDesc, gpuDriver, ramInfo, password, email ):
    cpuCount = 0            
    f = open('sysinfo', 'w')
    f.write(ClientID+'\n')
    f.write('system.'+system+'\n')
    f.write('bits.'+bits+'\n')
    for cpu in cpuInfo:
        f.write('cpu.')
        f.write(cpu)
        f.write('\n')
        cpuCount += 1
    f.write('cpuCount.'+str(cpuCount)+'\n')
    
    f.write('gpuType.'+str(gpuType)+'\n')
    f.write('gpu.'+str(gpuDesc)+'\n')
    f.write('gpuDriver.'+str(gpuDriver)+'\n')   
    f.write('ram.'+str(ramInfo)+'\n')
    f.write('pass.'+str(password)+'\n')
    f.write('email.'+email+'\n')
    f.close()
    
#Checks if system is 64bit.
def checkBits():
    bits = sys.maxsize > 2**32
    if bits == True:
        return "64bit"
    else:
        return "32bit"

#get RAM info on WIndows Computers. Some lock up python.exe but finish.
#change to winshell thingy
def winGetRAMinfo():
    try:
        from winmem import winmem
        m = winmem()
        return m.dwTotalPhys/1024**2
    
    except:
        print "Ram info got messed up"

#Get CPU info on Windows computers.
def winGetCPUinfo():
    """Retrieves Machine information from the registry"""
    cpuInfo = []
    try:
       hHardwareReg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "HARDWARE")
       hDescriptionReg = _winreg.OpenKey(hHardwareReg, "DESCRIPTION")
       hSystemReg = _winreg.OpenKey(hDescriptionReg, "SYSTEM")
       hCentralProcessorReg = _winreg.OpenKey(hSystemReg, "CentralProcessor")
       nbProcessors = _winreg.QueryInfoKey(hCentralProcessorReg)[0]

       for idxKey in range(nbProcessors):
           hProcessorIDReg = _winreg.OpenKey(hCentralProcessorReg, str(idxKey))
           processorDescription = _winreg.QueryValueEx(hProcessorIDReg,"ProcessorNameString")[0]
           mhz = _winreg.QueryValueEx(hProcessorIDReg, "~MHz")[0]
           cpuInfo.append(str(idxKey)+'.'+string.lstrip(processorDescription)+'.'+str(mhz))
            
       return cpuInfo

    except WindowsError:
       print "Cannot retrieve processor information from registry!"

#Get GPU info on Windows computers.
def winGetGPUinfo():
    #GPUinfo = []
    #gpuDesc = ''
    #amdCatalystVer = ''
    #gpuMem = ''
    #nvDriverVer = ''
    try:
        hHardwareReg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "HARDWARE")
        hDeviceMapReg = _winreg.OpenKey(hHardwareReg, "DEVICEMAP")
        hVideoReg = _winreg.OpenKey(hDeviceMapReg, "VIDEO")
        hVideoDevices = _winreg.QueryInfoKey(hVideoReg)[1]
        VideoCardString = []
        for x in range(0, hVideoDevices, 1):
            VideoCardString.append(_winreg.EnumValue(hVideoReg, x)[1])
            ClearnVideoCardString = []
            for line in VideoCardString:
                ClearnVideoCardString.append("\\".join(str(line).split("\\")[3:]))

                done = False #So it only runs once for GPU info. 
                #Get the graphics card information
                for line in ClearnVideoCardString:
                    for item in line.split("\\")[2:3]:
                        if done == False and item == 'Control':
                            hVideoCardReg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, str(line))
                            VideoCardDescription  = _winreg.QueryValueEx(hVideoCardReg,"Device Description")[0]
                            
                            #check if its a AMD/ATI card and if so return detailed info.
                            if re.search('AMD|ATI', str(VideoCardDescription)) != None:
                                gpuDesc = str(VideoCardDescription)
                                amdCatalystVer = _winreg.QueryValueEx(hVideoCardReg, "Catalyst_Version")[0]
                                VideoCardMemorySize = _winreg.QueryValueEx(hVideoCardReg,"HardwareInformation.MemorySize")[0]
                                gpuMem = str(VideoCardMemorySize / 1024 / 1024)
                                gpuType = "ocl"
                                done = True 
                        
                        
                            #check if its a Nvidia card and if so return detailed info.
                            elif re.search('nvidia', str(VideoCardDescription)) != None:
                                gpuDesc(VideoCardDescription)
                                nvDriverVer = _winreg.QueryValueEx(hVideoCardReg, "DriverVersion")[0]
                                GPUinfo.append(nvDriverVer)
                                VideoCardMemorySize = _winreg.QueryValueEx(hVideoCardReg,"HardwareInformation.MemorySize")[0]
                                gpuMem(VideoCardMemorySize / 1024 / 1024)
                                gpuType = "cuda"
                                done = True

            #breaks to step out of for loops once done.                                        
                    if done == True:
                        break
                if done == True:
                    break
            if done == True:
                break
            
        #checks if gpu driver is good and return info
        if re.search('AMD|ATI', gpuDesc):
            if amdCatalystVer == '13.1':
                return gpuType, gpuDesc, amdCatalystVer, VideoCardMemorySize
            else:
                print "Your GPU driver for  %s is %s and needs to be upgraded or downgraded to match oclhashcat requirements 13.1" % ( gpuDesc, amdCatalystVer )
                return None, None, None, None
            
        elif re.search('nvidia', gpuDesc):
            if float(nvDriverVer) >= float(310.02):
                return gpuType, gpuDesc, nvDriverVer, VideoCardMemorySize
            else:
                print "Your GPU driver for  %s is %s and needs to be upgraded or downgraded to match oclhashcat requirements 13.1" % ( gpuDesc, nvDriverVer )
                return None, None, None, None
        else:
            return None, None, None, None
     
    except WindowsError:
        print "Cannot Retrieve Graphics Card Name and Memory Size!"

    
def getClientID( system, bits, cpuInfo, gpuType, gpuDesc, gpuDriver, gpuMem, ramInfo ):
    #system = windows = 50, Linux = 100, OSX = 10
    #64bit = 50pts 32bit = 20pts
    #CPUcores = 150pts per core
    #CPU.GHZ = 100pts per 1ghz
    #ram = 20pt per 1GB of ram
    #GPU.Nvidia = GTX690 
    #GPU.AMD = 79** = 5,000 pts  7800 = 900pts
    #GPU ram 2pts per megabyte.
    #Random number between 1 - 50 #might have to do this to make sure the clientID stays random. or could add IP addres?
    #subtotal of above equals a number. add that number to .clientID<number>

    points = 0
    if system == "Windows":
        points += 50 
    if system == "Linux":
        points += 100
    if system == "Darwin":
        points += 10
    if bits == "64bit":
        points += 50
    if bits == "32bit":
        points += 20
    for cpu in cpuInfo:
        points += 250
        
    rampts = (ramInfo/1024) * 20
    points += int(rampts)

    if gpuDesc:
        gpuPts = gpuLookup(gpuDesc)
        points += int(gpuPts)
        
        gpuRamPts = (gpuMem / 1024 / 1024) * 2
        points += int(gpuRamPts)

    rand = random.randint(000,999)

    return ("CID"+"_"+str(points)+"_"+str(rand))

#needs a lot of work. Check for different types of GPU cards and give it points.
def gpuLookup(card):
    points = 0
    try:
        if re.search('AMD|ATI', card):
            if re.search('ATI', card):
                if card == "ATI Radeon HD \d\d\d\d":
                    points = 1000

                elif re.search('X\d\d\d|x\d\d\d|R\d\d\d', card):
                    points = 500

                else:
                    points = 100
                    
            if re.search('AMD', card):
                    
                if re.search('7\d\d\d', card):
                    points = 7000
                    
                elif re.search('6\d\d\d', card):
                    points = 6000

                elif re.search('5\d\d\d', card):
                    points = 5000

                elif re.search('4\d\d\d', card):
                    points = 4000

                elif re.search('3\d\d\d', card):
                    points = 3000

                elif re.search('2\d\d\d', card):
                    points = 2000

                else:
                    points = 100
                    

        if re.search('nvidia', card):
            points = 1000
            
        return points
    
    except:
        print "GPU not in LookUp table"            


def download(ClientID, system, bits, gpuType):
    try:
        
        import urllib2

        def saveit(filename, fileobj):
            print "this is the file name %s" % filename
            f = open(filename,'w')
            f.write(fileobj.read())
            f.close()        
            
        
        if system == "Windows":
            if gpuType == "ocl":
                if bits == "32bit":
                    winOCL32bit = urllib2.urlopen("http://cookie.baconseed.org/~cookie/win.ocl.32bit.7z")
                    saveit('winOCL32bit.7z', winOCL32bit)
                        
                elif bits == "64bit":
                    winOCL64bit = urllib2.urlopen("http://cookie.baconseed.org/~cookie/win.ocl.64bit.7z")
                    saveit('winOCL64bit.7z', winOCL64bit)
                    
            if gpuType == "cuda":
                if bits == "32bit":
                    winCUDA32bit = urllib2.urlopen("http://cookie.baconseed.org/~cookie/win.cuda.32bit.7z")
                    saveit('winCUDA32bit.7z', winCUDA32bit)
                    
                elif bits == "64bit":
                    winCUDA64bit = urllib2.urlopen("http://cookie.baconseed.org/~cookie/win.cuda.64bit.7z")
                    saveit('winCuda64bit.7z', winCUDA64bit)
                    
            if gpuType == "None":
                if bits == "32bit":
                    winHC32bit = urllib2.urlopen("http://cookie.baconseed.org/~cookie/win.hashcat.32bit.7z")
                    saveit('winHC32bit.7z', winHC32bit)
                    
                elif bits == "64bit":
                    winHC64bit = urllib2.urlopen("http://cookie.baconseed.org/~cookie/win.hashcat.64bit.7z")
                    saveit('winHC32bit.7z', winHC64bit)
                    
        if system == "Linux":
            if gpuType == "ocl":
                if bits == "32bit":
                    linOCL32bit = urllib2.urlopen("http://cookie.baconseed.org/~cookie/lin.ocl.32bit.7z")
                    saveit('linOCL32bit.7z', linOCL32bit)
                    
                elif bits == "64bit":
                    linOCL64bit = urllib2.urlopen("http://cookie.baconseed.org/~cookie/lin.ocl.64bit.7z")
                    saveit('linOCL64bit.7z', linOCL64bit)
                    
            if gpuType == "cuda":
                if bits == "32bit":
                    linCUDA32bit = urllib2.urlopen("http://cookie.baconseed.org/~cookie/lin.cuda.32bit.7z")
                    saveit('linCUDA32bit.7z', linCUDA32bit)
                    
                elif bits == "64bit":
                    linCUDA64bit = urllib2.urlopen("http://cookie.baconseed.org/~cookie/lin.cuda.64bit.7z")
                    saveit('linCUDA64bit.7z', linCUDA64bit)
                    
            if gpuType == "None":
                if bits == "32bit":
                    linHC32bit = urllib2.urlopen("http://cookie.baconseed.org/~cookie/lin.hashcat.32bit.7z")
                    saveit('linHC32bit.7z', linHC32bit)
                    
                elif bits == "64bit":
                    linHC64bit = urllib2.urlopen("http://cookie.baconseed.org/~cookie/lin.hashcat.64bit.7z")
                    saveit('linHC64bit.7z', linHC64bit)
                    
        if system == "Darwin":
            print "nothing here"

    except:
        print "something went wrong downloading the files"


def getPassword( ClientID, system, bits, gpuType ):
    var = "DC214"
    if not gpuType:
        gpuType = 'n'
    password = "%s%s%s%s%s%s" % (system[0], system[random.randint(0,4)], bits[0], gpuType[0], ClientID[-3:], var )
    return password

############
#
#LINUX ONLY FUNCTIONS
#
############
    
def linGetGPUinfo():

    def getGpuMemory():
        clinfo_process = subprocess.Popen(['clinfo'], 
                                            stdout=subprocess.PIPE)
        
        grep1_process = subprocess.Popen(['grep', 'Max memory allocation'],
                                            stdin=clinfo_process.stdout,
                                            stdout=subprocess.PIPE)
        cut_process = subprocess.Popen(['cut', '-d:', '-f2'],
                                            stdin=grep1_process.stdout,
                                            stdout=subprocess.PIPE)
                                                            
        gpuMem = cut_process.communicate()[0] 
        gpuMem = int(gpuMem.split()[0]) / 1024 / 1024
	return str(gpuMem)

    def checkamddriver():
        clinfo_process = subprocess.Popen(['clinfo'], 
                                            stdout=subprocess.PIPE)
        
        grep1_process = subprocess.Popen(['grep', 'Driver version'],
                                            stdin=clinfo_process.stdout,
                                            stdout=subprocess.PIPE)
        cut_process = subprocess.Popen(['cut', '-d:', '-f2'],
                                            stdin=grep1_process.stdout,
                                            stdout=subprocess.PIPE)
                                                            
        amddriveroutput = cut_process.communicate()[0] 
        amdDriver = float(amddriveroutput.split()[0])
        if amdDriver == 1084.4:
            return str(amdDriver)
        else:
            return None
            
    
    def checknvdriver():
        
        clinfo_process = subprocess.Popen(['clinfo'], 
                                            stdout=subprocess.PIPE)
        grep1_process = subprocess.Popen(['grep', 'Driver version'],
                                            stdin=clinfo_process.stdout,
                                            stdout=subprocess.PIPE)
        cut_process = subprocess.Popen(['cut', '-d:', '-f2'],
                                            stdin=grep1_process.stdout,
                                            stdout=subprocess.PIPE)
                                                            
        nvdriveroutput = cut_process.communicate()[0] 
        nvDriver = float(nvdriveroutput.split()[0]) 
        if nvDriver >= 310.32:
            return str(nvDriver)
        else:
            return None
	
    def getdevicename(device):
        result = device.split(':')
	return result[len(result)-1]
        
        
    lspci_process = subprocess.Popen(['lspci'], 
                                        stdout=subprocess.PIPE)
    grep_process = subprocess.Popen(['grep', 'VGA'],
                                        stdin=lspci_process.stdout,
                                        stdout=subprocess.PIPE)
    stdoutdata = grep_process.communicate()[0] 
    
    vcDevices = []
    for item in stdoutdata.split('\n'):
        vcDevices.append(item)
        
    for device in vcDevices:
        if re.search('AMD|ATI', device):
            amddriver = checkamddriver()
            gpuType = "ocl" 
            deviceName = getdevicename(device)
	    gpuMem = getGpuMemory()
            return gpuType, deviceName,  amddriver, gpuMem
            
        elif re.search('NVIDIA', device):
            nvdriver = checknvdriver()
            gpuType = "cuda"
	    deviceName = getdevicename(device)
	    gpuMem = getGpuMemory()
	    return gpuType, deviceName,  nvdriver, gpuMem
            
        else:
            gpudriver = None
            gpuType = None
	    deviceName = None
	    gpuMem = None
	    return gpuType, deviceName,  gpudriver, gpuMem
            

def linGetCPUinfo():
    import subprocess
    cpuInfo = []

    cat_process = subprocess.Popen(['cat', '/proc/cpuinfo'],
                                        stdout=subprocess.PIPE)

    grep_process = subprocess.Popen(['grep', 'processor\|name\|MHz'],
                                        stdin=cat_process.stdout,
                                        stdout=subprocess.PIPE)

    cut_process = subprocess.Popen(['cut', '-d:', '-f2'],
		            stdin=grep_process.stdout,
		            stdout=subprocess.PIPE)


    stdoutdata = cut_process.communicate()[0]
		
    temp = []
    for item in stdoutdata.split('\n'):
        temp.append(item.strip())
	
    temp2 = [temp[x:x+3] for x in range(0, len(temp),3)]
		
    for list in temp2:
        cpuInfo.append('.'.join(list))
		
    last = cpuInfo.pop()
    if last == '':
        return cpuInfo
    else:
        cpuInfo.append(last)
        return cpuInfo


def linGetRAMinfo():
    import subprocess
    cat_process = subprocess.Popen(['cat', '/proc/meminfo'], 
					stdout=subprocess.PIPE)

    grep_process = subprocess.Popen(['grep', 'MemTotal'], 
					stdin=cat_process.stdout, 
					stdout=subprocess.PIPE)

    awk_process = subprocess.Popen(['awk', '{print $2}'], 
					stdin=grep_process.stdout, 
					stdout=subprocess.PIPE)


    stdoutdata = awk_process.communicate()[0]
    ramsize = int(stdoutdata) / 1024 / 1024
    #print "ram size in GB %s" % ramsize
    return ramsize

 
 
 
main()
