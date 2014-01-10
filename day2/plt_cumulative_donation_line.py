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
obamadonations = list()
mccaindonations = list()

for row in reader:
    name = row['cand_nm']
    amount = float(row['contb_receipt_amt'])
    
    if 'Obama' in name:
        obamadonations.append(amount)
    
    if 'McCain' in name:
        mccaindonations.append(amount)
    

obamadonations = sorted(obamadonations)
mccaindonations = sorted(mccaindonations)
#obamadonations = filter(lambda x: x>= -18000 and x<=19000, obamadonations)
#mccaindonations = filter(lambda x: x>= -22000 and x<=22000, mccaindonations)

bucket_size = 100
range_obama = range(int(min(obamadonations)/bucket_size), int(max(obamadonations)/bucket_size))
range_mccain = range(int(min(mccaindonations)/bucket_size), int(max(mccaindonations)/bucket_size))

def cumulated_donation_uptoamt(donations, donation_range):
    cumulated_donation = list()
    print('Total index number: %d' % len(donation_range)) 
    print('Now processing...')        
    for index in range(0, len(donation_range)):
        print('Index %d' % index)
        cumulated_donation_amt = sum(filter(lambda x: x<=donation_range[index]*bucket_size, donations))
        cumulated_donation.append(cumulated_donation_amt)
    return (cumulated_donation)

cumulated_donation_uptoamt_obama = cumulated_donation_uptoamt(obamadonations, range_obama)
cumulated_donation_uptoamt_mccain = cumulated_donation_uptoamt(mccaindonations, range_mccain)


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
#plt.savefig('day2/donation_cumulated_filtered.png', format='png')