import streamlit as st
import numpy as np
import pandas as pd
from src.mechanismTemplate import MechanismTemplate

class DateTime(MechanismTemplate):

    # Returns data modified
    # Description: Dates value from columns are modified by generalization to year-month-day or randomization dates or shifting by one day

    def create_form(self):
        """
         @brief Create and fill form with anonymization options. @untestable - just draws nothing @return
        """
        self.option = st.selectbox("Anonymization type", ('Generalization to year', 'Generalization to month', 'Generalization to day', 'Randomize dates', 'Shift by one day'))

    def apply_mech(self, col_to_anonymize: list):
        """
         @brief Applies mechanisms to a list of columns. This is a wrapper around : meth : ` ~scikit_learn. model. Model. apply_mech ` to convert datetime columns to year month or day
         @param col_to_anonymize list of columns to
        """
        # This method is used to convert the session_state df_anonymize column to anonymize.
        for col in col_to_anonymize:
            st.session_state['df_anonymize'][col] = pd.to_datetime(st.session_state['df_anonymize'][col], format='%Y-%m-%d', errors='coerce')
            # generalizes to year, month or day
            # This method is used to set the session state of the session_state.
            if self.option == 'Generalization to year':
                st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].dt.year
            elif self.option == 'Generalization to month':
                st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].dt.month
            elif self.option == 'Generalization to day':
                st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].dt.day
            # randomizes date
            elif self.option == 'Randomize dates':
                st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col] + pd.DateOffset(np.random.randint(1, 8))
            # shifts by one day
            elif self.option == 'Shift by one day':
                st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col] + pd.DateOffset(days=1)