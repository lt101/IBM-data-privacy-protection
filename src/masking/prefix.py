import streamlit as st
import re
import random
from src.formatting import SYMBOL
from src.mechanismTemplate import MechanismTemplate


class Prefix(MechanismTemplate):

    # Returns data modified
    # Description: Values from columns chosen are modified in function of the number of prefix caracters to mask with symbol regex

    def create_form(self):
        self.nPrefix = st.number_input(label="Number of prefix caracters to mask", value=0, help="Number of prefix caracters to mask")

    def apply_mech(self, col_to_anonymize: list):
        for col in col_to_anonymize:
            if not isinstance(st.session_state['df_anonymize'][col], str):
                st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].astype(str)
            st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].apply(
                lambda item: re.sub(item[0:self.nPrefix], ''.join(random.choices(SYMBOL, k=self.nPrefix)), str(item)))
