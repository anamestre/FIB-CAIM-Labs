"""
.. module:: SearchIndexWeight

SearchIndex
*************

:Description: SearchIndexWeight

    Performs a AND query for a list of words (--query) in the documents of an index (--index)
    You can use word^number to change the importance of a word in the match

    --nhits changes the number of documents to retrieve

:Authors: bejar
    

:Version: 

:Created on: 04/07/2017 10:56 

"""
from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

import argparse

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.client import CatClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
import math
import functools
import operator
import argparse

import numpy as np

__author__ = 'bejar'

beta = 1
alpha = 1
R = 5
nrows = 4

def document_term_vector(client, index, id):
    """
    Returns the term vector of a document and its statistics a two sorted list of pairs (word, count)
    The first one is the frequency of the term in the document, the second one is the number of documents
    that contain the term

    :param client:
    :param index:
    :param id:
    :return:
    """
    termvector = client.termvectors(index=index, doc_type='document', id=id, fields=['text'],
                                    positions=False, term_statistics=True)

    file_td = {}
    file_df = {}

    if 'text' in termvector['term_vectors']:
        for t in termvector['term_vectors']['text']['terms']:
            file_td[t] = termvector['term_vectors']['text']['terms'][t]['term_freq']
            file_df[t] = termvector['term_vectors']['text']['terms'][t]['doc_freq']
    return sorted(file_td.items()), sorted(file_df.items())


def toTFIDF(client, index, file_id):
    # Get document terms frequency and overall terms document frequency
    file_tv, file_df = document_term_vector(client, index, file_id)

    max_freq = max([f for _, f in file_tv])

    dcount = doc_count(client, index)

    tfidfw = {}
    for (t, w),(_, df) in zip(file_tv, file_df):
        idfi = np.log2((dcount/df))
        tfdi = w/max_freq               
                                      
        #tfidfw.append((t,tfdi * idfi))  
        tfidfw[t] = tfdi * idfi
         
    return normalize(tfidfw)



def normalize(d):
    s = sum(d.values())
    r = np.sqrt(s)
    norm = {t: d.get(t, 0)/r for t in set(d)}
    return norm


def search_file_by_path(client, index, path):
    """
    Search for a file using its path

    :param path:
    :return:
    """
    s = Search(using=client, index=index)
    q = Q('match', path=path)  # exact search in the path field
    s = s.query(q)
    result = s.execute()

    lfiles = [r for r in result]
    if len(lfiles) == 0:
        raise NameError('File [%s] not found'%path)
    else:
        return lfiles[0].meta.id

def doc_count(client, index):
    """
    Returns the number of documents in an index

    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])

def queryToDict(query):
    query_dict = {}
    for elem in query:
        if '^' in elem:
            key, value = elem.split('^')
            value = float(value)
        else:
            key = elem
            value = 1.0
        query_dict[key] = value
        
    return normalize(query_dict)

def dictToquery(di):
    query = []
    for elem in di:
        q = elem + '^' + str(di[elem])
        query.append(q)
    return query

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index to search')
    parser.add_argument('--nhits', default=10, type=int, help='Number of hits to return')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')

    args = parser.parse_args()

    index = args.index
    query = args.query
    
    nhits = args.nhits

    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)
        
        if query is not None:
            for i in range(0, nrows):
                # coses random d'Elasticsearch
                q = Q('query_string',query=query[0])
                for i in range(1, len(query)):
                    q &= Q('query_string',query=query[i])
                s = s.query(q)
                response = s[0:nhits].execute()
                
                print("QUERY:")
                print(query)
                
                query_dict = queryToDict(query)
                
                sumDocs = {}

                # calcul dels documents
                #print( "------------------- CALULEM ELS DOCUMENTS -------------")
                for r in response:  # only returns a specific number of results
                    file_tw = toTFIDF(client, index, r.meta.id) # tf-idf
                    sumDocs = {t: sumDocs.get(t, 0) + file_tw.get(t, 0) for t in set(sumDocs) | set(file_tw)} # sumem els valors de cada document
                    print('ID= %s SCORE=%s' % (r.meta.id,  r.meta.score))
                    print('PATH= %s' % r.path)
                    print('TEXT: %s' % r.text[:50])
                    print('-----------------------------------------------------------------')                
                
                sumDocs = {t: sumDocs.get(t,0)*beta/nhits for t in set(sumDocs)} # Beta * vector de documents / K
                oldQuery = {t: query_dict.get(t,0)*alpha for t in set(query_dict)} # Alpha * query
                query2 = {}
                query2 = {t: sumDocs.get(t, 0) + oldQuery.get(t, 0) for t in set(sumDocs) | set(oldQuery)} # alpha * query + beta * vector documents / K
                query2 = sorted(query2.items(), key=operator.itemgetter(1), reverse = True) # ordenem per valor, es converteix en tuples
                query2 = query2[:R] #agafem els R mes relevants
                query_dict = dict((t, val) for (t, val) in query2) #ho tornem a transformar en un diccionari
                query = dictToquery(normalize(query_dict))
                
              

        else:
            print('No query parameters passed')

        print ('%d Documents'% response.hits.total)

    except NotFoundError:
        print('Index %s does not exists' % index)

