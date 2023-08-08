import re
import numpy as np
import pandas as pd
import streamlit as st
import datetime as dt
from src.constants import FORMAT_NAME, FORMAT_TYPES, FORMAT_DATE, FORMAT_NAS, FORMAT_EMAIL, FORMAT_ADDRESS, \
    FORMAT_PHONE, FORMAT_NUMBER, FORMAT_LOGIN, FORMAT_TEXT

# normalization forms. These determine how the str.normalize method converts non alphanum. characters
NFD = "NFD"
NFC = "NFC"
NFKD = "NFKD"
NFKC = "NFKC"

# regexes
NON_ALPHANUMERICAL = r"[^a-zA-Z0-9]"
NON_NUMERICAL = r"[^0-9]"
NUMERICAL = r"[0-9]+"
NON_EMAIL_CHAR = r"[^a-zA-Z0-9@.-]"
NON_ADDRESS_CHAR = r"[^a-zA-Z0-9-/_]|[hH].[nN][oO]."
ADDRESS_TEMP_SEPARATOR = "_"
EMAIL_FORMAT = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
APPARTMENT_FORMAT = r"[0-9]+-|[0-9]+/|[aA][pP][tT]_[0-9]+"
PHONE_NUM_FORMAT = r"[2-9][0-9]{2}[2-9][0-9]{6}"
DATE_FORMAT = r"[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])"
DATE_CHAR = r"[^0-9-]"
SPACES = r" +"
UNDERSCORES = r"_+"
SYMBOL = "(?<!^).(?=.+@)"
# date

DATE_SEP = "-"
YEAR = 0
MONTH = 1
DAY = 2
MAX_DATE = "9999-12-31"

# ssn
SSN_LENGTH = 9
SSN_REF = [1,2,1,2,1,2,1,2,1]
FORBIDDEN_SSN = ["123456780","000000000","888888880"]

# address
ABBREVIATIONS = {
    "AVENUE":"AV",
    "AVE":"AV",
    "BOULEVARD":"BLVD",
    "BOUL":"BLVD",
    "E":"EST",
    "EAST":"EST",
    "O":"OUEST",
    "WEST":"OUEST",
    "N":"NORD",
    "NORTH":"NORD",
    "S":"SUD",
    "SOUTH":"SUD",
    "AGGLOMERATION":"AGGLO",
    "CARREFOUR":"CARREF",
    "CENTRE":"CTRE",
    "CHEMIN":"CH",
    "IMPASSE":"IMP",
    "PLACE":"PL",
    "RANG":"RG",
    "ROUTE":"RT",
    "SAINT":"ST",
    "SAINTE":"STE",
    "MAC":"MC"
}
# phone number

PHONE_NUM_LENGTH = 10
NA_CALLING_CODE = "1"



