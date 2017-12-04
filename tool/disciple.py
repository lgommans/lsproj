#!/usr/bin/env python3

import sys, os, socket, datetime, time
from shared import *

if os.name == 'posix':
    os.system('''
    ip l | grep ifb0 > /dev/null;
    if [ $? -ne 0 ]; then
        modprobe ifb;
        ip link set dev ifb0 up;
        tc qdisc add dev eno1 ingress;
        tc filter add dev eno1 parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0;
        echo Setup ifb interface;
    else
        echo ifb interface already setup;
    fi;
    ''')
    os.system('tc qdisc add dev ifb0 root netem delay 0ms loss 0%')
    os.system('tc qdisc change dev ifb0 root netem delay 0ms loss 0%')

controlleraddr = None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', TCPPORT))
sock.listen(1)

print('Ready to receive commands.')

while True:
    controller, addr = sock.accept()
    controlleraddr = addr
    print('Controller connection from {}.\n'.format(addr))
    while True:
        data = read(controller)
        if data == 'test':
            print('Received connection test at ' + time.ctime())

        elif data == MSG_GETVERSION:
            send(controller, VERSION)

        elif data == MSG_GETNAME:
            send(controller, socket.gethostname())

        elif data == MSG_BYE:
            print('Controller disconnected from socket.')
            break

        elif data == MSG_SETTIME:
            recvtime = read(controller)
            if os.name == 'nt':
                t = datetime.datetime.fromtimestamp(float(recvtime))
                recvtime = t.strftime('%H:%I:%S') + recvtime.split('.')[1][:3]
                os.system('echo ' + recvtime + ' | time')
            else:
                os.system('date -s @' + recvtime + ' >/dev/null')

            print('Set the time to ' + recvtime)

            send(controller, time.time())
            print("Set time to: " + str(time.time()))

        elif data == MSG_SEND:
            dst = read(controller)
            dataport = int(read(controller))
            duration = int(read(controller))
            when = float(read(controller))

            ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ds.connect((dst, dataport))
            print('Connected to data sink, waiting until ' + str(when))

            while time.time() < when:
                pass
            
            until = when + duration
            while time.time() < until:
                ds.send(TRANSMIT_DATA)

            ds.close()
            print('Done. Disconnecting from data sink.')

        elif data == MSG_LISTEN:
            dataport = int(read(controller))

            ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ds.bind(('0.0.0.0', dataport))
            ds.listen(1)
            print('Listening on port {} for data, awaiting client.'.format(dataport))

            t = int(time.time())
            bytecounts = {}
            for i in range(t, t+MAXTESTDURATION):
                bytecounts[i] = 0

            ds.settimeout(CONNTESTGAP * 3)
            client, addr = ds.accept()
            print('Client {} connected at {}.'.format(addr, time.time()))
            while True:
                l = len(client.recv(MTU))
                if l == 0:
                    break
                bytecounts[int(time.time())] += l

            client.close() # Should already be closed, since received_data.length==0 earlier, but just to be sure that the listsock doesn't remain in time-wait
            ds.close()
            print('Closed listening data socket at {}.'.format(time.time()))

            print('Resetting delay and loss to 0%/ms')
            os.system('tc qdisc change dev ifb0 root netem delay 0ms loss 0%')

            first = float('inf')
            for t in bytecounts:
                if bytecounts[t] > 0 and t < first:
                    first = t

            if first == float('inf'):
                print('No results?!')
                raise Exception('No results to report!')

            results = ''
            for t in range(first, first + MAXTESTDURATION):
                if bytecounts[t] == 0:
                    break
                results += str(bytecounts[t]) + ' '
            results = results.strip()

        elif data == MSG_GETRESULTS:
            print('Sending results.')
            send(controller, results)

        elif data == MSG_SETALGO:
            algo = read(controller)
            if os.name == 'nt':
                print('Ignoring setalgo because I am New Technology.')
            else:
                print('Setting algo={}'.format(algo))
                os.system('sysctl net.ipv4.tcp_congestion_control=' + algo)

        elif data == MSG_SETCONNPROPS:
            loss = read(controller)
            delay = read(controller)
            print('Setting delay={} loss={}'.format(delay, loss))
            os.system('tc qdisc change dev ifb0 root netem delay ' + delay + ' loss ' + loss)

        elif data == MSG_DIE:
            exit(0)

        else:
            print('Unrecognized command')
