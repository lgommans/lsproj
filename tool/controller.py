#!/usr/bin/env python3

# Settings
algos = ['cubic', 'ctcp', 'dctcp', 'bic', 'bbr']
delays = [8, 64, 120, 176, 232, 290]
losses = [0, 0.01, 0.1, 0.6, 1.2]

hosts = {
    'server1': '10.0.0.6',
    'server2': '10.0.0.1',
    'winserv': '10.0.0.3',
    'client1': '10.0.0.2',
    'client2': '10.0.0.4',
}
# End of settings

import socket, time
from shared import *
from controllerlib import *

hostnames = {}  # Will be automatically obtained

for host in hosts:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hosts[host], TCPPORT))

    send(sock, MSG_GETNAME)
    name = read(sock)
    hostnames[host] = name

    send(sock, MSG_GETVERSION)
    version = int(read(sock))
    if version != VERSION:
        print('Incompatible client detected: {}|{} (v{} instead of {}). Aborting.'.format(host, name, version, VERSION))
        exit(2)

    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    send(sock, MSG_SETTIME)
    time.sleep(0.1)  # Sleep briefly, so that the client is definitely ready and blocking on the recv call, awaiting the time
    send(sock, time.time())
    read(sock)  # Unused currently
    print('Time synchronized with {}|{}.'.format(host, name))

    send(sock, MSG_BYE)

    #conn_test(host_from, host_to, duration=int(time.time()) + 3)
