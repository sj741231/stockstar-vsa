# -*- coding: utf-8 -*-
__author__ = 'songtao'




#
# def getwinsize():
#     """This function use to get the size of the windows!"""
#     if 'TIOCGWINSZ' in dir(termios):
#         TIOCGWINSZ = termios.TIOCGWINSZ
#     else:
#         TIOCGWINSZ = 1074295912L  # Assume
#     s = struct.pack('HHHH', 0, 0, 0, 0)
#     x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
#     return struct.unpack('HHHH', x)[0:2]


def sigwinch_passthrough (sig, data):
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(),
                                          termios.TIOCGWINSZ , s))
    global p
    p.setwinsize(a[0],a[1])



def connect_by_paramiko(ip, port, username):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
    except Exception, e:
        print '连接失败:' + str(e)
    t = paramiko.Transport(sock)
    try:
        t.start_client()
    except paramiko.SSHException:
        print 'print *** SSH negotiation failed.'
    keys = {}
    pw = getpass.getpass('password for %s@%s \n' % (username, ip))
    try:
        t.auth_password(username, pw)
        chan = t.open_session()
        chan.get_pty()
        size = getwinsize()
        chan.invoke_shell()
        print('*** Here we go!\n')
        interactive.interactive_shell(chan)
        chan.close()
        t.close()
    except:
        print "username or password error,please check your input"