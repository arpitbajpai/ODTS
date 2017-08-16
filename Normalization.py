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
import gviz_api

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
    df = df.drop('maxAbsError', 1)
    df=sample_data(df,interval_in_min);
    
    return df;
    

#Testing Purpose
#db=establish_connection("mongodb://192.168.21.240","fortiss");
#df= fetch_results(db,"DoubleEvents",1497530178000,1501504578000,"36",60)
#generate_googlechart_jsonresponse(df);
#df1.reset_index(inplace=True)
#print(df.to_json(orient='index'))
#df.columns = range(df.shape[1]) # to remove column header



