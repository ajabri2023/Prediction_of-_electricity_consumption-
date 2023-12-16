import streamlit as st 
import numpy as np
import pandas as pd 

from datetime import datetime, date

import statsmodels
from statsmodels.tsa.arima.model import sarimax
from PIL import Image
# Title and images
st.header("Prediction of monthly electricity consumption in France")
st.image("IA_Electronics.png", use_column_width="auto")
st.sidebar.image("logo_ADS.png", use_column_width="auto")



# Test loop A (Inputs)

st.sidebar.header("Inputs")
def user_input(): 
    Months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    Month=st.sidebar.slider('Month', 1, 12, 6)
    Year=st.sidebar.slider('Year', 2023, 2030, 2031)
    a=str(f'{Year}/{Month}')
    A = datetime.strptime(a, '%Y/%m').date()  
    st.write(f'{Year}')
    st.write(f'{Months[(Month-1)]}')
    
   
    return  A
  
daf=user_input()  


# Data preparation and model training
##############################################################################################

df1 = pd.read_csv("Brut consumption.csv", sep=';', header=0, parse_dates=[0], index_col=0, decimal=',') 
# corrected consumption 
df2= pd.read_csv("Corre_consumption.csv", sep=';', header=0, parse_dates=[0], index_col=0, decimal=',') 
#Removing columns 'Filière' 
df1=df1.drop(columns=['Filière'])
df2=df2.drop(columns=['Filière'])
# df_test
df_test=df2[108:118]
df2.drop(df2.index[108:118], inplace=True)
df=np.log(df2)

#Model train
from statsmodels.tsa.statespace.sarimax import SARIMAX
# Dataset split 
size = int(len(df['Valeur (TWh)']) * 0.75)
train1, test1 = df['Valeur (TWh)'][0:size], df['Valeur (TWh)'][size:len(df['Valeur (TWh)'])]
test1 = test1.reset_index()['Valeur (TWh)']
history1 = [x for x in train1]
predictions1 = list()
# fitting 
for t in range(len(test1)):
    model1 = SARIMAX(history1 , order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))

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

####################################################################################
# Correction coefficien 
Coeff=df2/df1
# Model Train (correction coeffiecien forcasting)
from statsmodels.tsa.statespace.sarimax import SARIMAX
# Dataset split 
size = int(len(Coeff['Valeur (TWh)']) * 0.75)
train_, test_ = Coeff['Valeur (TWh)'][0:size], Coeff['Valeur (TWh)'][size:len(Coeff['Valeur (TWh)'])]
test_ = test_.reset_index()['Valeur (TWh)']
history_ = [x for x in train_]
predictions_ = list()

for t in range(len(test_)):
    model_ = SARIMAX(history_, order=(1, 1, 1) , seasonal_order=(1, 1, 1, 12))
    model_fit_ = model_.fit(disp=False)
    output_ = model_fit_.forecast()
    yhat_ = output_[0]
    predictions_.append(yhat_)
    obs = test_[t]
    history1.append(yhat_)
# Focrcast function (Correction coefficien forcasting)
pred_correc=model_fit_.predict(start=108, end=215, dynamic=True)
# add pred_correc to dataframe forcasting
df_forcasting = df_forcasting.assign(Correc_coefficient=pred_correc)



# Result  loop

date_target=df_forcasting['forcast_date'].values
forcasted_values=df_forcasting['forcasted values'].values
Ccoff=df_forcasting['Correc_coefficient'].values 
i=0
for i in range(len(date_target)):
       B=datetime.strptime(str(date_target[i]), '%Y/%m').date()
        #b=str(date_target[i])
       if B==daf:
         #print(b)
         #print(daf)
               
            print(f'corrected_consumption={np.exp(forcasted_values[i])}')   # convert result by exp. 
            result1=np.exp(forcasted_values[i])
            corrected= round(result1, 2)
            print((Ccoff[i])) # correction coefficien
            print(f'Brut consumption={np.exp(forcasted_values)[i]/Ccoff[i]}')
            result2=np.exp(forcasted_values)[i]/Ccoff[i]
            brut=round(result2, 2)

st.subheader('Outputs')
st.write('Corrected consumption in (TWh) and (GWh):')
st.write(f'{corrected} TWh')
st.write(f'{corrected*1000} GWh')
st.write('Brut consumption in (TWh) and (GWh):')
st.write(f'{brut} TWh')
st.write(f'{brut*1000} GWh')

st.sidebar.image('H_voltage.png', use_column_width="auto")