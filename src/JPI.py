"""
Author : Raphaël Lasalle
Date : 06-03-2023
"""

import subprocess as sp
import pandas as pd
import random
import math
import json
import pika as pk
import streamlit as st
import time
import threading

DEFAULT_SAMPLE_SIZE = 0.1
ENCODING = "UTF-8"

#key constants for parsing rabbitmq config file
CONFIG_FILE_PATH = "config/python_rmq_config.json"
USER_KEY = "user"
PSWD_KEY = "pswd"
HOST_KEY = "host"
PORT_KEY = "port"
EXCH_NAME_KEY = "exchange_name"
EXCH_TYPE_KEY = "exchange_type"
Q_KEY  = "queues"
TIQ = "python_type_id_queue"
VIQ = "python_vuln_id_queue"
JAVA_TIQ_RTK = "java_type_id"
JAVA_VIQ_RTK = "java_vuln_id"
PYTHON_TIQ_RTK = "python_type_id"
PYTHON_VIQ_RTK = "python_vuln_id"
Q_NAME_KEY = "queue_name"
RTK_KEY = "routing_key"
DRBL_KEY = "durable"
EXCL_KEY = "exclusive"
AUT_DEL_KEY = "auto_del"
Q_ARGS_KEY = "queue_args"

V_HOST = "/"

