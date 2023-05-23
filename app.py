from surveys import Question, Survey, satisfaction_survey
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import os

app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "32j54hwcon49s1k"

debug = DebugToolbarExtension(app)


def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))
# credit: MarredCheese at https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file
# is used to automatically update static files without having to hard refresh the browser for every change :D

@app.route("/")
def root():
    return render_template("root.html", title=satisfaction_survey.title, instructions=satisfaction_survey.instructions, last_updated=dir_last_updated("static"))

@app.route("/create_session", methods=["POST"])
def create_session():
    session["responses"] = []
    return redirect(f"questions/0")

@app.route("/questions/<int:num>")
def questions(num):
    if (len(session.get("responses", [])) == len(satisfaction_survey.questions)):
        flash("To redo the survey click here")
        return redirect("/thank_you")
    elif (session.get("responses", False) == False or num != len(session["responses"])):
        flash("Invalid question access")
        return redirect(f"/questions/{len(satisfaction_survey.questions)}")
    return render_template("question.html", question=satisfaction_survey.questions[num], num=num+1, last_updated=dir_last_updated("static"))

@app.route("/answer", methods=["POST"])
def answer():
    responses = session["responses"]
    responses.append(request.args['ans'])
    session["responses"] = responses
    if (int(request.args['num']) == len(satisfaction_survey.questions)):
        return redirect("/thank_you")
    return redirect(f"/questions/{request.args['num']}")

@app.route("/thank_you")
def thank_you():
    if (session.get("responses", False) == False):
        flash("You hadn't started the survey yet!")
        return redirect(f"/questions/{len(session['responses'])}")
    elif (len(satisfaction_survey.questions) != len(session["responses"])):
        flash("You haven't finished the survey yet!")
        return redirect(f"/questions/{len(session['responses'])}")
    return render_template("thank_you.html", session=session["responses"], last_updated=dir_last_updated("static"))

