from matplotlib import pyplot as plt
import streamlit as st
from src.filemanager import read_data_file

# Returns outliers for a given dataframe
def boxplot_outliers(df):
    """
     @brief Plots boxplots of data. This is a function to be used in tests. It takes a dataframe as input and plots the data in a boxplot.
     @param df The dataframe that is to be plotted.
     @return A tuple containing the plot and the outlier_by_column list of the column that are outliers
    """
    fig, ax = plt.subplots()
    numeric_columns = df.select_dtypes(include=['float', 'int']).columns
    df[numeric_columns].plot(kind='box', ax=ax, figsize=(20, 10))
    plt.show()
    outlier_by_column = []
    # This function calculates the outliers of the outliers of the columns in the dataframe.
    for col in numeric_columns:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        num_outliers = len(outliers)

        total_rows = len(df)
        pct_outliers = (num_outliers / total_rows) * 100
        outlier_by_column.append(pct_outliers)
        print(f"Column '{col}': {num_outliers} outliers ({pct_outliers:.2f}%)")
    return outlier_by_column

# Save uploaded file as dataframe
decrypted_uploaded_file = None
uploaded_file = st.file_uploader("Choose a file", type=["csv", "json", "xml", "xlsx"])
# This function is used to save the uploaded file
if uploaded_file is not None:
    st.session_state['df.filename'] = uploaded_file.name
    #if "Encrypted" in uploaded_file.name:   # If uploaded file is encrypted, decrypt first
    #    decrypted_uploaded_file = decrypt(uploaded_file)
    data = read_data_file(uploaded_file,decrypted_uploaded_file)

    # verif_load(data)
    st.session_state['file'] = decrypted_uploaded_file if decrypted_uploaded_file is not None else uploaded_file
    st.success('Successfully uploaded file', icon="✅")
    df = data
    
    # Replace outliers with median or mean value of the column
    outliers_value = boxplot_outliers(df)
    numeric_columns = df.select_dtypes(include=['float', 'int']).columns
    # This function is used to fill the dataframe with the median and mean values.
    for i in range(len(numeric_columns)):
        # If outliers_value i is greater than 5 median median median median median median mean mean
        if outliers_value[i] >= 5:
            df[numeric_columns[i]].fillna(round(df[numeric_columns[i]].median(),1), inplace=True)
        else:
            df[numeric_columns[i]].fillna(round(df[numeric_columns[i]].mean(),1), inplace=True)
            
    df.isnull().sum()
    # Create copies of dataframe in session state for different pages
    st.session_state['df'] = df
    st.session_state['df_preview'] = df.copy()
    st.session_state['df_format'] = df.copy()
    st.session_state['df_anonymize'] = df.copy()

