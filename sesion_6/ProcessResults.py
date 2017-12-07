"""
.. module:: ProcessPrototype

ProcessPrototype
******

:Description: ProcessPrototype

    Prints the results of a clustering for a specific iteration

    It assumes that the results are written in two files assignmentsN.txt and prototypesN.txt.

    assignments.txt has lines with three elements "CLASSN documentid"
    prototypes.txt has the standard format

:Authors:
    bejar

:Version: 

:Date:  14/07/2017
"""

from __future__ import print_function, division

import argparse

__author__ = 'bejar'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prot', default='prototypes-final.txt', help='prototype file')
    parser.add_argument('--natt', default=5, type=int, help='Number of attributes to show')
    args = parser.parse_args()

    f = open(args.prot, 'r')

    for line in f:
        cl, attr = line.split(':')
        print(cl)
        latt = sorted([(float(at.split('+')[1]), at.split('+')[0]) for at in attr.split()], reverse=True)
        print(latt[:args.natt])

