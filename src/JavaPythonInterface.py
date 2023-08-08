"""
Author : Raphaël Lasalle
Date : 06-03-2023
"""

import subprocess as sp
import pandas as pd
import random
import math


WORKING_DIR = "src/jpi"
GRADLEW_CLEAN_BUILD = "gradlew clean build -x test --refresh-dependencies"
GRADLEW_RUN = "gradlew run"
DEFAULT_SAMPLE_SIZE = 0.1  


class JavaPythonInterface:

    def __init__(self) -> None:
        """
         @brief Initializes the Gradle instance. This is the entry point for the build process. It calls the clean build and run commands to clean the build process and run the Java gateway
        """
        sp.call(GRADLEW_CLEAN_BUILD, shell=True, cwd = WORKING_DIR)
        self.java_process = sp.Popen(GRADLEW_RUN, shell=True, cwd = WORKING_DIR)
        self.gateway = JavaGateway()
        self.entry_point = self.gateway.entry_point

    """
    Selects a randomly distributed sample of the provided dataset to identify 
    the predominant semantic type. Makes a call to the data-privacy-toolkit library through the py4j interface. 

    @param data : the source dataset
    @param sample_size_ratio : size of the selected sample expressed as a percentage of the total dataset.
        must be a number between 0 and 1
    @return : the predominant semantic type of the dataset as a string
    """

    def identify_type(self,data:pd.Series,sample_size_ratio:float=DEFAULT_SAMPLE_SIZE) -> str:
        """
         @brief Identify the type of data. This is a wrapper around the entry point's identify_type method to allow the user to specify a sample size for example if the user wishes to sample a data set with 10% of the data you would use this method to identify the type
         @param data The data that will be sampled
         @param sample_size_ratio The ratio of the data size to sample
         @return A string that can be used as the type of the data in the form " TYPE_NAME "
        """
        sample_size = math.ceil(data.size * sample_size_ratio)
        random_indices = random.sample(range(data.size),sample_size)
        sample = self.gateway.jvm.java.util.ArrayList()
        # Generate a sample of random indices.
        for index in random_indices:
            sample.append(str(data[index]))
        return self.entry_point.identify_type(sample)
    

    """
    Identifies the vulnerabilities in a dataset by finding potential identifiers and quasi-identifiers.
    Makes a call to the data-privacy-toolkit library through the py4j interface. 

    @param n_trhreads : the number of threads used to run the algorithm
    @param uniqueness_threshold : the k value used to check the frequency of a value against. If a value appears less times than the 
        threshold, the corresponding fied will be flagged as a vulnerability (identifier or quasi-identifier)
    @param data : the source dataset

    @return : the indices of the vulnerable columns as a list of int (single indices for identifiers and nested list for quasi-identifiers)
    """

    def identify_vulnerabilities(self,n_threads:int, uniqueness_threshold:int, data:pd.DataFrame) -> list:
        """
         @brief Identify vulnerabilities using the entry point. This is a wrapper around the : meth : ` VirtualizationEntryPoint. identify_vulnerabilities ` method of the virtualization entry point
         @param n_threads Number of threads to use for parallelization
         @param uniqueness_threshold Threshold for uniqueness of data
         @param data Data to use for parallelization. Each row is a list of strings
         @return List of vulnerabilities that were identified by the entry point. Each element in the list corresponds to a column in the data
        """
        java_dataset = self.gateway.jvm.java.util.ArrayList()
        # Add all the elements in the dataset to java_dataset.
        for index,row in data.iterrows():
            list = self.gateway.jvm.java.util.ArrayList()
            # Append the row to the list of strings.
            for element in row.to_list():
                list.append(str(element))
            java_dataset.append(list)
        return self.entry_point.identify_vulnerabilities(n_threads, uniqueness_threshold, java_dataset)

