p = ['a', 'b', 'c', 'd']

new = dict([(key, a) for key in range(4) for a in p])

print new

