import pandas as pd
from sklearn.preprocessing import power_transform,OneHotEncoder
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data = pd.read_csv('D:/Dropbox/Code/Bootcamp/financial_ratio_transpose.csv')

columns = data.columns

data = data.drop(['day -1','day 0','day 1','day 2','day 3'],axis = 1).copy()

power =power_transform(data.drop('Feature',axis = 1))

y = power[:,14]

X = power[:,1:13]

model = LinearRegression()

model.fit(X,y)

pred = model.predict(X)

plt.scatter(range(len(pred)),y - pred)

plt.show()

