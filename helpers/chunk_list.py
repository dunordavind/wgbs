def chunk_list(l, n):
    out = []
    for i in range(0, len(l), n):
        out.append(l[i:i+n])
    return out
