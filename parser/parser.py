#!/usr/bin/env python

# Dependency: python-matplotlib

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import os

results = open("newresnew", "r")

algorithms = ['cubic', 'ctcp', 'dctcp', 'bic', 'bbr']
delays = [8, 80, 150, 220, 290]
losses = [0, 0.01, 0.1, 0.6, 1.2]
interval = 1 #1 second per bandwidth measurement
result_data = {}
counter = 1

def plot_graph(dataset, base_algo, sub_algo, loss, delay):
    global datastrs

    datastr = ''
    base_plot = {}
    sub_plot = {} 
    
    for result in dataset:
        if dataset[result][0]["run"] == "1" or dataset[result][0]["run"] == "2" or dataset[result][0]["run"] == "3" or dataset[result][0]["run"] == "4": #Always combined same run in dict
            #Yes, the if statement below is pretty useless. As of now. Not sure if this will have a purpose. 
            if "r" in result:
                if dataset[result][0]["c"] == "1":
                    client1 = 1
                    client2 = 0
                elif dataset[result][0]["c"] == "2":
                    client1 = 0
                    client2 = 1
            else:
                if dataset[result][0]["c"] == "1":
                    client1 = 0
                    client2 = 1
                elif dataset[result][0]["c"] == "2":
                    client1 = 1
                    client2 = 0
            
            if len(dataset[result]) < 2:
                print("Not complete error for algorithm: " + base_algo + " in combination with " + sub_algo) 
                return False

            if dataset[result][client1]["algo"] == base_algo and dataset[result][client2]["algo"] == sub_algo:
                if dataset[result][client1]["loss"] == loss and dataset[result][client1]["delay"] == delay: #The other one will always have the same delay and loss
                    if dataset[result][client1]["bandwidth"].strip() == '' or dataset[result][client2]["bandwidth"].strip() == '':
                        print('Warn: set without bandwidth, testnum={}'.format(dataset[result][client1]["testnum"]))
                        continue

                    #base_plot[dataset[result][client1]["run"]] = [int(x) for x in dataset[result][client1]["bandwidth"].strip().split(" ")]
                    #sub_plot[dataset[result][client2]["run"]] = [int(x) for x in dataset[result][client2]["bandwidth"].strip().split(" ")]
                    base_plot[dataset[result][client1]["run"]] = [float(x)/(2**20) for x in dataset[result][client1]["bandwidth"].strip().split(" ")]
                    sub_plot[dataset[result][client2]["run"]] = [float(x)/(2**20) for x in dataset[result][client2]["bandwidth"].strip().split(" ")]
                    datastr += 'base' + dataset[result][client1]["run"] + ': ' + str(base_plot[dataset[result][client1]["run"]]) + '\n'
                    datastr += 'sub' + dataset[result][client2]["run"] + ': ' + str(sub_plot[dataset[result][client2]["run"]]) + '\n'
    
    if "1" not in base_plot:
        return False

    filename = base_algo + "/" + base_algo + "_vs_" + sub_algo + "_" + delay + "_" + loss + ".png"
    datastrs[base_algo + "_vs_" + sub_algo + "_" + delay + "_" + loss] = datastr
    print(filename)

    #print("Bandwidth points " + base_algo +  " per 1 second: " + str(base_plot))
    #print("Bandwidth points " + sub_algo + " per 1 second: " + str(sub_plot)) 
    base_y = np.array(base_plot["1"])
    sub_y = np.array(sub_plot["1"])
    base_algor, = plt.plot(base_y, label=base_algo + ' run 1', color="red")
    sub_algor, = plt.plot(sub_y, label=sub_algo + ' run 1', color="darkgreen")
    plot_height = max(max(base_plot["1"]), max(sub_plot["1"])) * 1.1
    if len(base_plot) > 1 and len(sub_plot) > 1:
        base_y_2 = np.array(base_plot["2"])
        sub_y_2 = np.array(sub_plot["2"])
        if len(base_plot) > 2:
            print(">2 subplots for {}".format(filename))
        if len(base_plot) == 4 and len(sub_plot) == 4:
            base_y_3 = np.array(base_plot["3"])
            sub_y_3 = np.array(sub_plot["3"])
            base_y_4 = np.array(base_plot["4"])
            sub_y_4 = np.array(sub_plot["4"])
            base_algo_3, = plt.plot(base_y_3, label=base_algo + " run 3")
            sub_algo_3, = plt.plot(sub_y_3, label=sub_algo + " run 3")
            base_algo_4, = plt.plot(base_y_4, label=base_algo + " run 3")
            sub_algo_4, = plt.plot(sub_y_4, label=sub_algo + " run 3")
        else:    
            plot_height = max(max(base_plot["1"]), max(sub_plot["1"]), max(base_plot["2"]), max(sub_plot["2"])) * 1.1
        label1 = base_algo + " run 2"
        label2 = sub_algo + " run 2"
        base_algo_2, = plt.plot(base_y_2, label=label1, color="purple")
        sub_algo_2, = plt.plot(sub_y_2, label=label2, color="lightgreen")
        if len(base_plot) == 4 and len(sub_plot) == 4:
            plt.legend(handles=[base_algor, sub_algor, base_algo_2, sub_algo_2, base_algo_3, sub_algo_3, base_algo_4, sub_algo_4])
        else:
            plt.legend(handles=[base_algor, sub_algor, base_algo_2, sub_algo_2])
    else:
        plt.legend(handles=[base_algor, sub_algor])
    plt.ylabel("MiB/s")
    plt.xlabel("Time (seconds)")
    #plt.yscale('log')
    plt.axis([0,20,0,plot_height])
    #plt.axis([0,20,1110,plot_height])
    if not os.path.exists(base_algo):
        os.makedirs(base_algo)
    plt.savefig(filename)
    plt.close()
    #plt.show()
    return True

