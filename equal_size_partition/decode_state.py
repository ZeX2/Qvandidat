def decode_state(state, S):
    (a, b) = ([], [])
    partition_difference = 0

    # It is probably possible to this in some nice pythonic way
    for si,s in enumerate(state):
        if s == 1: a.append(S[si])
        else: b.append(S[si])

    return (a, b)
