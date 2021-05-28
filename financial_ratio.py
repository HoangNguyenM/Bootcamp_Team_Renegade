# this file collects the financial ratios data
# and the stock movements from the selected stocks

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time

#stock_syms = ['AAPL','TSLA', 'NVDA', 'MSFT', 'AMZN', 'V', 'WMT', 'MA', 'PG', 'INTC']
#stock_names = ['apple','tesla', 'nvidia', 'microsoft', 'amazon', 'visa', 'walmart', 'mastercard', 'procter-gamble', 'intel']

stock_syms = ['AAPL','TSLA', 'NVDA', 'MSFT', 'AMZN', 'V', 'WMT', 'MA', 'PG', 'INTC', 'VZ',
              'ADBE', 'ORCL', 'CSCO', 'NKE', 'UPS', 'MCD', 'COST', 'SBUX',
              'GS', 'CSV', 'MMM', 'DE', 'LMT', 'EL', 'ANTM', 'AMD']
stock_names = ['apple','tesla', 'nvidia', 'microsoft', 'amazon', 'visa', 'walmart', 'mastercard', 'procter-gamble',
               'intel', 'verizon', 'adobe', 'oracle', 'cisco',
               'nike', 'ups', 'mcdonalds', 'costco', 'starbucks',
               'goldman-sachs', 'carriage-services', '3m', 'deere', 'lockheed-martin', 'estee-lauder', 'anthem', 'amd']

number_of_points = 40

rng = [1,4,5,6,8,9,10,12,13,14,15,16,17,18]


#%%

# read the html for financial ratios releases
def get_html(stock_sym, stock_name):
    
    success = False
    html = 0
    while success==False:
        try: 
            html = urlopen("https://www.macrotrends.net/stocks/charts/"+stock_sym+"/"+stock_name+"/financial-ratios?freq=Q")
            success = True
        except:
            success = False
        time.sleep(1)
    
    
    soup = BeautifulSoup(html, 'html.parser')
    
    info = soup.prettify()
    
    return info


#%%

# parse the html and create the dataframe of financial ratios
def get_data(info, stock_sym, stock_name):

    pos = info.find('var originalData')
    
    info = info[pos:]
    
    ls = info.split('field_name')
    
    Ratio = []
    Value = []

    for i in rng:
        
        pos1 = ls[i].find('t: \''+stock_sym+'\', s:')
    
        Ratio.append(ls[i][(pos1+11+len(stock_sym)):].split('\'')[0])
        
        temp = ls[i][(pos1+11+len(stock_sym)):].split('div>')[1]
    
        temp = temp.split('\":\"')
    
        hold = []
        for j in range(number_of_points):
            hold.append(temp[j+1].split('\"')[0])
            
        Value.append(hold)
    
    df = pd.DataFrame()
    df['Feature'] = Ratio[:len(rng)]
    for i in range(number_of_points):
        hold = []
        for j in range(len(rng)):
            hold.append(float(Value[j][i]))
        df['Q'+str(i+1)] = hold
    
    return df

#%%

