from shared import *
import time
import socket

dataport = int(40e3)

def conn_test(host_from, host_to, duration, delay, loss, algo, at, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host_to, port))
    send(sock, MSG_SETCONNPROPS)
    send(sock, str(loss) + '%')
    send(sock, str(delay) + 'ms')

    send(sock, MSG_LISTEN)
    send(sock, dataport)

    send(sock, MSG_BYE)

    time.sleep(0.1)  # Otherwise the other host apparently tries to connect too fast

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host_from, port))

    send(sock, MSG_SETALGO)
    send(sock, algo.lower())

    send(sock, MSG_SEND)
    send(sock, host_to)
    send(sock, dataport)
    send(sock, duration)
    send(sock, at)

    send(sock, MSG_BYE)


def get_results(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    send(sock, MSG_GETRESULTS)
    results = read(sock)
    send(sock, MSG_BYE)

    return results


def runtest(hosts, hostnames, defaultport, ports, test_duration, delay, loss, algo1, algo2):
    global dataport

    tag = 'delay={} duration={} '.format(delay, test_duration)

    if algo1 == 'ctcp':
        s1 = hosts['winserv']
    else:
        s1 = hosts['server1']

    if algo2 == 'ctcp':
        s1 = hosts['winserv']
    else:
        s2 = hosts['server2']

    results = {}

    print('{}->{} and {}->{}'.format(hostnames[s1], hostnames[hosts['client1']], hostnames[s2], hostnames[hosts['client2']]))
    at = time.time() + CONNTESTGAP
    conn_test(s1, hosts['client1'], duration=test_duration, loss=loss, delay=delay, algo=algo1, at=at, defaultport if 'client1' not in ports else ports['client1'])
    conn_test(s2, hosts['client2'], duration=test_duration, loss=loss, delay=delay, algo=algo2, at=at, defaultport if 'client2' not in ports else ports['client2'])
    dataport += 1
    time.sleep(test_duration + CONNTESTGAP * 2)

    results[tag + 'algo={} run=1 s={} c=1'.format(algo1, s1)] = get_results(hosts['client1'], defaultport if 'client1' not in ports else ports['client1'])
    results[tag + 'algo={} run=1 s={} c=2'.format(algo2, s2)] = get_results(hosts['client2'], defaultport if 'client2' not in ports else ports['client2'])

    print('{}->{} and {}->{}'.format(hostnames[s1], hostnames[hosts['client2']], hostnames[s2], hostnames[hosts['client1']]))
    at = time.time() + CONNTESTGAP
    conn_test(s1, hosts['client2'], duration=test_duration, loss=loss, delay=delay, algo=algo1, at=at, defaultport if 'client2' not in ports else ports['client2'])
    conn_test(s2, hosts['client1'], duration=test_duration, loss=loss, delay=delay, algo=algo2, at=at, defaultport if 'client1' not in ports else ports['client1'])
    dataport += 1
    time.sleep(test_duration + CONNTESTGAP * 2)

    results[tag + 'algo={} run=2 s={} c=2'.format(algo1, s1)] = get_results(hosts['client2'], defaultport if 'client2' not in ports else ports['client2'])
    results[tag + 'algo={} run=2 s={} c=1'.format(algo2, s2)] = get_results(hosts['client1'], defaultport if 'client1' not in ports else ports['client1'])

    return results

