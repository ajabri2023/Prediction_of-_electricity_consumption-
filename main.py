import streamlit as st 
import numpy as np
import pandas as pd 
from datetime import date
from datetime import datetime
import statsmodels
from statsmodels.tsa.arima.model import sarimax


st.write(''' #Prediction of electrical consumption in France''')

#Month=input('Month')
#Year=input('Year')  


# Test loop A
st.sidebar.header("Inputs")
def user_input(): 
    Month=st.sidebar.slider('Month', 1, 12, 6)
    Year=st.sidebar.slider('Year', 2023, 2030, 2031)
    a='f{Year}/{Month}' 
    A = datetime.datetime.strptime(a, '%Y/%m')
    
    return  A
   
daf=user_input()  
st.subheader('the forcasted value of consumption')
st.write(daf)


##############################################################################################
df1 = pd.read_csv("Brut consumption.csv", sep=';', header=0, parse_dates=[0], index_col=0, decimal=',') 
# corrected consumption 
df2= pd.read_csv("Corre_consumption.csv", sep=';', header=0, parse_dates=[0], index_col=0, decimal=',') 
#Removing columns 'Filière' 
df1=df1.drop(columns=['Filière'])
df2=df2.drop(columns=['Filière'])

df_test=df2[108:118]
df2.drop(df2.index[108:118], inplace=True)
df=np.log(df2)
################################""
from statsmodels.tsa.statespace.sarimax import SARIMAX
# Dataset split 
size = int(len(df['Valeur (TWh)']) * 0.75)
train1, test1 = df['Valeur (TWh)'][0:size], df['Valeur (TWh)'][size:len(df['Valeur (TWh)'])]
test1 = test1.reset_index()['Valeur (TWh)']
history1 = [x for x in train1]
predictions1 = list()
#####################################################""
for t in range(len(test1)):
    model1 = SARIMAX(history1
                    , order=(1, 1, 1) # order = (p,d,q) AR(p)I(d)MA(q)
                    , seasonal_order=(1, 1, 1, 12) # order = (P,D,Q,m) Seasonal AR(P)I(D)MA(Q) m Seasonal Period
                    )
    model_fit = model1.fit(disp=False)
    output = model_fit.forecast()
    yhat = output[0]
    predictions1.append(yhat)
    obs = test1[t]
    history1.append(yhat)


# Focrcast function (Corrected consuption forcasting)
Fotcasted=model_fit.predict(start=108, end=215, dynamic=True)

# From array to dataframe of forecasting 
df_forcasting=pd.DataFrame(Fotcasted, columns =['forcasted values'])

# Time function preparation 1
Date_index=pd.date_range(start='2023-01', periods=108, freq='M')


# from array to dataframe (time)
df_date=pd.DataFrame(Date_index)

# Date from YYYY/MM/DD to YYYY/MM
df_date['modified']=df_date[0].dt.strftime('%Y/%m')

# To data frame for casting 
df_forcasting=pd.DataFrame(Fotcasted, columns =['forcasted values'])

df_forcasting['forcast_date']=df_date['modified']
df_forcasting=df_forcasting.reindex(columns = ['forcast_date', 'forcasted values'])

# User interface (Year/Month)
#a='f{Year}/{Month}'
#print(a)

#a=f'{Year}/{Month}'

#A = datetime.datetime.strptime(a, '%Y/%m')
####################################################################################






date_target=df_forcasting['forcast_date'].values
forcasted_values=df_forcasting['forcasted values'].values
i=0
for i in range(len(date_target)):
        B=datetime.datetime.strptime(str(date_target[i]), '%Y/%m')
        if B==daf:
         print(B)
         print(daf)
               
        print(np.exp(forcasted_values[i])) 
        result=np.exp(forcasted_values[i] )   # convert result by exp. 
        print((forcasted_values[i]))
        
st.subheader('the predicted consommation:')
st.write(result)