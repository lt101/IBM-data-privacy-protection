"""
reference: https://diffprivlib.readthedocs.io/en/latest/index.html

The Snapping mechanism for differential privacy.
"""
import streamlit as st
from diffprivlib.mechanisms import Snapping as SnappingLib
from src.mechanismTemplate import MechanismTemplate


class Snapping(MechanismTemplate):

    def create_form(self):
        self.eps = st.number_input(key="epsilon", label="epsilon", value=0.0, min_value=0.0, help="Privacy parameter for the mechanism. Must be in [2n, ∞], where n is the machine epsilon of the floating point type.")
        self.sens = st.number_input(key="sensitivity", label="sensitivity", value=0, min_value=0, help="The sensitivity of the mechanism. Must be in [0, ∞).")
        self.up = st.number_input(key="upper", label="upper", value=0, help="The upper bound of the mechanism.")
        self.low = st.number_input(key="lower", label="lower", value=0, help="The lower bound of the mechanism.")
        
    def apply_mech(self, col_to_anonymize: list):
        for col in col_to_anonymize:
            dp_mech = SnappingLib(epsilon=self.eps, sensitivity=self.sens, lower=self.low, upper=self.up) 
            st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].map(lambda x: dp_mech.randomise(x))

