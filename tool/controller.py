#!/usr/bin/env python3

# Settings
algos = ['cubic', 'ctcp', 'dctcp', 'bic', 'bbr']
delays = [8, 64, 120, 176, 232, 290]
losses = [0, 0.01, 0.1, 0.6, 1.2]
test_duration = 10

hosts = {
    'server1': '10.0.0.5',
    'server2': '10.0.0.1',
    'winserv': '10.0.0.3',
    'client1': '10.0.0.2',
    'client2': '10.0.0.4',
}
# End of settings

import socket, time, sys
from shared import *
from controllerlib import *

kill = False
if len(sys.argv) == 2 and sys.argv[1] == 'killclients':
    kill = True

hostnames = {}  # Will be automatically obtained

for host in hosts:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    if not kill:
        print('Connecting to ' + hosts[host])
    sock.connect((hosts[host], TCPPORT))

    if kill:
        print('Killing ' + hosts[host])
        send(sock, MSG_DIE)
        continue

    send(sock, MSG_GETNAME)
    name = read(sock)
    hostnames[host] = name
    hostnames[hosts[host]] = name

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

if kill:
    exit(0)

print('')

results = {}

for algo1 in algos:
    for algo2 in algos:
        for delay in delays:
            for loss in losses:
                print('Running algo1={} algo2={} delay={} loss={}'.format(algo1, algo2, delay, loss))
                results.update(runtest(hosts, hostnames, test_duration, delay, loss, algo1, algo2))
                print('')

for result in results:
    print(result + ": " + str(results[result]))

