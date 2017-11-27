#!/usr/bin/env python3

import socket, time
from config import Config
from shared import *

for host in Config.hosts:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host['ip'], TCPPORT))
    send(sock, 'test')
    send(sock, MSG_GETNAME)
    name = read(sock)
    print('Connected to ' + name + ', syncing time...')

    send(sock, MSG_SETTIME)
    time.sleep(0.1)
    starttime = time.time()
    send(sock, time.time())
    d = time.time() - float(read(sock))
    print('Time sync\'d to {0:f} seconds.'.format(d/2))
    send(sock, MSG_BYE)

