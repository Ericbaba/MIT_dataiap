# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:54:48 2014

@author: bing
"""

import numpy
#from collections import defaultdict
import os
import matplotlib.pyplot as plt
import csv
from collections import Counter

os.chdir('/home/bing/Projects/dataiap')
#reader = csv.DictReader(open('datasets/donations/donations_sampled.csv', 'r'))
reader = csv.DictReader(open('datasets/donations/donations.csv', 'r'))

obamadonations = list()
mccaindonations = list()

for row in reader:
    name = row['cand_nm']
    #date = datetime.datetime.strptime(row['contb_receipt_dt'], '%d-%b-%y')
    amt = float(row['contb_receipt_amt'])
    
    if 'Obama' in name:
        obamadonations.append(amt)
    
    if 'McCain' in name:
        mccaindonations.append(amt)

bucket_size = 100
obamadonations_bucketed = map(lambda amt: amt - amt%bucket_size, obamadonations)
mccaindonations_bucketed = map(lambda amt: amt - amt%bucket_size, mccaindonations)

obamadonations_hist = Counter(obamadonations_bucketed)
mccaindonations_hist = Counter(mccaindonations_bucketed)

min_amt = min(min(obamadonations), min(mccaindonations))
max_amt = max(max(obamadonations), max(mccaindonations))

buckets = range(int(min_amt), int(max_amt), bucket_size)

# bar plot
fig = plt.figure(figsize=(30,10))
sub = fig.add_subplot(111)
width = 50
sub.bar(obamadonations_hist.keys(), obamadonations_hist.values(),
        color='b', width=width, label='Obama Donations')
sub.bar([amt+width for amt in mccaindonations_hist.keys()], mccaindonations_hist.values(), 
        color='r', width=width, label='McCain Donations')
sub.legend(loc='top left', ncol=1)
sub.set_xlim((-20000, 20000))
plt.savefig('day3/donations_histgrams.png', format='png')


# box plot
fig = plt.figure(figsize=(10,6))
sub = fig.add_subplot(111)
sub.boxplot([obamadonations, mccaindonations], whis=1)
sub.set_xticklabels(("Obama", "McCain"))
sub.set_ylim((-250, 1250))
sub.set_title('Obama Vs. McCain Donation')
plt.savefig('day3/donations_boxplot.png', format='png')


# significance test with Welch's T-Test
import sys
sys.path.append('day3/')
import welchttest
print "Welch's T-Test p-value:", welchttest.ttest(obamadonations, mccaindonations)