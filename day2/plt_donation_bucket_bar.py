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

#reader = csv.DictReader(open(sys.argv[1], 'r'))
#reader = csv.DictReader(open('datasets/donations/donations_sampled.csv', 'r'))
reader = csv.DictReader(open('datasets/donations/donations.csv', 'r'))
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
    
## dictionaries
#def sorted_by_date(donation_by_date):
#    return (sorted(donation_by_date, key=lambda (key, val):key))

filtered_donation_obama = filter(lambda (x,y): y>=-18000 and y<=19000, obamadonations.items())
filtered_donation_mccain = filter(lambda (x,y): y>=-22000 and y<=22000, mccaindonations.items())

def fill_donation_bucket(donations):
    donation_bucket = defaultdict(lambda:0)
    for row in donations:
        bucket = int(row[1]/100)
        donation_bucket[bucket] += 1
    return (donation_bucket)

donation_bucket_obama = fill_donation_bucket(filtered_donation_obama)
sorted_donation_bucket_obama = sorted(donation_bucket_obama.items(), key=lambda (key, value):key)
donation_bucket_mccain = fill_donation_bucket(filtered_donation_mccain)
sorted_donation_bucket_mccain = sorted(donation_bucket_mccain.items(), key=lambda (key, value):key)

xs1,ys1 = zip(*sorted_donation_bucket_obama)
#ys1 = [ys/100 for ys in ys1]
xs2,ys2 = zip(*sorted_donation_bucket_mccain)
#ys2 = [ys/100 for ys in ys2]


fig = plt.figure(figsize=(10,6))
#plt.plot(xs1, ys1, label='Obama\'s Donations')
#plt.plot(xs2, ys2, label='McCain\'s Donations')
#plt.legend(loc='upper center', ncol=4)
#plt.savefig('datasets/donation_by_date.png', format='png')
width = 0.25
subplot = fig.add_subplot(111)
subplot.bar(xs1, ys1,  color='blue', linewidth=0, label='Obama\'s Donations')
subplot.bar([x+width for x in xs2], ys2, color='green', linewidth=0, label='McCain\'s Donations')
subplot.legend(loc='upper left', ncol=1)
subplot.set_title('Donation Buckets')
subplot.set_xlabel('$100 Buckets')
plt.savefig('day2/donation_buckets.png', format='png')