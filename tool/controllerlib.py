from shared import *

def conn_test(host_from, host_to, duration, delay, loss, algo, at):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host_to, TCPPORT))
    send(sock, MSG_LISTEN)

    send(sock, MSG_SETCONNPROPS)
    send(sock, str(loss) + '%')
    send(sock, str(delay) + 'ms')
    send(sock, algo.lower())

    send(sock, MSG_BYE)

    time.sleep(0.1)  # Otherwise the other host apparently tries to connect too fast

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host_from, TCPPORT))
    send(sock, MSG_SEND)
    send(sock, host_to)
    send(sock, duration)
    send(sock, at)
    send(sock, MSG_BYE)

    time.sleep(duration + CONNTESTGAP * 2)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host_to, TCPPORT))
    send(sock, MSG_GETRESULTS)
    results = map(int, read(sock).split(' '))
    send(sock, MSG_BYE)

    return results

