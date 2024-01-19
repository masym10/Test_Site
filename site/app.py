from flask import Flask, session,render_template, request, redirect, url_for
from random import shuffle
from sql_queries import get_question, get_quises, check_answer

def index():
    if request.method == "GET":
        quizz= get_quises()
        return render_template("index.html", quizz=quizz, title='Title')
    
    else:
        session["quiz_id"] = request.form.get('quiz')
        session["question_id"] = 0
        session["total"] = 0
        session["answer"] = 0
        return redirect(url_for("test"))
    
def test():
    if 'quiz_id' not in session:
        return redirect(url_for('index'))
    
    if request.method == "POST":
        answer = request.form.get('quiz')
        question_id = request.form.get('question_id')

        session['question_id'] = question_id
        session['total'] += 1
    
    if check_answer(question_id, answer):
        session["answer"] += 1

    question = get_question(session["quiz_id"], session["question_id"])
    
    if question == None:
        return redirect(url_for('result'))
    answers = [question[2], question[3], question[4], question[5]]
    shuffle(answers)

    return render_template("test.html", question=question[1], answers=answers, question_id= question[0])

def result():
    return render_template("result.html", right=['answer'], total=['total'])

app = Flask(__name__, template_folder='', static_folder='')
app.config["SECRET_KEY"] = "qweqwe123"

app.add_url_rule('/', 'index', index)
app.add_url_rule('/index', 'index', index, methods=["POST", "GET"])

app.add_url_rule('/test', 'test', test, methods=["POST", "GET"])

app.add_url_rule('/result', 'result', result)

app.run(debug=False, port=5007)
