#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
product_name = pd.read_csv('data/Product_Name.csv')
cooking_data = pd.read_csv('data/Cooking_data_set.csv')
# booking_data = pd.read_csv('data/booking_data.csv')
booking_sort2 = pd.read_csv('data/booking_sort2.csv')
error_message = pd.read_csv('data/Error_Message.csv')


# In[2]:


product_name[product_name['품목명'].isnull()]
product_name['품목명'].fillna(product_name['품목코드'], inplace=True)
product_name.drop('Column 4', axis=1, inplace=True)
product_name = product_name.drop(0)
product_name.reset_index(drop=True, inplace=True)
pro1 = product_name[['품목코드', '품목명']]
pro1['품목코드'].nunique()


# In[3]:


cooking_name = cooking_data[['품목코드', '품목명']]
cooking_name['품목명'].fillna(cooking_name['품목코드'], inplace=True)
cooking_name = cooking_name.drop_duplicates()
concat_name = pd.concat([cooking_name, pro1], axis = 0)
concat_name = concat_name.drop_duplicates()
concat_name
#cookingdata, product_name에 있는 품목코드와 품목명은 서로 일치한다.


# In[4]:


booking_sort2 = booking_sort2.rename(columns ={'수주품목코드': "품목코드"})
booking_sort2['품목코드'].nunique()


# In[5]:


booking_merge = pd.merge(booking_sort2, concat_name, on='품목코드', how='left')
booking_merge_drop = booking_merge.dropna(subset=['품목명'])
booking_merge_drop['품목코드'].nunique()


# In[6]:


# cooking_name = cooking_data[['품목코드', '품목명']]
# cooking_name['품목명'].fillna(cooking_name['품목코드'], inplace=True)
# cooking_name = cooking_name.drop_duplicates()
# concat_name = pd.concat([cooking_name, pro1], axis = 0)
# concat_name = concat_name.drop_duplicates()
# concat_name
# #cookingdata, product_name에 있는 품목코드와 품목명은 서로 일치한다.


# In[7]:


booking_merge_drop['품목코드_1'] = booking_merge_drop['품목코드'].str[0:1]


# In[8]:


#60만개 드롭 후 isnull()
booking_merge_drop['수주사업장'].fillna('20.0', inplace=True)


# In[9]:


#booking_merge_drop_sort.isnull().sum()


# In[10]:


booking_merge_drop.drop('Unnamed: 0', axis=1, inplace = True)


# In[ ]:





# In[11]:


booking_merge_drop.reset_index(drop=True, inplace=True)


# In[12]:


booking_merge_drop[booking_merge_drop['납기일자'].isnull()]


# In[13]:


booking_merge_drop['납기일자'].fillna(method ='ffill',inplace=True)


# In[14]:


booking_merge_drop[booking_merge_drop['거래처코드'].isnull()]


# In[15]:


booking_merge_drop_sort = booking_merge_drop.sort_values(by=['수주일자','수주일련번호'], ascending = True)
booking_merge_drop_sort.reset_index(drop=True, inplace=True)
booking_merge_drop_sort['거래처코드'].fillna(method ='ffill',inplace=True)


# In[16]:



booking_merge_drop_sort[booking_merge_drop_sort['거래처코드'].isnull()]


# In[17]:


booking_merge_drop_sort.drop('생산지시', axis=1, inplace=True)


# In[18]:


booking_merge_drop_sort[booking_merge_drop_sort['수주단위'].isnull()]


# In[19]:


#booking_merge_drop_sort.drop('수주단위', axis=1, inplace=True)
booking_merge_drop_sort.drop('수주부서', axis=1, inplace=True)


# In[20]:


#booking_merge_drop_sort[booking_merge_drop_sort['수주부서'].isnull()]


# In[21]:


test1 = booking_merge_drop_sort.query('수주사업장==20.0')
test1


# In[22]:


# 모든 행과 열 보기
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


# In[23]:


