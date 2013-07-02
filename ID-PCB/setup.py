# Gather info about the computer and save to file for client.py.
# Only have to run setup.py one time on each computer. 

import platform
import sys

import string
import struct
import re
import random

def main():
    system = platform.system()
    #email = raw_input("What is your e-mail address incase your client disconnects? ")
    email = "init6@init6.me"
    
    if system == 'Windows':
        import _winreg
        bits = checkBits()
        cpuInfo = winGetCPUinfo()
        gpuInfo = winGetGPUinfo()
        ramInfo = winGetRAMinfo()
        ClientID = getClientID( system, bits, cpuInfo, gpuInfo, ramInfo )
        writeit(ClientID, system, bits, cpuInfo, gpuInfo, ramInfo, email)
        download(ClientID, system, bits, gpuInfo)
        
    if system == 'Linux':
        import subprocess
        bits = checkBits()
	cpuInfo = linGetCPUinfo()
        ramInfo = linGetRAMinfo()
	gpuInfo = linGetGPUinfo()        

    if system == 'Darwin':
        print "Not supported at this time"

#write info to a file for client.py to read later.
def writeit( ClientID, system, bits, cpuInfo, gpuInfo, ramInfo, email ):
    cpuCount = 0
    gpuType = "None"
    if gpuInfo:
        if re.search('AMD|ATI', gpuInfo[0]):
            gpuType = "ocl"
        elif re.search('nvidia', gpuInfo[0]):
            gpuType = "cuda"
        else:
            gpuType = "None"
                   
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
    if gpuInfo:
        f.write('gpuType.'+gpuType+'\n')
        f.write('gpu.'+gpuInfo[0]+'\n')
        f.write('gpuDriver.'+gpuInfo[1]+'\n')
    if not gpuInfo:
        f.write('gpuType.'+gpuType+'\n')
        f.write('gpu.'+gpuType+'\n')
        f.write('gpuDriver.'+gpuType+'\n')
        
    f.write('ram.'+str(ramInfo)+'\n')
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
    GPUinfo = []

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
                                GPUinfo.append(VideoCardDescription)
                                amdCatalystVer = _winreg.QueryValueEx(hVideoCardReg, "Catalyst_Version")[0]
                                GPUinfo.append(amdCatalystVer)
                                VideoCardMemorySize = _winreg.QueryValueEx(hVideoCardReg,"HardwareInformation.MemorySize")[0]
                                GPUinfo.append(VideoCardMemorySize / 1024 / 1024)
                                done = True 
                        
                        
                            #check if its a Nvidia card and if so return detailed info.
                            elif re.search('nvidia', str(VideoCardDescription)) != None:
                                GPUinfo.append(VideoCardDescription)
                                nvDriverVer = _winreg.QueryValueEx(hVideoCardReg, "DriverVersion")[0]
                                GPUinfo.append(nvDriverVer)
                                VideoCardMemorySize = _winreg.QueryValueEx(hVideoCardReg,"HardwareInformation.MemorySize")[0]
                                GPUinfo.append(VideoCardMemorySize / 1024 / 1024)
                                done = True

            #breaks to step out of for loops once done.                                        
                    if done == True:
                        break
                if done == True:
                    break
            if done == True:
                break
            
        #Checks to see if GPUinfo has a value if so continues else return None.
        if not GPUinfo:
            #check driver is compatible with HashCat if so return GPUinfo else return None.
            if checkDriver(GPUinfo) == True:
                return GPUinfo
            else:
                return None
        else:
            return None
        
    except WindowsError:
        print "Cannot Retrieve Graphics Card Name and Memory Size!"


#checks to see if GPU driver is compatible with HashCat  
def checkDriver(gpuDriver):
    try:
        if re.search('AMD|ATI', gpuDriver[0]):
            if gpuDriver[1] == "13.1":
                return True

        elif re.search('nvidia', gpuDriver[0]):
            if gpuDriver[1] == "9.18.13.1422":
                return True            

        else:
            print "Your GPU driver for  %s is %s and needs to be upgraded or downgraded to match oclhashcat requirements" % (gpuDriver[0] , gpuDriver[1] )
            
    except:
        print "Something went wrong while checking GPU driver version." 

    
def getClientID( system, bits, cpuInfo, gpuInfo, ramInfo ):
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
        points ++ 50
    if system == "Linux":
        points += 100
    if system == "Darwin":
        points += 10
    if bits == "64bit":
        points += 50
    if bits == "32bit":
        points += 20
    for cpu in cpuInfo:
        points += 150
        ghz = cpu.split('.')[2]
        points += int(( float(ghz) / 1000 ) * 100)
    rampts = (ramInfo/1024) * 20
    points += int(rampts)

    if gpuInfo:
        gpuPts = gpuLookup(gpuInfo[0])
        points += int(gpuPts)

        gpuRamPts = gpuInfo[2] * 2
        points += int(gpuRamPts)

    rand = random.randint(0,999)
    return ("CID"+"_"+str(points)+"_"+str(rand))

#needs a lot of work. Check for different types of GPU cards and give it points.
def gpuLookup(card):
    points = 0
    try:
        if re.search('AMD|ATI', card):
            if re.search('ATI', card):
                if card == "ATI Radeon HD 4250":
                    points = 100
                elif card == "string":
                    points = 100
            if re.search('AMD', card):
                if re.search('7/d/d/d', card):
                    points = 7000
                if re.search('6/d/d/d', card):
                    points = 6000

        if re.search('nvidia', card):
            points = 1000
            
        return points
    
    except:
        print "GPU not in LookUp table"            


def download(ClientID, system, bits, gpuInfo):
    try:
        
        import urllib2

        def saveit(filename, fileobj):
            print "this is the file name %s" % filename
            f = open(filename,'w')
            f.write(fileobj.read())
            f.close()        
            
        
        gpuType = "None"
        if gpuInfo:
            if re.search('AMD|ATI', gpuInfo[0]) != None:
                gpuType = "ocl"
            elif re.search('nvidia', gpuInfo[0]) != None:
                gpuType = "cuda"
            else:
                gpuType = "None"

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

############
#
#LINUX FUNCTIONS
#
############
    
def linGetGPUinfo():
    import subprocess

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
            return "None"
            
    
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
            return "None"
	
    def getdevicename(device):
        _,_,rest = device.partition('\[') 
        result,_,_ = rest.partition('\]')
        return result
        
        
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
            print gpuType, deviceName,  amddriver
            
        elif re.search('NVIDIA', device):
            nvdriver = checknvdriver()
            gpuType = "cuda"
            
        else:
            gpudriver = "None"
            gpuType = "None"
            

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
	print cpuInfo
        return cpuInfo
    else:
        cpuInfo.append(last)
	print cpuInfo
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
    print "ram size in GB %s" % ramsize
    return ramsize

 
 
 
main()
