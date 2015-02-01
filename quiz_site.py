import copy
import json
import os
import random
import flask
from cache import DBCache
from pagination import Pagination
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)
quizzes = {}
questions = {}
quiz_dir = 'quizzes'
quiz_file = 'sample_qns'
PER_PAGE = 1

def init():
    cacheHandle  = DBCache()
    # Load sample questions from the template
    print 'Loading', quiz_file
    
 

# Deafult app route
# Displays the list of quizzes available in the system
@app.route('/')
def index():
    return redirect(url_for('quiz'))

# Display questions for the quiz given by the specific id
@app.route('/quiz')
def quiz():
    cacheHandle  = DBCache()
    quiz = cacheHandle.tableHandle.all()[0]
    questions = list(enumerate(quiz["questions"]))
    if not questions:
        abort(404)
    random.shuffle(questions)
    posted_qns = quiz["questions"]
    print json.dumps(posted_qns, sort_keys=True, indent=4, separators=(',', ': ')) 

    quiz["questions"] = map(lambda t: t[1], questions)
    ordered_qns = map(lambda t: t[0], questions)

    return render_template('quiz.html', q_eid=str(quiz.eid), quiz=quiz, ordered_qns=json.dumps(ordered_qns), posted_qns=json.dumps(posted_qns))

# Compute stats of each question based on the option choosen
@app.route('/update_quiz', methods=['POST'])
def update_quiz():
    ordering = json.loads(flask.request.form["ord_qns"])
    posted_qns = json.loads(flask.request.form["post_qns"])
    q_eid = flask.request.form["q_eid"]
    cacheHandle  = DBCache()
    table = cacheHandle.tableHandle
    answers = dict( (int(k), posted_qns[int(k)]['options'][int(v)]) for k, v in flask.request.form.items() if k != 'ord_qns' and k != 'post_qns' and k != 'q_eid')
    if len(answers.keys()) != len(posted_qns):
        return flask.redirect(flask.url_for('quiz'))

    for q_id in answers:
        question = posted_qns[q_id]
        options = question['options']
        for opt in options:
            if opt[0] == answers[q_id][0]:
                print opt[0]
                opt[1] += 1
    # print json.dumps(posted_qns, sort_keys=True, indent=4, separators=(',', ': ')) 
    table.update({"questions": posted_qns}, eids=[q_eid])
    return flask.render_template('check_quiz.html', quiz=quiz)

@app.route('/stats')
def stats():
    cacheHandle  = DBCache()
    quiz = cacheHandle.tableHandle.all()[0]
    quiz_stats = quiz['questions']

    return quiz_stats


if __name__ == '__main__':
    init()
    app.run(debug=True)