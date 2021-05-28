# Bootcamp_Team_Renegade
Erdos Institute Data Science Bootcamp - Team Renegade Project

Project: investigate the stock movements of the market corresponding to a specific piece of information.
The information that we work with decide the dataset. There are two types of information we want to focus on: the news and financial reports release.

1. For the financial release component: 
- Data gathering is performed in "financial_ratio.py". Data was collected on 27 stocks for financial ratios and 10 stocks for news headline on a quarterly basis. Financial ratios are transformed to percentage change of themselves compared to the previous period.
- Linear regression model is performed in "linear_regression_model.py", the data are transformed using powertransform (Box-Cox) before running the linear model for better result.
- Random forest model is performed in "random_forest.ipynb", ProfileReport was performed on the features first in order to detect variables with high correlations and remove some of those variables, we also run powertransform on the remaining features before running random forest.
- A demonstration of features correlations are shown in "Profile Report on Financial Ratios.html".

2. For the news component:
- Data gathering and PCA are performed in "news_reader.ipynb", the news gathering uses same stocks and same dates as the financial ratios above for potential combination in the future.

Results:
The data are successfully gathered The data set has been formated in the wanted structure. However more data may be needed to improve the model. A demonstration of the data set is shown in "financial_data_updated_transpose.csv".
1. For the financial release component: linear regression model provides good residuals, with all the residuals spread around 0 with approximately normal distribution and the scatter plot looks relatively random for the noise. Random forest also provides similar scatter plot, with nicely distributed random residuals.
2. For the news component: PCA result shows that the news are clustered nicely and can be classified. The linear regression model on the headlines classification also shows that the headlines are significant in explaining the volatility of the stocks.
