with open("day3/input.txt") as f:
    lines = f.readlines()

lowerAlphabet = "abcdefghijklmnopqrstuvwxyz"
upperAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

priority_values = {}
p = 1
for c in  lowerAlphabet:
    priority_values[c] = p
    p += 1

for c in  upperAlphabet:
    priority_values[c] = p
    p += 1


total = 0
for i in range(0,len(lines),3):
    first = set(list(lines[i].rstrip()))
    second = set(list(lines[i+1].rstrip()))
    third = set(list(lines[i+2].rstrip()))
    inter = first & second & third
    total += priority_values[inter.pop()]

print(total)

