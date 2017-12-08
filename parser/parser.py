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
                    base_plot[dataset[result][client1]["run"]] = [int(x) for x in dataset[result][client1]["bandwidth"].split(" ")]
                    sub_plot[dataset[result][client2]["run"]] = [int(x) for x in dataset[result][client2]["bandwidth"].split(" ")]
    
    if "1" not in base_plot:
        return False
    #print("Bandwidth points " + base_algo +  " per 1 second: " + str(base_plot))
    #print("Bandwidth points " + sub_algo + " per 1 second: " + str(sub_plot)) 
    base_y = np.array(base_plot["1"])
    sub_y = np.array(sub_plot["1"])
    base_algor, = plt.plot(base_y, label=base_algo, color="red")
    sub_algor, = plt.plot(sub_y, label=sub_algo, color="darkgreen")
    plot_height = max(max(base_plot["1"]), max(sub_plot["1"])) + 7000
    if len(base_plot) > 1 and len(sub_plot) > 1:
        base_y_2 = np.array(base_plot["2"])
        sub_y_2 = np.array(sub_plot["2"])
        if len(base_plot) > 2:
            print("YES")
        if len(base_plot) == 4 and len(sub_plot) == 4:
            print("Should print 2 extra by now")
            base_y_3 = np.array(base_plot["3"])
            sub_y_3 = np.array(sub_plot["3"])
            base_y_4 = np.array(base_plot["4"])
            sub_y_4 = np.array(sub_plot["4"])
            base_algo_3, = plt.plot(base_y_3, label=base_algo + "extra")
            sub_algo_3, = plt.plot(sub_y_3, label=sub_algo + "extra")
            base_algo_4, = plt.plot(base_y_4, label=base_algo + "extra2")
            sub_algo_4, = plt.plot(sub_y_4, label=sub_algo + "extra2")
        else:    
            plot_height = max(max(base_plot["1"]), max(sub_plot["1"]), max(base_plot["2"]), max(sub_plot["2"])) + 1000
        label1 = base_algo + " reverse"
        label2 = sub_algo + " reverse"
        base_algo_2, = plt.plot(base_y_2, label=label1, color="purple")
        sub_algo_2, = plt.plot(sub_y_2, label=label2, color="lightgreen")
        if len(base_plot) == 4 and len(sub_plot) == 4:
            plt.legend(handles=[base_algor, sub_algor, base_algo_2, sub_algo_2, base_algo_3, sub_algo_3, base_algo_4, sub_algo_4])
        else:
            plt.legend(handles=[base_algor, sub_algor, base_algo_2, sub_algo_2])
    else:
        plt.legend(handles=[base_algor, sub_algor])
    plt.ylabel("Bytes sent")
    plt.xlabel("Seconds")
    plt.axis([0,20,20000,plot_height])
    if not os.path.exists(base_algo):
        os.makedirs(base_algo)
    filename = base_algo + "/" + base_algo + "_vs_" + sub_algo + "_" + delay + "_" + loss + ".png"
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

print("length result_data: " + str(len(result_data)))
#print(result_data)

# Plot graph for base_algorithm and sub_algorithm
for delay in delays:
    for loss in losses:
        for algo1 in algorithms:
            for algo2 in algorithms:
                if algo1 == algo2:
                    continue
                try:
                    plot_graph(result_data, algo1, algo2, str(loss), str(delay))
                except:
                    pass
