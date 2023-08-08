import streamlit as st
import numpy as np
from src.mechanismTemplate import MechanismTemplate


class Shifting(MechanismTemplate):

    # Returns data modified
    # Description: Values from numerical columns chosen sare modified in circular way and in function of the value of offset given

    def create_form(self):
        self.offset = st.number_input(label="Offset", value=0, help="Offset")

    def apply_mech(self, col_to_anonymize: list):
        for col in col_to_anonymize:
            st.session_state['df_anonymize'][col] = np.roll(st.session_state['df_anonymize'][col], self.offset)
