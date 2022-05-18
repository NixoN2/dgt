import random
import os
import sys

ports = [1,2,3]

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



cluster = sys.argv[1]
node = sys.argv[2]
n = int(sys.argv[3])
max_node = int(sys.argv[4])

nodes = []
for i in range(1,max_node+1):
    nodes.append(i)

prefixes = []

for i in nodes:
    prefixes.append(f"python3 transaction_time.py {cluster} {i}")

#prefix = f"python3 transaction_time.py {cluster} {node}"

wallet_number = random.randint(1, n) % 15

wallets = []

for i in range(wallet_number):
    wallets.append(f"wal{i}")

for prefix in prefixes: 
    for wallet in wallets:
        os.system(f"{prefix} -f set -w {wallet} -c {random.randint(100,10000)}")

functions = ["inc","trans","dec"]

commands = []
commands_for_closed_port = []

port_to_close = random.choice(ports)

process = os.popen(f'docker ps -aqf "name=validator-dgt-c1-{port_to_close}"').read()

os.system(f"docker container pause {process}")

for i in range(n):
    choice = random.choice(prefixes)
    command = create_command(functions,choice,wallets)
    commands.append(command)
    if prefixes.index(choice) != port_to_close - 1:
        commands_for_closed_port.append(command)
    
for i in range(n):
    os.system(commands[i])

for i in range(n):
    os.system(commands_for_closed_port[i])

os.system(f"docker container unpause {process}")

