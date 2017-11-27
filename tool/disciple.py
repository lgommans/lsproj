#!/usr/bin/env python3

import sys, os, socket, datetime, time
from shared import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', TCPPORT))
sock.listen(1)

print('Ready to receive commands.')

while True:
    controller, client_address = sock.accept()
    while True:
        data = read(controller)
        if data == 'test':
            print('Received connection test at ' + time.ctime())

        elif data == MSG_GETNAME:
            send(controller, socket.gethostname())

        elif data == MSG_BYE:
            break

        elif data == MSG_SETALGO:
            algo = read(controller)
            os.system('sysctl net.ipv4.tcp_congestion_control=' + algo)

        elif data == MSG_SETTIME:
            recvtime = read(controller)
            if os.name == 'nt':
                t = datetime.fromtimestamp(float(recvtime))
                recvtime = t.strftime('%H:%I:%S') + recvtime.split('.')[1][:3]
                os.system('echo ' + recvtime + ' | recvtime')
            else:
                os.system('date -s @' + recvtime)

            print('Set the time to ' + recvtime)

            send(controller, time.time())

        else:
            print('Unrecognized command')