for result in results:
    if result != "\n":
        parameters = result.split(":")
        test_info = parameters[0]
        test_data = parameters[1].rstrip("\n").lstrip()
        dictionary = dict(item.split("=") for item in test_info.split(" "))
        dictionary.update({"bandwidth":test_data})
        if dictionary["testnum"] not in result_data:
            result_data[dictionary["testnum"]] = [dictionary]
        else:
            result_data[dictionary["testnum"]].append(dictionary)

lastf = None
last = None
def create_html(algo1, algo2, recursed=False):
    global last, lastf

    if not recursed:
        create_html(algo2, algo1, recursed=True)

    filename = '{}/{}_vs_{}.html'.format(algo1, algo1, algo2)
    f = open(filename, 'w')

    if lastf:
        lastf.write(' <a href="../{}">next</a>'.format(filename))
    lastf = f

    if last:
        f.write('<a href="../{}">previous</a>'.format(last))
    last = filename

    f.write('<title>{} vs {}</title>'.format(algo1, algo2))
    f.write('<table border=1><tr>')
    i = 0
    exists = 0
    for loss in losses:
        for delay in delays:
            try:
                datastr = datastrs['{}_vs_{}_{}_{}'.format(algo1, algo2, delay, loss)]
            except:
                datastr = '(unknown)'

            f.write('<td>{algo1} vs {algo2} with {delay}ms delay and {loss}% loss<br><img src="{algo1}_vs_{algo2}_{delay}_{loss}.png" title="{datastr}" width=640 height=480></td>'
                .format(algo1=algo1, algo2=algo2, delay=delay, loss=loss, datastr=datastr))

            if os.path.isfile('{algo1}/{algo1}_vs_{algo2}_{delay}_{loss}.png'.format(algo1=algo1, algo2=algo2, delay=delay, loss=loss)):
                exists += 1

            i += 1
            if i % 3 == 0:
                f.write('</tr><tr>')
    f.write(' This page contains {} images.'.format(exists))
    index.write('<a href="{}">{}</a><br>\n'.format(filename, filename))

def create_html_delay_loss(delay, loss):
    f = open('params/delay={}/loss={}.html'.format(delay, loss), 'w')
    f.write('<title>delay={} loss={}</title>'.format(delay, loss))
    f.write('<table border=1><tr>')
    i = 0
    done = {}
    for algo1 in algorithms:
        for algo2 in algorithms:
            if algo1 == algo2:
                continue

            if (algo2, algo1) in done:
                continue

            done[(algo1, algo2)] = True

            try:
                datastr = datastrs['{}_vs_{}_{}_{}'.format(algo1, algo2, delay, loss)]
            except:
                datastr = '(unknown)'

            f.write('<td>{algo1} vs {algo2} with {delay}ms delay and {loss}% loss<br><img src="../../{algo1}/{algo1}_vs_{algo2}_{delay}_{loss}.png" width=640 height=480 title="{datastr}"></td>'
                .format(algo1=algo1, algo2=algo2, delay=delay, loss=loss, datastr=datastr))

            i += 1
            if i % 3 == 0:
                f.write('</tr><tr>')

print("length result_data: " + str(len(result_data)))
#print(result_data)

# Plot graph for base_algorithm and sub_algorithm
datastrs = {}
done = {}
for delay in delays:
    for loss in losses:
        for algo1 in algorithms:
            for algo2 in algorithms:
                if algo1 == algo2:
                    continue

                if (algo2, algo1) in done:
                    #print('Already had {},{}: not doing {},{}'.format(algo2, algo1, algo1, algo2))
                    continue

                done[(algo1, algo2)] = True
                plot_graph(result_data, algo1, algo2, str(loss), str(delay))

index = open('index.html', 'w')
for algo1 in algorithms:
    for algo2 in algorithms:
        if algo1 == algo2:
            continue

        create_html(algo1, algo2)

if not os.path.isdir('params'):
    os.makedirs('params')
    for delay in delays:
        os.makedirs('params/delay={}'.format(delay))

for delay in delays:
    for loss in losses:
        create_html_delay_loss(delay, loss)

