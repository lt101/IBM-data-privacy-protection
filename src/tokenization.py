import streamlit as st
from io import StringIO
import random
import string

class Tokenizer:

    def tokenize(self,col_to_anonymize: list):
        """
         @brief Anonymize a list of columns. This is a wrapper around maping to be able to do something with the data
         @param col_to_anonymize list of columns to
        """
        # maping the columns to anonymize.
        for col in col_to_anonymize:
            st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].map(lambda x: self.maping(x))


    def de_tokenize(self,col_to_decrypt: list):
        """
         @brief Remove tokenization from a list of columns. This is useful for decrypting data that was generated by anonymize
         @param col_to_decrypt list of columns to
        """
        # Decrypts the columns in the session_state dictionary.
        for col in col_to_decrypt:
            st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].map(lambda x: st.session_state[x])
    
    def maping(self, value):
        """
         @brief Maps a value to a random token. This is used to prevent accidental mistakes in user input
         @param value The value to map to a random token
         @return A random token that can be used as a key in the session_state dictionary for the user input
        """
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        st.session_state[token] = value
        return token