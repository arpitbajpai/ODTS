
from pymongo import MongoClient

#Reason, Handling it at the database side was too much overhead. Moreover the queries were complex 
#and it takes a lot of time to customize those queries for a particular requirement. Also the mongodb
#aggregation profile is not as flexible as pandas library provided by python, therefore, it makes
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