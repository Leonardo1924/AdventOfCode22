from functools import reduce

def SNAFUtoDec(num):
    return reduce(
        lambda r, v: (
            r[0] + ("=-012".index(v) - 2)* r[1],
            r[1] * 5,
        ),
        num[::-1],
        (0, 1),
    )[0]

def DecToSNAFU(num): # assume non-zero
    res = []
    while num > 0:
        res.append("012=-"[num % 5])
        num = (2 + num) // 5
    return ''.join(res[::-1])

print (DecToSNAFU(sum(SNAFUtoDec(l) for l in open("input.txt").read().splitlines())))