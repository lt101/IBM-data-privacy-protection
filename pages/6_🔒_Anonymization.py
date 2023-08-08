import streamlit as st
import src.JPI
from src.diffPrivacy.DPMechFactory import DPMechFactory
from src.masking.maskingFactory import MaskingFactory
from src.encryption import Encryption
from src.tokenization import Tokenizer
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import pandas as pd

# Anonymization page layout
st.set_page_config(layout="wide")
st.title("Anonymization")
st.markdown("***")

def applyMech(col_to_anonymize):
    """
     @brief Applies mech to a column. This is a wrapper around apply_mech to catch errors that are raised when Epsilon and Delta are zero
     @param col_to_anonymize name of column to
    """
    try:
        mech.apply_mech(col_to_anonymize)
        st.session_state['selected_columns'] = col_to_anonymize
    except ValueError:
        st.error("Epsilon and Delta cannot both be zero | Lower bound must not be greater than upper bound")   
    except TypeError:
        st.error("Epsilon and Delta cannot both be zero | Lower bound must not be greater than upper bound")         
    except KeyError:
        st.error("Epsilon and Delta cannot both be zero | Lower bound must not be greater than upper bound")

def get_vuln_cols(vulnerabilities):
    """
     @brief Get vulnerabilities from anonymize. This is a helper function to get the quasi - identifiers and identifiers for a list of vulnerabilities
     @param vulnerabilities a list of vulnerabilities
     @return a tuple of two lists : 1
    """
    identifiers = []
    quasi_identifiers = []
    # Add quasi identifiers to identifiers.
    for col in vulnerabilities:
        # Add identifiers to identifiers.
        if len(col) > 1:
            q = [st.session_state['df_anonymize'].columns[i] for i in col]
            quasi_identifiers.append(', '.join(q))
        else:
            identifiers.append(st.session_state['df_anonymize'].columns[col[0]])
    return identifiers, quasi_identifiers
  
# Verify if the file is uploaded
# This function is used to select the data to be uploaded.
if 'df_anonymize' not in st.session_state:
    st.warning('Please go back to the Upload page and select the data.')
