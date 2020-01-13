# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect, session, g, jsonify
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
import os
import json

application = Flask(__name__)
application.config.update(dict(SECRET_KEY="LOPDEWQUN25x", WTF_CSRF_SECRET_KEY="LOPDEWQUN25x")) #key for sending forms
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/student.db"
application.config["SECRET_KEY"] = "SQUOIMD1892xe" #Secret cipher for DB

db = SQLAlchemy(application)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    school = db.Column(db.String(80))

def calculate(ans1, ans2, ans3, ans4, ans5, egg):
    points = 0
    if ans1 == "Wubba-Lubba-Dub-Dub!":
        points += 2
    if ans2 == "restart":
        points += 2
    if ans3 == "jablko":
        points += 3
    if ans4 == "morseovka":
        points += 3
    if ans5 == "eelworm":
        points += 6
    if egg == "1":
        points += 2
    return points

@application.route("/", methods = ["GET", "POST"])
def index():
    #delete last student in session
    session.pop("student", None)

    if request.method == "POST":
        #get data from form
        username = request.form["id"]
        password = request.form["password"]

        #Authorization
        student = Student.query.filter_by(username = username, password = password).first()
        
        if student:
            #correct password
            student = {"name":student.name, "username":student.username, "school": student.school}
            session["student"] = student
            return redirect(url_for("info"))
        else:
            #bad password
            return render_template("index.html", status = "no")

    #GET METHOD    
    else:
        #rewrite easteregg js file & load page
        url = request.host_url + "helloworldKominik123"
        with open("static/scripts/scriptLog.js", 'w') as file:
            file.write("for(i = 0; i <10; i++){console.log( ' " + url + " '); console.log('');}")
        return render_template("index.html", status = "yes")
        
@application.route("/info", methods=["GET", "POST"]) 
def info():
    if request.method == "POST":
        return redirect(url_for("quest1"))
    else:
        if g.student:
            return render_template("info.html", name = session["student"]["name"], school = session["student"]["school"])
        else:
            return redirect(url_for("index"))

@application.route("/quest1", methods = ["GET", "POST"])
def quest1():
    if g.student:
        return render_template("quest1.html", name = session["student"]["name"], school = session["student"]["school"])
    else:
        return redirect(url_for("index"))

@application.route("/quest2", methods=["GET", "POST"])
def quest2():
    if g.student:
        return render_template("quest2.html", name = session["student"]["name"], school = session["student"]["school"])
    else:
        return redirect(url_for("index"))

@application.route("/quest3", methods = ["GET", "POST"])
def quest3():
    if g.student:
        return render_template("quest3.html", name = session["student"]["name"], school = session["student"]["school"])
    else:
        return redirect(url_for("index"))

@application.route("/quest4", methods = ["GET", "POST"])
def quest4():
    if g.student:
        return render_template("quest4.html", name = session["student"]["name"], school = session["student"]["school"])
    else:
        return redirect(url_for("index"))

@application.route("/quest5", methods = ["GET", "POST"])
def quest5():
    if g.student:
        return render_template("quest5.html", name = session["student"]["name"], school = session["student"]["school"])
    else:
        return redirect(url_for("index"))

@application.route("/end", methods = ["GET", "POST"])
def end():
    #get score-data
    answer1 = request.cookies["answer1"]
    answer2 = request.cookies["answer2"]
    answer3 = request.cookies["answer3"]
    answer4 = request.cookies["answer4"]
    answer5 = request.cookies["answer5"]
    try:
        easteregg = request.cookies["easteregg"]
    except KeyError:
        easteregg=""
    finally:
        #calculate score-data
        points = calculate(answer1, answer2, answer3, answer4, answer5, easteregg)
        session["student"].update({"score" : int(points), "cipher" : "true"})
        jsonData = session["student"]

    #jsonify and write all data
    with open('output.txt', 'a', encoding="utf8") as file:
        json.dump(jsonData, file, ensure_ascii=False)
        file.write("\n")
    
    #REDIRECT TO SIGNPOST
    g.student = None
    return redirect("https://www.purkiada.cz/rick-and-morty")

@application.route("/helloworldKominik123")
def easteregg():
    if g.student:
        return render_template("easteregg.html")
    else:
        return redirect(url_for("index"))

@application.before_request
def before_request():
    g.student = None
    if "student" in session:
        g.student = session["student"]

@application.errorhandler(404)
def error404(error):
    return render_template("error404.html")

@application.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(application.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == "__main__":
    application.run(debug="true", host = "0.0.0.0", port = 5207)
