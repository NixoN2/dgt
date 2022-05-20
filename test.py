import os
from datetime import date

today = date.today()

with open('results.txt', 'w') as f:
    text = ""
    time = 0
    for i in range(10):
        content = os.popen("python test2.py")
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
            
        