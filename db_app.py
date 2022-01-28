import pandas as pd
import numpy as np
import copy

import streamlit as st

import sqlite3 as sql3
import pyodbc  as pydb
#https://www.sqlitetutorial.net/sqlite-sample-database

import plotly.express as px


def main():
    # eksperymenty http://awesome-streamlit.org/  ---> layout experiment

    st.sidebar.title(':clipboard: Filtry') #https://emojipedia.org/clipboard/
    add_filtr('Banki', 'banki_grupa', 'Peers', ['A', 'B', 'C','D','E','F'], ['C','D','E'], True )
    add_filtr('nazwa_grp', 'labelki_nazwa', 'domyslne_nazwa', ['q','w','e','r','t','y'], ['t','y'], False )

    f2=st.sidebar.expander("inne", expanded=True)
    f2.write('ciekawe')
    
    st.write(st.session_state['Banki'])
    st.write(st.session_state['nazwa_grp'])

def add_filtr(nazwa_grp, labelki_nazwa, domyslne_nazwa, labelki_wart, domyslne_wart, expanded_bool ):

    if domyslne_nazwa not in st.session_state:  #tutaj state to tylko słownik wartości
        st.session_state[domyslne_nazwa] = domyslne_wart
    if nazwa_grp not in st.session_state: #tutaj state to stan widget (odniesione przez key) to coś innego niż zmienna zwracana przez widget
        init_selection=st.session_state[domyslne_nazwa]  
    else:
        init_selection=st.session_state[nazwa_grp]


    f1=st.sidebar.expander(nazwa_grp, expanded=expanded_bool)
    f1_containter=f1.container()

    col = f1.columns(6)  #sąsiadujące przyciski
    alls= col[0].button('All',key=nazwa_grp+'1')
    allp= col[1].button(domyslne_nazwa,key=nazwa_grp+'2')

    if alls:  #powiązanie przycisków z listą wyboru
        selected_options =  f1_containter.multiselect('Wybierz:',
               labelki_wart,labelki_wart,key=nazwa_grp)
    elif allp:
        selected_options =  f1_containter.multiselect('Wybierz:',
                labelki_wart,st.session_state[domyslne_nazwa],key=nazwa_grp)               
    else:
        selected_options =  f1_containter.multiselect('Wybierz:',
                labelki_wart,init_selection ,key=nazwa_grp ) 



@st.cache(persist=True, suppress_st_warning=True,allow_output_mutation=True)  #przetrzymuje w cache zmienną a potem ją modyfikuję
def get_w():
    st.write('Cache miss - the first run')   
    return pd.DataFrame(data=[9999], columns=['output']) #trzeba zwracać object - do zbadania dlaczego na int nie działa

@st.cache(persist=True, suppress_st_warning=True,allow_output_mutation=True)
def get_database_connection():
    st.write('DB connection cache miss - the first run')  
    c = sql3.connect('BAZA_imf.db', check_same_thread=False)
    #c = conn.cursor()   
    return c



if __name__ == '__main__':
    main()