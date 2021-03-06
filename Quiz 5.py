def perms(xs, low=0):
    if low + 1 >= len(xs):
        yield xs
    else:
        for p in perms(xs, low + 1):
            yield p
        for i in range(low + 1, len(xs)):
            xs[low], xs[i] = xs[i], xs[low]
            for p in perms(xs, low + 1):
                yield p
            xs[low], xs[i] = xs[i], xs[low]


print(sorted(perms({1,2})))
