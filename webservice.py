#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 22:19:58 2017

@author: Arpit
"""

#!flask/bin/python
from flask import Flask
from flask import make_response,request
from normalization import fetch_results
from database_connection import establish_connection
from pymongo import MongoClient
from pandas import DataFrame, read_csv
import pandas as pd
import gviz_api

app = Flask(__name__)

def get_dataframe():
	"""Method Description: Utility method to establish connection with the database and extract results based on the request parameters 
	Return
	----------
	df : DataFrame
	dataframe containing resampled data for a specified period.
	"""
	start_timestamp = request.args.get('start');
	end_timestamp = request.args.get('end');
	container_id = request.args.get('containerId');
	interval_in_mins = request.args.get('interval');
	db= establish_connection("mongodb://192.168.21.240","fortiss");
	dataframe= fetch_results(db,"DoubleEvents",int(start_timestamp),int(end_timestamp),container_id,int(interval_in_mins));
	return dataframe;


def generate_csv_response(df,file_name):
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

def generate_json_response(df):
	"""Method Description: Method to generate JSON response for resampled data
	Parameters
	----------
   
	df : DataFrame
	dataframe containing resampled data for a specified period.
	"""
	response = make_response(df.to_json(orient='table',date_format='iso'));
	return response;

def generate_datatable_response(df):
	"""Method Description: Method to generate datatable response for resampled data which is appropriate for consumption in Google Charts
	Parameters
	----------
   
	df : DataFrame
	dataframe containing resampled data for a specified period.
	"""
	df.reset_index(inplace=True)
	description = {("timestamp", "datetime"),("value", "number")
				   }
	data_table = gviz_api.DataTable(description)
	data_table.LoadData(df.values)
	print ("Content-type: text/plain")
	#return data_table.ToJSon(columns_order=("timestamp", "value"),
	 #                           order_by="timestamp")
	response = data_table.ToJSon();
	#return data_table;
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
#example : http://localhost:5000/ODTS/api/normalizecsv?start=1497530178000&end=1501504578000&containerId=36&interval=15
@app.route('/ODTS/api/normalizecsv', methods=['GET'])
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
	df= get_dataframe();
	return generate_csv_response(df,"normalised_data.csv");


#http://localhost:5000/ODTS/api/normalizejson?start=1497530178000&end=1501504578000&containerId=36&interval=15
@app.route('/ODTS/api/normalizejson', methods=['GET'])
def get_normalized_json():
	"""Method Description: Resource to generate JSON requested by the user.
	User supplies the startdate, enddate, containerId and sampling interval in request link 
	and the response is generated in JSON format.
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
	df= get_dataframe();
	return generate_json_response(df);

@app.route('/ODTS/api/normalizejsondatatable', methods=['GET'])
def generate_googlechart_jsonresponse():
	"""Method Description: Resource to generate JSON(suitable for consumption in google charts) requested by the user.
	User supplies the startdate, enddate, containerId and sampling interval in request link 
	and the response is generated in json datatable format.
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
	df =get_dataframe();
	return generate_datatable_response(df);


if __name__ == '__main__':
	app.run(debug=True)