# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 15:31:13 2014

@author: bing
"""

from collections import defaultdict
import matplotlib.pyplot as plt
import csv, datetime
import os

os.chdir('/home/bing/Projects/dataiap')

#reader = csv.reader(open(sys.argv[1], 'r'))
#reader = csv.DictReader(open('datasets/donations_sampled.csv', 'r'))
reader = csv.DictReader(open('datasets/donations.csv', 'r'))
obamadonations = defaultdict(lambda:0)
mccaindonations = defaultdict(lambda:0)

for row in reader:
    name = row['cand_nm']
    datestr = row['contb_receipt_dt']
    amount = float(row['contb_receipt_amt'])
    date = datetime.datetime.strptime(datestr, '%d-%b-%y')
    
    if 'Obama' in name:
        obamadonations[date] += amount
    
    if 'McCain' in name:
        mccaindonations[date] += amount
    
# dictionaries
sorted_by_date_obama = sorted(obamadonations.items(), key=lambda (key, val):key)
sorted_by_date_mccain = sorted(mccaindonations.items(), key=lambda (key, val):key)
xs1,ys1 = zip(*sorted_by_date_obama)
xs2,ys2 = zip(*sorted_by_date_mccain)

fig = plt.figure(figsize=(15,7))
plt.plot(xs1, ys1, label='Obama\'s Donations')
plt.plot(xs2, ys2, label='McCain\'s Donations')
plt.legend(loc='upper center', ncol=4)
plt.savefig('datasets/test.png', format='png')