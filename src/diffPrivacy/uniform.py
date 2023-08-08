"""
reference: https://diffprivlib.readthedocs.io/en/latest/index.html

The Uniform mechanism in differential privacy.

This emerges as a special case of the LaplaceBoundedNoise mechanism when epsilon = 0. Paper link: https://arxiv.org/pdf/1810.00877.pdf
"""
import streamlit as st
from diffprivlib.mechanisms import Uniform as UniformLib
from src.mechanismTemplate import MechanismTemplate


class Uniform(MechanismTemplate):

    def create_form(self):
        self.delta = st.number_input(key="delta", label="delta", value=0.0, min_value=0.0, max_value=0.5, format="%f", help="Privacy parameter delta for the mechanism. Must be in (0, 0.5].")
        self.sens = st.number_input(key="sensitivity", label="sensitivity", value=0, min_value=0, help="The sensitivity of the mechanism. Must be in [0, ∞).")
        self.rand = st.number_input(key="random_state", label="random_state", value=0, min_value=0, help="Controls the randomness of the mechanism. To obtain a deterministic behaviour during randomisation, random state has to be fixed to an integer.")

    def apply_mech(self, col_to_anonymize: list):
        for col in col_to_anonymize:
            col_type = float if st.session_state['df_anonymize'].dtypes[col] == 'float64' else int
            dp_mech = UniformLib(delta=self.delta, sensitivity=self.sens, random_state=self.rand)
            st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].map(lambda x: (col_type)(dp_mech.randomise(x)))

