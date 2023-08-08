# PolyBM Data Analysis Tool

## What it is?
The PolyBM Data Analysis Tool is an AI tool that helps users profile, format, and anonymize data from CSV, JSON, and XML files. The tool offers various functionalities such as creating charts, generating data quality reports, and anonymizing sensitive data.

## How to use it? 
To use the tool, the user needs to log in to their account first. Afterward, they can upload their file from the 'Upload' section and start manipulating their data. Here is a brief explanation of each section of the tool:
### Login
This section allows users to log in to their account using their username and password.  
**Username** : testAdmin  
**Password** : AdminTest  
**Username** : testUser   
**Password** : UserTest
### Home
The home section provides an overview of the tool and its functionalities. From here, the user can access other sections of the tool, such as Upload, Preview, Profile, Visualize, Refine, and Anonymization.
### 📁Upload
In this section, the user can upload their data file in CSV, JSON, or XML format. The tool supports data files up to 45GB in size.
### :mag_right: Preview 
The preview section allows users to view and modify their data before processing. The user can apply modifications such as changing column names or converting the name column to upper or lower case. This section also includes a search bar to quickly find specific values in the data.

###  :book: Profile 
The profile section provides an in-depth analysis of the dataset's statistics. The user can see the number of rows and columns in the dataset, the data types of each column, the number of missing values, and other statistics. The user can choose to download the full report in HTML format. 

###  :bar_chart: Visualize
In this section, the user can create different types of charts using their data. The tool offers various chart types such as line charts, bar charts, scatter plots, and pie charts. The user can choose the columns to use as the x-axis and y-axis, and select different chart settings such as colors, titles, and legends.

###  :arrows_counterclockwise: Refine 
The refine section provides options for data manipulation such as filtering data based on specific criteria or transforming data using mathematical functions. The user can select the column to filter, the operator to use, and the value to filter by. The user can also apply mathematical functions such as addition, subtraction, multiplication, and division to specific columns.
###  🔒 Anonymization 
The anonymization section allows users to remove any sensitive data from the dataset. The tool offers several options such as removing specific columns, masking certain values with random characters, or replacing values with predefined values. The user can also select the type of masking to use, the columns to anonymize, and the characters to use for masking.

###  🧠 ML Evaluation
This section allows users to compare the performance of a machine learning model using a raw dataset versus an anonymized dataset. The model used is a logistical regression model. The user starts by uploading a raw dataset and an anonymized dataset. The user then selects the target and predictors and tests the model. Performance metrics are then computed, and predictions are available to see.   

## Installation and launching the application 

Running the application requires **docker** to be installed. 
The supported os are windows and linux (alpine).

Once docker is installed, run the following command in the project root:

   
    docker-compose up 

After booting up, the app can be accessed at localhost:8501. 
Allow for a few seconds for the app components to properly setup.


## Who are we?
The PolyBM Data Analysis Tool was developed by a team of five software engineering students from Polytechnique Montreal. The tool aims to help users with their science data assignments by providing a user-friendly interface for data analysis and manipulation
