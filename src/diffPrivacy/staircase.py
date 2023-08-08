"""
reference: https://diffprivlib.readthedocs.io/en/latest/index.html

The staircase mechanism in differential privacy.

The staircase mechanism is an optimisation of the classical Laplace Mechanism (Laplace), described as a “geometric mixture of uniform random variables”. Paper link: https://arxiv.org/pdf/1212.1186.pdf
"""
import streamlit as st
import math
from diffprivlib.mechanisms import Staircase as StaircaseLib
from src.mechanismTemplate import MechanismTemplate


class Staircase(MechanismTemplate):

    def create_form(self):
        self.eps = st.number_input(key="epsilon", label="epsilon", value=0.0, min_value=0.0, help="Privacy parameter epsilon for the mechanism. Must be in (0, ∞].")
        self.sens = st.number_input(key="sensitivity", label="sensitivity", value=0, min_value=0, help="The sensitivity of the mechanism. Must be in [0, ∞).")
        self.gamma = st.number_input(key="gamma", value=(1 / (1 + math.exp(self.eps/2))), min_value=0.0, max_value=1.0, label="gamma", help="Value of the tuning parameter gamma for the mechanism. Must be in [0, 1].")
        self.rand = st.number_input(key="random_state", label="random_state", value=0, min_value=0, help="Controls the randomness of the mechanism. To obtain a deterministic behaviour during randomisation, random_state has to be fixed to an integer.")

    def apply_mech(self, col_to_anonymize: list):
        for col in col_to_anonymize:
            col_type = float if st.session_state['df_anonymize'].dtypes[col] == 'float64' else int
            dp_mech = StaircaseLib(epsilon=self.eps, sensitivity=self.sens, gamma=self.gamma, random_state=self.rand)
            st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].map(lambda x: (col_type)(dp_mech.randomise(x)))

