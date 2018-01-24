#!/usr/bin/env python
"""
Simple module implementing LSH
"""

from __future__ import print_function, division
import pylab
import numpy
import sys
import argparse
import time

__version__ = '0.2'
__author__  = 'marias@cs.upc.edu'

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print ('%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts))
        return result

    return timed


class lsh(object):
    """
    implements lsh for digits database in file 'images.npy'
    """  
    
    def __init__(self, k, m):
        """ k is nr. of bits to hash and m is reapeats """
        # data is numpy ndarray with images
        self.data = numpy.load('images.npy')
        self.k = k
        self.m = m

        # determine length of bit representation of images
        # use conversion from natural numbers to unary code for each pixel,
        # so length of each image is imlen = pixels * maxval
        self.pixels = 64
        self.maxval = 16
        self.imlen = self.pixels * self.maxval

        # need to select k random hash functions for each repeat
        # will place these into an m x k numpy array
        numpy.random.seed(12345)
        self.hashbits = numpy.random.randint(self.imlen, size=(m, k))

        # the following stores the hashed images
        # in a python list of m dictionaries (one for each repeat)
        self.hashes = [dict() for _ in range(self.m)]

        # now, fill it out
        self.hash_all_images()

        return
    

    def hash_all_images(self):
        """ go through all images and store them in hash table(s) """
        # Achtung!
        # Only hashing the first 1500 images, the rest are used for testing
        for idx, im in enumerate(self.data[:1500]):
            for i in range(self.m):
                str = self.hashcode(im, i)

                # store it into the dictionary.. 
                # (well, the index not the whole array!)
                if str not in self.hashes[i]:
                    self.hashes[i][str] = []
                self.hashes[i][str].append(idx)
        return


    def hashcode(self, im, i):
        """ get the i'th hash code of image im (0 <= i < m)"""
        pixels = im.flatten()
        row = self.hashbits[i]
        str = ""
        for x in row:
            # get bit corresponding to x from image..
            pix = int(x) // int(self.maxval)
            num = x % self.maxval
            if (num <= pixels[pix]):
                str += '1'
            else:
                str += '0'
        return str


    def candidates(self, im):
        """ given image im, return matching candidates (well, the indices) """
        res = set()
        for i in range(self.m):
            code = self.hashcode(im, i)
            if code in self.hashes[i]:
                res.update(self.hashes[i][code])
        return res


def distance(image1, image2):
    dist = abs(image2 - image1)  # Això retorna la matriu diferència en valor absolut
    return sum(map(sum, dist))  # Això retorna la suma de tots els valors de la matriu


def bruteForceSearch(me, index):
    img = me.data[index]
    minDist = distance(img, me.data[0])
    minIndex = 0
    for i in range(1,1499):
        dist = distance(img, me.data[i])
        if dist < minDist:
            minDist = dist
            minIndex = i
            
    return (minDist, minIndex)            
    
    
def search(me, index, candidates):
    if len(candidates) == 0:
        return (-1, -1)
    
    img = me.data[index]
    minDist = -1
    minIndex = 0
    
    for cand in candidates:
        dist =  distance(img, me.data[cand])
        if minDist == -1:
            minDist = dist
            minIndex = cand
        if dist < minDist:
            minDist = dist
            minIndex = cand
    
    return minDist, minIndex
       

#############################################

@timeit
def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', default=20, type=int)
    parser.add_argument('-m', default=5, type=int)
    args = parser.parse_args()    

    print ("Running lsh.py with parameters k =", args.k, "and m =", args.m)
    me = lsh(args.k, args.m)
    
    # show candidate neighbors for first 10 test images
    for r in range(1500,1510):
        im = me.data[r]
        cands = me.candidates(im)
        print ("There are %4d candidates for image %4d" % (len(cands), r)) 
        
        dist, indexIm = bruteForceSearch(me, r)
        print ("Brute-force search: ")
        print ("For image %4d , the nearest image is %4d with a distance of%4d" % (r, indexIm, dist ))
        
        dist, indexIm = search(me, r, cands)
        print ("Hashing search: ")
        if dist == -1:
            print ("There isn't a nearest image for %4d" %(r))
        else:
            print ("For image %4d , the nearest image is %4d with a distance of%4d" % (r, indexIm, dist ))
        print()
        
    return

if __name__ == "__main__":
  sys.exit(main())
