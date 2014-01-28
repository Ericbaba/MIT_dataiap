# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 23:32:10 2014

@author: bing
"""

#import re
#import sys
#from collections import defaultdict
#from mrjob.protocol import JSONValueProtocol
#from term_tools import get_terms
#import json

#file = open('../datasets/emails/lay-k.json')
#words = defaultdict(lambda: 0)
#for line in input:
#    email = JSONValueProtocol.read(line)[1]
#    for term in get_terms(email['text']):
#        words[term] += 1
#
#for word, count in words.items():
#    print word, count


import sys
from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from term_tools import get_terms

class MRWordCount(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, email):
        for term in get_terms(email['text']):
            yield term, 1

    def reducer(self, term, occurrences):
        yield None, {'term': term, 'count': sum(occurrences)}

if __name__ == '__main__':
        MRWordCount.run()