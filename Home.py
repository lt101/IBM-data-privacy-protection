import streamlit as st
import streamlit_authenticator as stauth
import yaml
from src.components.header import header
from src.components.footer import footer
import pandas as pd

## Set page title and icon
st.set_page_config(
    page_title="PolyBM Data",
    page_icon="🆔",
)
st.markdown(header, unsafe_allow_html=True)
st.markdown(footer, unsafe_allow_html=True)
st.markdown(header, unsafe_allow_html=True)
st.markdown(footer, unsafe_allow_html=True)

## Hide menu if not logged in
def hide_menu():
    st.sidebar.info("Please login to access all features")
    hide_bar = """
           <style>
           [data-testid="stSidebarNav"] {visibility:hidden;}
           </style>
           """
    st.markdown(hide_bar, unsafe_allow_html=True)
   


## Get and hash passwords
hashed_passwords = stauth.Hasher(['UserTest', 'AdminTest']).generate()
## Create a dictionary of users and passwords
with open('utils/passwords.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

## Authenticate user
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login('Login', 'main')

## Dynamically render home page according to login status
if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    if username == 'testAdmin':
        st.write(f'Welcome *{name}*')
    elif username == 'testUser':
        st.write(f'Welcome *{name}*')
    st.markdown(
        """
        PolyBM Data is a collaborative project between Polytechnique Montréal and IBM. 
        The application allows users to visualize, analyze and anonymize data. Users can also evaluate the performance of a machine learning model with raw and anonymized datasets.      
        ### How to use the app
        - Start by uploading a file in the Upload page
        - Choose any functionality in the sidebar
        - Changed datasets (through refining, anonymization, etc.) can be downloaded by right-clicking on the dataframe and exporting it.
        - Note: Not all functionalities are available as the app is currently under development! 
    """
    )
    
## If user is not logged in, render login page
else:
    hide_menu()
    if not authentication_status:
        st.error('Username/password is incorrect')