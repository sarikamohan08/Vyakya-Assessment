#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np
import pandas as pd 
import json
from datetime import datetime
import re
import csv
from pandas import ExcelWriter


# In[12]:


fileObject = open("task_input_list.json", "r")
jsonContent = fileObject.read()
df = json.loads(jsonContent)


# In[13]:


df2=[]
expr = '^(?!$).-*[0-9,]*\.[0-9]+'
for x in range(1,len(df)):
    match = re.search(expr,df[x])
    # print(match)
    if match != None:
        # print(df[x-1])
        if "other" not in df[x-1].lower():
            # print(df[x])

            df2.append(match.group(0))


# In[14]:


for i in range(1,len(df)):
    if df[i]=="Deposits and other additions":
        x=i
    if df[i]=="Total other subtractions":
        y=i
print(x,y)
data=df[x:y]
print(data)


# In[ ]:


x=(data.index('Withdrawals and other subtractions'))
deposit=data[:x]
withdraw=data[x:]
print(deposit,withdraw)


# In[ ]:


ds = ' '.join(deposit)
ws = ' '.join(withdraw)
d_dates = re.findall(r'\d{2}/\d{2}/\d{2}',ds)
w_dates=re.findall(r'\d{2}/\d{2}/\d{2}',ws)
print(d_dates,w_dates)


# In[ ]:


d_amount=[]
w_amount=[]
expr = '^(?![$]).-*[0-9,]*\.[0-9]+'
for x in range(0,len(deposit)):
    match = re.search(expr,deposit[x])
    # print(match)
    if match != None:

        d_amount.append(match.group(0))
for x in range(0,len(withdraw)):
    match = re.search(expr,withdraw[x])
    # print(match)
    if match != None:

        w_amount.append(match.group(0))
print(d_amount,w_amount)


# In[ ]:


d_desc=[]
w_desc=[]
for x in range(0,len(d_dates)):
    start_string = d_dates[x]
    end_string = d_amount[x]
    result_string = ds.split(start_string)[1].split(end_string)[0]
    d_desc.append(result_string)
for x in range(0,len(w_dates)):
    start_string = w_dates[x]
    end_string = w_amount[x]
    result_string = ws.split(start_string)[1].split(end_string)[0]
    w_desc.append(result_string)

print(d_desc)
print(w_desc)


# In[ ]:


deposit_amount=[float(item.replace(',','')) for item in d_amount]
withdraw_amount=[float(item.replace(',','')) for item in w_amount]


# In[ ]:


dep_f=pd.DataFrame(columns=['date','description','amount'])
with_f=pd.DataFrame(columns=['date','description','amount'])
w_dates=[datetime.strptime(item,"%m/%d/%y") for item in w_dates]
d_dates=[datetime.strptime(item,"%m/%d/%y") for item in w_dates]



# In[ ]:


dep_f['date']=d_dates
dep_f['description']=d_desc
dep_f['amount']=deposit_amount

with_f['date']=w_dates
with_f['description']=w_desc
with_f['amount']=withdraw_amount
with_f


# In[ ]:


dep_f['day'] = dep_f['date'].dt.day
dep_f['month'] = dep_f['date'].dt.month
dep_f['year'] = dep_f['date'].dt.year
dep_f

with_f['day'] = with_f['date'].dt.day
with_f['month'] = with_f['date'].dt.month
with_f['year'] = with_f['date'].dt.year
with_f


# In[ ]:


with_f['date']=w_dates
dep_f['date']=d_dates


# In[ ]:


insights={}
insights["max amount"]= max(deposit_amount)
insights["min amount"]=min(withdraw_amount)
insights


# In[ ]:


from urlextract import URLExtract
s = ' '.join(df)
extractor = URLExtract()
urls = extractor.find_urls(s)
phone=[]

phone=re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', s)
phone=phone[:3]
emails = re.findall(r'[\w\.-]+@[\w\.-]+', s)
print(urls,emails)
insights["website"]=','.join(urls)
insights["email"]=','.join(emails)
insights["phone"]=','.join(phone)


# In[ ]:


insights_f = pd.DataFrame()
c1= list(insights.keys())
c2= list(insights.values())
insights_f["keys"]=c1
insights_f["value"]=c2
insights_f


# In[ ]:


writer = pd.ExcelWriter('result.xlsx')

dep_f.to_excel(writer,index=False,sheet_name="DEPOSIT")
with_f.to_excel(writer,index=False,sheet_name="WITHDRAWAL")
insights_f.to_excel(writer,index=False,sheet_name="INSIGHTS")

writer.save()


# insights
