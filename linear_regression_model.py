import pandas as pd
from sklearn.preprocessing import PowerTransformer
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

# read the data set and transform plain ratios into percentage change compared to the previous period

df = pd.read_csv('D:/Dropbox/Code/Bootcamp/financial_data_updated_transpose.csv')

data = df.copy()

for i in range(len(df['day 0'])):
    if i % 40 == 0:
        for j in range(1,14):
            data.iloc[i,j] = 0
    else:
        for j in range(1,14):
            data.iloc[i,j] = (df.iloc[i,j]-df.iloc[i-1,j])/df.iloc[i-1,j]

position = 0

for i in range(len(df['day 0'])):
    if i % 40 == 0:
        data.drop(position, inplace=True)
    else:
        position = position+1

temp = data

#%%

# form the training data set and the labels without highly correlated variables
# also perform the power transform

data = temp

data = data.drop(['Feature','operating-margin','pre-tax-profit-margin','roa','day -1','sigma','day 1','day 2','day 3'],axis = 1).copy()
columns = data.columns
powr = PowerTransformer()
data = powr.fit_transform(data)

y = data[:,11]
temp_X = data[:,0:11]
X = np.empty((0,12))

for i in range(len(temp_X)):
    X = np.append(X, np.reshape(np.append(np.array([1]),temp_X[i]), (1,12)), axis=0)

print(X)

#%%

# run the linear regression and plot the residuals
model = LinearRegression()

model.fit(X,y)

pred = model.predict(X)

plt.scatter(range(len(pred)),y - pred)

plt.show()
plt.close()
plt.hist(y - pred)
plt.show()

#%%

# get the summary of coefficients and check which variables are significant
model = sm.OLS(y,X)

results = model.fit()

print(results.summary())

#%%
print(columns[[0,4,5,6]])
print(powr.lambdas_[[0,4,5,6]])
