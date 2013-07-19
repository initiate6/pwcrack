filename = 'ftpTest.txt'

def ftpDownload(filename):
    from ftplib import FTP_TLS
    import os
    
    ftps = FTP_TLS()
    ftps.connect('pwcrack.init6.me', '21')
    ftps.auth()
    ftps.login('DC214', 'passwordcrackingcontest')
    ftps.prot_p()
    ftps.set_pasv(True)
    local_filename = filename
    with open(local_filename, 'wb') as f:
        def callback(data):
            f.write(data)
        ftps.retrbinary('RETR %s' % filename, callback)

ftpDownload(filename)
