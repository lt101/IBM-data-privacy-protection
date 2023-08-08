import streamlit as st
import numpy as np
import pandas as pd
from src.mechanismTemplate import MechanismTemplate


class Binning(MechanismTemplate):

    # Returns data modified
    # Description: Values from numerical columns chosen are replaced by bins created by number of bins given

    def create_form(self):
        """
         @brief Create form for number of bins ( 0 by default ) @ In None @ Out form object form object for
        """
        self.nBins = st.number_input(label='Bins', value=0, help="Number of bins")

    def apply_mech(self, col_to_anonymize: list):
        """
         @brief Applies mech to columns in df_anonymize. It cuts the data to be a multiple of nBins
         @param col_to_anonymize list of columns to
        """
        # This function is used to calculate the bin edges of the session_state df_anonymize.
        for col in col_to_anonymize:
            bin_edges = np.linspace(st.session_state['df_anonymize'][col].min(), st.session_state['df_anonymize'][col].max(), self.nBins*2)
            st.session_state['df_anonymize'][col] = pd.cut(st.session_state['df_anonymize'][col], bin_edges,include_lowest=True).astype(str)
