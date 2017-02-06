import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
from pandas import DataFrame
import seaborn as sns
from scipy.stats import gaussian_kde
import geopandas as gpd

plt.style.use('ggplot')

comb_ind = pd.read_csv('combineddata.csv')
comb_ind['BeginDate'] = pd.to_datetime(comb_ind['BeginDate'])

# crime by type and hours of day
sns.set_palette('Spectral',10) # set color palette
comb_ind['hour'] = comb_ind['BeginDate'].map(lambda x:x.hour)
group_hour = comb_ind.groupby(['hour','OffType']).size().unstack()
group_hour['Total'] = comb_ind.groupby(['hour']).size()

styles = ['.-','.-','.-','.-','.-','.-','.-','.-','.-']
group_hour.plot(style=styles,figsize=(10,6))
plt.subplots_adjust(right=0.75)
plt.title('Number of Crimes by hours of day')
plt.xlabel('Hours')
plt.ylabel('Number of Crimes')
plt.legend(loc=3, bbox_to_anchor=(1.0, 0.5))

# crime by type and month
comb_ind['month'] = comb_ind['BeginDate'].map(lambda x:x.month)
group_month = comb_ind.groupby(['month','OffType']).size().unstack()
group_month['Total'] = comb_ind.groupby(['month']).size()

styles = ['.-','.-','.-','.-','.-','.-','.-','.-','.-']
group_month.plot(style=styles,figsize=(10,6))
plt.subplots_adjust(right=0.75)
plt.title('Number of Crimes by months')
plt.xlabel('Month')
plt.ylabel('Number of Crimes')
plt.legend(loc=3, bbox_to_anchor=(1.0, 0.5))

# plot offense type for years trend
comb_ind['year'] = comb_ind['BeginDate'].map(lambda x:x.year)
group_type = comb_ind.groupby(['year','OffType',]).size().unstack(1)

# normalize data to percentage
group_type.loc[2010] = group_type.loc[2010]/ group_type.sum(1).loc[2010]
group_type.loc[2011] = group_type.loc[2011]/ group_type.sum(1).loc[2011]
group_type.loc[2012] = group_type.loc[2012]/ group_type.sum(1).loc[2012]
group_type.loc[2013] = group_type.loc[2013]/ group_type.sum(1).loc[2013]
group_type.loc[2014] = group_type.loc[2014]/ group_type.sum(1).loc[2014]
group_type.loc[2015] = group_type.loc[2015]/ group_type.sum(1).loc[2015]

sns.set_palette('Spectral',10)
group_type.plot.bar(stacked=True, alpha = 0.7, rot=20)
plt.title('Crimes Type Break Down by Year')
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.legend(loc=1)
plt.legend(loc=3, bbox_to_anchor=(1.0, 0.5))
plt.show()

# heatmap by Precinct
plt.figure()
drop18 = comb_ind[comb_ind['Precinct']!=18]
group_prec = drop18.groupby(['Precinct','OffType']).size().unstack()
plt.xticks(rotation=20)
plt.title('Types of Crime in Each Precinct')
plt.xlabel('Crime type')
ax = sns.heatmap(group_prec)

# number of crime over time
plt.figure()
comb_ind = comb_ind.set_index(pd.DatetimeIndex(comb_ind['BeginDate']))
trend = comb_ind.resample('d').size()

# add trendline
trend = DataFrame(trend,index = trend.index)
trend['t'] = range(1,len(trend)+1)
trend.columns = ['num','t']

regression = pd.ols(y=trend['num'], x=trend['t'])

fit = regression.predict(beta=regression.beta, x=trend['t'])
trendline = pd.DataFrame(index=trend.index, data={'y': fit, 'trend': trend['num']})

#fig, ax = plt.subplots()
trendline['trend'].plot(color = 'tomato',alpha = 0.8)
trendline['y'].plot(color = 'lightseagreen',linewidth = 2)

plt.title('Number of Crimes Over Time')
plt.xlabel('Time')
plt.ylabel('Number of Crimes')

# calculate sum of crime by year
by_year = comb_ind.resample('A').size()

# heatmap, you need to zoom in to see the data just for Minnapolis
x = comb_ind['Long']
y = comb_ind['Lat']

xy = np.vstack([x,y])
z = gaussian_kde(xy)(xy)

fig, ax = plt.subplots()
ax.scatter(x, y, c=z, s=100, edgecolor='')

# add boundries for neighborhood
neighborhood = gpd.read_file("Neighborhoods.geojson")
neighborhood.plot(ax=ax, color = 'white', alpha = 0,lw = 2)

plt.show()

