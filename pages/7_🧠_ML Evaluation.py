import streamlit as st
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from src.filemanager import read_data_file

# Anonymization page layout
st.set_page_config(layout="wide")
st.title("Classification Model Evaluation")
st.subheader("Logistical Regression")
st.markdown("***")


def generate_overview(df_type: str):
    """
     @brief Generate overview of the data. It is used to visualize the correlations and the number of rows
     @param df_type Type of data to
    """
    # Dataset selection
    decrypted_uploaded_file = None
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "json", "xml", "xlsx"], key=df_type + "upload")
    # If uploaded_file is encrypted decrypt first and read the data from the file and store it in session_state.
    if uploaded_file is not None:
        # if "Encrypted" in uploaded_file.name:  # If uploaded file is encrypted, decrypt first
        # decrypted_uploaded_file = decrypt(uploaded_file)
        st.session_state[df_type + "_filename"] = uploaded_file.name
        data = read_data_file(uploaded_file, decrypted_uploaded_file)
        st.session_state[df_type] = data

    # Visualize data space_1 col space_1 col space_2
    if df_type not in st.session_state:
        st.warning('Please select the dataset for the ML model.')

    else:
        dataset = st.session_state[df_type]
        # Visualize data

        space_1, col, space_2 = st.columns((1, 3, 1))
        with col:
            fig, ax = plt.subplots()
            sns.heatmap(dataset.corr(), ax=ax)
            st.write(fig)


def select_parameters(df_type: str):
    """
     @brief Select predictor and target parameters from SessionState. This is a subheader and multiselect function to allow user to select a subset of X and y data
     @param df_type Type of data to select
     @return X_labels y_label : Labels for X and y data in session_state [ df_type
    """
    # X_labels y_label Predictor selection target selection
    if df_type in st.session_state:
        # Evaluation parameters
        st.subheader("Evaluation parameters")
        # Predictor selection
        X_labels = st.multiselect("Predictor(s)", st.session_state[df_type].columns, key=df_type + "predictor")

        # Target selection
        y_label = st.selectbox("Target", st.session_state[df_type].columns, key=df_type + "target")

        # TODO: verify that there is no overlap between X and y
        return X_labels, y_label


def compute_metrics(df_type: str, X_labels, y_label):
    """
     @brief Compute metrics for each data set. This is a wrapper around Logistic Regression algorithm to train and test the model
     @param df_type Type of data set to evaluate
     @param X_labels List of labels for X_type
     @param y_label Label for y_type ( used for cross validation )
     @return A dictionary with metrics for each data set. Key is dataframe name value is numpy array of shape ( n_samples
    """
    # Evaluate results for a given dataset.
    if df_type in st.session_state:
        # Evaluation results
        X = st.session_state[df_type][X_labels]
        y = st.session_state[df_type][y_label]
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 3, random_state=0)
        # Train model using Logistic Regression algorithm
        model = LogisticRegression(random_state=0)
        # Initiate k-fold cross-validation with k=10
        kfold = model_selection.KFold(n_splits=10, random_state=0, shuffle=True)
        predictions = model_selection.cross_val_predict(model, X_test, y_test, cv=kfold)
        # Calculate performance metrics
        accuracy = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
        neg_log_loss = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring='neg_log_loss')
        roc_auc = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring='roc_auc')
        f1_weighted = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring='f1_weighted')
        precision_weighted = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring='precision_weighted')
        recall_weighted = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring='recall_weighted')

        return [
            accuracy.mean(),
            neg_log_loss.mean(),
            roc_auc.mean(),
            f1_weighted.mean(),
            precision_weighted.mean(),
            recall_weighted.mean()
        ], confusion_matrix(y_test, y_pred=predictions), pd.DataFrame({y_label: predictions})


def compare_metrics(unchanged_metrics: list, anonymized_metrics: list):
    """
     @brief Compare metrics to see if they are equal. This is used to calculate how much a metric was changed in the data set
     @param unchanged_metrics List of metrics that were not in the data set
     @param anonymized_metrics List of metrics that were anonymized
     @return A list of metrics that have been changed in the data set or None if there are no differences in
    """
    # Returns true if the number of ununchanged metrics is equal to the number of anonymized metrics.
    if len(unchanged_metrics) != len(anonymized_metrics):
        return
    deltas = []
    # Add deltas to the list of deltas.
    for i in range(len(unchanged_metrics)):
        delta = unchanged_metrics[i] - anonymized_metrics[i]
        deltas.append(delta)
    return deltas


# Upload and overview section
st.subheader("Overview")
unchanged_col, anonymized_col = st.columns(2)
with unchanged_col:
    generate_overview('df_ML')

with anonymized_col:
    generate_overview('df_ML_anonymized')

st.markdown("***")

# Parameters and metrics section
# This function is used to analyze the model and return a dataframe with the results of the model.
if 'df_ML' in st.session_state and 'df_ML_anonymized' in st.session_state:
    # if list(st.session_state['df_ML'].columns) == list(st.session_state['df_ML_anonymized'].columns):
    # TODO: check that both datasets have same columns (anonymization changes column names)
    X_labels, y_label = select_parameters('df_ML')

    analyze = st.button("Start evaluation", help="Evaluate model using k-fold cross-validation with k=10")
    st.markdown("***")
    # Analyze the data for the given data set.
    if analyze:
        unchanged_metrics, unchanged_matrix, unchanged_predictions = compute_metrics('df_ML', X_labels, y_label)
        anonymized_metrics, anonymized_matrix, anonymized_predictions = compute_metrics('df_ML_anonymized', X_labels, y_label)
        deltas = compare_metrics(unchanged_metrics, anonymized_metrics)
        df = pd.DataFrame(list(zip(unchanged_metrics, anonymized_metrics, deltas)), index=["accuracy", "neg log loss", "roc auc", "f1 weighted", "precision weighted", "recall weighted"],
                          columns=[st.session_state["df_ML_filename"], st.session_state["df_ML_anonymized_filename"], "Delta"])
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.subheader("Comparaison")
            st.dataframe(df.style.applymap((lambda x: "background-color: #F28679" if x < 0 else "background-color: #8AEC7E"), subset=["Delta"]))
        with col_2:
            st.subheader(st.session_state["df_ML_filename"])
            st.write("Confusion matrix")
            st.write(unchanged_matrix)
            with st.expander("See predictions for " + st.session_state["df_ML_filename"]):
                st.write(unchanged_predictions)
        with col_3:
            st.subheader(st.session_state["df_ML_anonymized_filename"])
            st.write("Confusion matrix")
            st.write(anonymized_matrix)
            with st.expander("See predictions for " + st.session_state["df_ML_anonymized_filename"]):
                st.write(anonymized_predictions)

