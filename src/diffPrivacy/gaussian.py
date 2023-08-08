"""
reference: https://diffprivlib.readthedocs.io/en/latest/index.html

The Gaussian mechanism in differential privacy.

"""
import streamlit as st
from diffprivlib.mechanisms import Gaussian as GaussLib
from src.mechanismTemplate import MechanismTemplate

class Gaussian(MechanismTemplate):

    def create_form(self):
        """
         @brief Creates the form for the Privacy Mechanism. @ In None @ Out form st. Variable the
        """
        self.eps = st.number_input(key="epsilon", label="epsilon", min_value=0.0, max_value=1.0, help="Privacy parameter epsilon for the mechanism. Must be in (0, 1].")
        self.sens = st.number_input(key="sensitivity", label="sensitivity", value=0, min_value=0, help="The sensitivity of the mechanism. Must be in [0, ∞).")
        self.delta = st.number_input(key="delta", label="delta", min_value=0.0, max_value=1.0, help="Privacy parameter delta for the mechanism. Must be in (0, 1].")
        self.rand = st.number_input(key="random_state", label="random_state", value=0, min_value=0, help="Controls the randomness of the mechanism. To obtain a deterministic behaviour during randomisation, random state has to be fixed to an integer.")
    
    def apply_mech(self, col_to_anonymize: list):
        """
         @brief Apply gaussian randomisation to columns in session_state. This is a wrapper around : py : func : ` ~gensim. models. gausslib. GaussLib. randomise `
         @param col_to_anonymize List of columns to
        """
        # Add a randomization of the given column to anonymize.
        for col in col_to_anonymize:
            col_type = float if st.session_state['df_anonymize'].dtypes[col] == 'float64' else int
            dp_mech = GaussLib(epsilon=self.eps, sensitivity=self.sens, delta=self.delta, random_state=self.rand)
            st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].map(lambda x: (col_type)(dp_mech.randomise(x)))

