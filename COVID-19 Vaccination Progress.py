#!/usr/bin/env python
# coding: utf-8

# ### <center> COVID-19 World Vaccination Progress - Data Visualization And Analysis
# 

# <img src="Coronavirus-vaccine-Reuters.jpg" width="200">

# 1. What vaccines are used and in which countries?
# 2. What country is vaccinated more people?
# 3. What country is vaccinated a larger percent from its population?

# In[2]:


import pandas as pd
import numpy as np


#for data visualization
import matplotlib.pyplot as plt
import seaborn as sns
import chart_studio.plotly as py
import cufflinks as cf
import plotly.graph_objs as go
import plotly.express as px
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot 
# to get the connection 
init_notebook_mode(connected = True) 

# plotly also serves online, 
# but we are using just a sample 
cf.go_offline 


# In[4]:


covid_df = pd.read_csv('country_vaccinations.csv')
covid_df


# In[5]:


#let's drop source_name	and source_website
covid_df.drop(['source_name','source_website'], axis=1, inplace = True)
covid_df


# In[6]:


covid_df.head()


# *As we can see, there are a lot of nan values in dataset. For correct visualization some of columns are needed to be interpolate*

# In[7]:


covid_df.isnull().sum(axis=0)


# In[8]:


covid_df.shape


# In[18]:


covid_df.dropna(subset=["total_vaccinations", "people_vaccinated"], how="all", inplace=True)


# In[9]:


covid_df


# In[10]:


covid_df.isnull().sum()


# **1. What vaccines are used and in which countries?**

# In[11]:


vaccinebycountry_df = covid_df[['country','iso_code','vaccines']]
vaccinebycountry_df                         


# In[62]:


vaccinesbycountry_grd = vaccinebycountry_df.groupby('country').max()
vaccinesbycountry_grd


# In[63]:


fig = px.choropleth(vaccinesbycountry_grd, locations='iso_code', projection='natural earth',
                   color=vaccinesbycountry_grd.index, hover_name='vaccines')

fig.update_layout(title="Vaccines used by each Country")
iplot(fig)

#Hover and Zoom on the country to view the details of vaccines being used


# Let's explore what the most commonly used vaccination scheme. Here are top-5 that are the most used.

# In[15]:


vaccines = covid_df.groupby(['vaccines','date']).sum().reset_index()
vaccines_top5 = vaccines.groupby('vaccines').max()['total_vaccinations'].reset_index()
vaccines_top5 = vaccines_top5.nlargest(5, columns=['total_vaccinations'])
vaccines_top5


# In[17]:


fig = px.bar(x=vaccines_top5['vaccines'], y=vaccines_top5['total_vaccinations'],
            color=vaccines_top5['vaccines'],
            color_discrete_sequence = px.colors.sequential.Viridis[1:][::2])
fig.show()


# **So, the most commonly used vaccination scheme is "Moderna, Pfizer/BioNTech". And, as we can see, Pfizer/BioNTech vaccine presents in 3/5 the most used vaccination schemes.**
# 
# 

# In[20]:


vaccinebycountry_df = covid_df[['country','iso_code','vaccines', 'total_vaccinations']]
vaccinebycountry_df


# In[69]:


total_vaccinations= vaccinebycountry_df.groupby(['country']).max()[['total_vaccinations'
                     ,'vaccines','iso_code']].reset_index()
total_vaccinations


# In[74]:


fig = px.choropleth(total_vaccinations, locations = 'country', locationmode = 'country names',color = 'vaccines',
                   title = 'total Vaccines used for each country',hover_data= ['total_vaccinations'],
                    color_discrete_map=dict(zip(total_vaccinations['vaccines'], px.colors.sequential.Viridis)),
                   labels={'vaccines': 'Name of vaccine', 'country': 'Country',
                           'total_vaccinations': 'Number of vaccinations'})
fig.update_geos(
    visible=True, 
    resolution=50,
    showcountries=True, 
    countrycolor="darkgrey"
    )
fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
)
fig.show()


# We can see the large violet area of Sputnik V vaccine, but it is used only in Russia and in Argentina. The most European Middle Eastern and North American countries use Pfizer/BioNTech. CNBG, Sinovac is second most used vaccination scheme, but it is used only in China. The Oxford/AstraZeneca vaccine is distributed in United Kingdom, Brazil, Myanmar and India.

# In[76]:


countries = covid_df.country.unique()
print(countries)
print(len(countries))


# #### What country is vaccinated more people?

# Now, let's see what countries vaccinate the most people. Here is the top-10 countries by number of vaccinations.

# In[83]:


total_vaccinations_top10 = covid_df.groupby(['country']).max()["total_vaccinations"]
total_vaccinations_top10 = total_vaccinations_top10.sort_values(ascending=False)[:10]
total_vaccinations_top10


# In[82]:


fig = px.bar(x=total_vaccinations_top10.index ,y=total_vaccinations_top10.values,
            color=total_vaccinations_top10.index,
            labels={"x": "country", "y": "total vaccinations"},
            color_discrete_sequence =px.colors.sequential.Viridis)

fig.show()


