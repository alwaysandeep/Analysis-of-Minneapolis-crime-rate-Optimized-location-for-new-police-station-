import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')

ind2015 = pd.read_csv('Police_Incidents_2015.csv')
ind2014 = pd.read_csv('Police_Incidents_2014.csv')
ind2013 = pd.read_csv('Police_Incidents_2013.csv')
ind2013.rename(columns={'Time_': 'Time', 'Long_': 'Long'}, inplace=True)
ind2012 = pd.read_csv('Police_Incidents_2012.csv')
ind2011 = pd.read_csv('Police_Incidents_2011.csv')
ind2010 = pd.read_csv('Police_Incidents_2010.csv')
offtype = pd.read_csv('OffenceType.csv', index_col = 'Offense')

# conbine data from every year
comb_ind = pd.concat([ind2010,ind2011,ind2012,ind2013,ind2014,ind2015])

# add column of offense type
comb_ind['OffType'] = comb_ind.Offense.map(offtype.OffenseType)

# convert BeginDate to datetime 
comb_ind['BeginDate'] = pd.to_datetime(comb_ind['BeginDate'])

comb_ind.to_csv('combineddata.csv')

# group by year, month, neighborhood
comb_ind['month'] = comb_ind['BeginDate'].map(lambda x:x.month)
comb_ind['year'] = comb_ind['BeginDate'].map(lambda x:x.year)
by_ym = comb_ind.groupby(['year','month','Neighborhood'],as_index=False).size().reset_index()


# add population
population = pd.read_csv('population_by_year.csv')
population['Neighborhood'] = map(str.upper, population['Neighborhood'])
#population1 = by_ym.merge(population,how = "left", left_on = ('Neighborhood','year'), right_on = ('Neighborhood', 'year'))
by_ym1 = pd.merge(by_ym,population,on = ['Neighborhood','year'],how = "left")


# add vacant rate
vacant = pd.read_csv('Neighborhood Info.csv')

# calculate vacant rate
vacant['Occupied housing units'] = pd.to_numeric(vacant['Occupied housing units'],errors='coerce')
vacant['Vacant housing units'] = pd.to_numeric(vacant['Vacant housing units'],errors='coerce')
vacant['vacant_rate'] = vacant['Vacant housing units']/(vacant['Vacant housing units']+vacant['Occupied housing units'])

# merge data
vacant['Neighborhood'] = map(str.upper, vacant['Neighborhood'])
by_ym2 = pd.merge(by_ym1,vacant[['vacant_rate','Neighborhood']],on = ['Neighborhood'],how = "left")

# reset column names
by_ym2.columns = ['year','month','Neighborhood','Crimes','Population','Vacancy_rate']

# export ready to use data!!
by_ym2.to_csv('readydata.csv')