booking_merge_drop_sort.drop('품목명', axis=1, inplace=True)


# In[24]:


booking_merge_drop_sort[booking_merge_drop_sort['수주금액']<0]

#df_kospi['방법1'] = df_kospi['ChagesRatio'].apply(lambda x: '오른 주식' if x > 0 else '내린 주식')


# In[25]:


#최종본 booking_lamda
booking_lamda = booking_merge_drop_sort.copy()
# booking_lamda['수주수량KG'] = booking_lamda['수주수량KG'].apply(lambda x: x*0.001 if x<-10000 else x )
# booking_lamda[booking_lamda['부가세금액']<-10000000]
# booking_lamda[booking_lamda['수주금액']<-100000000]
# booking_lamda['수주금액'] = booking_lamda['수주금액'].apply(lambda x: x*0.001 if x<-100000000 else x)
# booking_lamda['부가세금액'] = booking_lamda['부가세금액'].apply(lambda x: x*0.001 if x<-10000000 else x)


# In[26]:


#booking_lamda.reset_index(drop=True, inplace = True)


# In[27]:


# import numpy as np
# booking_test = booking_merge_drop_sort.where(booking_merge_drop_sort['수주금액'] >= 0, np.nan)
# booking_test.isnull()


# In[28]:


booking_lamda = booking_lamda.drop(booking_lamda[booking_lamda['수주금액']<0].index)


# In[29]:


booking_lamda['수주일자_dt'] = pd.to_datetime(booking_lamda['수주일자_dt'])


# In[30]:


booking_lamda['year'] = booking_lamda['수주일자_dt'].dt.year


# In[31]:


booking_lamda


# In[32]:


year_earn = booking_lamda.groupby('year')['수주금액'].sum()
year_earn = pd.DataFrame(year_earn)
year_earn.reset_index(inplace = True)

import plotly.express as px

fig = px.bar(year_earn, x="year", y="수주금액", title='연도별 순수주금액 변동추이')
fig.show()


# In[33]:


year_earn


# In[34]:


buyer = booking_lamda.groupby('year')['거래처코드'].count()
# = booking_lamda.groupby('year')['수주금액'].sum()
buyer = pd.DataFrame(buyer)
buyer.reset_index(inplace = True)
buyer


# In[35]:


import plotly.express as px

fig = px.bar(buyer, x="year", y="거래처코드", title='연도별 거래처수 변동추이')
fig.show()


# In[36]:


error_message


# In[37]:


pro1['품목코드23'] = pro1['품목코드'].str[1:3]
pro1


# In[38]:


get_ipython().run_cell_magic('writefile', "'01start.py'", '#!/usr/bin/python\n# -*- coding: <encoding name> -*-\n\nfrom dash import Dash, html, dcc\nimport plotly.express as px\nimport pandas as pd\n\nfig = px.bar(buyer, x="year", y="거래처코드", title=\'연도별 거래처수 변동추이\')\n\napp = Dash(__name__)\n# app layout: html과 dcc 모듈을 이용\napp.layout = html.Div(children=[\n    # Dash HTML Components module로 HTML 작성 \n    html.H1(children=\'첫번째 Dash 화면\'),\n    html.Div(children=\'\'\'\n        대시를 이용하여 웹어플리케이션 작성 연습...\n    \'\'\'),\n    \n    \n    # dash.core.component(dcc)의 그래프컴포넌트로 plotly 그래프 렌더링\n    dcc.Graph(\n        id=\'graph1\',\n        figure=fig\n    )\n])\n\nif __name__ == \'__main__\':\n    app.run_server(debug=True)\n    #app.run_server(debug=False, host=\'0.0.0.0\', port=8888)')


# In[ ]:


#히히 머지하꺼야
#이건 민경환이 쓰는 머지테스트용 잡소립니다. 
#히히 시공이 최고야!
#포크로 찍어버릴꺼야!
# 포크 무서워 찍찌마
# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




