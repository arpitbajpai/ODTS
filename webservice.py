#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 22:19:58 2017

@author: Arpit
"""

#!flask/bin/python
from flask import Flask
from flask import make_response,request
from normalization import establish_connection
from normalization import fetch_results
from pymongo import MongoClient
from pandas import DataFrame, read_csv
import pandas as pd

app = Flask(__name__)

def generate_csv(df,file_name):
    """Method Description: Method to generate CSV file for resampled data
    Parameters
    ----------
    file_name : String
    Name of the output CSV file.
    
    df : DataFrame
    dataframe containing resampled data for a specified period.
    """
    response = make_response(df.to_csv());
    response.headers["Content-Disposition"] = "attachment; filename="+file_name;
    response.headers["Content-Type"] = "text/csv";
    return response;


@app.route('/')
def index():
    """Method Description: Root URL to access this service running on http://localhost:5000
    ReturnType
    ----------
    To be decided: Resources that will be exposed by this service
    """
	return "ODTS!";



#The webservice is available on http://localhost:5000/ODTS/api/normalize
#Params ?start=1497530178000&end=1501504578000 
#example : http://localhost:5000/ODTS/api/normalize?start=1497530178000&end=1501504578000&containerId=36&interval=15
@app.route('/ODTS/api/normalize', methods=['GET'])
def get_normalized_csv():
    """Method Description: Resource to generate CSV requested by the user.
    User supplies the startdate, enddate, containerId and sampling interval in request link 
    and the response is generated in the form of a CSV file.
    Example: example : http://localhost:5000/ODTS/api/normalize?start=1497530178000&end=1501504578000&containerId=36&interval=15
    Request Parameters
    ----------
    start: Timestamp
    Timestamp in epochs for a specified starting date.
    
    end: Timestamp
    Timestamp in epochs for a specified ending date.
    
    containerId: Number
    Differentiates between different devices
    
    interval: number
    Supplied in minute format. Frequency conversion and Resampling of time series.
    """
    start_timestamp = request.args.get('start');
    end_timestamp = request.args.get('end');
    container_id = request.args.get('containerId');
    interval_in_mins = request.args.get('interval');
    db= establish_connection("mongodb://192.168.21.240","fortiss");
    df= fetch_results(db,"DoubleEvents",int(start_timestamp),int(end_timestamp),container_id,interval_in_mins);
    return generate_csv(df,"abc.csv");
	
if __name__ == '__main__':
	app.run(debug=True)