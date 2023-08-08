from cryptography.fernet import Fernet
import streamlit as st
from io import StringIO

class Encryption:
    def __init__(self):
        """
         @brief Initialize Fernet object from key file. This is called by __init__ and should not be called directly
        """
        with open('utils/filekey.key', 'rb') as filekey:
            key = filekey.read()
        self.fernet = Fernet(key)

    def encrypt(self,col_to_anonymize: list):
        """
         @brief Encrypt a list of columns using Fernet. This is useful for anonymizing data that is stored in the session
         @param col_to_anonymize list of columns to
        """
        # Add the columns to the session_state df_anonymize.
        for col in col_to_anonymize:
            st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].map(lambda x: (self.fernet.encrypt(str(x).encode("ISO-8859-1"))))


    def decrypt(self,col_to_decrypt: list):
        """
         @brief Decrypt a list of columns. Decryption is done in place and will be stored in session_state
         @param col_to_decrypt list of columns to
        """
        # Decrypts the columns in the session_state df_anonymize.
        for col in col_to_decrypt:
            st.session_state['df_anonymize'][col] = st.session_state['df_anonymize'][col].map(lambda x: (self.fernet.decrypt(x.decode("ISO-8859-1"))))



#def decrypt(uploaded_file):
#    decrypted = 
#    return StringIO(decrypted.decode("ISO-8859-1"))
