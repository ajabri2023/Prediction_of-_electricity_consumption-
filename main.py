import streamlit as st 
import numpy as np
import pandas as pd 

import statsmodels
from statsmodels.tsa.arima.model import sarimax


st.write(''' #Prediction of electrical consumption in France''')
st.sidebar.header("Inputs")
def user_input(): 
    Month=st.sidebar.slider('Month', 1, 12, 6)
    Year=st.sidebar.slider('Year', 2023, 2030, 2024)
    
Month=input('Month')
Year=input('Year')  
List=[Month, Year, '01']

 
#Prediction_date=pd.DataFrame(data, index=[0])
 #   return Prediction_date
#df=user_input()     ''''   