"""
reference: https://diffprivlib.readthedocs.io/en/latest/index.html

The exponential mechanism for achieving differential privacy on candidate selection, as first proposed by McSherry and Talwar.

The exponential mechanism achieves differential privacy by randomly choosing a candidate subject to candidate utility scores, with greater probability given to higher-utility candidates.
"""
import streamlit as st
from diffprivlib.mechanisms import Exponential as ExpoLib
from src.mechanismTemplate import MechanismTemplate


class Exponential(MechanismTemplate):

    def create_form(self):
        """
         @brief Creates the form for the mechanical mechanism. It is used to define the parameters that are required for the mechanism
        """
        self.eps = st.number_input(key="epsilon", label="epsilon", value=0.0, min_value=0.0, help="Privacy parameter epsilon for the mechanism. Must be in (0, ∞].")
        self.sens = st.number_input(key="sensitivity", label="sensitivity", value=0, min_value=0, help="The sensitivity in utility values to a change in a datapoint in the underlying dataset.")
        self.monotonic = st.checkbox('Monotonic', help='Specifies if the utility function is monotonic, i.e. that adding an individual to the underlying dataset can only increase the values in utility.')

    def apply_mech(self, col_to_anonymize: list):
        """
         @brief Apply anonymization mechanism to data. This is a wrapper around : py : class : ` ExpoLib ` to randomise the data and store the result in session_state
         @param col_to_anonymize List of columns to
        """
        # This function creates anonymize matrix for each column in col_to_anonymize.
        for col in col_to_anonymize:
            col_type = float if st.session_state['df_anonymize'].dtypes[col] == 'float64' else int
            data_length = st.session_state['df_anonymize'][col].shape[0]
            dp_mech = ExpoLib(epsilon=self.eps, sensitivity=self.sens, utility=[1 for _ in range(data_length)], candidates=st.session_state['df_anonymize'][col].astype(float).tolist(), monotonic=self.monotonic)
            st.session_state['df_anonymize'][col] = [(col_type)(dp_mech.randomise()) for _ in range(data_length)]

