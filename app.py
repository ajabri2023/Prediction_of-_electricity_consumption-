import streamlit as st 
import numpy as np
import pandas as pd 
from datetime import datetime, date


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
##################################
# Data import 
df_forcasting = pd.read_csv("forecasted_values.csv",  sep=',', header=0, parse_dates=[0], index_col=0)  
########################################
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

