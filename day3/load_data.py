# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 21:10:35 2014

@author: bing
"""

import os
import csv
import numpy

os.chdir('/home/bing/Projects/dataiap/day3')

## Load Data
# Read & Filter data from CSV file
def read_csv(filename, selected_columns, check_reliable):
    reader = csv.DictReader(open(filename, 'r'))
    rows = {}         
    for row in reader:
        if check_reliable and row['Unreliable'] == 'x':
            continue
        if row['County'] == "":
            continue
        
        rname = "%s_%s" % (row['State'], row['County'])        
        try:
            rows[rname] = [float(row[col]) for col in selected_columns]
        except:
            pass
        
    return rows


# 'Join' the two readings
def get_array(ypll_cols, add_measures_cols):
    ypll = read_csv('../datasets/county_health_rankings/ypll.csv', ypll_cols, True)
    measures = read_csv('../datasets/county_health_rankings/additional_measures_cleaned.csv', add_measures_cols, False)
    
    ypll_list = []
    measures_list = []
    for key, value in ypll.iteritems():
        if key in measures.keys():
            ypll_list.append(value[0])
            measures_list.append(measures[key])
    return (numpy.array(ypll_list), numpy.array(measures_list))
            
            
ypll_cols = ["YPLL Rate"]
add_measures_cols = ["Population", "< 18", "65 and over", "African American",\
                    "Female", "Rural", "%Diabetes" , "HIV rate",\
                    "Physical Inactivity" , "mental health provider rate",\
                    "median household income", "% high housing costs",\
                    "% Free lunch", "% child Illiteracy", "% Drive Alone"]
                    
ypll_arr, measures_arr = get_array(ypll_cols, add_measures_cols)

## Plot for quick view
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(6, 12))

sub = fig.add_subplot(3,1,1)
sub.scatter(measures_arr[:,6], ypll_arr, color="b")
sub.set_title("ypll Vs. %Diabetes")

sub = fig.add_subplot(3,1,2)
sub.scatter(measures_arr[:,1], ypll_arr, color="b")
sub.set_title("ypll Vs. Population under 18")

sub = fig.add_subplot(3,1,3)
sub.scatter(measures_arr[:,-2], ypll_arr, color="b")
sub.set_title("ypll Vs. Population of child illiteracy")

plt.savefig('scatter_plot.png', format='png')

## Regression with Ordinary Least Square Method
import ols
#model = ols.ols(ypll_arr, measures_arr[:,6], 'YPLL Rate', ['% Diabetes'])
#model.summary()

# plot the best fit linear curve
def best_fit(m, b, x):
    return (m*x+b)
    
fig = plt.figure(figsize=(6,12))

sub = fig.add_subplot(3,1,1)
independent_arr = measures_arr[:,6]
sub.scatter(independent_arr, ypll_arr, color="b")
model = ols.ols(ypll_arr, independent_arr, 'YPLL Rate', ['% Diabetes'])
line_ys = [best_fit(model.b[1], model.b[0], x) for x in independent_arr]
sub.plot(independent_arr, line_ys, color='r')
sub.set_title("ypll Vs. %Diabetes")

sub = fig.add_subplot(3,1,2)
independent_arr = measures_arr[:,1]
sub.scatter(independent_arr, ypll_arr, color="b")
model = ols.ols(ypll_arr, independent_arr, 'YPLL Rate', ['% Population < 18'])
line_ys = [best_fit(model.b[1], model.b[0], x) for x in independent_arr]
sub.plot(independent_arr, line_ys, color='r')
sub.set_title("ypll Vs. Population under 18")

sub = fig.add_subplot(3,1,3)
independent_arr = measures_arr[:,-3]
sub.scatter(independent_arr, ypll_arr, color="b")
model = ols.ols(ypll_arr, independent_arr, 'YPLL Rate', ['% Population of Illiteracy'])
line_ys = [best_fit(model.b[1], model.b[0], x) for x in independent_arr]
sub.plot(independent_arr, line_ys, color='r')
sub.set_title("ypll Vs. Population of child illiteracy")

plt.savefig('scatter_plot_fit.png', format='png')


dependent_cols = ["YPLL Rate"]
independent_cols = ["< 18", "%Diabetes" , "median household income"]
ypll_arr, measures_arr = get_array(dependent_cols, independent_cols)
model = ols.ols(ypll_arr, measures_arr, "YPLL Rate", independent_cols)
print "p-value", model.Fpv
print "coefficients", model.b
print "R-squared and adjusted R-squared:", model.R2, model.R2adj


## Linear regression with scikit-learn package
from sklearn import linear_model
lr_model = linear_model.LinearRegression()
lr_model.fit(measures_arr, ypll_arr)
lr_model.coef_
lr_model.intercept_
lr_model.score(measures_arr, ypll_arr)