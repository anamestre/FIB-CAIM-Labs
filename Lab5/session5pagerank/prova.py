p = ['a', 'b', 'c', 'd']

#new = dict([(key, a) for key in range(4) :  for a in p])

#d = {key:value for key, value in zip(keys, values)}

new = {key : a for key, a in zip(range(4) ,p)}

print new

