import copy
import flask
import json
import os
import random

app = flask.Flask(__name__)
quiz_dir = 'quizzes'

# Load sample questions from the template
quizzes = {}
for quiz in os.listdir(quiz_dir):
    print 'Loading', quiz
    quizzes[quiz] = json.loads(open(os.path.join(quiz_dir, quiz)).read())

# Deafult app route
@app.route('/')
def index():
    return flask.render_template('index.html', quiz_names=zip(quizzes.keys(), map(lambda q: q['name'], quizzes.values())))

# Display questions for the quiz given by the specific id
@app.route('/quiz/<id>')
def quiz(id):
    if id not in quizzes:
        return flask.abort(404)
    quiz = copy.deepcopy(quizzes[id])
    questions = list(enumerate(quiz["questions"]))
    random.shuffle(questions)
    quiz["questions"] = map(lambda t: t[1], questions)
    ordering = map(lambda t: t[0], questions)

    return ordering
    # return flask.render_template('quiz.html', id=id, quiz=quiz, quiz_ordering=json.dumps(ordering))

# Compute stats of each question based on the option choosen
@app.route('/check_quiz/<id>', methods=['POST'])
def check_quiz(id):
    ordering = json.loads(flask.request.form['ord'])
    quiz = quizzes[id]
    quiz['questions'] = sorted(quiz['questions'], key=lambda q: ordering.index(quiz['questions'].index(q)))
    answers = dict( (int(k), quiz['questions'][int(k)]['options'][int(v)]) for k, v in flask.request.form.items() if k != 'ord' )
    
    for q_id in answers:
    question = quiz['questions'][q_id]
    options = question['options']
    for opt in options:
        print opt[0], answers[q_id][0]
        if opt[0] == answers[q_id][0]:
            opt[1] += 1

    if not len(answers.keys()):
        return flask.redirect(flask.url_for('quiz', id=id))

    for k in xrange(len(ordering)):
        if k not in answers:
            answers[k] = [None, False]

    answers_list = [ answers[k] for k in sorted(answers.keys()) ]

    return flask.render_template('check_quiz.html', quiz=quiz, question_answer=zip(quiz['questions'], answers_list), correct=0, total=len(answers_list))

@app.route('/stats')
def stats(id):
    if id not in quizzes:
        return flask.abort(404)
    quiz = quizzes[id]
    quiz_stats = quiz['questions']

    return quiz_stats


if __name__ == '__main__':
    app.run(debug=True)