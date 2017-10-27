"""
.. module:: SearchIndex

SearchIndex
*************

:Description: SearchIndex

    Searches for a specific word in the field 'text' (--text)  or performs a query (--query) (LUCENE syntax,
    between single quotes) in the documents of an index (--index)

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

__author__ = 'bejar'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index to search')
    parser.add_argument('--text', default=None, help='text to search')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='Lucene query')

    args = parser.parse_args()

    text = args.text
    index = args.index
    if args.query:
        query = ' '.join(args.query)

    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)


        if text is not None:
            q = Q('multi_match', query=text, fields=['text'])
            s = s.query(q)
            s = s.highlight('text', fragment_size=10)
            response = s.execute()

            for r in s.scan(): # scan allows to retrieve all matches
                print('ID= %s PATH=%s' % (r.meta.id, r.path))
                for j, fragment in enumerate(r.meta.highlight.text):
                    print(' ->  TXT=%s' % fragment)
        elif query is not None:
            q = Q('query_string',query=query)
            s = s.query(q)
            response = s.execute()

            for r in s.scan(): # scan allows to retrieve all matches
               print('ID= %s TXT=%s PATH=%s' % (r.meta.id, r.text[0:10], r.path))
        else:
            print('No query parameters passed')

        print ('%d Documents'% response.hits.total)
    except NotFoundError:
        print('Index %s does not exists' % index)

