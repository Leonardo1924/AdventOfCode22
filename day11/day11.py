import math

def solve(rounds):
    items = [[[int(x) for x in (data[y][18:]).split(", ")] for y in range(1, len(data), 7)]][0]
    n = [0] * len(divs)
    for _ in range(rounds):
        for i in range(len(n)):
            for j in range(0, len(items[i])):
                x = items[i][j]
                if ops[i] == "* old":
                    x *= x
                else:
                    op, val = ops[i].split()
                    x = x + int(val) if op == "+" else x * int(val)
                x = x // 3 if rounds == 20 else x % M
                if x % divs[i] == 0:
                    items[friends[i][0]].append(x)
                else:
                    items[friends[i][1]].append(x)
                n[i] += 1
            items[i] = []
    return max(n) * sorted(n)[-2]

data = open("input.txt").read().strip().split("\n")
ops = [(" ".join(data[x].split("= ")[-1].split()[1:])) for x in range(2, len(data), 7)]
divs = [int(data[x][21:]) for x in range(3, len(data), 7)]
friends = [[int(data[x].split()[-1]), int(data[x + 1].split()[-1])] for x in range(4, len(data), 7)]
M = math.prod(divs)
print(f"Part 1: {solve(20)}")
print(f"Part 2: {solve(10000)}")