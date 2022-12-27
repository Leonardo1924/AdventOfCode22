INP = {tuple([int(x) for x in l.split(",")]) for l in open("input.txt","r")}
I = (0, 1, 2)
BL = tuple(min(t[i] - 1 for t in INP) for i in I)
TR = tuple(max(t[i] + 1 for t in INP) for i in I)
D = [(-1, 0, 0), (0, -1, 0), (0, 0, -1), (0, 0, 1), (0, 1, 0), (1, 0, 0)]
add = lambda lh, rh: tuple(lh[i] + rh[i] for i in I)
incube = lambda t: all(BL[i] <= t[i] <= TR[i] for i in I)

part1 = sum(1 for d in D for t in INP if add(t, d) not in INP)
visited = set()
part2 = 0
water = [TR]
for w in water:
    if w in INP:
        part2 += 1
        continue
    if w in visited:
        continue
    visited.add(w)
    water.extend([add(w, d) for d in D if incube(w)])

print(part1, part2)
