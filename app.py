from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://survey_user:your_password@localhost/survey_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def survey_start():
    return render_template('survey_start.html', survey=satisfaction_survey)

@app.route('/start', methods=['POST'])
def start_survey():
    session['responses'] = []
    return redirect(url_for('question', qid=0))

@app.route('/questions/<int:qid>')
def question(qid):
    responses = session.get('responses')
    if responses is None:
        return redirect(url_for('survey_start'))

    if qid >= len(satisfaction_survey.questions):
        flash("Invalid question number.")
        return redirect(url_for('completion'))

    if len(responses) != qid:
        flash("You're trying to access an invalid question.")
        return redirect(url_for('question', qid=len(responses)))

    question = satisfaction_survey.questions[qid]
    return render_template('question.html', survey=satisfaction_survey, question_num=qid, question=question)

@app.route('/answer', methods=['POST'])
def answer():
    choice = request.form['answer']
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect(url_for('completion'))
    else:
        return redirect(url_for('question', qid=len(responses)))

@app.route('/completion')
def completion():
    return render_template('completion.html', survey=satisfaction_survey)

if __name__ == '__main__':
    app.run(debug=True)