# As we can see, USA vaccinate the most people (95.3 millions). China has slightly less vaccinations than the United States, but many times more than other countries. In Europe leaders in number of vaccinations are Germany, Italy and United Kingdom, which includes England.
# 
# 
# 

# #### What country is vaccinated a larger percent from its population?

# As we can see before, USA and China vaccinate the most people, but what about how many people are vaccinate per hundred of population?

# In[84]:


covid_df


# In[186]:


total_vac_hundrd = covid_df[['country','iso_code', 'total_vaccinations_per_hundred']]
total_vac_hundrd['total_vaccinations_per_hundred'] = total_vac_hundrd['total_vaccinations_per_hundred'].fillna(0)
total_vac_hundrd = total_vac_hundrd.groupby(['country', 'iso_code']).max().reset_index()


# In[192]:


def create_choropleth(loc,z,text, title):
    fig = go.Figure(data=go.Choropleth(
          locations = loc,
           z=z,
           text=text,
           colorscale = 'viridis',
           autocolorscale=False,
           reversescale=True,
           marker_line_color='white',
           marker_line_width=0.5
           
     ))
    
    fig.update_geos(
         visible=True,
         resolution=50,
         showcountries=True,
         countrycolor = 'darkgrey'
         )
    
    fig.update_layout(
         title_text = title,
         geo=dict(
             showframe=False,
             showcoastlines=False,
             projection_type='natural earth'
     )) 
    
    fig.show()
    


# In[193]:


create_choropleth(total_vac_hundrd['iso_code'],
                  total_vac_hundrd['total_vaccinations_per_hundred'], 
                  total_vac_hundrd['country'], 
                  'Total vaccinations per hundred')


# The most dark colors have Israel and UAE. It means that this countries have the largest percent of vaccinated people. In USA there are only 28 people per hundred are vaccinated, for China it is 3.

# In[139]:


fully_vac_hundrd = covid_df[['country', 'iso_code', 'people_fully_vaccinated_per_hundred']]
fully_vac_hundrd['people_fully_vaccinated_per_hundred'] = fully_vac_hundred['people_fully_vaccinated_per_hundred'].fillna(0)
fully_vac_hundrd = fully_vac_hundred.groupby(['country', 'iso_code']).max().reset_index()


# In[140]:


create_choropleth(fully_vac_hundrd['iso_code'], 
                  fully_vac_hundrd['people_fully_vaccinated_per_hundred'], 
                  fully_vac_hundrd['country'], 
                  'People fully vaccinated per hundred')


# Fully vaccinated is the number of people that received the entire set of immunization according to the immunization scheme . Now, the largest percent of fully vaccinated people in Israel and UAE. But we have no data about fully vaccinated for other countries.

# On the next choropleth you can see how many people per million are vaccinated every day in different countries.

# In[141]:


dayly_vac_million = covid_df[['country', 'iso_code', 'daily_vaccinations_per_million']]
dayly_vac_million['daily_vaccinations_per_million'] = dayly_vac_million['daily_vaccinations_per_million'].fillna(0)
dayly_vac_million = dayly_vac_million.groupby(['country', 'iso_code']).max().reset_index()


# In[142]:


create_choropleth(dayly_vac_million['iso_code'], 
                  dayly_vac_million['daily_vaccinations_per_million'], 
                  dayly_vac_million['country'], 
                  'Daily vaccinations per million')


# Daily vaccinations per million is high in UAE and israel.

# Let's explore which countries have daily vaccinations the most.

# In[143]:


dayly_vac = covid_df[['country', 'iso_code', 'daily_vaccinations']]
dayly_vac['daily_vaccinations'] = dayly_vac['daily_vaccinations'].fillna(0)
dayly_vac = dayly_vac.groupby(['country', 'iso_code']).max().reset_index()


# In[144]:


create_choropleth(dayly_vac['iso_code'], 
                  dayly_vac['daily_vaccinations'], 
                  dayly_vac['country'], 
                  'Daily vaccinations')


# More tha 1 million of people are vaccinated in USA, China And India. This is the best result among other countries, but due to large number of population this countries still have not big percent of vaccinated people.

# In[146]:


total_vac_hundred = covid_df[['country', 'total_vaccinations_per_hundred' ]]
total_vac_hundred['total_vaccinations_per_hundred'] = total_vac_hundred['total_vaccinations_per_hundred'].fillna(0
                                                                                                                )
total_vac_hundred.head()


# In[149]:


total_vac_hundred = total_vac_hundred.groupby('country').mean()
total_vac_hundred.head()


# In[151]:


#Sorting the data based on total_vaccinations_per_hundred from higher to lower
total_vac_hundred.sort_values(by="total_vaccinations_per_hundred", ascending=False, inplace=True)
total_vac_hundred


# In[152]:


trace = go.Bar(x=total_vac_hundred.index[:25], y=total_vac_hundred["total_vaccinations_per_hundred"], 
                marker=dict(
                  color=np.arange(26)
              ))

fig = go.Figure(data=[trace])
fig.update_layout(title="Top 25 highly vaccinated countries (as per population)")
fig.update_xaxes(title="Country")
fig.update_yaxes(title="Vaccination per hundred")

iplot(fig)


# *We can observe that Israel, UAE, etc. have a higher ratio of total vaccinations per hundred as compared to USA, UK, China*
