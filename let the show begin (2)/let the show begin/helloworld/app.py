import os

from flask import Flask,session
from flask import *
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
from flask_session import Session
import uuid
import datetime
from bson import Binary
load_dotenv(find_dotenv())
#############################################
password = os.environ.get('MONGODB_PWD')
connection_string = f"mongodb+srv://root:{password}@waliwo.devaw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

dbs = client.list_database_names()
tets_db = client.user

collections = tets_db.list_collection_names()
print(collections)
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = 'tuwnhkmdbgspqlloskm523943557'
Session(app)
##############################################

##############################################
@app.route('/',methods=["POST","GET"])
def hello_world():
    if request.method == 'POST':
        email =  request.form.get("email")
        pass_word = request.form.get("pass_word")
        name = request.form.get("name")
        collection = tets_db.user
        inuq_id = uuid.uuid4()
        Crt_Time = datetime.datetime.now()
        test_docu = {
            'email':email,
            'password':pass_word,
            'name':name,
            'username':'',
            'uuID':str(inuq_id),
            'Account_Created':Crt_Time
        }
        duplex = collection.count_documents({'email':email})>0
        print(duplex)
    try:
        if duplex == True:
            return "<h1>Email Already Exist</h1>" 
    except:
        pass
    else:
        session['user'] = inuq_id
        session['USRCRD'] = test_docu
        inserted_id = collection.insert_one(test_docu).inserted_id
        return redirect('/username')
    if 'user' in session:
        inuq_ID = session['user']
        collection = tets_db.user
        exists_ID = collection.count_documents({'uuID':str(inuq_ID)})>0
        if exists_ID == True:
            return "<h1>User Logged In</h1>"
        else:
            return "<h1>User Not Logged In</h1>"    
        
        print(inserted_id)
    return render_template('register.html')
##############################################

##############################################
@app.route('/username',methods=["POST","GET"],)
def username():
    if request.method == 'POST':
        username = request.form.get("username")
        collection = tets_db.user
        test_docu = {
            'username':username
        }
        if "user" in session:
            user = session['user']
            session['USRCRD'] = test_docu
        duplex = collection.count_documents({'username':username})>0
        hail =(user)
        print(collection)
    try:
        if duplex == True:
            return "<h1>Username Taken !</h1>" 
    except:
        pass
    else:
        all_updates ={
            '$set':{'username':username}
        }
        collection.update_one({'_id':str(user)},all_updates)
        return redirect('/home')
        print(duplex)
    return render_template('username.html')
##############################################


##############################################
@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email =  request.form.get("email")
        username =  request.form.get("email")
        pass_word =  request.form.get("pass_word")
        collection = tets_db.user
        exists = collection.count_documents({'email':email,'password':pass_word})>0
        exists_username = collection.count_documents({'username':username,'password':pass_word})>0
        print(exists)
    
        if exists or exists_username == True:
            inuq_id = uuid.uuid4()
            print(inuq_id)
            all_updates ={
            '$set':{'uuID':str(inuq_id)}}
            collection.update_one({'email':email},all_updates)
            session['user'] = inuq_id
            print(inuq_id)
            return "<h1>Account Found</h1>"
        else: 
            return "<h1>Account Not found</h1>"
    if 'user' in session:
        inuq_ID = session['user']
        collection = tets_db.user
        exists_ID = collection.count_documents({'uuID':str(inuq_ID)})>0
        if exists_ID == True:
            return "<h1>User Logged In</h1>"
        else:
            return "<h1>User Not Logged In</h1>"
    return render_template('login.html')
##############################################

##############################################
@app.route('/home',methods=["GET","POST"])
def home():
    collection = tets_db.post
    if 'user' in session:
      user = session['user']
      if request.method =='POST':
        text = request.form.get('text')
        if not text:
            flash("Post cannot be empty", category='error')
            flash("Post Created", category='success')
        else:
            collection.insert_one({'post':text,'creator':'test','show':True})
            cursor = collection.find()
        for each_document in cursor:
            print(each_document)
            
    return render_template('home.html',post=each_document)

##############################################







if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))