# used to apply formatting functions on panda series
class Formatter:

        def __init__(self,normalization_form:str=NFD):
            """
             @brief Initialize the instance. This is called by __init__ and should not be called directly. Instead the constructor should be called.
             @param normalization_form The normalization form to use for
            """
            self.normalization_form =normalization_form

        def format_name(self, data:pd.Series)->pd.Series:
            """
             @brief Formats data to be used in name. This is a helper function for L { parse_name }.
             @param data The data to be formatted. Must be a : class : ` pandas. Series ` of strings.
             @return A : class : ` pandas. Series ` of strings with normalized names and capitalized letters. : 0.
            """
            data = data.apply(lambda x: np.nan if x == "" else x)
            data = data.str.normalize(self.normalization_form)
            data = data.apply(lambda x: re.sub(NON_ALPHANUMERICAL, "", x) if not pd.isnull(x) else x)
            data = data.str.upper()
            return data

        def check_date(self,date:str)->dt.datetime:
            """
             @brief Checks if a date is valid and returns it as a datetime object. This is a helper for : meth : ` get_date `
             @param date Date to check. Must be in YYYYMMDD format.
             @return Date as a datetime object or np. nan if invalid date is passed or not a valid date ( year month day
            """
            match = re.search(DATE_FORMAT,date)
            # Return a datetime object from the match string.
            if match is not None and date!=MAX_DATE:
                date = match.string
                date_vector = date.split(DATE_SEP)
                year = int(date_vector[YEAR])
                month = int(date_vector[MONTH])
                day = int(date_vector[DAY])
                try:
                    return dt.datetime(year,month,day)
                except(ValueError,TypeError):
                    return np.nan
            return np.nan

        def format_date(self,data:pd.Series)->pd.Series:
            """
             @brief Formats date to make it easier to read. This is a helper method for : meth : ` check_date `
             @param data Data to be formatted.
             @return Data with formatted date ( s ) as columns. If data is null it is returned as - is
            """
            data = data.apply(lambda x: re.sub(DATE_CHAR,"",x) if not pd.isnull(x) else x)
            data = data.apply(lambda x: self.check_date(x) if not pd.isnull(x) else x)
            return data

        def validate_ssn(self, ssn:str)->str:
            """
             @brief Validates SSN and returns it if valid. The validation is based on the sum of the refractive digits and the sum of the digits is equal to 10
             @param ssn String representation of the SSN
             @return String representation of the SSN or NaN if it is not valid for the user's account ( in this case we are trying to get a valid one
            """
            ssn_vector = [int(n) for n in ssn]
            sum = 0
            # Calculate the sum of the number of SSN digits and the reference digit of the SSN vector.
            for ssn_digit, ref_digit in zip(ssn_vector,SSN_REF):
                product = (ssn_digit * ref_digit) % 10 + (ssn_digit * ref_digit) // 10
                sum += product

            # Returns the SSN of the current SSN.
            if sum % 10 == 0 and ssn not in FORBIDDEN_SSN and len(ssn)==SSN_LENGTH:
                return ssn

            return np.nan

        def format_ssn(self,data:pd.Series)->pd.Series:
            """
             @brief Formats SSN to make it easier to read. This is a helper for : meth : ` validate_ssn `
             @param data Data to be formatted.
             @return Data with formatted SSN ( s ) in it's column ( s ). If data is empty it will be
            """
            data = data.apply(lambda x: re.sub(NON_NUMERICAL, "", x) if not pd.isnull(x) else x)
            data = data.apply(lambda x: self.validate_ssn(x) if not pd.isnull(x) else x)
            return data


        def validate_email(self, email:str)->str:
            """
             @brief Validate email and return it. This is a helper for : meth : ` get_email `.
             @param email The email to validate. It should be in the format defined in : attr : ` EMAIL_FORMAT `.
             @return The email if valid else NaN. : 0. 6 Added support for email format in Python 3.
            """
            match = re.search(EMAIL_FORMAT,email)
            # Returns the string representation of the match.
            if match is not None:
                return match.string
            return np.nan

        def format_email(self,data:pd.Series)->pd.Series:
            """
             @brief Formats data to be email. Normalizes data to normalization_form replaces non - email characters with spaces and validates email
             @param data Data to be formatted.
             @return Data formatted to be email ( uppercase ). The result is a Series of strings with each string being a valid
            """
            data = data.str.normalize(self.normalization_form)
            data = data.apply(lambda x: re.sub(NON_EMAIL_CHAR, '', x) if not pd.isnull(x) else x)
            data = data.apply(lambda x: self.validate_email(x) if not pd.isnull(x) else x)
            data = data.str.upper()
            return data

        def format_appartment_number(self, address:str)->str:
            """
             @brief Formats apartment number to be used in mail. It is possible to use'' as separator.
             @param address email address to be formatted. Must be in format'abcdefghijklmnopqrstuvwxyz '
             @return email address with appartment
            """
            match = re.search(APPARTMENT_FORMAT,address)
            appartment_num = ''
            # Return the address of the address.
            if not match is None:
                match = match.group()
                appartment_num = re.search(NUMERICAL,match).group()
                address = address.replace(match,'')
                address = appartment_num + "-" + address.replace('-','')
                address = re.sub(SPACES,' ',address)
            return address

        def format_abbreviation(self,address:str)->str:
            """
             @brief Formats an address to be used in email addresses. This is a helper method to make it easier to use in email addresses
             @param address The address to be formatted
             @return The formatted address as a string with each word replaced by its abbreviations if they are in the
            """
            address = address.split(' ')
            # Remove all ABBREVIATIONS from address.
            for index, a in enumerate(address):
                a = a.strip()
                # Get the address of the address.
                if ABBREVIATIONS.get(a) is not None:
                    address[index] = ABBREVIATIONS.get(a)
            address = ' '.join(address)
            return address


        def format_address(self,data:pd.Series)->pd.Series:
            """
             @brief Formats address to human readable format. This is a helper for format_address_from_data and format_address_from_data.
             @param data Data to be formatted. Should be a pandas Series.
             @return Data formatted as a string with no whitespace and special characters replaced with'_ '. If data is None it is returned as - is
            """
            data = data.apply(lambda x: np.nan if x=='' else x)
            data = data.str.strip()
            data = data.str.replace('_', '')
            data = data.apply(lambda x: re.sub(SPACES, '_', x) if not pd.isnull(x) else x)
            data = data.str.normalize("NFD")
            data = data.apply(lambda x: re.sub(NON_ADDRESS_CHAR, '', x) if not pd.isnull(x) else x)
            data = data.apply(lambda x: self.format_appartment_number(x) if not pd.isnull(x) else x)
            data = data.apply(lambda x: re.sub(UNDERSCORES,' ',x) if not pd.isnull(x) else x)
            data = data.str.upper()
            data = data.apply(lambda x: self.format_abbreviation(x) if not pd.isnull(x) else x)
            return data

        def validate_phone_num(self, phone_num:str)->str:
            """
             @brief Validates and normalizes phone number. This is a helper method for : meth : ` get_valid_phone_num `.
             @param phone_num The phone number to validate. It can be : A string with at least 3 digits ( 0 - 9 ) or a regular expression ( \
            """
            # if phone_num is a valid phone number
            if len(phone_num)==PHONE_NUM_LENGTH+1 and phone_num[0]==NA_CALLING_CODE:
                phone_num = phone_num[1:]
            # Returns the phone number as a string.
            if len(phone_num)==PHONE_NUM_LENGTH:
                phone_num = re.search(PHONE_NUM_FORMAT, phone_num)
                # Returns the phone number as a string.
                if not phone_num is None:
                    phone_num = phone_num.string
                    phone_num = phone_num[0:3] + "-" + phone_num[3:6] + "-" + phone_num[6:10]
                    return phone_num
            return np.nan

        def format_phone_number(self,data:pd.Series)->pd.Series:
            """
             @brief Formats phone numbers to be used in dialing. This is a wrapper around : meth : ` format_number ` and : meth : ` validate_phone_num `
             @param data Series of phone numbers to be formatted
             @return A Series of formatted phone numbers with null values removed from the series if they are not valid or empty
            """
            data = self.format_number(data)
            data = data.apply(lambda x: self.validate_phone_num(x) if not pd.isnull(x) else x)
            return data

        def format_number(self,data:pd.Series)->pd.Series:
            """
             @brief Formats numbers to be human readable. This is a helper for : meth : ` ~RabbitData. format `
             @param data Data to be formatted.
             @return Data formatted for humans / megabytes / speakers ( string ) and numerics
            """
            data = data.astype(str).str.normalize(self.normalization_form)
            data = data.astype(str).apply(lambda x: re.sub(NON_NUMERICAL, '', x) if not pd.isnull(x) else x)
            return data

        def format_text(self,data:pd.Series)->pd.Series:
            """
             @brief Formats text to upper case strips whitespace and converts to nan. This is useful for converting data that is read from a file to an Excel spreadsheet
             @param data Data to be formatted.
             @return Data with formatted text as column headings. >>> format_text ( pd. Series ('Somewhere '
            """
            data = data.apply(lambda x: np.nan if x == "" else x)
            data = data.str.strip()
            data = data.str.upper()
            return data

        def format_login(self,data:pd.Series)->pd.Series:
            """
             @brief Formats data for login. This is a wrapper around format_text that replaces non - alphanumeric characters with spaces
             @param data pandas Series to be formatted
             @return pandas Series with formatted data ready to be logged into Panda. Data is filtered to be in alphabetical
            """
            data = data.apply(lambda x: re.sub(NON_ALPHANUMERICAL, '', x) if not pd.isnull(x) else x)
            data = self.format_text(data)
            return data

        # Format method
        def apply_format(self, format_type: str, col_to_format: any):
            """
             @brief Applies a format to a column. This is a wrapper around format_name to be able to do something like this
             @param format_type type of format to apply
             @param col_to_format column to format ( name date nas
            """
            # format_type is the format_type of the session_state df_format column_to_format
            if format_type == FORMAT_NAME:
                st.session_state['df_format'][col_to_format] = self.format_name(
                    st.session_state['df_format'][col_to_format])
            elif format_type == FORMAT_DATE:
                st.session_state['df_format'][col_to_format] = self.format_date(
                    st.session_state['df_format'][col_to_format])
            elif format_type == FORMAT_NAS:
                st.session_state['df_format'][col_to_format] = self.format_ssn(
                    st.session_state['df_format'][col_to_format])
            elif format_type == FORMAT_EMAIL:
                st.session_state['df_format'][col_to_format] = self.format_email(
                    st.session_state['df_format'][col_to_format])
            elif format_type == FORMAT_ADDRESS:
                st.session_state['df_format'][col_to_format] = self.format_address(
                    st.session_state['df_format'][col_to_format])
            elif format_type == FORMAT_PHONE:
                st.session_state['df_format'][col_to_format] = self.format_phone_number(
                    st.session_state['df_format'][col_to_format])
            elif format_type == FORMAT_NUMBER:
                st.session_state['df_format'][col_to_format] = self.format_number(
                    st.session_state['df_format'][col_to_format])
            elif format_type == FORMAT_LOGIN:
                st.session_state['df_format'][col_to_format] = self.format_login(
                    st.session_state['df_format'][col_to_format])
            elif format_type == FORMAT_TEXT:
                st.session_state['df_format'][col_to_format] = self.format_text(
                    st.session_state['df_format'][col_to_format])



