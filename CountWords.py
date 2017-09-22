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

import argparse


def checkWord(word):
    for c in word:
        if c < 'A' or ((c > 'Z') and (c < 'a')) or c > 'z':
            return False
    return True


__author__ = 'bejar'

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
        for pal, cnt in sorted(lpal, key=lambda x: x[0 if args.alpha else 1]):
            if checkWord(pal):
                print('%d, %s' % (cnt, pal))
                cont += 1
        print('%s Words' % cont)
    except NotFoundError:
        print('Index %s does not exists' % index)
