# Gather info about the computer and save to file for client.py.
# Only have to run setup.py one time on each computer. 

import platform
import sys
import _winreg
import string
import struct
import re
import random

def main():
    system = platform.system()

    if system == 'Windows':
        bits = checkBits()
        cpuInfo = winGetCPUinfo()
        gpuInfo = winGetGPUinfo()
        ramInfo = winGetRAMinfo()
        ClientID = getClientID( system, bits, cpuInfo, gpuInfo, ramInfo )
        writeit(ClientID, system, bits, cpuInfo, gpuInfo, ramInfo)
        
    if system == 'Linux':
        bits = checkBits()

    if system == 'Darwin':
        bits = checkBits()

#write info to a file for client.py to read later.
def writeit( ClientID, system, bits, cpuInfo, gpuInfo, ramInfo ):
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
    f.write('gpu.'+gpuInfo[0]+'\n')
    f.write('gpuDriver.'+gpuInfo[1]+'\n')
    f.write('ram.'+str(ramInfo)+'\n')
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
        #print '%d MB physical RAM.' %(m.dwTotalPhys/1024**2)
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
        if not GPUinfo == False:
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
        if re.search('AMD|ATI', gpuDriver[0]) != None:
            if gpuDriver[1] == "13.1":
                return True

        elif re.search('nvidia', gpuDriver[0]) != None:
            if gpuDriver[1] == "9.18.13.1422":
                return True            

        else:
            print "Your GPU driver for "+gpuDriver[0]+" is " + gpuDriver[1] + " and needs to be upgraded or downgraded to match oclhashcat requirements"
            
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
        if re.search('AMD|ATI', card) != None:
            if re.search('ATI', card) != None:
                if card == "ATI Radeon HD 4250":
                    points = 100
                elif card == "string":
                    points = 100
            if re.search('AMD', card) != None:
                if re.search('7/d/d/d', card) != None:
                    points = 7000
                if re.search('6/d/d/d', card) != None:
                    points = 6000

        if re.search('nvidia', card) != None:
            points = 1000
            
        return points
    
    except:
        print "GPU not in LookUp table"            
        
main()