class JPI:

    def __init__(self) -> None:
        """
         @brief Initializes JPI. Initializes connection credentials and connection parameters. This method is called by __init__ method of class
        """
        
        try:
            print("starting JPI init !")
            self.config_file = open(CONFIG_FILE_PATH)
            self.config_data = json.load(self.config_file)

            self.rabbitmq_username = self.config_data[USER_KEY]
            self.rabbitmq_password = self.config_data[PSWD_KEY]
            self.rabbitmq_host = self.config_data[HOST_KEY]
            self.rabbitmq_port = self.config_data[PORT_KEY]

            self.rabbitmq_exchange_name = self.config_data[EXCH_NAME_KEY]
            self.rabbitmq_exchange_type = self.config_data[EXCH_TYPE_KEY]

            self.queues = self.config_data[Q_KEY]
            self.connection_credentials = pk.PlainCredentials(self.rabbitmq_username,self.rabbitmq_password)
            self.connection_param = pk.ConnectionParameters(self.rabbitmq_host,self.rabbitmq_port,V_HOST,self.connection_credentials)

            self.data_types = []
            self.vulnerabilities = []

            try:
                self.connection = pk.BlockingConnection(self.connection_param)
                self.channel = self.connection.channel()
                self.exchange = self.channel.exchange_declare(self.rabbitmq_exchange_name,self.rabbitmq_exchange_type)

                # declare durable exclusive auto_delete arguments and arguments
                for queue in self.queues:
                    
                    self.channel.queue_declare(
                        str(queue[Q_NAME_KEY]),
                        durable=bool(queue[DRBL_KEY]),
                        exclusive=bool(queue[EXCL_KEY]),
                        auto_delete=bool(queue[AUT_DEL_KEY]),
                        arguments=queue[Q_ARGS_KEY]
                    )

                    self.channel.queue_bind(
                        str(queue[Q_NAME_KEY]),
                        str(self.config_data[EXCH_NAME_KEY]),
                        str(queue[RTK_KEY])
                    )
                
                
                    
            except pk.exceptions.AMQPConnectionError as e:
                st.error("could not connect to rabbitmq server !")

        except FileNotFoundError as e:
            st.error("config file not found !")
        except json.JSONDecodeError as e:
            st.error("config file could not be read !")

 
    def __enter__(self):
        """
         @brief Return self to allow __enter__ to be called multiple times. This is useful for debugging the code that calls __enter__ in a context manager.
         @return self to allow __enter__ to be called multiple times in a context manager. Note that __enter__ does not have to be called when you're inside a context
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
         @brief Called when exception is raised. Closes the connection if it's open. This is a no - op if the connection isn't open.
         @param exc_type The type of exception raised. Ignored.
         @param exc_val The value of the exception raised. Ignored
         @param exc_tb
        """
        # Closes the connection to the server.
        if self.connection is not None:
            self.connection.close()
    
    def send(self,message:str,routing_key:str,reply_queue:str):
        """
         @brief Send a message to RabbitMQ and consume the reply queue. This is a low - level method to be used by subclasses that want to send messages to RabbitMQ without having to re - use the AMQP protocol.
         @param message The message to be sent. It should be a string in the format " message. text "
         @param routing_key The routing key for the message.
         @param reply_queue The queue to consume the reply from
        """
        self.channel.basic_publish(self.rabbitmq_exchange_name,routing_key,message)
        self.channel.basic_consume(reply_queue,on_message_callback=self.handle_delivery,auto_ack=True)
        self.channel.start_consuming()
    
    def handle_delivery(self,ch, method, properties, body):
       """
        @brief Called when RabbitMQ has received a message. We need to update our data types and vulnerabilities
        @param ch Channel that sent the message
        @param method Message method that was sent to RabbitMQ ( not used )
        @param properties Properties associated with the message ( not used )
        @param body Message body ( unencoded JSON string ) This method is responsible for parsing the message
       """
       
       json_data = body.decode(ENCODING)
       routing_key = method.routing_key #check syntax when internet is back

       # Load the data types and vulnerabilities from the data_types and vulnerabilities.
       if routing_key == PYTHON_TIQ_RTK:
           self.data_types = json.loads(json_data)
       elif routing_key == PYTHON_VIQ_RTK:
           self.vulnerabilities = json.loads(json_data)
       self.channel.stop_consuming()

    """
    Selects a randomly distributed sample of the provided dataset to identify 
    the predominant semantic type. 

    @param data : the source dataset
    @param sample_size_ratio : size of the selected sample expressed as a percentage of the total dataset.
        must be a number between 0 and 1
    @return : the predominant semantic type of each column of the dataset
    """

    def identify_type(self,df:pd.DataFrame,sample_size:float=DEFAULT_SAMPLE_SIZE) -> str:
        """
         @brief Identify type of data. This is a method to use when you want to send data to TIQ and get a string that can be used as a type identifier.
         @param df Dataframe with columns and values to be sent
         @param sample_size Number of samples to send per time step
         @return JSON string of type identifier ( RTK / IDQ ) for the data in the DataFrame and the
        """
        samples = []
        effective_sample_size = math.ceil(len(df) * sample_size)
        # Generate a sample of the columns in the dataframe.
        for column in df.columns:
            sample = []
            random_indices = random.sample(range(len(df)),effective_sample_size)
            # Generate a sample of random indices.
            for index in random_indices:
                sample.append(str(df.loc[index,column]))
            samples.append(sample)
        json_samples = json.dumps(samples)
        self.send(json_samples,JAVA_TIQ_RTK,TIQ)

    """
    Identifies the vulnerabilities in a dataset by finding potential identifiers and quasi-identifiers.
    Makes a call to the data-privacy-toolkit library. 

    @param n_trhreads : the number of threads used to run the algorithm
    @param uniqueness_threshold : the k value used to check the frequency of a value against. If a value appears less times than the 
        threshold, the corresponding fied will be flagged as a vulnerability (identifier or quasi-identifier)
    @param data : the source dataset

    @return : the indices of the vulnerable columns as a list of int (single indices for identifiers and nested list for quasi-identifiers)
    """

    def identify_vulnerabilities(self,df:pd.DataFrame,k_value:int,n_threads:int) -> list:
        """
         @brief Identify vulnerabilities by sending a message to the Java Vulnerability Queue. This is a low - level method that should be used in conjunction with
         @param df DataFrame containing data to analyze
         @param k_value Number of k - values to use
         @param n_threads Number of threads to use for the analysis
         @return A list of dictionaries that contain the following keys : data : A Pandas DataFrame that can be converted to a list
        """
        df_rows = []
        # Append all rows in the dataframe to the dataframe.
        for index,row in df.iterrows():
            df_rows.append(row.to_list())
        payload = {
            "data":df_rows,
            "k_value":k_value,
            "n_threads":n_threads
        }
        json_message = json.dumps(payload)
        self.send(json_message,JAVA_VIQ_RTK,VIQ)
    