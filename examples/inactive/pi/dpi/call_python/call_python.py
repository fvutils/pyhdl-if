
def countones(v):
    ones = 0
    
    while v:
        if v & 1:
            ones += 1
        v >>= 1

    return ones

