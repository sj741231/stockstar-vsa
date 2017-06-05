import termios
import sys
import struct
import fcntl

def getwinsize():
    """This function use to get the size of the windows!"""
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912L  # Assume
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    print x
    print struct.unpack('HHHH', x)[0:2]
    return struct.unpack('HHHH', x)[0:2]


getwinsize()
