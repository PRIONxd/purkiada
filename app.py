# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect, session, g, make_response
from flask_sqlalchemy import SQLAlchemy
import os
import json

application = Flask(__name__)
application.config.from_object("config.BaseConfig")
base_url = "/rick-and-morty/uloha7"  #/example/example2
db = SQLAlchemy(application)

class Student(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    testDone = db.Column(db.String(30))
    points = db.Column(db.Integer)
    
    def calculate(self):
        points = 0
        if get_cookie("answer1") == "Wubba-Lubba-Dub-Dub!":
            points += 1
        if get_cookie("answer2") == "restart":
            points += 2
        if get_cookie("answer3") == "jablko":
            points += 3
        if get_cookie("answer4") == "morseovka":
            points += 3
        if get_cookie("answer5") == "eelworm":
            points += 6
        if get_cookie("egg") == "2":
            points += 2
        return points
    
    def to_json(self):
        result = dict()
        result["id"] = self.id
        result["name"] = self.name
        result["username"] = self.username
        result["password"] = self.password
        result["testDone"] = self.testDone
        result["points"] = self.points
        return result
    
def get_cookie(name):
    try:
        cookie = format(request.cookies[name])
    except KeyError:
        cookie = ""
    return cookie

@application.route(base_url + "/", methods = ["GET", "POST"])
def index():
    #delete last student in session
    session.pop("student", None)

    if request.method == "POST":
        #get data from form
        username = request.form["id"]
        password = request.form["password"]

        #Authorization
        student = Student.query.filter_by(username = username, password = password).first()

        #correct password
        if student:
            #student haven't test done
            if student.testDone =="N":
                session["student"] = student.to_json()    
                return redirect(base_url + "/info")
            #student have test done
            else:
                return render_template("index.html", status = "done")
        #bad password        
        else:
            return render_template("index.html", status = "no")

    #GET METHOD
    else:
        return render_template("index.html", status = "yes")

@application.route(base_url + "/info", methods=["GET", "POST"])
def info():
    if request.method == "GET":
        if g.student:
            return render_template("info.html", name = session["student"]["name"])
        else:
            return redirect(base_url + "/")
    elif request.method == "POST":
        return redirect(base_url + "/quest1")

@application.route(base_url + "/quest1", methods = ["GET", "POST"])
def quest1():
    if request.method == "GET":
        if g.student:
            return render_template("quest1.html", name = session["student"]["name"], answer = get_cookie("answer1"))
        else:
            return redirect(base_url + "/")
    elif request.method == "POST":
        resp = make_response(redirect(base_url + "/quest2"))
        resp.set_cookie("answer1", request.form["ans1"])
        return resp

@application.route(base_url + "/quest2", methods=["GET", "POST"])
def quest2():
    if request.method == "GET":
        if g.student:
            return render_template("quest2.html", name = session["student"]["name"], answer = get_cookie("answer2"))
        else:
            return redirect(base_url + "/")
    elif request.method == "POST":
        number = request.form.get("button")
        resp = make_response(redirect(base_url + "/quest" + number))
        resp.set_cookie("answer2", request.form["ans2"])
        return resp 

@application.route(base_url + "/quest3", methods = ["GET", "POST"])
def quest3():
    if request.method == "GET":
        if g.student:
            return render_template("quest3.html", name = session["student"]["name"], answer = get_cookie("answer3"))
        else:
            return redirect(base_url + "/")
    elif request.method == "POST":
        number = request.form.get("button")
        resp = make_response(redirect(base_url + "/quest" + number))
        resp.set_cookie("answer3", request.form["ans3"])
        return resp

@application.route(base_url + "/quest4", methods = ["GET", "POST"])
def quest4():
    if request.method == "GET":
        if g.student:
            return render_template("quest4.html", name = session["student"]["name"], answer = get_cookie("answer4"))
        else:
            return redirect(base_url + "/")
    elif request.method == "POST":
        number = request.form.get("button")
        resp = make_response(redirect(base_url + "/quest" + number))
        resp.set_cookie("answer4", request.form["ans4"])
        return resp 

@application.route(base_url + "/quest5", methods = ["GET", "POST"])
def quest5():
    if request.method == "GET":
        if g.student:
            return render_template("quest5.html", name = session["student"]["name"], answer = get_cookie("answer5"))
        else:
            return redirect(base_url + "/")
    elif request.method == "POST":
        number = request.form.get("button")
        if number == "6":
            resp = make_response(redirect(base_url + "/end"))
            resp.set_cookie("answer5", request.form["ans5"])
            return resp 
        resp = make_response(redirect(base_url + "/quest" + number))
        resp.set_cookie("answer5", request.form["ans5"])
        return resp 

@application.route(base_url + "/end", methods = ["SET","GET"])
def end():
    #get student
    student_id = session["student"]["id"]
    student = Student.query.get(student_id)

    #calculate score and store it in db
    student.points = student.calculate()
    student.testDone = "Y"
    db.session.commit()

    #delete all data
    resp = make_response(redirect("https://www.purkiada.cz/rick-and-morty")) 
    resp.set_cookie("answer1", "", expires=0)
    resp.set_cookie("answer2", "", expires=0)
    resp.set_cookie("answer3", "", expires=0)
    resp.set_cookie("answer4", "", expires=0)
    resp.set_cookie("answer5", "", expires=0)
    resp.set_cookie("egg", "", expires=0)
    session["student"] = None
    g.student = None

    #REDIRECT TO SIGNPOST
    return resp

@application.route(base_url + "/helloworldKominik123")
def easteregg():
    if g.student:
        resp = make_response(render_template("easteregg.html"))
        resp.set_cookie("egg", "2")
        return resp
    else:
        return redirect(base_url + "/")

@application.route(base_url + "/results")
def results():
    data = ""
    students = Student.query.all()
    for student in students:
        data += json.dumps(student.to_json(), ensure_ascii=False)
        data += "<br><br>"
    return data

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
    #application.run(host = "0.0.0.0", port = 5207)
    application.run()