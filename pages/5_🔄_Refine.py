# This is the heart of the code. We need to careful about the order of the arguments so that we don't have to worry about them
import streamlit as st
import numpy as np
import pandas as pd
from src.formatting import Formatter
from st_aggrid import AgGrid, GridOptionsBuilder
from src.constants import FORMAT_TYPES
import src.JPI






# Refine page layout
st.set_page_config(layout="wide")
st.title("Refining")

if 'df_format' not in st.session_state:
    st.warning('Please go back to the Upload page and select the data.')
else:
    # Column formatting
    df = st.session_state['df_format']
    col_a, col_b = st.columns(2)
    with col_a:
        with st.form(key="form_format"):
            col_to_format = st.selectbox("Column to format", df.columns)
            format_type = st.selectbox("Format type", FORMAT_TYPES)
            submit_format = st.form_submit_button(label='Format')

        

    if submit_format:
        try:
            st.session_state['df_format'][col_to_format] = st.session_state['df'][col_to_format].copy()
            f = Formatter()
            f.apply_format(format_type, col_to_format)
            st.session_state['df_format'][col_to_format] = st.session_state['df_format'][col_to_format].replace(np.nan,
                                                                                                                "null").copy()
        except AttributeError:
            st.error('Cannot format this column : invalid data type')
        except TypeError:
            st.error('Cannot format this column : invalid data type')

    # Reset column
    with col_b:

        with st.form(key="type_id"):
            sample_size_input = st.number_input('Sample size', min_value=0.05, max_value=1.0, step=0.05, value=src.JPI.DEFAULT_SAMPLE_SIZE)
            submit_identify_type = st.form_submit_button(label='Identify data types')

        with st.form(key="form_reset"):
            col_to_reset = st.selectbox("Column to reset", df.columns)
            submit_reset = st.form_submit_button(label='Reset column')

    if submit_reset:
        st.session_state['df_format'][col_to_reset] = st.session_state['df'][col_to_reset].copy()
    
    if submit_identify_type:
        
        with src.JPI.JPI() as jpi:
            st.session_state['df_format'] = st.session_state['df'].copy()
            jpi.identify_type(st.session_state['df_format'],sample_size_input)
            types = pd.DataFrame({'Column': st.session_state['df_format'].columns, 'Type': jpi.data_types})
            st.dataframe(types.T)
            

    # Create dataframe grid
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_side_bar()  # Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True,
                           groupSelectsChildren="Group checkbox select children")  # Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=False,
        theme='alpine',  # Add theme color to the table
        enable_enterprise_modules=True,
        height=600,
        width='100%',
        reload_data=True
    )

    inter_cols_pace, col2 = st.columns((11, 1))
    with col2:
        submit_reset_all = st.button(label='Reset dataset')

    if submit_reset_all:
        st.session_state['df_format'] = st.session_state['df'].copy()
        st.experimental_rerun()
