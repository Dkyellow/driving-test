from flask import Flask, render_template, request, session, redirect, url_for
import random
import json

app = Flask(__name__)
app.secret_key = 'my_key'

with open('questions.json', 'r') as f:
    quiz_questions = json.load(f)

NUM_QUESTIONS = 25
TIME_LIMIT = 25 * 60


@app.route('/')
def index():
    session['random_questions'] = random.sample(quiz_questions, NUM_QUESTIONS)
    session['answers'] = {}
    enumerated_questions = list(enumerate(session['random_questions']))
    return render_template(
        'index.html',
        quiz_questions=enumerated_questions,
        total=NUM_QUESTIONS,
        time_limit=TIME_LIMIT
    )


@app.route('/submit', methods=['POST'])
def submit():
    results = []
    score = 0
    for i, question in enumerate(session.get('random_questions', [])):
        answer = request.form.get(f'question_{i}', '')
        is_correct = answer == question['answer']
        if is_correct:
            score += 1
        results.append({
            "question": question['question'],
            "image": question['image'],
            "user_answer": answer,
            "correct_answer": question['answer'],
            "is_correct": is_correct
        })
    return render_template(
        'result.html',
        score=score,
        total=NUM_QUESTIONS,
        results=results
    )


if __name__ == '__main__':
    app.run(debug=True)
