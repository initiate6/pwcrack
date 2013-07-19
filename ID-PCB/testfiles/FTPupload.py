filename = 'testme.txt'

def ftpUpload(filename):
    from ftplib import FTP_TLS
    import os
    
    ftps = FTP_TLS()
    ftps.connect('pwcrack.init6.me', '21')
    ftps.auth()
    ftps.login('DC214', 'passwordcrackingcontest')
    ftps.prot_p()
    ftps.set_pasv(True)
    local_file = open(filename, 'rb')
    ftps.storbinary('STOR '+filename, local_file)


ftpUpload(filename)
