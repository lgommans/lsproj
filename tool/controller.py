#!/usr/bin/env python3

# Settings
algos = ['cubic', 'ctcp', 'dctcp', 'bic', 'bbr']
delays = [8, 80, 150, 220, 290]
losses = [0, 0.01, 0.1, 0.6, 1.2]
test_duration = 20

hosts = {
    'server1': '10.0.0.1',
    'server2': '10.0.0.2',
    'winserv': '10.0.0.3',
    'client1': '10.0.0.4',
    'client2': '10.0.0.4',
}

# Only non-standard ports need to be mentioned in the ports table.
defaultport = 1
ports = {
    'client2': 2,
}
# End of settings

import socket, time, sys, os, random
from shared import *
from controllerlib import *

kill = False
if len(sys.argv) == 2 and sys.argv[1] == 'killclients':
    kill = True

hostnames = {}  # Will be automatically obtained

if not kill:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((hosts['winserv'], defaultport if 'winserv' not in ports else ports['winserv']))

    send(sock, MSG_GETTIME)
    starttime = time.time()
    wintime = read(sock)
    os.system('date -s @' + wintime + ' >/dev/null')
    print('Corrected time by ' + str(starttime-float(wintime)) + ' seconds')
    send(sock, MSG_BYE)
    sock.close()

for host in hosts:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    if not kill:
        print('Connecting to ' + hosts[host])
    try:
        sock.connect((hosts[host], defaultport if host not in ports else ports[host]))
    except:
        if not kill:
            raise
        continue

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

    if host != 'winserv':
        # We just got the time from Windows, we don't wanna sync with that
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        send(sock, MSG_SETTIME)
        time.sleep(0.1)  # Sleep briefly, so that the client is definitely ready and blocking on the recv call, awaiting the time
        starttime = time.perf_counter()
        send(sock, time.time())
        returntime = float(read(sock))
        print('Time synchronized with {}|{}. Their time is {} offset from ours. Setting time took {}.'.format(host, name, time.time() - returntime, time.perf_counter() - starttime))

    send(sock, MSG_BYE)
    sock.close()

if kill:
    exit(0)

print('')

results = {}
if os.path.isfile('savefile2'):
    savefile = open('savefile2').read()
else:
    savefile = ''

savefileout = open('savefile2', 'a')
resultfileout = open('results2', 'a')
resultfileout.write('\n')

num_total_tests = 0
count = 0
todotests = []
try:
    for algo1 in algos:
        for algo2 in algos:
            for delay in delays:
                for loss in losses:
                    num_total_tests += 1
                    if algo1 == algo2:
                        continue

                    if algo1 == 'ctcp' or algo2 == 'ctcp':
                        continue # skip for now

                    config = 'algo1={} algo2={} delay={} loss={}'.format(algo1, algo2, delay, loss)
                    config_alt = 'algo2={} algo1={} delay={} loss={}'.format(algo1, algo2, delay, loss)  # Swap algo1 and 2
                    if config in savefile or config_alt in savefile:
                        print('Skipping ' + config + ': already in savefile')
                        continue

                    todotests.append([algo1, algo2, delay, loss])

    print('Starting {} tests ({} skipped or already done)'.format(len(todotests), num_total_tests))
    random.shuffle(todotests)
    for algo1, algo2, delay, loss in todotests:
        print('Running ' + config + ' ({}/{}, {} minutes remaining)'.format(count, len(todotests), round((len(todotests) - count) * 2 * test_duration * CONNTESTGAP / 60)))
        results.update(runtest(hosts, hostnames, defaultport, ports, test_duration, delay, loss, algo1, algo2))
        savefileout.write(config + '\n')
        print('')
        count += 1

    raise ':)'
except: # Catch keyboardinterrupt -- or error but in all cases, the exception will be printed after the results.
    for result in results:
        print(result + ": " + str(results[result]))

    for result in results:
        resultfileout.write(result + ": " + str(results[result]) + '\n')

    sys.stdout.flush()  # flush stdout so it doesn't mix with stderr that will get printed
    resultfileout.close()

    raise

