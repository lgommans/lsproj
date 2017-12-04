# Settings
MAXMSGLEN = 100  # bytes
TCPPORT = 1
MTU = 1400  # bytes
MAXTESTDURATION = 1000  # seconds
CONNTESTGAP = 3  # seconds
VERSION = 1
# End of settings

import os

TRANSMIT_DATA = os.urandom(MTU)

MSG_GETNAME = 'Dear sir/madam, could you please tell me your name?'
MSG_BYE = 'If you will excuse me, I have got to go catch a bus.'
MSG_SETTIME = 'Could you synchronize the clock at your earliest convenience?'
MSG_LISTEN = 'Data will be forthcoming. Observe, hack, make.'
MSG_SEND = 'ATTACK'
MSG_GETRESULTS = 'What were the results? :D'
MSG_SETCONNPROPS = 'chprops plz'
MSG_SETALGO = 'chalgo plz'
MSG_GETVERSION = 'How old are you, if I may ask?'
MSG_DIE = 'The end is near'

def send(sock, data):
    data = str(data)
    sock.send(bytes(data + (' ' * (MAXMSGLEN - len(data))), 'utf-8'))

def read(sock):
    return str(sock.recv(MAXMSGLEN), 'utf-8').strip()