# get the dates that the financial ratios were released yearly
def get_yearly_date(stock_sym):

    success = False
    html2 = 0
    while success==False:
        try:
            html2 = urlopen("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+stock_sym+"&type=10-K&dateb=&owner=exclude&count=100")
            success = True
        except:
            success = False
        time.sleep(1)

    soup2 = BeautifulSoup(html2, 'html.parser')
    
    tables  = soup2.find_all('tr')
    
    texts = []
    for table in tables:
        texts.append(table.text.strip().replace('\n',''))
    
    dates = []
    count = 0
    for text in texts:
        pos = text.find('Amend')
        if pos<0:
            pos = text.find('MB')
            if pos>0:
                while text[pos] != '2':
                    pos = pos+1
                if count < 10:
                    dates.append(text[pos:pos+10])
                    count = count+1
                
    return dates

#%%

# combine the yearly dates with quarterly dates for comprehensive dates
def get_date(stock_sym, year_dates):

    success = False
    html1 = 0
    while success==False:
        try: 
            html1 = urlopen("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+stock_sym+"&type=10-Q&dateb=&owner=exclude&count=100")
            success = True
        except:
            success = False
            time.sleep(1)
            
    soup1 = BeautifulSoup(html1, 'html.parser')
    
    tables  = soup1.find_all('tr')
    
    texts = []
    for table in tables:
        texts.append(table.text.strip().replace('\n',''))
    
    dates = []
    count = 0
    for text in texts:
        pos = text.find('Amend')
        if pos<0:
            pos = text.find('MB')
            if pos>0:
                while text[pos] != '2':
                    pos = pos+1
                if count < number_of_points:
                    dates.append(text[pos:pos+10])
                    count = count+1
    
    final_dates = []
    count = 0
    pos1 = 0
    pos2 = 0
    dates.append('1990-01-01')
    year_dates.append('1990-01-01')
    while count < number_of_points:
        if dates[pos1]>year_dates[pos2]:
            final_dates.append(dates[pos1])
            pos1 = pos1+1
        else:
            final_dates.append(year_dates[pos2])
            pos2 = pos2+1
        count = count+1
    
    return final_dates
    

#%%

# get the stock prices from the selected stocks above on the dates gathered
import yfinance as yf
import datetime
import pandas_market_calendars as mcal

def get_stock_price(dates, stock_sym):
    
    nyse = mcal.get_calendar('NYSE')
    start_dates = []
    end_dates = []
    for date in dates:
    
        d = datetime.datetime.strptime(date, '%Y-%m-%d')
    
        # determine start dates
        delta = -40
        valid = nyse.valid_days(start_date=d+datetime.timedelta(days=delta), end_date=d+datetime.timedelta(days=-1))
        start_date = valid[-20]
        
        start_dates.append(start_date.date().strftime('%Y-%m-%d'))
        
        # determine end dates
        delta = 30
    
        end_date = d + datetime.timedelta(days=delta)
        
        end_dates.append(end_date.date().strftime('%Y-%m-%d'))

    data = []
    for i in range(number_of_points):
        data.append(yf.download(stock_sym, start=start_dates[i], end=end_dates[i]))
        time.sleep(1)
    
    return data


#%%

# compute the stock prices log return and add to the dataframe with the financial ratios
import numpy as np
import math

def combine_data(df, data):
    log_return = []
    combined_data = df
    
    for i in range(number_of_points):
        vec = np.zeros(26)
        for j in range(26):
            if not (math.isnan(data[i]['Open'].iloc[j+1]) or math.isnan(data[i]['Open'].iloc[j])):
                vec[j] = np.log(data[i]['Open'].iloc[j+1]/data[i]['Open'].iloc[j])
            else:
                vec[j] = 0
        log_return.append(vec)
    
    for j in range(26):
        for i in range(number_of_points):
            combined_data.loc[len(rng)+j,'Feature'] = 'day '+str(j-20)
            combined_data.loc[len(rng)+j,'Q'+str(i+1)] = log_return[i][j]
    
    return combined_data

#%%

all_data = []
k = 0

#%%

# run all the functions above to create the data and then output the data
temp = k

for k in range(temp,len(stock_syms)):
    info = get_html(stock_syms[k],stock_names[k])
    df = get_data(info, stock_syms[k], stock_names[k])
    yearly_dates = get_yearly_date(stock_syms[k])
    dates = get_date(stock_syms[k], yearly_dates)
    data = get_stock_price(dates, stock_syms[k])
    final = combine_data(df, data)
    all_data.append(final)


#%%
print(k)
print(len(all_data))
print(stock_syms[k])
print(stock_names[k])

#%%

combined_data = pd.concat([all_data[0],all_data[1].iloc[:,1:]],axis=1)

for i in range(len(stock_syms)-2):
    combined_data = pd.concat([combined_data,all_data[i+2].iloc[:,1:]],axis=1)

combined_data.to_csv("D:/Dropbox/Code/Bootcamp/financial_data_updated.csv",index=False)
