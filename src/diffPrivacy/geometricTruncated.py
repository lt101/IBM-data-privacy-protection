"""
reference: https://diffprivlib.readthedocs.io/en/latest/index.html

The truncated geometric mechanism, where values that fall outside a pre-described range are mapped back to the closest point within the range.
"""
import streamlit as st
from diffprivlib.mechanisms import GeometricTruncated as GeoTruncLib
from src.mechanismTemplate import MechanismTemplate


class GeometricTruncated(MechanismTemplate):

    def create_form(self):
        """
         @brief Creates the form for Privacy parameter. @ In None @ Out form st. Variable the form to
        """
        self.eps = st.number_input(key="epsilon", label="epsilon", value=0.0, min_value=0.0, help="Privacy parameter epsilon for the mechanism. Must be in (0, ∞].")
        self.sens = st.number_input(key="sensitivity", label="sensitivity", value=1, min_value=0, help="The sensitivity of the mechanism. Must be in [0, ∞).")
        self.up = st.number_input(key="upper", label="upper", value=0, help="The upper bound of the mechanism.")
        self.low = st.number_input(key="lower", label="lower", value=0, help="The lower bound of the mechanism.")
        self.rand = st.number_input(key="random_state", label="random_state", value=0, min_value=0, help="(Optional) Controls the randomness of the mechanism. To obtain a deterministic behaviour during randomisation, random state has to be fixed to an integer.")


    def apply_mech(self, col_to_anonymize: list):
        """
         @brief Apply mechanisms to columns. This is a wrapper for : func : ` ge trunclib. GeoTruncLib. randomise `
         @param col_to_anonymize list of column names to
        """
        # This function will generate a randomized geographical truncation library for each column in col_to_anonymize.
        for col in col_to_anonymize:
            dp_mech = GeoTruncLib(epsilon=self.eps, sensitivity=self.sens, lower=self.low, upper=self.up, random_state=self.rand)
            st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].map(
                lambda x: dp_mech.randomise(int(float(x))))

