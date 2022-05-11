import random
import os
import sys

def create_command(functions,prefix,wallets):
    new_wallets = random.shuffle([wallet for wallet in wallets])
    print(new_wallets)
    random_wallet_1 = new_wallets[0]
    random_wallet_2 = new_wallets[1]
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

prefix = f"python3 transaction_time.py {cluster} {node}"

wallet_number = random.randint(1, n)

wallets = []

for i in range(wallet_number):
    wallets.append(f"wal{i}")

for wallet in wallets:
    os.system(f"{prefix} -f set -w {wallet} -c {random.randint(100,10000)}")

functions = ["inc","trans","dec"]

for i in range(n):
    os.system(create_command(functions,prefix,wallets))


