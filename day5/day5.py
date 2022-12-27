import re


dat = re.compile(r'\[(\w)\]')
com = re.compile(r'move (\d+) from (\d+) to (\d+)')
mem = [[] for i in range(9)]

with open('day5/input.txt', 'r') as f:
    data = f.readlines()

for line in data:

    for match in dat.finditer(line):
            mem[match.start(1)//4].insert(0, match.group(1))
    op = com.findall(line)
    if op != []:
            op = op[0]
            n = int(op[0])
            source = int(op[1])
            mem[int(op[2])-1] += mem[source-1][-n:]
            mem[source-1][-n:] = []

out = ""
for i in range(9):
    out += mem[i].pop()

print(out)