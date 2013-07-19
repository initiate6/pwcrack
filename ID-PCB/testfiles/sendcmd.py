def sendCMD(clientID, command):
    import socket, string, ssl, re, os

    def join(channel):
        irc.send('JOIN #%s \r\n' % channel)
    
    network = 'irc.init6.me'
    chan1 = 'pwc'+'_'.join(clientID.split('_')[1:])
    port = 16667
    nick = 'sendingCMD'

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((network,port))
    
    irc = ssl.wrap_socket(socket,do_handshake_on_connect=False)
    
    while True:
        try:
            irc.do_handshake()
            break
        except ssl.SSLError as err:
            if err.args[0] == ssl.SSL_ERROR_WANT_READ:
                select.select([irc], [], [])
            elif err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
                select.select([], [irc], [])
            else:
                raise
    
    irc.send('NICK %s\r\n' % nick)
    print irc.recv(4096)
    irc.send('USER %s %s %s :My bot\r\n' % (nick,nick,nick))
    print irc.recv(4096)
    join(chan1)
    print irc.recv(4096)
    
    msg = '!%s' % clientID
    for cmd in command:
        msg += '..'
        msg += re.sub(' ', '..', cmd)
    
    irc.send('PRIVMSG #%s %s\r\n' % (chan1, msg))
