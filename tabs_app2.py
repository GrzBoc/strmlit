import streamlit as st
import pandas as pd
import numpy as np
from collections import OrderedDict

def page_hello():

    st.title("Hello")
    st.write("First page content.")

    s=0

    if st.button('cos'):   
        s=1
    if st.button('cos2'):
        s=2  
    st.button('cos3')
    my_slot1 = st.empty()
    my_slot1.write('XXX')
    if s==1:
        my_slot1.write('1x moze i dziala')  
        st.write(' s --> 1')
        st.sidebar.write(":triangular_flag_on_post: menu pomocnicze")
    elif s==2:
        my_slot1.write('2x moze i dziala')
        st.write(' s --> 2')  
    return s

def page_world():
    s=-99
    st.title("World")
    st.write("Second page content.")
    return s


@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def get_w():
    st.write('Cache miss')   
    return pd.DataFrame(data=[9999], columns=['output'])
w=get_w()

pages = OrderedDict([
    ("Hello", page_hello),
    ("World", page_world),
])
st.sidebar.title(":triangular_flag_on_post: Page sample")
page = st.sidebar.selectbox("Browse page.", list(pages.keys()))

st.sidebar.write('Zmienna w (start):',w.iloc[0,0])
x=pages[page]()  # wywołuje funkcję ze słownika 
w.iloc[0,0]=x
st.sidebar.write('Zmienna x:',x)
st.sidebar.write('Zmienna w:',w.iloc[0,0])