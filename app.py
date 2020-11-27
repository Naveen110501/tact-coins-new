#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, url_for, request,session,redirect
import requests
import random
import os.path
import os
import random
from flask_pymongo import PyMongo
import pandas as pd
import math
import sys
import numpy as np
import sqlite3,csv
# Local import
import CoinCalc as cc
from pymongo import MongoClient
from cryptography.fernet import Fernet
key=Fernet.generate_key()
salt=key.decode('utf8')




#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config["MONGO_URI"] ="mongodb+srv://analytics:analytics-password@mflix.9xllz.mongodb.net/<dbname>?retryWrites=true&w=majority"
#app.config["MONGO_URI"] = "mongodb+srv://featurepreneur-admin:MO58BxBlmRZTcqos@cluster0.tgas9.mongodb.net/<dbname>?retryWrites=true&w=majority"
client = MongoClient("mongodb+srv://analytics:analytics-password@mflix.9xllz.mongodb.net/<dbname>?retryWrites=true&w=majority")
mongo = PyMongo(app)
db = client['TactCoinx']
user_db = db['users']
total_db = db['TotalCoins']
released_db = db['ReleasedCoins']


app.secret_key = "hi"

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/',methods=["POST","GET"])
def login():
    return render_template('login.html')

@app.route('/signup',methods=["POST","GET"])
def register():
    return render_template('sign.html')

@app.route('/register',methods=["POST","GET"])
def reg():
    message=''
    if request.method =='POST':
      user=request.form['username']
      e_mail=request.form['email']
      pass_word=request.form['password']
      r_pass_word=request.form['rpassword']
      #user=str(u).lower()
      obj=pass_word.encode()
      instance=salt.encode()
      crypter=Fernet(instance)
      bush=crypter.encrypt(obj)
      k=str(bush,'utf8')
      '''session["user_name"]=user
      session["password"]=k
      session["email"]=e_mail
      session["salt"]=salt
      return render_template('login.html')'''
      users=user_db.find({})
      for x in users:
        usr=x['username']
        if usr == user:
          message="Username already exists"
          return render_template("sign.html",msg=message)
      if pass_word != r_pass_word:
          message="Password doesnot match"
          return render_template("sign.html",msg=message)
      else:
          user_db.insert_one({"username":user,"password":k,"email":e_mail,"salt":salt,"type":"user"})
          return render_template("login.html") 
    
    
@app.route("/allow",methods=["POST","GET"])
def allow():
   # message=''
    flag=0
    if request.method == "POST":
      u=request.form["username"]
      pass_word=request.form["password"]
      '''if "user_name" in session:
          return render_template('login.html')
      else:
          return render_template('sign.html
      for user_name in session:  
          if u==session["user_name"]:
              return render_template('login.html')
          else:
              return render_template('sign.html')'''

      #name=str(u).lower()
      users=user_db.find({})
      for x in users:
        n=x['username']
        if n == u:
          flag=1
      if(flag==0):
        message="Invalid Username"  
        return render_template("login.html",msg=message) 
      user_1=user_db.find({"username":u})
      for x in user_1:
        s_user = x['username']
        pwd=x['password']
        sss=x['salt']
        user_type=x['type']
        s=pwd.encode()
        instance=sss.encode()
        crypter=Fernet(instance)
        decryptpw=crypter.decrypt(s)
        returned=decryptpw.decode('utf8')
        if returned == pass_word:
            if user_type == "admin" :
                session["user_name"]=s_user
                session["password"]=pwd
                session["type"]= x['type']
                return render_template("admin-entry.html")
            else :
                session["user_name"]=s_user
                session["password"]=pwd
                session["type"]= x['type']
                return redirect(url_for('index'))
                
                #return render_template("index.html")
        else:
          message="Invalid Password"  
          return render_template("login.html",msg=message) 

@app.route('/entry',methods=["POST","GET"])
def entry():
    return render_template('admin-entry.html')


@app.route('/adding',methods=["POST","GET"])
def adding():
    if "user_name" in session :
        if session["type"] == "admin" :
            if request.method == 'POST':
                user  = request.form['user']
                event = request.form['event']
                coins = request.form['coins']
                coins = int(coins)
                #users=total_db.find().sort({"_id":-1}).limit(1)
                users=total_db.find().sort([('_id', -1)]).limit(1)
                for x in users:
                    i = x['index']
                i = int(i) +1
                users = total_db.insert_one({"index":i,"Name":user,"Event":event,"TactPoints":coins})
            return render_template('admin-entry.html')
        else :
            return render_template('login.html',msg="Invalid Access")
    else :
        return render_template('login.html',msg="Login Required")

@app.route('/releasing',methods=["POST","GET"])
def releasing():
    if "user_name" in session :
        if session["type"] == "admin" :
            if request.method == 'POST':
                user  = request.form['user']
                event = request.form['event']
                coins = request.form['coins']
                coins = int(coins)
                #users =released_db.find().sort({"_id":-1}).limit(1)
                users=released_db.find().sort([('_id', -1)]).limit(1)
                for x in users:
                    i = x['index']
                i = int(i) +1
                users = released_db.insert_one({"index":i,"Name":user,"Event":event,"TactPoints":coins})
            return render_template('admin-entry.html')
        else :
            return render_template('login.html',msg="Invalid Access")
    else :
        return render_template('login.html',msg="Login Required")

@app.route("/logout")
def logout():
    session.pop("user_name",None)
    return render_template('login.html')
 



@app.route('/collection', methods=['GET'])
def index():
    if "user_name" in session :
        Intern_list = cc.get_names()
        to_release = []
        for i in Intern_list:
            coins=cc.totalcoins_to_be_Released(i)
            result={
                'Name':i,
                'Coins':coins
            }
            to_release.append(result)
        to_release = sorted(to_release, key = lambda i: i['Coins'],reverse = True)
        result = {
            'Intern_list' : to_release
        }
        
        return render_template('index.html', result = result)
    else :
        return render_template('login.html',msg="Login Required")


@app.route('/collection', methods=['POST'])
def result():
    if "user_name" in session :
        name = request.values.get('name')
    
        #print(insert_data.select_data(soul_name))
        name = name.capitalize()
        #print(name)
        Intern_list = cc.get_names()
        to_release = []
        for i in Intern_list:
            coins=cc.totalcoins_to_be_Released(i)
            result={
                'Name':i,
                'Coins':coins
            }
            to_release.append(result)
        to_release = sorted(to_release, key = lambda i: i['Coins'],reverse = True)
        if cc.is_name_present(name):
            total = cc.totalcoins(name)
            released = cc.totalcoinsReleased(name)
            to_be_released = total - released
            history = cc.get_history(name)
            result = {
                'Name' : name,
                'total' : total,
                'released' : released,
                'to_be_released' : to_be_released,
                'Intern_list' :to_release,
                'history' : history
            }

            return render_template('index.html', result = result)
        else:
            result = {
                'Name' : 'NotFound',
                'total' : 0,
                'released' : 0,
                'to_be_released' : 0,
                'Intern_list' : Intern_list
            
            }
            
            return render_template('index.html', result = result)
    else :
        return render_template('login.html',msg="Login Required")
    #print(rec_list)


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


if __name__ == '__main__':
    #app.debug = True;1
    app.run('127.0.0.1', 5000, True)
