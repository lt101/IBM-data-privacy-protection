# Rename columns and return form. This is a hack to allow users to rename columns. We don't want to use FormBuilder. column_to_change because it's called from a form builder
# This is a hack to allow users to rename columns. We don't want to use FormBuilder. column_to_change because it's the only method that can be called from a form
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

# Preview page layout
st.set_page_config(layout="wide")
st.title("Data preview")

if 'df_preview' not in st.session_state:
    st.warning('Please go back to the Upload page and select the data.')
else:

    # Column renaming
    col_a, col_b = st.columns(2)
    with col_a:
        data = st.session_state['df_preview']
        with st.form(key="form_rename"):
            col_to_change = st.selectbox("Column to change", data.columns)
            new_col_name = st.text_input("New name", value="")
            submit_button = st.form_submit_button(label='Save')

    if submit_button:
        st.session_state['df_preview'] = st.session_state['df_preview'].rename(columns={col_to_change: new_col_name})
        st.experimental_rerun()

    # Column to upper/lower case
    with col_b:
        with st.form(key="form_case"):
            col_to_case = st.selectbox("Column to change", data.columns)
            case = st.radio(
                "Upper/lower case",
                ('Uppercase', 'Lowercase'), horizontal=True)
            submit_case = st.form_submit_button(label='Save')

    if submit_case:
        if case == 'Uppercase':
            try:
                st.session_state['df_preview'][col_to_case] = st.session_state['df_preview'][col_to_case].str.upper()
                st.experimental_rerun()
            except AttributeError:
                st.error('Cannot capitalize this column : invalid data type')
        else:
            try:
                st.session_state['df_preview'][col_to_case] = st.session_state['df_preview'][col_to_case].str.lower()
                st.experimental_rerun()
            except AttributeError:
                st.error('Cannot lowercase this column : invalid data type')

    # Create dataframe grid
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_side_bar()  # Add a sidebar
    gb.configure_selection('multiple', use_checkbox=True,
                           groupSelectsChildren="Group checkbox select children")  # Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        data,
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

    # Display Dataframe general info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("Filename: " + st.session_state['df.filename'])
    with col2:
        st.write("Rows: " + str(data.shape[0]))
    with col3:
        st.write("Columns: " + str(data.shape[1]))
    with col4:
        st.write("Size: " + str(round(data.memory_usage(deep=True).sum() / 1024)) + " KB")
