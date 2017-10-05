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
# k = 36, Beta = 0

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch.exceptions import NotFoundError

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import argparse

def func(N, k, beta):
    return k*(N**beta)

def heap_linear(numArray, freqArray, fitArray):
    plt.plot(numArray, freqArray, 'b-', label='Actual values')
    plt.plot(numArray, fitArray,'r-',label='Heap\'s law')
    plt.legend()
    plt.xlabel('x = Number of total words')
    plt.ylabel('y = Number of different words')
    plt.show()
    
def heap_log_plot(logNumArray,logFreqArray,logFitArray):
    plt.plot(logNumArray, logFreqArray, 'b-', label='Log of actual values')
    plt.plot(logNumArray, logFitArray,'r-',label='Log of Heap\'s law')
    plt.legend()
    plt.xlabel('x = Number of total words')
    plt.ylabel('y = Number of different words')
    plt.show()    

def heap(dif, total):
     popt, pcov = curve_fit(func, total, dif)
     print('Heap\'s optimal parameters:')
     print('k = %d, Beta = %d' % (popt[0],popt[1]))
     fitArray = []
     logFitArray = []
     for num in total:
        fitArray.append(func(num,*popt))
        logFitArray.append(np.log(func(num,*popt)))
    
     #Choose plot here
     heap_linear(total, dif, fitArray)
     heap_log_plot(np.log(total), np.log(dif), logFitArray)
     
    
    

#Filters the strings containing non-letter characters
def checkWord(word):
    for c in word:
		#Ugly 'if' statement
        if c < 'A' or ((c > 'Z') and (c < 'a')) or ((c > 'z') and (c < 128)) or ((c > 144) and  (c < 147)) or ((c > 154) and (c < 160)) or ((c > 165) and (c < 181)) or ((c > 183) and (c < 224)) or (c == 225) or ((c > 229) and (c < 233)) or ((c > 237) and (c < 255)):
            return False
    return True


__author__ = 'bejar'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=False, help='Index to search')
    parser.add_argument('--alpha', action='store_true', default=False, help='Sort words alphabetically')
    args = parser.parse_args()

    index = ["news", "news1", "news2", "news3", "news4", "news5","news6", "news7", "news8"]

    try:
        client = Elasticsearch()
        
        
        differentWords = []
        totalWords = []
        
        for i in index:
            voc = {}
            sc = scan(client, index=i, doc_type='document', query={"query" : {"match_all": {}}})
            
            for s in sc:
                tv = client.termvectors(index=i, doc_type='document', id=s['_id'], fields=['text'])
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
            wordFreqArray = reversed(sorted(lpal, key=lambda x: x[0 if args.alpha else 1]))
            totalCont = 0
            
            
            
            for pal, cnt in wordFreqArray:
                if checkWord(pal):
                    # print('%d. %d, %s' % (cont, cnt, pal))
                    cont += 1
                    totalCont += cnt
            #print('%s Different words' % cont) # Cont = num de diferentes palabras
            #print('%s Total words' % totalCont)
            differentWords.append(cont)
            totalWords.append(totalCont)
            
            
        heap(differentWords, totalWords)
        
    except NotFoundError:
        print('Index %s does not exists' % index)
