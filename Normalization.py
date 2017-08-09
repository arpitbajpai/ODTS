#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 14:51:00 2017

@author: Arpit
"""

from pymongo import MongoClient
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date


#Reason, Handling it at the database side was too much overhead. Moreover the queries were complex 
#and it takes a lot of time to customize those queries for a particular requirement. Also the mongodb
#aggregation profile is not as flexible as pandas library provided by python, therefore, it makes much
#more sense to retrieve the results first and then handle it according to the client requirements.
 
def establish_connection(url,database):
    """Method Description: Establishing the connection with ODTS system
    Parameters
    ----------
    url : String
    URL to ODTS Mongodb server.
    
    database: String
    Database name from where information is retrieved.
    """
    client = MongoClient()
    client = MongoClient(url) #mongodb://192.168.21.240
    db = client[database];    #db = client['fortiss']
    return db;

 
def sample_data(df,interval_in_min):
    """Method Description: Samping of data based on specified interval
    Parameters
    ----------
    df : DataFrame
    dataframe containing raw data for a specified period.
    
    interval_in_min: number
    Supplied in minute format. Frequency conversion and Resampling of time series.
    """
    if(interval_in_min==60):
        df = df.resample('1H').mean();
    elif(interval_in_min==5):
        df = df.resample('5T').mean(); #modify this method to perform integration
    elif(interval_in_min==15):
         df = df.resample('15T').mean(); #modify this method to perform integration
    #add more conditions
    return df;

        
def fetch_results(db,document_name,start_timestamp,end_timestamp,container_id,interval_in_min):
    """Method Description: Function to fetch Raw data from ODTS 
    Parameters
    ----------
    db : Database handle
    Database handle pointing to 'fortiss' database at ODTS.
    
    document_name: Collection
    Collection containing raw data which has to be resampled or visualized.
    
    start_timestamp: Timestamp
    Timestamp in epochs for a specified starting date.
    
    end_timestamp: Timestamp
    Timestamp in epochs for a specified ending date.
    
    containerId: Number
    Differentiates between different devices
    
    interval_in_min: number
    Supplied in minute format. Frequency conversion and Resampling of time series.
    """
    col = db[document_name];
    cursor = col.find({"containerid":container_id , 
                       "timestamp": 
                           {"$gte" : start_timestamp, 
                            "$lte" : end_timestamp 
                            }
                     })
    df = pd.DataFrame(list(cursor))
    df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')
    df = df.set_index(['timestamp'])  
    df=sample_data(df,interval_in_min);
    return df;
    

#db=establish_connection("mongodb://192.168.21.240","fortiss");
#df= fetch_results(db,"DoubleEvents",1502186455000,1502272855000,"36","1")




