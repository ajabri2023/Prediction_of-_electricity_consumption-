import streamlit as st 
import numpy as np
import pandas as pd 

import statsmodels
from statsmodels.tsa.arima.model import sarimax


st.write(''' #Pridection of electrical consumption in France''')
st.sidebar.header("Inputs")
         