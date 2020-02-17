#!/usr/bin/env python
# coding: utf-8

# Get the necessary packages

# In[1]:


get_ipython().system('pip install beautifulsoup4')
get_ipython().system('pip install lxml')
import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

#!conda install -c conda-forge geopy 
#from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values


# Get some more packages

# In[2]:


from IPython.display import Image 
from IPython.core.display import HTML 

from IPython.display import display_html
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize

get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium # plotting library
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
import matplotlib.cm as cm
import matplotlib.colors as colors

print('Folium installed')
print('Libraries imported.')


# Wikipedia table

# In[3]:


wiki = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
wikipedia=BeautifulSoup(wiki,'lxml')
print(wikipedia.title)
from IPython.display import display_html
data = str(wikipedia.table)
display_html(data,raw=True)


# Pandas to read data

# In[4]:


dat = pd.read_html(data)
da=dat[0]
da.head()


# Remove Not assigned values

# In[5]:


data_restructured = da[da.Borough != 'Not assigned']

# Combining the neighbourhoods with same Postalcode
data_restructured1 = data_restructured.groupby(['Postcode','Borough'], sort=False).agg(', '.join)
data_restructured1.reset_index(inplace=True)

# Replacing the name of the neighbourhoods which are 'Not assigned' with names of Borough
data_restructured1['Neighbourhood'] = np.where(data_restructured1['Neighbourhood'] == 'Not assigned',data_restructured1['Borough'], data_restructured1['Neighbourhood'])

data_restructured1.shape


# Get latitudes and longitudes

# In[6]:


latidute_longitude = pd.read_csv('https://cocl.us/Geospatial_data')
latidute_longitude.head()


# Data merging

# In[7]:


latidute_longitude.rename(columns={'Postal Code':'Postcode'},inplace=True)
datamerge = pd.merge(data_restructured1,latidute_longitude,on='Postcode')
datamerge.head()


# Neighbourhoods of Canada which have Toronto in Borough

# In[8]:


TorontoBorough = datamerge[datamerge['Borough'].str.contains('Toronto',regex=False)]
TorontoBorough


# Visualizing all the Neighbourhoods Toronto in Borough

# In[9]:


Toronto = folium.Map(location=[43.651070,-79.347015],zoom_start=10)

for lat,lng,borough,neighbourhood in zip(TorontoBorough['Latitude'],TorontoBorough['Longitude'],TorontoBorough['Borough'],TorontoBorough['Neighbourhood']):
    label = '{}, {}'.format(neighbourhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
    [lat,lng],
    radius=5,
    popup=label,
    color='blue',
    fill=True,
    fill_color='#3186cc',
    fill_opacity=0.7,
    parse_html=False).add_to(Toronto)
Toronto


# KMeans clustering

# In[10]:


k=5
torontoclustering = TorontoBorough.drop(['Postcode','Borough','Neighbourhood'],1)
kmeans = KMeans(n_clusters = k,random_state=0).fit(torontoclustering)
kmeans.labels_
TorontoBorough.insert(0, 'Cluster Labels', kmeans.labels_)
TorontoBorough


# Map with clusters

# In[11]:


mapfnal = folium.Map(location=[43.651070,-79.347015],zoom_start=10)

# set color scheme for the clusters
x = np.arange(k)
ys = [i + x + (i*x)**2 for i in range(k)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, neighbourhood, cluster in zip(TorontoBorough['Latitude'], TorontoBorough['Longitude'], TorontoBorough['Neighbourhood'], TorontoBorough['Cluster Labels']):
    label = folium.Popup(' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(mapfnal)
       
mapfnal


# In[ ]:





# In[ ]:




