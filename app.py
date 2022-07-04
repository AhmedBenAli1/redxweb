from flask import Flask, render_template ,redirect, request , session, jsonify
app=Flask(__name__)
import mysql.connector 
import mysql
import json
import test
from threading import Thread
import time
def register():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="redx")
    mycursor=mydb.cursor()
    
    sql = "INSERT INTO user (iduser,name,username,email,password,phone,score) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val = ("154",request.form.get('Name'),request.form.get('Username'),request.form.get('Email'),request.form.get('Password'),request.form.get('Number'),"0")
    mycursor.execute(sql, val)
    mydb.commit()
def Login():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="redx")
    mycursor=mydb.cursor()
    print(request.form.get('username'))
    print(request.form.get('password'))
    mycursor.execute("SELECT password FROM user WHERE username=%s",(request.form.get('username'),))
    result=mycursor.fetchone()
    print(result[0])
    givenpass=request.form.get('password')

    if (givenpass==result[0]):
        return True
    else:
        return False
def createworkspace():
    createdinstanceID = test.create_instance("subnet-03aa61e53890ca6ae")
    time.sleep(50)
    print(test.get_running_instancesids()[-1])
    lines = []
    with open('scriptemptynotebook.txt') as f:
        lines = f.readlines()
    for i in lines :
        test.runRemoteShellCommands(test.get_running_instancesids()[-1],i)
    



@app.route('/register',methods=["GET","POST"])
def RegistrationForm():
    render_template("Register.html")
    if request.method == "POST":
        try:
            register()
            return redirect('/login')
        except:
            return render_template("Registererror.html") 
          
        
    else:
        return render_template("Register.html")
@app.route('/login',methods=["GET","POST"])
def LoginForm():
    render_template("Login.html")
    if request.method == "POST":
            Validation=Login()
            if (Validation):
               return redirect('/auth')
    else:
        return render_template("login.html")
@app.route('/')
def HomePage():
    return render_template("index.html")
    
@app.route('/auth',methods=["GET","POST"])
def Userdash():
    
    if request.method == "POST":
               
            Thread(target=createworkspace, args=()).start()
            time.sleep(130)
            instancelist=test.get_running_instancesips()
            print(instancelist)
                
            url="http://"+instancelist[-1]+":8888"
            print(url)
            return redirect(url,code=302) 
    else:
        return render_template("jupyter.html")    
    
    



    



