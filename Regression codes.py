from statsmodels.formula.api import ols
import statsmodels.formula.api as smf
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
plt.style.use('ggplot')

incidents=pd.read_csv("readydata.csv")
incidents_temp=pd.read_csv("Police_Incidents_2015_updatedwithTemp.csv")
parse=lambda x:(pd.to_datetime(x, format='%H:%M:%S').hour)
incidents_temp["crime_happened"]=1
incidents_temp=incidents_temp.dropna()

#Fit regression models

#Time column contains the time of the crime incident
incidents_temp["hour"]=incidents_temp["Time"].apply(parse)

#just temperature
grouped=incidents_temp.groupby(["temperature"],as_index=False).agg({"crime_happened":"sum"})
model = smf.ols(formula="crime_happened ~ temperature", data=grouped).fit()
print(model.summary())
# r^2 11.5%

#Plotting the regression model
#Crime happened ~ temperature
fig = plt.figure(figsize=(12,8))
fig = sm.graphics.plot_regress_exog(model,"temperature",fig=fig)
plt.plot(edgecolor='')

plt.show()

#number of crimes ~ population of neighborhood
model = smf.ols(formula="Crimes ~ Population", data=incidents).fit()
print(model.summary())
#rsqare 21.9%

#number of crimes ~ vacancy rate
model = smf.ols(formula="Crimes ~ Vacancy_rate", data=incidents).fit()
print(model.summary())
# rsquare 8.8 %

#Combine two predictors
#number of crimes ~ population + vacancy rate
model = smf.ols(formula="Crimes ~ Population + Vacancy_rate", data=incidents).fit()
print(model.summary())
# rsquare 34.2%


#Plotting the regression model
#Crime happened ~ population
fig = plt.figure(figsize=(12,8))
fig = sm.graphics.plot_regress_exog(model,"Population", fig=fig)
plt.plot(edgecolor='')
plt.show()

#Crime happened ~ vacancy rate
fig = plt.figure(figsize=(12,8))
fig = sm.graphics.plot_regress_exog(model, "Vacancy_rate", fig=fig)
plt.plot(edgecolor='')
plt.show()