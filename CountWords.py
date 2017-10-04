"""
.. module:: CountWords
CountWords
*************
:Description: CountWords
    Generates a list with the counts and the words in the 'text' field of the documents in an index
:Authors: bejar
    
:Version: 
:Created on: 04/07/2017 11:58 
"""
from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch.exceptions import NotFoundError

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import argparse


def func(x, b, c):
    return c/(x+b)

#Filters the strings containing non-letter characters
def checkWord(word):
    for c in word:
		#Ugly 'if' statement
        if c < 'A' or ((c > 'Z') and (c < 'a')) or ((c > 'z') and (c < 128)) or ((c > 144) and  (c < 147)) or ((c > 154) and (c < 160)) or ((c > 165) and (c < 181)) or ((c > 183) and (c < 224)) or (c == 225) or ((c > 229) and (c < 233)) or ((c > 237) and (c < 255)):
            return False
    return True


__author__ = 'bejar & mestre'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index to search')
    parser.add_argument('--alpha', action='store_true', default=False, help='Sort words alphabetically')
    args = parser.parse_args()

    index = args.index

    try:
        client = Elasticsearch()
        voc = {}
        sc = scan(client, index=index, doc_type='document', query={"query" : {"match_all": {}}})
        for s in sc:
            tv = client.termvectors(index=index, doc_type='document', id=s['_id'], fields=['text'])
            if 'text' in tv['term_vectors']:
                for t in tv['term_vectors']['text']['terms']:
                    if t in voc:
                        voc[t] += tv['term_vectors']['text']['terms'][t]['term_freq']
                    else:
                        voc[t] = tv['term_vectors']['text']['terms'][t]['term_freq']
        lpal = []

        for v in voc:
            lpal.append((v.encode("utf8", "ignore"), voc[v]))
        
        cont = 0
        wordCount = 500
        wordFreqArray = reversed(sorted(lpal, key=lambda x: x[0 if args.alpha else 1]))
        
        freqArray = []
        logFreqArray = []
        numArray = range(1,wordCount+1)
        logNumArray = np.log(numArray)
    
        
        for pal, cnt in wordFreqArray:
            if checkWord(pal):
                print('%d. %d, %s' % (cont, cnt, pal))
                cont += 1
                freqArray.append(cnt)
                logFreqArray.append(np.log(cnt))
            if cont >= wordCount:
                break
        print('%s Words' % cont)
        
        popt, pcov = curve_fit(func,numArray,freqArray)
        print(popt)
        
        fitArray = []
        for num in numArray:
            fitArray.append(np.log(func(num,*popt)))
        
        plt.plot(logNumArray, logFreqArray, 'b-', label='Log of actual frequencies')
        plt.plot(logNumArray, fitArray,'r-',label='Log of Zipf\'s fit')
        plt.legend()
        plt.xlabel('x = Log of the rank of the word (sorted by most frequent)')
        plt.ylabel('y = Log of the frequency of the word')
        plt.show()
    except NotFoundError:
        print('Index %s does not exists' % index)
