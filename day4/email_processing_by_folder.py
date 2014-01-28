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
    #ex7, stop at the first ">"
    try:
        terms = terms[:terms.index('>')]
    except:
        pass
    terms = filter(lambda term: len(term) > 3, terms)
    from email_util import STOPWORDS
    terms = filter(lambda term: term not in STOPWORDS, terms)
    #matched_terms = list()    
    #filter with regular expression
    import re    
    pattern = r"^[a-zA-Z]+[a-zA-Z\-\']*[a-zA-Z]+$"

    terms = filter(lambda term: re.match(pattern, term), terms)    
    return (terms)

# calculate term frequency
folder_tf = defaultdict(Counter)


for e in EmailWalker('../datasets/emails/lay-k'):
    #terms_in_email = e['text'].split()
    terms_in_email = get_terms(e['text'])
    folder_tf[e['folder']].update(terms_in_email)

#ex8, normalizing weights
def cal_i2norm(vect):
    vect = [item*item for item in vect]
    return (math.sqrt(sum(vect)))

for key in folder_tf.keys():
    vect = [v for (k, v) in folder_tf[key].items()]    
    vect_i2norm = cal_i2norm(vect)
    i2nrom_value = dict([(k, v/vect_i2norm) for (k, v) in folder_tf[key].items()])
    folder_tf[key] = i2nrom_value


# calculate inverse document frequency
terms_per_folder = defaultdict(set)
nemails = 0
for e in EmailWalker('../datasets/emails/lay-k'):
    #terms_in_email = e['text'].split() # split the email text using whitespaces
    terms_in_email = get_terms(e['text'])
    # this collects all of the terms in each folder
    terms_per_folder[e['folder']].update(terms_in_email)
    
allterms = Counter()
for folder, terms in terms_per_folder.items():
    # this will increment the counter value for each term in `terms`
    allterms.update(terms)
    
idfs = {}
nfolders = len(terms_per_folder)  # the number of keys should be the number of folders    
for term, count in allterms.iteritems():
    idfs[term] = math.log( nfolders / (1.0 + count) )
    
# calculate tf-idf for each folder
tfidfs = {} # key is folder name, value is a list of (term, tfidf score) pairs
for folder, tfs in folder_tf.items():
    tfidfs[folder] = map(lambda (k, v): (k, v*idfs[k]), tfs.items())
    

# print the top terms
for folder, terms in tfidfs.items():
    print folder
    sorted_by_count_top20 = sorted(terms, key=lambda (k, v):v, reverse=True)[:20]
    for pair in sorted_by_count_top20:
        print '\t', pair
        

# calculate folder cosine similarity
def cal_similarity(folder1_tfidfs, folder2_tfidfs):
    folder1_score = dict(folder1_tfidfs)
    folder2_score = dict(folder2_tfidfs)
    
    numerator = 0.0
    for key, valus in folder1_score.items():
        dotscore = folder1_score[key]*folder2_score.get(key, 0.0)
        numerator += dotscore
    
    folder1_norm = math.sqrt(sum([score**2 for score in folder1_score.values()]))
    folder2_norm = math.sqrt(sum([score**2 for score in folder2_score.values()]))
    denominator = folder1_norm * folder2_norm + 1.0
    
    similarity = numerator/denominator
    return (similarity)

def sort_by_count(key_value, top_n):
    sorted_by_count_topn = sorted(key_value, key=lambda (k, v):v, reverse=True)[:top_n]
    return (sorted_by_count_topn)

num_of_folders = len(tfidfs.keys())
folder_similarity = dict()
for i in range(0, num_of_folders-1):
    for j in range(i+1, num_of_folders):
        folder1 = tfidfs.keys()[i]
        folder2 = tfidfs.keys()[j]
        similarity = cal_similarity(sort_by_count(tfidfs[folder1], 100), sort_by_count(tfidfs[folder2], 100))
        key = '%s and %s' % (folder1, folder2)        
        folder_similarity[key] = similarity        
        #print('The similarity between folder [%s] and [%s] is %.2f' % (folder1, folder2, similarity))
sorted_similarity = sort_by_count(folder_similarity.items(), len(folder_similarity))
print('The sorted folder similarities are:')
for k,v in sorted_similarity:
    print('%s: %s' % (k, v))