import streamlit as st
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import pandas as pd

# Visualize page layout
st.set_page_config(layout="wide")
st.title("Visualization")


# Correlation matrix
def get_correlation_matrix(new_df):
    """
     @brief Get correlations between new and old dataframe and write to st file. This is useful for debugging the correlation matrix
     @param new_df dataframe to get correlation
    """
    st.write(new_df.corr())


# Bar chart
def get_bar_plot(new_df):
    """
     @brief Creates a bar plot of data. It is used to show the progress of the simulation. This plot can be visualized by clicking on the bar and clicking on the legend
     @param new_df dataframe with data to
    """
    st.bar_chart(new_df)


# Line chart
def get_line_chart(new_df):
    """
     @brief Create and set line chart for new_df. It is used to plot data from different sources.
     @param new_df dataframe with data to plot in new
    """
    st.line_chart(new_df)


# Distance chart
def get_dist_chart(new_df):
    """
     @brief Creates a histogram of data. It is useful for visualizing the distribution of a data set. The data should be in float and int types
     @param new_df dataframe with data to
    """
    df = new_df
    column_names = list(df.select_dtypes(include=['float', 'int']).columns)
    hist_data = [df[column_name] for column_name in column_names]
    group_labels = column_names
    fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1] * len(column_names))
    st.plotly_chart(fig)


# Pie chart
def get_pie_chart(new_df):
    """
     @brief Plot pie chart of data. This is a function to be used in tests. It takes a dataframe and returns a plot of the mean of each column
     @param new_df dataframe that contains the
    """
    column_names = list(new_df.columns)
    hist_data = []
    # Add the mean of the new dataframe to the histogram.
    for col in new_df.columns:
        hist_data.append(new_df[col].mean())
    group_labels = column_names
    fig, ax = plt.subplots()
    ax.pie(hist_data, labels=group_labels, autopct='%1.1f%%',
           shadow=True, startangle=90)
    ax.axis('equal')
    st.pyplot(fig)


# Area chart
def get_area_plot(new_df):
    """
     @brief Creates a plot of area. It is used to plot the data in a pandas dataframe. The plot is created by calling st. area_chart
     @param new_df dataframe with data to
    """
    st.area_chart(new_df)


# Expander with information about each diagram
def expand_info(info):
    """
     @brief Expand information about the program. This is a convenience function for use in : py : func : ` waflib. Tools. get_toolchain `
     @param info The information to expand
    """
    with st.expander("More informations"):
        st.write(info)


# Multiselect to choose columns to display
def multi_select(key_multi):
    """
     @brief Select columns to display in multiselect mode. This is useful for multi - select where you want to display a subset of the data in a single column
     @param key_multi key to use for multiselect
     @return True if columns selected False if there was no columns to display ( only columns with a numerical value in the data
    """
    col_to_change = st.multiselect("Columns to display (only columns with a numerical value)",
                                   st.session_state.df.select_dtypes(include=['float', 'int']).columns, key=key_multi)
    # If col_to_change is true then the session_state dfColumns is set to the column to change.
    if col_to_change:
        st.session_state['dfColumns'] = pd.DataFrame()
        st.session_state['dfColumns'] = st.session_state.df[col_to_change]
        return True
    else:
        st.warning('Please select at least one column')
        return False


# Selectbox to choose x and y axis for chart
def select(key_simple):
    """
     @brief Select X and Y columns from data frame and add them to dfColumns. This is useful for testing and to ensure that data is loaded in the correct order
     @param key_simple string to be used as key
     @return True if selected False
    """
    X_axis = st.selectbox("X", st.session_state.df.select_dtypes(include=['float', 'int']).columns,
                          key=(key_simple + 'X'))
    Y_axis = st.selectbox("Y", st.session_state.df.select_dtypes(include=['float', 'int']).columns,
                          key=(key_simple + 'Y'))
    # If X and Y axis are specified.
    if X_axis and Y_axis:
        st.session_state['dfColumns'] = pd.DataFrame()
        st.session_state['dfColumns'] = st.session_state.df[X_axis] + st.session_state.df[Y_axis]
        return True
    else:
        st.warning('Please select an X and a Y column.')
        return False


# This function is used to select the data from the upload page.
if 'df' not in st.session_state:
    st.warning('Please go back to the Upload page and select the data.')
else:
    # Column selecting code
    st.session_state['dfColumns'] = st.session_state.df
    st.markdown("""<br></br>""", unsafe_allow_html=True)

    button_space, diagram_space = st.columns((9, 3.5))

    # Column cleaning code
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ['Correlation matrix', 'Bar chart', 'Line chart', 'Distribution diagram', 'Pie chart', 'Area chart'])
    with tab1:
        # This is a correlation matrix.
        if multi_select("This is a correlation matrix"):
            get_correlation_matrix(st.session_state['dfColumns'])
            expand_info("https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html")
    with tab2:
        # This is a bar chart.
        if select("This is a bar chart"):
            get_bar_plot(st.session_state['dfColumns'])
            expand_info(
                "https://www.ibm.com/docs/pl/cognos-analytics/10.2.2?topic=SSEP7J_10.2.2/com.ibm.swg.ba.cognos.ug_rtm_db.10.2.2.doc/c_vert_combo_chrt.htm#vert_combo_chrt")
    with tab3:
        # This is a line chart.
        if select("This is a line chart"):
            get_line_chart(st.session_state['dfColumns'])
            expand_info(
                "https://www.ibm.com/docs/pl/cognos-analytics/10.2.2?topic=SSEP7J_10.2.2/com.ibm.swg.ba.cognos.ug_rtm_db.10.2.2.doc/c_vert_combo_chrt.htm#vert_combo_chrt")
    with tab4:
        # This is a distribution diagram.
        if multi_select("This is a distribution diagram"):
            get_dist_chart(st.session_state['dfColumns'])
            expand_info(
                "https://www.ibm.com/docs/pl/cognos-analytics/10.2.2?topic=SSEP7J_10.2.2/com.ibm.swg.ba.cognos.ug_rtm_db.10.2.2.doc/c_distributionchartsn300fa.htm")
    with tab5:
        # If this is a pie chart this is a pie chart
        if multi_select("This is a pie chart"):
            get_pie_chart(st.session_state['dfColumns'])
            expand_info(
                "https://www.ibm.com/docs/pl/cognos-analytics/10.2.2?topic=SSEP7J_10.2.2/com.ibm.swg.ba.cognos.ug_rtm_db.10.2.2.doc/c_piechartsn300b7.htm#PieChartsN300B7")
    with tab6:
        # This is an area chart.
        if select("This is an area chart"):
            get_area_plot(st.session_state['dfColumns'])
            expand_info(
                "https://www.ibm.com/docs/pl/cognos-analytics/10.2.2?topic=SSEP7J_10.2.2/com.ibm.swg.ba.cognos.ug_rtm_db.10.2.2.doc/c_vert_combo_chrt.htm#vert_combo_chrt")
    pass

# Add style to buttons
button_style = """
    <style>
    .stButton > button {
        background: transparent;
        width: 200px;
        height: 200px;
    }
    </style>
    """
st.markdown(button_style, unsafe_allow_html=True)
