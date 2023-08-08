import codecs
import csv
import json
from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import pandas_read_xml as pdx
#from src.encryption import decrypt

# Returns data read from a specific type of file
def read_data_file(fname, isDecrypted):
    """
     @brief Read a data file. This is a wrapper around the read_ * functions to handle file formats that are known to the file system.
     @param fname Name of the file to read. The extension must be one of the following : csv son xml lsx
     @param isDecrypted If True the file is
    """
    # Returns a pandas. DataFrame object.
    if fname.name[-3:] == 'csv': 
        return pd.read_csv(isDecrypted if isDecrypted is not None else fname,encoding="ISO-8859-1", on_bad_lines='skip', sep=None,engine='python') 
    elif fname.name[-3:] == 'son':
            return pd.read_json(fname) 
    elif fname.name[-3:] == 'xml':
            return pd.read_xml(fname)
    elif fname.name[-3:] ==  'lsx':
            return pd.read_excel(fname)

# Returns dictionnary where each column is converted to a list 
def read_generalization_file(fname):
    """
     @brief Read generalization file. This can be csv json xml lsx or excel depending on the file extension
     @param fname name of file to read
     @return data frame or None if not recognised ( file extension not recognized ) or a pandas. DataFrame if
    """
    # Returns a pandas. DataFrame object.
    if fname.name[-3:] == 'csv': 
        return pd.read_csv(fname,encoding="utf-8", on_bad_lines='skip', sep=None,engine='python') 
    elif fname.name[-3:] == 'son':
            return pd.read_json(fname) 
    elif fname.name[-3:] == 'xml':
            return pd.read_xml(fname)
    elif fname.name[-3:] ==  'lsx':
            return pd.read_excel(fname)

def from_df_to_dict(df):
    """
     @brief Convert a pandas DataFrame to a dictionary. This is useful for debugging the data returned by to_dict ('list')
     @param df The pandas DataFrame to convert
     @return A dictionary with the data from to_dict ('list') and print ('df '
    """
    df = df.to_dict('list')
    print(df)
    return df