else:
    submit_button = 'submit_button'
    col_a, col_b, col_f = st.columns(3)
    mech = None
    with col_a:
        st.subheader("Method selection")
        # Anonymization type selection
        anonymization_type = st.selectbox("Anonymization type", ('Differential privacy', 'Masking', 'Tokenization and Encryption'))

        # Mechanism selection
        # The anonymization type is one of the following two types Diffential privacy Masking Masking Tokenization Encryption Encryption Fernet
        if anonymization_type == 'Differential privacy':
            dp_mech = st.selectbox("Differential privacy mechanism", ('Geometric truncated', 'Exponential', 'Gaussian', 'Laplace', 'Snapping', 'Staircase', 'Uniform'))
            mech = DPMechFactory().create_mechanism(dp_mech)
            col_to_anonymize = st.multiselect("Columns to anonymize", st.session_state['df_anonymize'].select_dtypes(include=['float', 'int']).columns)

        elif anonymization_type == 'Masking':
            dp_mech = st.selectbox("Masking mechanism", ('Binning','Generalization', 'Prefix preservation', 'Date or time', 'Shifting'))
            mech = MaskingFactory().create_mechanism(dp_mech)
            # Select columns to anonymize for the current session state
            if(dp_mech == 'Binning'):
                col_to_anonymize = st.multiselect("Columns to anonymize", st.session_state['df_anonymize'].select_dtypes(include=['float', 'int']).columns)
            elif (dp_mech == 'Date or time'):
                date_cols = [col for col in st.session_state['df_anonymize'] if 'date' in col.lower()]
                col_to_anonymize = st.multiselect("Columns to anonymize", st.session_state['df_anonymize'][date_cols].columns)
            else:
                col_to_anonymize = st.multiselect("Columns to anonymize", st.session_state['df_anonymize'].columns)
            
        elif anonymization_type == 'Tokenization and Encryption':
            dp_mech = st.selectbox("Chose mechanism", ('Tokenization', 'Encryption (Fernet)'))
            # This function is used to perform the encryption and tokenization operations.
            if dp_mech == 'Encryption (Fernet)':
                encryption = Encryption()
                operation = st.selectbox("Chose operation to perform", ('Encrypt', 'Decrypt'))
                col_to_anonymize = st.multiselect("Columns to anonymize", st.session_state['df_anonymize'].columns)
                # Decrypt Encrypt Encrypt Encrypt Encrypt Encrypt Encrypt Encrypt Encrypt Encrypt Encrypt
                if operation == 'Decrypt' :
                    encryption.decrypt(col_to_anonymize)
                elif operation == 'Encrypt':
                    encryption.encrypt(col_to_anonymize)
            else:
                tokenization = Tokenizer()
                operation = st.selectbox("Chose operation to perform", ('Tokenize', 'Retrive'))
                col_to_anonymize = st.multiselect("Columns to anonymize", st.session_state['df_anonymize'].columns)
                # Tokenize Retrive Retrive Tokenize Retrive Retrive Tokenize Retrive
                if operation == 'Tokenize':
                    tokenization.tokenize(col_to_anonymize)
                elif operation == 'Retrive':
                    tokenization.de_tokenize(col_to_anonymize)

        

        # Add anonymization button to the table
        if col_to_anonymize:
            st.markdown("***")
            space_1, col, space_2 = st.columns((6, 4, 4))

            with col:
                if anonymization_type == 'Differential privacy' or anonymization_type == 'Masking':
                # Anonymization button
                    submit_button = st.button(label='Anonymize', type="primary", on_click=applyMech, args=(col_to_anonymize,))
        else:
            st.warning('Please select at least one column to anonymize')
        
        

    with col_b:
        # Create a form for the method parameters
        if mech != None:
            st.subheader("Method parameters")
            form = mech.create_form()  # Generate form for mechanism parameters

    with col_f:
        st.subheader('Identifiers and Quasi-Identifiers')
        k_value = st.number_input(label='k-value',min_value=1,step=1,value=1)
        n_threads = st.number_input(label='number of threads',min_value=1,step=1,value=1)
        submit_identify_vuln = st.button(label='Identify vulnerabilities')
        # submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_identify_vuln submit_vuln_vuln submit_vuln_vuln submit_vuln
        if submit_identify_vuln:
            with src.JPI.JPI() as jpi:
                jpi.identify_vulnerabilities(st.session_state['df_anonymize'],k_value,n_threads)
                identifiers, quasi_identifiers = get_vuln_cols(vulnerabilities=jpi.vulnerabilities)
                with st.expander("Show identifiers"):
                    df_identifiers = pd.DataFrame({'Identifiers': identifiers})
                    st.write(df_identifiers.T)
                with st.expander("Show quasi-identifiers"):
                    df_quasi = pd.DataFrame({'Quasi-Identifiers': quasi_identifiers})
                    st.write(df_quasi.T)

    # Reset column
    col_a, col_b = st.columns((2, 10))
    with col_a:
        col_to_reset = st.selectbox("Column to reset", st.session_state['df_anonymize'].columns)

    col_c, col_d, col_e = st.columns((1, 5, 1))
    with col_c:
        submit_reset = st.button(label='Reset column')
        # if submit_reset is true the session_state df_anonymize col_to_reset is set to the current value of the column to reset.
        if submit_reset:
            st.session_state['df_anonymize'][col_to_reset] = st.session_state['df'][col_to_reset].copy()
    with col_e:
        submit_reset_all = st.button(label='Reset dataset', help="Reset all columns to original values")
        # if submit_reset_all is true the session_state df_anonymize is set to the session_state df_anonymize and the experimental_rerun is set to the same value as the session_state df_anonymize.
        if submit_reset_all:
            st.session_state['df_anonymize'] = st.session_state['df'].copy()
            st.experimental_rerun()

    # Create dataframe grid
    gb = GridOptionsBuilder.from_dataframe(st.session_state['df_anonymize'])
    gb.configure_side_bar()  # Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True,
                           groupSelectsChildren="Group checkbox select children")  # Enable multi-row selection

    cellstyle_jscode = JsCode("""
     function(params) {
         return {
             'backgroundColor': 'rgb(77, 195, 255, 0.25)'
         }
     };
     """)

    # Configures the selected columns in the session state.
    if 'selected_columns' in st.session_state:
        # Configures the cell style of each selected column.
        for col in st.session_state['selected_columns']:
            gb.configure_column(col, cellStyle=cellstyle_jscode)

    gridOptions = gb.build()

    grid_response = AgGrid(
        st.session_state['df_anonymize'],
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=False,
        theme='alpine',  # Add theme color to the table
        enable_enterprise_modules=True,
        height=600,
        width='100%',
        reload_data=True,
        allow_unsafe_jscode=True
    )
