# Generate and display a data profile report. It is necessary to import streamlit_pandas_profiling in order to get the data
from streamlit_pandas_profiling import st_profile_report
import streamlit as st
import ydata_profiling  # Do not remove, necessary to use profile_report() method


# Profile page layout
st.set_page_config(layout="wide")
st.title("Data profile")

if 'df' not in st.session_state:
    st.warning('Please go back to the Upload page and select the data.')
else:
    df = st.session_state['df']
    # Generate profile report
    pr = df.profile_report()
    st_profile_report(pr)
    export = pr.to_html()
    st.download_button(label="Download Full Report", data=export, file_name='report.html')
