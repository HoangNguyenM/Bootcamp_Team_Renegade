# -*- coding: utf-8 -*-
"""
Created on Fri May 14 16:39:57 2021

@author: erik_
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen

stock_sym = ['TSLA']
stock_name = ['tesla']

html1 = urlopen("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+stock_sym[0]+"&type=10-K&dateb=&owner=exclude&count=100")


soup = BeautifulSoup(html1,'html.parser')
print(soup.prettify())

#%%
tables  = soup.find_all('tr')


texts = []
for table in tables:
    texts.append(table.text.strip().replace('\n',''))
    # pos = table.text.find('MB\n')
    # print(table.text[pos:13])

for text in texts:
    pos = text.find('Amend')
    if pos < 0:
        pos = text.find('MB')
        if pos >0:
            while text[pos] != '2':
                pos = pos +1
            print(text[pos:pos+10])
    
