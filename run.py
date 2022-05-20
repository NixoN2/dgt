import random
import os
import sys
from datetime import date

today = date.today()

ports = [4104,4106,4107,4108,4109,4110,
4204,4206,4207,4208,4209,4210,
4304,4306,4307,
4404,4406,4407,
4504,4506,4507,
4604,4606,4607]

clusters = [1,2,3,4,5,6]
nodes = [1,2,3,4,5,6]

def create_command(functions,prefix,wallets):
    random.shuffle(wallets)
    random_wallet_1 = wallets[0]
    random_wallet_2 = wallets[1]
    random_command = random.choice(functions)
    random_value = random.randint(1,1000)
    if random_command == "inc":
        return f"{prefix} -f inc -w {random_wallet_1} -c {random_value}"
    elif random_command == "dec":
        return f"{prefix} -f dec -w {random_wallet_1} -c {random_value}"
    elif random_command == "trans":
        return f"{prefix} -f trans -w {random_wallet_1} -c {random_value} -w2 {random_wallet_2}"

n = int(sys.argv[1])
nodes_to_down = int(sys.argv[2])


prefixes = []

for i in clusters:
    for j in nodes:
        if i in [3,4,5,6]:
            if j > 3:
                continue
        prefixes.append(f"python3 transaction_time.py {i} {j}")

#prefix = f"python3 transaction_time.py {cluster} {node}"

wallet_number = random.randint(3, n) % 10

wallets = []

for i in range(wallet_number):
    wallets.append(f"wal{i}")

for prefix in prefixes: 
    for wallet in wallets:
        os.system(f"{prefix} -f set -w {wallet} -c {random.randint(100,10000)}")

functions = ["inc","trans","dec"]

commands = []
#commands_for_closed_port = []


ports_to_close = random.sample(ports,nodes_to_down)

for i in range(n):
    choice = random.choice(prefixes)
    command = create_command(functions,choice,wallets)
    commands.append(command)

with open('results.txt', 'w') as f:
    text = ""
    time = 0
    for i in range(n):
        content = os.popen(commands[i])
        for j in content.readlines():
            if j.startswith("Execution time"):
                time += float(j.split()[6])
            text += j

    f.write("--------------------------------------------\n")
    f.write(f"date: {today}\n")
    f.write(f"nodes: 24\n")
    f.write(f"nodes down: 4\n")
    f.write(f"time: {time} seconds\n")
    f.write("--------------------------------------------\n")
    f.write(text)   
    f.write(f"-------------------------------------------\n")
    f.write(f"Ports closed\n")
    f.write(f"-------------------------------------------\n")
    #for i in range(n):
    #    os.system(commands[i])

    #print(f"tttttttttttttttttttest: {os.popen(f'{commands[0]}').read()}")

    for i in ports_to_close:
        os.system(f"sudo /sbin/iptables -A DOCKER -p tcp --destination-port {i} -j DROP")

    os.system(f"sudo /sbin/iptables-save")
    

    text = ""
    time = 0
    for i in range(n):
        content = os.popen(commands[i])
        for j in content.readlines():
            if j.startswith("Execution time"):
                time += float(j.split()[6])
            text += j
            
    #for i in range(n):
    #    os.system(commands[i])
    f.write(text)   


    for i in ports_to_close:
        os.system(f"sudo /sbin/iptables -A DOCKER -p tcp --destination-port {i} -j ACCEPT")

    #for i in range(len(ports_to_close)*2+1):
    #    os.system(f"sudo /sbin/iptables -D DOCKER 73")

    os.system(f"sudo /sbin/iptables-save")



