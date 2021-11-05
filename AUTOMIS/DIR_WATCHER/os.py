import os

path = "../SCRATCH"
proj_name = "AUTOMIS"
test_arr = []
with open("../TABLE.txt","w") as table:
    pass
for root, dirs, files in os.walk(path):
    temp_arr = root.split("/")
    if len(temp_arr) == 5:
        table_id = f"{proj_name}_{temp_arr[3]},{temp_arr[4]}\n"
        with open("../TABLE.txt","r") as f:
            read_file = f.readlines()
            if table_id not in read_file:
                test_arr.append(table_id)

with open("../TABLE.txt","a") as f:
    for each in test_arr:
        f.write(each)