# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:11:27 2014

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
def sorted_by_amount(donations):
    return (sorted(donations, key=lambda (key, value):value))

sorted_by_amount_obama = sorted_by_amount(obamadonations.items())
date1, sorted_donation_obama = zip(*sorted_by_amount_obama)
sorted_by_amount_mccain = sorted_by_amount(mccaindonations.items())
date2, sorted_donation_mccain = zip(*sorted_by_amount_mccain)
#filtered_donation_obama = filter(lambda (x,y): y>=-18000 and y<=19000, obamadonations.items())
#filtered_donation_mccain = filter(lambda (x,y): y>=-22000 and y<=22000, mccaindonations.items())

bucket_size = 1000
range_obama = range(int(min(sorted_donation_obama)/bucket_size), int(max(sorted_donation_obama)/bucket_size))
range_mccain = range(int(min(sorted_donation_mccain)/bucket_size), int(max(sorted_donation_mccain)/bucket_size))

def cumulated_donation_uptoamt(donations, donation_range):
    cumulated_donation = list()
    for index in range(0, len(donation_range)):
        cumulated_donation_amt = sum(filter(lambda x: x<=donation_range[index]*1000, donations))
        cumulated_donation.append(cumulated_donation_amt)
    return (cumulated_donation)

cumulated_donation_uptoamt_obama = cumulated_donation_uptoamt(sorted_donation_obama, range_obama)
cumulated_donation_uptoamt_mccain = cumulated_donation_uptoamt(sorted_donation_mccain, range_mccain)


xs1,ys1 = [amt*bucket_size for amt in range_obama], cumulated_donation_uptoamt_obama
xs2,ys2 = [amt*bucket_size for amt in range_mccain], cumulated_donation_uptoamt_mccain

fig = plt.figure(figsize=(10,6))
#plt.plot(xs1, ys1, label='Obama\'s Donations')
#plt.plot(xs2, ys2, label='McCain\'s Donations')
#plt.legend(loc='upper center', ncol=4)
#plt.savefig('datasets/donation_by_date.png', format='png')
width = 0.25
subplot = fig.add_subplot(111)
subplot.plot(xs1, ys1,  color='blue', label='Obama\'s Donations')
subplot.plot([x+width for x in xs2], ys2, color='green', label='McCain\'s Donations')
subplot.legend(loc='upper left', ncol=1)
subplot.set_title('Donation Cumulated-to-amount')
subplot.set_xlabel('Donation Amount')
plt.savefig('day2/donation_cumulated.png', format='png')