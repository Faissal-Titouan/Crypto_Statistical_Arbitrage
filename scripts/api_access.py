import pandas as pd
import sqlalchemy
from binance.client import Client
from binance import BinanceSocketManager
import matplotlib.pyplot as plt
import time
from datetime import datetime
import numpy as np
import json


####### MAIN PATH 

PATH_DATA = './data/'
PATH_SCRIPTS = './'

API_FILE_NAME = 'api_access.json'

# =============================================================================
#  API CODE
# =============================================================================

def save_api_code(api_file_name = API_FILE_NAME, path_data = PATH_DATA):
    """
       Parameters
    ----------
    api_file_name : Str, optional
         Name of the targeted api file. The default is API_FILE_NAME.
    path_data : Str, optional
         Path of the targeted api file. The default is PATH_DATA.

    Returns
    -------
    None.
    """
    
    dictionary ={
        'api_key' : "test",
        'api_secret' : "test"
    }
  
    with open(path_data + api_file_name, "w") as outfile:
        json.dump(dictionary, outfile)


def get_api_code(api_file_name = API_FILE_NAME, path_data = PATH_DATA):
    """   
    Parameters
    ----------
    api_file_name : Str, optional
        DESCRIPTION. Name of the targeted api file. The default is API_FILE_NAME.
    path_data : Str, optional
        Path of the targeted api file. The default is PATH_DATA.

    Returns
    -------
    DICTIONNARY
        Dictionnary of api_key and api_secret.

    """
    
    file = open(path_data + api_file_name ,'r')
    return json.load(file)


# =============================================================================
# API INIT ACCESS AND CHECK ACCOUNT
# =============================================================================

def InitConnection(client):
    """
    This function inits the connection and check the servers status

    Parameters
    ----------
    client : BINANCE CLIENT OBJECT
        The client we are connected to.

    Returns
    -------
    DSATETIME OBJECT
        Current time of the API

    """
    
    ## ACCESS TIME :
    time_res = client.get_server_time()
    df = pd.DataFrame([time_res])
    df.serverTime = pd.to_datetime(df.serverTime,unit = 'ms')
    time_res = df.serverTime

    #CHECK STATUS
    status = client.get_system_status()
    assert status['status'] == 0,"Serveur is in maintenance, connection not possible"
    
    return time_res[0]

def convert_balances(df):
    for col in df.columns:
        if col not in ["asset"] :
            df[col] = df[col].astype(float)
    return df


def convert_fees(df):
    for col in df.columns:
        if col not in ["symbol"] :
            df[col] = df[col].astype(float)
    return df


class My_api:
    
    def __init__(self, api_key,api_secret):
        
        self.client = Client(api_key,api_secret)
        
        self.bsm = BinanceSocketManager(self.client)
        
        self.api_time = InitConnection(self.client)
        
        self.info = self.client.get_account()
        
        self.balances_df = convert_balances(pd.DataFrame(self.info['balances']))
        
        self.fees_df = convert_fees(pd.DataFrame(self.client.get_trade_fee()))
        
    ## PRINT AND MAIN FUNCTION
    def __str__(self):
        return "<API  time:%s  >" % (self.api_time)
    
    def print_api(self):
        dictionnary = self.__dict__
        for key in dictionnary.keys():
            print(key + " : ",end = "")
            print(dictionnary[key])
   
    ## FUNCTION   
    def get_time(self):
        
        time_res = self.client.get_server_time()
        df = pd.DataFrame([time_res])
        df.serverTime = pd.to_datetime(df.serverTime,unit = 'ms')
        time_res = df.serverTime

        self.api_time = time_res
        
        return self.api_time
        
    def get_info(self):
        self.info = self.client.get_account()
        return self.info
    
    def get_balances(self):
        self.balances_df = convert_balances(pd.DataFrame(self.get_info()['balances']))
        return self.balances_df
    
    def get_fees(self):
        self.fees_df = convert_fees(pd.DataFrame(self.client.get_trade_fee()))
        return self.fees_df