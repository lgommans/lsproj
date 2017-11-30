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
    
for setup in Config.setups:
    duration = setup['settings']['duration']
    name = setup['settings']['name']
    print("Running setup: " + name)

    for host_from, host_to in setup['hosts']:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host_to, TCPPORT))
        send(sock, MSG_LISTEN)
        send(sock, MSG_BYE)
        time.sleep(0.1) # Otherwise the other host apparently tries to connect too fast

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host_from, TCPPORT))
        send(sock, MSG_SEND)
        send(sock, host_to)
        send(sock, duration)
        send(sock, int(time.time()) + 3)
        send(sock, MSG_BYE)

    print('Sleeping till end of test...')
    time.sleep(duration + 6)

    for host, role in setup['hosts']:
        if role == 'receiver':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, TCPPORT))
            send(sock, MSG_GETRESULTS)
            print(read(sock))
            send(sock, MSG_BYE)

    print('Done running setups')

