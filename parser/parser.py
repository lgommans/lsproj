results = open("newresults", "r")

temp_data = {}
result_data = {}
counter = 1

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
print(result_data)
            #print(temp_data)
            #print(len(temp_data))
            #test_dict = {}
            #for i in result_data:
            # if result_data[i]["c"] == "1":
            # if result_data[i]["run"] == "1":
            # if result_data[i]["algo"] == "cubic":
            # print(result_data[i])



