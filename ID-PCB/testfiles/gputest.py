import sys, re, _winreg
        
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
        for line in ClearnVideoCardString:
            for item in line.split("\\")[2:3]:
                if item == 'Control':
                    hVideoCardReg = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, str(line))
                    VideoCardDescription  = _winreg.QueryValueEx(hVideoCardReg,"Device Description")[0]
                    print VideoCardDescription
