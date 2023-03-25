import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
import seaborn as sns
import numpy as np
from datetime import datetime

#Reading input files 
df= pd.read_csv("Commodities_Retail_Prices_1997_2015.csv")



# Select a Region
df['Region'].value_counts()
Region= df.loc[df['Region']=='NORTH EAST']
Region.head(5)

#Plots for all Commodities for Selected Region

list=Region["Commodity"].unique()
for i in list:
    listof = Region.loc[Region["Commodity"]==i]
    listof['Date'] = pd.to_datetime(listof['Date'])
    plt.figure(figsize = (20, 5))
    plt.title("listof="+ i)
    plt.ylabel("Price per Kg")
    # print(listof['Date'].dt.year)
    df_grouped = listof.groupby([listof['Date'].dt.year,listof['Date'].dt.month])["Price per Kg"].mean().plot()
    

# Select a Commodity
#['Tur/Arhar Dal', 'Tomato', 'Tea Loose', 'Sunflower Oil (Packed)',
#'Sugar', 'Salt Pack (Iodised)', 'Onion', 'Milk', 'Rice']
Comm = Region.loc[Region['Commodity'] == 'Milk']



#checking NAN/Na/Null values in data 
data_frame = Comm
data_frame.tail(10)
missing_values = data_frame.isnull().sum()
print(missing_values)

print('Starting date:',data_frame['Date'].min())
print('Ending date:',data_frame['Date'].max())

[features for features in data_frame.columns if data_frame[features].isnull().sum()>0]

# Remove NAN/NA/Null rows
data_frame.dropna(how='any', inplace=True)
data_frame.tail(10)
missing_values = data_frame.isnull().sum()
print(missing_values)


#Converting Dates into datetime formats
data_frame['Date'] = pd.to_datetime(data_frame['Date'])


# Drop unrelevant variables:
cols = ['Centre','Commodity' ,'Region', 'Country']
data_frame.drop(cols, axis=1, inplace= True)
data_frame.tail(10)

#Aggregating data by date
data_frame= data_frame.groupby('Date')['Price per Kg'].mean().reset_index()

data_frame= data_frame.set_index('Date') #setting date variable as index 

#Plotting selected commidity for a selected region
data_frame['Price per Kg'].plot()
plt.xlabel('Date')
plt.ylabel('Price per Kg')
plt.title('Total over years')
plt.show()

#############
# Plotting Monthly price variations for selected commodity & Region
data_frame['year'] = [d.year for d in data_frame.index]
data_frame['month'] = [d.strftime('%b') for d in data_frame.index]
years= data_frame['year'].unique()
years

fig, axes = plt.subplots(1, 2, figsize=(20,7), dpi= 80)
sns.boxplot(x='year', y='Price per Kg', data=data_frame, ax=axes[0])
sns.boxplot(x='month', y='Price per Kg', data=data_frame.loc[~data_frame.year.isin([2014,2917]), :])
# Set Title
axes[0].set_title('Year-wise Box Plot\n(The Trend)', fontsize=18); 
axes[1].set_title('Month-wise Box Plot\n(The Seasonality)', fontsize=18)
plt.show()
#########
cols = ['year','month']
data_frame.drop(cols, axis=1, inplace= True)




#######Data Aggregation at Monthly level  
#DataFrame by monthly
Monthly = pd.DataFrame()
Monthly['Price per Kg'] = data_frame['Price per Kg'].resample('MS').mean()
#plot monthly/weekly  data
plt.plot(Monthly.index,Monthly['Price per Kg'], linewidth=3)

## Seasonality based on graphs 
from pylab import rcParams
import plotly
rcParams['figure.figsize'] = 18, 8
#plt.title("Linear graph")
decomposition = sm.tsa.seasonal_decompose(Monthly['Price per Kg'], model='additive', period=12)
fig = decomposition.plot()
#fig=plotly.tools.mpl_to_plotly(fig)
#fig.update_layout( title_text='your title here', title_x=0.5)
plt.show()


## Testing For Stationarity (Unit Root Test)
##Dicky-fuller Test  #KPSS test # PP test 
def test_stationarity(data):
    from statsmodels.tsa.stattools import adfuller
    print ('Results of Dickey-Fuller Test:')
    print('Null Hypothesis H0 : The time series is non-stationary (i.e., it has a unit root)')
    print('Alternative hypothesis H1: The time series is stationary')
    dftest = adfuller(data, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)


test_stationarity(Monthly)

# =============================================================================
# Dickey-Fuller Test
# 
# In theory ,if the test statistic is less than the critical value, we reject the null hypothesis 
#and conclude that the time series is stationary.
# 
# The test statistic (-0.809381) is greater than the critical values at all levels of significance (1%, 5%, and 10%).
# This means that we cannot reject the null hypothesis that the time series has a unit root, which indicates that the data is non-stationary.
# 
# To make time series stationary , we can try the following methods 
#a. Differencing 
#    i. Decompose plots
#    ii.ADF test 
#b. Log transformations 
#    i.Decompose plots
#    ii. ADF test
# =============================================================================



## Lets take a log transform here:
y = Monthly['Price per Kg']
ts_log = np.log(y)
test_stationarity(ts_log)

## Lets take a Moving average transform here:
moving_avg = ts_log.rolling(12).mean()
ts_log_moving_avg_diff = ts_log - moving_avg
ts_log_moving_avg_diff.head(12)
ts_log_moving_avg_diff.dropna(inplace=True)
test_stationarity(ts_log_moving_avg_diff)


#Lets take a log difference here
ts_log_diff = ts_log - ts_log.shift()
ts_log_diff.dropna(inplace=True)
#plt.plot(ts_log_diff)
test_stationarity(ts_log_diff)


#Lets take a Exponentially weighted moving average transform here
expwighted_avg = ts_log.ewm(halflife=12).mean()
#plt.plot(expwighted_avg, color='red')
ts_log_ewma_diff = ts_log - expwighted_avg
ts_log_ewma_diff.dropna(inplace=True)
test_stationarity(ts_log_ewma_diff)

