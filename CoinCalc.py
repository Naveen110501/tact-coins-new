import pandas as pd
import math
import sys
import numpy as np
import sqlite3,csv

# Imports
import pandas as pd
from pymongo import MongoClient


# Connect to MongoDB
client = MongoClient("mongodb+srv://analytics:analytics-password@mflix.9xllz.mongodb.net/<dbname>?retryWrites=true&w=majority")
#client =  MongoClient("mongodb+srv://featurepreneur-admin:MO58BxBlmRZTcqos@cluster0.tgas9.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client['TactCoinx']
user_db = db['users']
total_db = db['TotalCoins']
released_db = db['ReleasedCoins']
#cursor = collection.find() 
#print('Type of cursor:',type(cursor)) 
  
# Converting cursor to the list of  
# dictionaries 
#list_cur = list(cursor) 
  
# Converting to the DataFrame 
#df = pd.DataFrame(list_cur) 
#print(df['Name']) 
#to insert in to table
def insert_into_db_total():
    data = pd.read_csv('tactcoinstotal.csv')
    data.reset_index(inplace=True)
    data_dict = data.to_dict("records")# Insert collection
    total_db.insert_many(data_dict)
def insert_into_db_released():
    data = pd.read_csv('tactreleased.csv')
    data.reset_index(inplace=True)
    data_dict = data.to_dict("records")# Insert collection
    released_db.insert_many(data_dict)

def totalcoins(name):
    #con=sqlite3.connect("tactcoindetails.db")
    #sql = 'select * from TotalCoins'
    #coins = pd.read_sql(sql,con)
    cursor = total_db.find() 
    list_cur = list(cursor)
    coins = pd.DataFrame(list_cur)
    selected_name = coins[coins['Name'] == name]
    #print(selected_name)
    selected_name = selected_name.infer_objects() 
    #print(selected_name['TactPoints'].sum())
    total = selected_name['TactPoints'].sum()
    return total

def totalcoinsReleased(name):
    #con=sqlite3.connect("tactcoindetails.db")
    #sql = 'select * from ReleasedCoins'
    #coins = pd.read_sql(sql,con)
    cursor = released_db.find()
    list_cur = list(cursor)
    coins = pd.DataFrame(list_cur)
    r_selected_name = coins[coins['Name'] == name]
    #print(r_selected_name)
    r_selected_name = r_selected_name.infer_objects() 
    #print(r_selected_name['TactPoints'].sum())
    totalreleased = r_selected_name['TactPoints'].sum()
    return totalreleased

def totalcoins_to_be_Released(name):
    total = totalcoins(name)
    released = totalcoinsReleased(name)
    to_be_released = total - released
    return to_be_released


def get_names():
    #con=sqlite3.connect("tactcoindetails.db")
    #sql = 'select * from TotalCoins'
    cursor = total_db.find() 
    list_cur = list(cursor)
    coins = pd.DataFrame(list_cur)
    #coins = pd.read_sql(sql,con)
    selected_name = coins['Name'].unique()
    return selected_name

def is_name_present(name):
    names = get_names()
    if name in names:
        return 1
    return 0

def get_history(name):
    #con=sqlite3.connect("tactcoindetails.db")
    #sql = 'select * from TotalCoins'
    #coins = pd.read_sql(sql,con)
    cursor = total_db.find() 
    list_cur = list(cursor)
    coins = pd.DataFrame(list_cur)
    selected_name = coins[coins['Name'] == name]
    selected_name = selected_name.infer_objects() 
    #print(selected_name.dtypes)
    history = []
    for i,j in selected_name.iterrows() :
        #print(i)
        #print(j.Name)
        #print(j.Event)
        res = {
            'Name' : j.Name,
            'Event' : j.Event,
            'CoinsAwarded' : j.TactPoints
        }
        history.append(res)
    return history
    


'''
total = totalcoins(name)
released = totalcoinsReleased(name)
cur_total = total - released
#print(cur_total)
print(get_history(name))'''
#insert_into_db_released()
#insert_into_db_total()