import os
import sqlite3
# import cv2 as cv
import numpy as nu
from datetime import datetime
# import pyzbar.pyzbar as pyzbar (Scanning QR Code)
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import flask_session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, user_tracked_location, input_location_coords, password_check, send_notification_email


# Configure application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Connecting to database
conn = sqlite3.connect("database.db", timeout = 50, check_same_thread=False)
db = conn.cursor()
try:
    sqliteConnection = sqlite3.connect("database.db")
    print("Database created and succcessfully connected to SQLite")

    sqlite_select_Query = "select sqlite_version();"
    db.execute(sqlite_select_Query)
    record = db.fetchall()
    print("SQlite database version is: ", record)
except:
    print(f"Error while connecting to sqlite")



# Database one time generating table
'''
db.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, email TEXT, password TEXT)")

db.execute(""" /*hjhj*/
CREATE TABLE colleges(
SrNo DOUBLE,
Merit_Score VARCHAR(100),
Choice_Code DOUBLE,
Institute VARCHAR(100),
Course_Name VARCHAR(100),
Exam_JEEMHT__CET VARCHAR(100),
Type VARCHAR(100),
Seat_Type VARCHAR(100)
);""")
'''



# Loading colleges info in SQLite table
"""
with open('cetcell 2020.csv','r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['Sr.No.'], i['Merit (Score)'], i['Choice Code'], i['Institute'], i['Course Name'], i['Exam (JEE/MHT  CET)'], i['Type'], i['Seat Type']) for i in dr]
db.executemany("INSERT INTO colleges (SrNo, Merit_Score, Choice_Code, Institute, Course_Name, Exam_JEEMHT__CET, Type, Seat_Type) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()
print("clg insertion successfull")
"""

#commenting feature
# Database table creation (Run once)
'''
db.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
name TEXT, 
email TEXT, 
password TEXT
);""")

db.execute("""
CREATE TABLE IF NOT EXISTS comments(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
text TEXT NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""")

db.execute("""
CREATE TABLE IF NOT EXISTS replies(
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
comment_id INTEGER NOT NULL,
text TEXT NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE
);""")
'''

#Routes for commenting

# Function to add comment
'''
@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    text = data['text']
    
    db.execute("INSERT INTO comments (text) VALUES (?)", (text,))
    conn.commit()
    return jsonify({"message": "Comment added!"})

# Function to add reply
@app.route('/add_reply', methods=['POST'])
def add_reply():
    data = request.get_json()
    comment_id = data['comment_id']
    text = data['text']
    
    db.execute("INSERT INTO replies (comment_id, text) VALUES (?, ?)", (comment_id, text))
    conn.commit()
    return jsonify({"message": "Reply added!"})

# Function to get comments and replies
@app.route('/get_comments', methods=['GET'])
def get_comments():
    db.execute("SELECT * FROM comments")
    comments = db.fetchall()

    response = []
    for comment in comments:
        comment_id, text, created_at = comment
        db.execute("SELECT text FROM replies WHERE comment_id=?", (comment_id,))
        replies = db.fetchall()
        response.append({
            "id": comment_id,
            "text": text,
            "created_at": created_at,
            "replies": [{"text": reply[0]} for reply in replies]
        })
    
    return jsonify({"comments": response})

if __name__ == '__main__':
    app.run(debug=True)

'''
# APP ROUTES

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/details", methods=["GET", "POST"])
def details():
    # If user reached route via POST
    if request.method == "POST":
        # Getting user info
        cet = request.form.get("cet") # Getting input via scanning QR of marklist
        jee = request.form.get("jee")
        location = request.form.get("location") # Location tracking using ip address
        entered_location = request.form.get("entered_location")
        ce = request.form.get("Computer Engineering")
        it = request.form.get("Information Technology")
        cse = request.form.get("Computer Science and Engineering(Data Science)")
        ai = request.form.get("Artificial Intelligence and Data Science")
        mech = request.form.get("Mechanical Engineering")
        ee = request.form.get("Electronics Engineering")
        che = request.form.get("Chemical Engineering")
        et = request.form.get("Electronics and Telecommunication\nEngg")
        ae = request.form.get("Automobile Engineering")

        # Basic errorhandeling
        if cet=="" and jee=="":
            return apology("Atleast one marks are required")
        

        # Scanning QR code
        '''
        NOT IMPLEMENTED DUE TO PYZBAR ".dll" DISCREPANCY
        cap = cv.VideoCapture(2)

        while True:
            _, frame = cap.read()

            barcode = pyzbar.decode(frame)
            for bdata in barcode:
                print(f"data  {bdata.data}")
                Data = barcode.data.decode("utf-8")
                Type = barcode.type
                print(f"data  {Data}")
                print(f"type  {Type}")
            break
        '''

        # Database query for best clg suggestions
        li = [ce, it, cse, ai, mech, ee, che, et, ae]
        fli = []
        ffli = []
        for item in li:
            if item != None:
                fli.append([item])

        for item in range(len(fli)):
            ffli.append(fli[item][0])

        params = []
        params.append(jee)
        for item in ffli:
            params.append(item)
        # print(f"params: {params}")
        
        # Database query for colleges in which admission is possible due to jee
        db.execute("SELECT * FROM colleges WHERE Merit_Score<=? AND Exam_JEEMHT__CET='JEE' AND Course_Name IN (%s)"%', '.join('?' for a in ffli), params)
        global clg_jee_list
        clg_jee_list = db.fetchall()
        # print(f"clg_jee_list: {clg_jee_list}")

        params[0] = cet
        #print(f"params: {params}")
        # Database query for colleges in which admission is possible due to mht-cet
        db.execute("SELECT * FROM colleges WHERE Merit_Score<=? AND Exam_JEEMHT__CET='MHT CET' AND Course_Name IN (%s)"%', '.join('?' for a in ffli), params)
        global clg_cet_list
        clg_cet_list = db.fetchall()
        # print(f"clg_cet_list: {clg_cet_list}")

        # Merging both jee and mht-cet lists
        global clg_list 
        clg_list = clg_jee_list + clg_cet_list
        # print(f"clg_list: {clg_list}")

        '''
        APLTERNATE CORRECT APPROCH BUT NOT WORKING PROPERLY DUE TO DISCREPANCY IN DATA
        skips some list items and displays it...........

        for list in clg_list:
            if (list[5] == "JEE" and list[1] > jee) or (list[5] == "MHT CET" and list[1] > cet):
                print(list)
                print()
                clg_list.remove(list)

        print(f"clg_list : {clg_list}")
        '''

        return redirect("/suggestions")
    # If user reached route via GET
    else:
        return render_template("details.html")



@app.route("/suggestions")
def suggestions():
    # Rendering suggestions along with clg list generated in runtime
    return render_template("suggestions.html", clg_list = clg_list)



@app.route("/faqs")
def faqs():
    return render_template("faqs.html")



# Error handlers
def errorhandler(e):
    # Basic error handeling
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)



# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)



if __name__ == '__main__':
    app.run(debug = True)


conn.close()
