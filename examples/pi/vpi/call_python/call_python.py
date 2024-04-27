
def countones(v):
    ones = 0
    print("countones: v=%d" % v, flush=True)
    
    while v:
        if v & 1:
            ones += 1
        v >>= 1

    return ones

