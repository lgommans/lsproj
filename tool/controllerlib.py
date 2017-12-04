from shared import *
import time
import socket

def conn_test(host_from, host_to, duration, delay, loss, algo, at):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host_to, TCPPORT))
    send(sock, MSG_LISTEN)

    send(sock, MSG_SETCONNPROPS)
    send(sock, str(loss) + '%')
    send(sock, str(delay) + 'ms')

    send(sock, MSG_BYE)

    time.sleep(0.1)  # Otherwise the other host apparently tries to connect too fast

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host_from, TCPPORT))

    send(sock, MSG_SEND)
    send(sock, host_to)
    send(sock, duration)
    send(sock, at)

    send(sock, MSG_SETALGO)
    send(sock, algo.lower())

    send(sock, MSG_BYE)

    time.sleep(duration + CONNTESTGAP * 2)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host_to, TCPPORT))
    send(sock, MSG_GETRESULTS)
    results = map(int, read(sock).split(' '))
    send(sock, MSG_BYE)

    return results

def runtest(hosts, test_duration, delay, loss, algo1, algo2):
    tag = 'algo1={} algo2={} delay={} duration={} '.format(algo1, algo2, delay, test_duration)

    if algo1 == 'ctcp':
        s1 = hosts['winserv']
    else:
        s1 = hosts['server1']

    if algo2 == 'ctcp':
        s1 = hosts['winserv']
    else:
        s2 = hosts['server2']

    at = time.time() + CONNTESTGAP
    results[tag + 'run=1 s={} c=1'.format(s1)] = conn_test(s1, hosts['client1'], duration=test_duration, loss=loss, delay=delay, algo=algo1, at=at)
    results[tag + 'run=1 s={} c=2'.format(s2)] = conn_test(s2, hosts['client2'], duration=test_duration, loss=loss, delay=delay, algo=algo2, at=at)
    time.sleep(test_duration + CONNTESTGAP * 2)

    at = time.time() + CONNTESTGAP
    results[tag + 'run=2 s={} c=2'.format(s1)] = conn_test(s1, hosts['client2'], duration=test_duration, loss=loss, delay=delay, algo=algo, at=at)
    results[tag + 'run=2 s={} c=1'.format(s2)] = conn_test(s2, hosts['client1'], duration=test_duration, loss=loss, delay=delay, algo=algo, at=at)
    time.sleep(test_duration + CONNTESTGAP * 2)

    return results

