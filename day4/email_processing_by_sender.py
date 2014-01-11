# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 14:57:05 2014

@author: bing
"""
    
import sys, math
sys.path.append('../resources/util')
from email_util import *
from collections import Counter, defaultdict

def get_terms(terms):
    terms = terms.lower().split()
    terms = filter(lambda term: len(term) > 3, terms)
    from email_util import STOPWORDS
    terms = filter(lambda term: term not in STOPWORDS, terms)

    #filter with regular expression
    import re    
    pattern = r"^[a-zA-Z]+[a-zA-Z\-\']*[a-zA-Z]+$"
    terms = filter(lambda term: re.match(pattern, term), terms)    
    return (terms)

# calculate term frequency
sender_tf = defaultdict(Counter)

for e in EmailWalker('../datasets/emails/lay-k'):
    #terms_in_email = e['text'].split()
    terms_in_email = get_terms(e['text'])
    sender_tf[e['sender']].update(terms_in_email)


# calculate inverse document frequency
terms_per_sender = defaultdict(set)
nemails = 0
for e in EmailWalker('../datasets/emails/lay-k'):
    #terms_in_email = e['text'].split() # split the email text using whitespaces
    terms_in_email = get_terms(e['text'])
    # this collects all of the terms for each sender
    terms_per_sender[e['sender']].update(terms_in_email)
    
allterms = Counter()
for sender, terms in terms_per_sender.items():
    # this will increment the counter value for each term in `terms`
    allterms.update(terms)
    
idfs = {}
nsenders = len(terms_per_sender)  # the number of keys should be the number of folders    
for term, count in allterms.iteritems():
    idfs[term] = math.log( nsenders / (1.0 + count) )
    
# calculate tf-idf for each folder
tfidfs = {} # key is folder name, value is a list of (term, tfidf score) pairs
for sender, tfs in sender_tf.items():
    tfidfs[sender] = map(lambda (k, v): (k, v*idfs[k]), tfs.items())
    

# print the top terms
for sender, terms in tfidfs.items():
    print sender
    sorted_by_count_top20 = sorted(terms, key=lambda (k, v):v, reverse=True)[:20]
    for pair in sorted_by_count_top20:
        print '\t', pair