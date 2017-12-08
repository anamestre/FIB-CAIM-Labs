import numpy as np


'''
def normalize(d):
    s = 0
    s = sum(dict(map(lambda t: (t, d[t]**2), d)))
    r = np.sqrt(s)
    norm = dict(map(lambda t: (t,d[t]/r), d))
    return norm
'''

def normalize(d):
    s = 0
    s = sum(d.values())
    r = np.sqrt(s)
    norm = {t: d.get(t, 0)/r for t in set(d)}
    return norm


holi = {'primer':1, 'segon':1, 'tercer':2}
print (normalize2(holi))
