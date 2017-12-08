"""
.. module:: TFIDFViewer

TFIDFViewer
******

:Description: TFIDFViewer

    Receives two paths of files to compare (the paths have to be the ones used when indexing the files)

:Authors:
    bejar

:Version: 

:Date:  05/07/2017
"""

from __future__ import print_function, division
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
    """
    Returns the term weights of a document

    :param file:
    :return:
    """

    # Get document terms frequency and overall terms document frequency
    file_tv, file_df = document_term_vector(client, index, file_id)

    max_freq = max([f for _, f in file_tv])

    dcount = doc_count(client, index)

    tfidfw = []
    for (t, w),(_, df) in zip(file_tv, file_df):
        idfi = np.log2((dcount/df)) # calculem el idfi com a log base 2 
                                    # (es el mateix que fer log base 10), numero total 
                                    # de documents (dcount) entre el nombre de documents 
                                    # que contenen aques terme
        tfdi = w/max_freq               # tfdi es el resultat de dividir el pes del terme entre 
                                        # la máxima ocurrència d'un document
        tfidfw.append((t,tfdi * idfi))  # Finalment es crea una llista de pairs amb el terme i el pes final
        
    return normalize(tfidfw)

def print_term_weigth_vector(twv):
    """
    Prints the term vector and the correspondig weights
    :param twv:
    :return:
    """
    print(twv, sep="\n")    # Imrpimeix els vectors amb salts de linea.


def normalize(tw):
    """
    Normalizes the weights in t so that they form a unit-length vector
    It is assumed that not all weights are 0
    :param tw:
    :return:
    """
    s = 0   # S tindrá la norma que utilitzarem després per dividir tot el vector
    s = sum(list(map(lambda x: x[1]**2, tw)))   # L'ús de funcions d'ordre superior es equivalent a:
                                                #    for (_,w) in tw:
                                                #       s += w*w

    r = np.sqrt(s) 
    norm = list(map(lambda pair: (pair[0],pair[1]/r),tw))   # Dividim tot el vector por la seva norma
                                                            # utilitzant una funció d'ordre superior com
                                                            # es el map.

    return norm


def cosine_similarity(tw1, tw2):
    """
    Computes the cosine similarity between two weight vectors, terms are alphabetically ordered
    :param tw1:
    :param tw2:
    :return:
    """

    # S'aplica el algorisme de fusió del mergesort
    index_tw1 = 0   # Els dos índex començen per 0.
    index_tw2 = 0
    sim = 0
    while index_tw1 < len(tw1) and index_tw2 < len(tw2):    # Mentres que hi hagi algún element per visitar
                                                            # en alguna de les dos llistes fem
        (t1,w1) = tw1[index_tw1]    # Agafem els pairs corresponents
        (t2,w2) = tw2[index_tw2]
        if t1 == t2:    # Si són el mateix terme, incrementem el sim i avançem els dos índex al mateix temps
            sim += w1 * w2
            index_tw1 = index_tw1 + 1
            index_tw2 = index_tw2 + 1
        elif t1 > t2:   # Resulta que el terme del primer vector és més gran, llavors incrementem el segon index
            index_tw2 = index_tw2 + 1
        else:   # L'inversa del cas anterior.
            index_tw1 = index_tw1 + 1
    
    return sim

def doc_count(client, index):
    """
    Returns the number of documents in an index

    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index to search')
    parser.add_argument('--files', default=None, required=True, nargs=2, help='Paths of the files to compare')
    parser.add_argument('--print', default=False, action='store_true', help='Print TFIDF vectors')

    args = parser.parse_args()


    index = args.index

    file1 = args.files[0]
    file2 = args.files[1]

    client = Elasticsearch()

    try:

        file1_id = search_file_by_path(client, index, file1)
        file2_id = search_file_by_path(client, index, file2)
        file1_tw = toTFIDF(client, index, file1_id)
        file2_tw = toTFIDF(client, index, file2_id)

        if args.print:
            print('TFIDF FILE %s' % file1)
            print_term_weigth_vector(file1_tw)
            print ('---------------------')
            print('TFIDF FILE %s' % file2)
            print_term_weigth_vector(file2_tw)
            print ('---------------------')

        print("Similarity = %3.5f" % cosine_similarity(file1_tw, file2_tw))

    except NotFoundError:
        print('Index %s does not exists' % index)

