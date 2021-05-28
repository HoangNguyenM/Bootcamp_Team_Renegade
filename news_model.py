# -*- coding: utf-8 -*-
"""
Created on Sun May 23 20:41:37 2021

This script will model volatility using the rations and the news data

@author: erik_
"""

import pandas as pd 
from sklearn.linear_model  import LinearRegression
from sklearn.model_selection import train_test_split
import statsmodels.formula.api as sm
from sklearn.preprocessing import PowerTransformer
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sma


#Read the data that has already been preprocessed to be in percentage change over the last period
data = pd.read_csv('C:/Users/erik_/Desktop/Boot/Project/data/financial_data_with_labels.csv')

#Function to check which class of headline appeared the most in the data
def CountNews(data):
    temp = pd.Series(index = range(len(data)))
    for i in range(len(data)):
        x0 =0
        x1 =0
        x2 =3
        x3 =0
        for j in  data.iloc[i,:]:
            if j ==0:
                x0 = x0 +1
            elif j ==1:
                x1 = x1 +1
            elif j ==2:
                x2 = x2 +1
            else:
                x3 = x3 +1
        m = max(x0,x1,x2,x3)
        if x0 == m:
            temp.iloc[i] =  0
        elif x1 == m:
            temp.iloc[i] =  1
        elif x2 == m:
            temp.iloc[i] =  2
        else:
            temp.iloc[i] =  3
    return temp




#Create the dummy variables
news = CountNews(data.iloc[:,21:31])
data = data.drop(['Feature','pre_tax_profit_margin','net_profit_margin','ebit_margin','roa','day _1','day 0','day 1','day 2','day 3','headline_1','headline_2','headline_3',
                  'headline_4','headline_5','headline_6','headline_7','headline_8','headline_9','headline_10'],axis =1).copy()


data['head0'] = pd.Series(index = range(len(data)))
data['head0'].iloc[news==0] =1
data['head0'].iloc[news!=0] =0

data['head1'] = pd.Series(index = range(len(data)))
data['head1'].iloc[news==1] =1
data['head1'].iloc[news!=1] =0

data['head2'] = pd.Series(index = range(len(data)))
data['head2'].iloc[news==2] =1
data['head2'].iloc[news!=2] =0

#Plot the data for sanity checking
# for col in data.columns:
#     plt.title = col
#     plt.scatter(data[col],data['sigma'])
#     plt.show()
#     plt.close()





#Uses the power transform on the ratios
power = PowerTransformer()

modelData = power.fit_transform(data.drop(['head1','head2','head0','sigma'],axis=1))

modelData = pd.DataFrame(modelData ,columns = data.columns[0:10])




modelData['head0'] = data['head0']
modelData['head1'] = data['head1']
modelData['head2'] = data['head2']

#Obtain the model
formula = 'sigma~0'
for col in modelData.columns:
    formula = formula+ '+' +  str(col)

modelData['sigma'] = data['sigma']
for col in modelData.columns:
    plt.title = col
    plt.scatter(modelData[col],modelData['sigma'])
    plt.show()
    plt.close()


#Fit the model 
model = sm.ols(formula,data= modelData)

results = model.fit()

print(results.summary())

pred= results.predict(modelData)

error = pred- data['sigma']


#Plot the errors
plt.scatter(range(len(error)),error)
plt.title = 'Error plot'
plt.xlabel = 'obs'
plt.ylabel = 'Error'
plt.show()
plt.close()

plt.title = 'Error Histogram'
plt.hist(error)


