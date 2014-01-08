# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 22:04:26 2014

@author: bing
"""

from collections import defaultdict
import matplotlib.pyplot as plt
import csv, datetime
import os

os.chdir('/home/bing/Projects/dataiap')

#reader = csv.DictReader(open(sys.argv[1], 'r'))
reader = csv.DictReader(open('datasets/donations_sampled.csv', 'r'))
#reader = csv.DictReader(open('datasets/donations.csv', 'r'))
obamadonations = defaultdict(lambda:0)
mccaindonations = defaultdict(lambda:0)

for row in reader:
    name = row['cand_nm']
    datestr = row['contb_receipt_dt']
    amount = float(row['contb_receipt_amt'])
    receipt_desc = row['receipt_desc'].lower()
    date = datetime.datetime.strptime(datestr, '%d-%b-%y')
    
    if 'Obama' in name and 'reattribution' in receipt_desc:
        obamadonations[date] += amount
    
    if 'McCain' in name and 'reattribution' in receipt_desc:
        mccaindonations[date] += amount
    
# function to sort dict by date
def sorted_by_date(donation_by_date):
    return (sorted(donation_by_date, key=lambda (key, val):key))
    
# function to calculate cumulated donations
def calculate_cumulated_donations(sorted_donations):
    accumulated_donations = [sorted_donations[0]]
    for index in range(1, len(sorted_donations)):
        accumulated_to_date = accumulated_donations[-1][1] + sorted_donations[index][1]
        accumulated_donations.append((sorted_donations[index][0], accumulated_to_date))
    return (accumulated_donations)
        

sorted_by_date_obama = sorted_by_date(obamadonations.items())
sorted_by_date_mccain = sorted_by_date(mccaindonations.items())
    
accumulated_obama = calculate_cumulated_donations(sorted_by_date_obama)
accumulated_mccain = calculate_cumulated_donations(sorted_by_date_mccain)

xs1,ys1 = zip(*accumulated_obama)
xs2,ys2 = zip(*accumulated_mccain)

fig = plt.figure(figsize=(15,7))
plt.plot(xs1, ys1, label='Obama\'s Donations')
plt.plot(xs2, ys2, label='McCain\'s Donations')
plt.legend(loc='upper center', ncol=4)
plt.savefig('datasets/donation_filtered.png', format='png')