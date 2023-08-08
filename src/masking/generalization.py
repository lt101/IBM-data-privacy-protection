import streamlit as st
import numpy as np
import pandas as pd
from src.mechanismTemplate import MechanismTemplate
from src.filemanager import read_generalization_file
from src.filemanager import from_df_to_dict
from src.formatting import SYMBOL
import random

class Generalization(MechanismTemplate):


    # Returns data modified
    # Description: Values are replaced  with one of their parent and it is support for static and code-based hierarchies

    def create_form(self):
        """
         @brief Create form to upload generalization file to Snapchat. This is called by Snapchat when the form is
        """
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "json", "xml", "xlsx"])
        # Read generalization file and set the dataframe to the data
        if uploaded_file is not None:
            data = read_generalization_file(uploaded_file)
            #if "Encrypted" in uploaded_file.name:  # If uploaded file is encrypted, decrypt first
               # decrypted_uploaded_file = decrypt(uploaded_file)
            self.dataframe = from_df_to_dict(data)

    # Assiocates value of column to the corresponding category of data
    def generalize_value(self, val):
        """
         @brief Generalize values based on whether they are in the data. This is used to make decisions about which levels of data should be used for a particular value
         @param val The value to be generalized
         @return The generalized value or the original value if it's not in the data set. In other words it returns
        """
        # Return the level of the dataframe.
        for lvl in self.dataframe.keys():
            # Return the lvl of the dataframe
            if val in self.dataframe[lvl]:
                return lvl     
        return val

    def apply_mech(self, col_to_anonymize: list):
        """
         @brief Apply mechanisms to a list of columns. This is a wrapper around : meth : ` generalize_value `
         @param col_to_anonymize list of columns to
        """
        # Apply generalize_value to each column in the column_to_anonymize.
        for col in col_to_anonymize:
            st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].apply(lambda x: self.generalize_value(x))
