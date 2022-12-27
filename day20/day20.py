inp = [int(x) for x in open("input.txt","r").read().splitlines()]
N = len(inp)


def jump(q, n):
    for _ in range(n):
        q = q["n"]
    return q


def run(m, iterations):
    Q = [{"v": x} for x in inp]
    for lh, rh in zip(Q, Q[1:]):
        lh["n"] = rh
    Q[-1]["n"] = Q[0]
    for i in range(iterations):
        q = Q[i % N]
        v = m * q["v"] % (N - 1)
        if v:
            after = jump(q, v % (N - 1))
            prev = jump(q, N - 1)
            prev["n"], q["n"], after["n"] = q["n"], after["n"], q
    return sum(
        jump(next(q for q in Q if q["v"] == 0), i % N)["v"] * m
        for i in (1000, 2000, 3000)
    )

print(run(1, N), run(811589153, 10 * N))
