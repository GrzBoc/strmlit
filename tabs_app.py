import pandas as pd
import numpy as np
import plotly.express as px

import sqlite3 as sql3
import pyodbc  as pydb

import streamlit as st
from collections import OrderedDict
import time

def main():
    # eksperymenty http://awesome-streamlit.org/  ---> layout experiment
    st.markdown(
        f"""
        <style>
        .reportview-container .main .block-container{{
            max-width: 95%; padding-top: 0 rem; margin-top: 0 rem;
        }}
        .reportview-container .main {{
            color: black; background-color: white;
        }}
        </style>
        """,
            unsafe_allow_html=True,
        )

    w=get_w()
    pages = OrderedDict([
        ("Hello", page_hello),
        ("World", page_world),
        ("IMF GDP", page_imf_gdp),
    ])
    st.sidebar.title(":triangular_flag_on_post: Page sample")
    page = st.sidebar.selectbox("Browse page.", list(pages.keys()))
     
    x=pages[page]()  # wywołuje funkcję ze słownika 
   
    w.iloc[0,0]=x


@st.cache(suppress_st_warning=True,allow_output_mutation=True)  #przetrzymuje w cache zmienną a potem ją modyfikuję
def get_w():
    st.write('Cache miss - the first run')   
    return pd.DataFrame(data=[9999], columns=['output']) #trzeba zwracać object - do zbadania dlaczego na int nie działa

@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def get_database_connection():
    st.write('DB connection cache miss - the first run')  
    c = sql3.connect('BAZA_imf.db', check_same_thread=False)
    #c = conn.cursor()   
    return c


def page_imf_gdp():
    s=31
    st.subheader("IMF gdp")
    with st.spinner("Loading data ..."):
        conn=get_database_connection()
        #st.write(conn)
        pkb_pct=pd.read_sql('select * from imf_indicators where country=\'Poland\' and indicators=\'NGDP_RPCH\'',conn)
        pkb_usd=pd.read_sql('select * from imf_indicators where country=\'Poland\' and indicators=\'NGDPD\'',conn)
        pkb_usd_pcapita=pd.read_sql('select * from imf_indicators where country=\'Poland\' and indicators=\'NGDPDPC\'',conn)
        time.sleep(1)
        #st.dataframe(pl_pkb)

    f1 = px.bar(pkb_pct, x="period", y='value',color='value' ,color_continuous_scale='RdYlGn')
    f1.update_layout(
        plot_bgcolor='rgb(240,240,240)',
        title={
            'text': "GDP, constant prices, precentage change",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="years",
        yaxis_title="% YoY",
        legend_title="Legend Title"    
        )

    f2 = px.bar(pkb_usd, x="period", y='value',color='value' ,color_continuous_scale='Geyser')
    f2.update_layout(
        plot_bgcolor='rgb(240,240,240)',
        title={
            'text': "GDP, current prices, USD bn",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="years",
        yaxis_title="USD bn",
        legend_title="Legend Title"    
        )

    f3 = px.bar(pkb_usd_pcapita, x="period", y='value',color='value' ,color_continuous_scale='Geyser')
    f3.update_layout(
        plot_bgcolor='rgb(240,240,240)',
        title={
            'text': "GDP per capita, current prices, USD",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="years",
        yaxis_title="USD per capita",
        legend_title="Legend Title"    
        )

    st.plotly_chart(f1, use_container_width =True)
    col = st.beta_columns(2)
    with col[0]:
        st.plotly_chart(f2, use_container_width =True)
    with col[1]:
        st.plotly_chart(f3, use_container_width =True)

    return s



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
    
    with st.beta_expander("Portfele"):
        with st.beta_container():
            st.write("This is inside the container")
            col = st.beta_columns(6)
            with col[0]:
                st.button('pfo 1__________')
            with col[1]:
                st.button('pfo 2          ')
            with col[5]:
                st.button('Mortgage loans')
    
    with st.beta_expander("See explanation"):
        st.write("OUT of container - with expander")           
    
    st.write("OUT of container.")    
    return s


if __name__ == "__main__":
    main()