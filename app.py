# app.py
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
app.secret_key = os.urandom(24)

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Connecting to database
conn = sqlite3.connect("database.db", timeout=50, check_same_thread=False)
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
    to_db = [(i['Sr.No.'], i['Merit (Score)'], i['Choice Code'], i['Institute'],
              i['Course Name'], i['Exam (JEE/MHT  CET)'], i['Type'], i['Seat Type']) for i in dr]
db.executemany("INSERT INTO colleges (SrNo, Merit_Score, Choice_Code, Institute, Course_Name, Exam_JEEMHT__CET, Type, Seat_Type) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()
print("clg insertion successfull")
"""

# commenting feature
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


# db.execute("DROP TABLE IF EXISTS answers")
# db.execute("DROP TABLE IF EXISTS questions")
# conn.commit()

db.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    question TEXT NOT NULL,
    created_at DATETIME DEFAULT (datetime('now', 'localtime')),
    upvotes INTEGER DEFAULT 0
)
""")

db.execute("""
CREATE TABLE IF NOT EXISTS answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at DATETIME DEFAULT (datetime('now', 'localtime')),
    upvotes INTEGER DEFAULT 0,
    FOREIGN KEY (question_id) REFERENCES questions(id)
)
""")
# Routes for commenting

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

    db.execute("INSERT INTO replies (comment_id, text) VALUES (?, ?)",
               (comment_id, text))
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
        # Getting input via scanning QR of marklist
        cet = request.form.get("cet")
        jee = request.form.get("jee")
        # Location tracking using ip address
        location = request.form.get("location")
        entered_location = request.form.get("entered_location")
        ce = request.form.get("Computer Engineering")
        it = request.form.get("Information Technology")
        cse = request.form.get(
            "Computer Science and Engineering(Data Science)")
        ai = request.form.get("Artificial Intelligence and Data Science")
        mech = request.form.get("Mechanical Engineering")
        ee = request.form.get("Electronics Engineering")
        che = request.form.get("Chemical Engineering")
        et = request.form.get("Electronics and Telecommunication\nEngg")
        ae = request.form.get("Automobile Engineering")

        # Basic errorhandeling
        if cet == "" and jee == "":
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
        db.execute("SELECT * FROM colleges WHERE Merit_Score<=? AND Exam_JEEMHT__CET='JEE' AND Course_Name IN (%s)" %
                   ', '.join('?' for a in ffli), params)
        global clg_jee_list
        clg_jee_list = db.fetchall()
        # print(f"clg_jee_list: {clg_jee_list}")

        params[0] = cet
        # print(f"params: {params}")
        # Database query for colleges in which admission is possible due to mht-cet
        db.execute("SELECT * FROM colleges WHERE Merit_Score<=? AND Exam_JEEMHT__CET='MHT CET' AND Course_Name IN (%s)" %
                   ', '.join('?' for a in ffli), params)
        global clg_cet_list
        clg_cet_list = db.fetchall()
        # print(f"clg_cet_list: {clg_cet_list}")

        # Merging both jee and mht-cet lists
        global clg_list
        clg_list = clg_jee_list + clg_cet_list
        # print(f"clg_list: {clg_list}")


        return redirect("/suggestions")
    # If user reached route via GET
    else:
        return render_template("details.html")

@app.route('/donation')
def donation():
    return render_template('donation.html')

@app.route('/button')
def button():
    return render_template('button.html')


# if __name__ == '__main__':
#     app.run(debug=True)

@app.route("/suggestions")
def suggestions():
    # Rendering suggestions along with clg list generated in runtime
    return render_template("suggestions.html", clg_list=clg_list)


@app.route("/faqs", methods=["GET", "POST"])
def faqs():
    if request.method == "POST":
        if "question" in request.form:
            name = request.form.get("name")
            question = request.form.get("question")
            if not name or not question:
                flash("Name and question are required!")
                return redirect("/faqs")
            db.execute("INSERT INTO questions (name, question) VALUES (?, ?)",
                       (name, question))
            conn.commit()

        elif "answer" in request.form:
            name = request.form.get("name")
            answer = request.form.get("answer")
            question_id = request.form.get("question_id")
            if not name or not answer:
                flash("Name and answer are required!")
                return redirect("/faqs")
            db.execute("INSERT INTO answers (question_id, name, answer) VALUES (?, ?, ?)",
                       (question_id, name, answer))
            conn.commit()
        return redirect("/faqs")

    db.execute("""
        SELECT 
            q.id, q.name, q.question, q.created_at, q.upvotes,
            a.name as answerer_name, a.answer, a.created_at as answer_date,
            a.id as answer_id, a.upvotes as answer_upvotes
        FROM questions q
        LEFT JOIN answers a ON q.id = a.question_id
        ORDER BY q.created_at DESC
    """)
    qa_pairs = db.fetchall()
    return render_template("faqs.html", qa_pairs=qa_pairs)


@app.route("/delete_question/<int:question_id>", methods=["POST"])
def delete_question(question_id):
    name = request.form.get("name")
    db.execute("SELECT name FROM questions WHERE id = ?", (question_id,))
    question = db.fetchone()

    if question and question[0] == name:
        db.execute("DELETE FROM answers WHERE question_id = ?", (question_id,))
        db.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        conn.commit()
        flash("Question deleted successfully!")
    else:
        flash("You can only delete your own questions!")
    return redirect("/faqs")


@app.route("/delete_answer/<int:answer_id>", methods=["POST"])
def delete_answer(answer_id):
    name = request.form.get("name")
    db.execute("SELECT name FROM answers WHERE id = ?", (answer_id,))
    answer = db.fetchone()

    if answer and answer[0] == name:
        db.execute("DELETE FROM answers WHERE id = ?", (answer_id,))
        conn.commit()
        flash("Answer deleted successfully!")
    else:
        flash("You can only delete your own answers!")
    return redirect("/faqs")


@app.route("/toggle_upvote", methods=["POST"])
def toggle_upvote():
    item_type = request.form.get("type")
    item_id = request.form.get("id")

    # Initialize upvoted items in session if not exists
    if 'upvoted' not in session:
        session['upvoted'] = []

    # Create unique identifier for the upvoted item
    item_identifier = f"{item_id}_{item_type}"

    if item_identifier in session['upvoted']:
        # Remove upvote
        session['upvoted'].remove(item_identifier)
        if item_type == "question":
            db.execute(
                "UPDATE questions SET upvotes = upvotes - 1 WHERE id = ?", (item_id,))
        elif item_type == "answer":
            db.execute(
                "UPDATE answers SET upvotes = upvotes - 1 WHERE id = ?", (item_id,))
    else:
        # Add upvote
        session['upvoted'].append(item_identifier)
        if item_type == "question":
            db.execute(
                "UPDATE questions SET upvotes = upvotes + 1 WHERE id = ?", (item_id,))
        elif item_type == "answer":
            db.execute(
                "UPDATE answers SET upvotes = upvotes + 1 WHERE id = ?", (item_id,))

    session.modified = True
    conn.commit()
    return redirect("/faqs")
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
    app.run(debug=True)


conn.close()
