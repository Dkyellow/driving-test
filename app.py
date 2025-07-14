from flask import Flask, render_template, request, session
import random
import json



app = Flask(__name__)
app.secret_key = 'my_key'


# Define the quiz questions and answers
with open('questions.json', 'r') as f:
    quiz_questions = json.load(f)



# Initialize score
score = 0
#Number of questions
num_questions = 25
@app.route('/')
def index():
    session['random_questions'] = random.sample(quiz_questions, num_questions)
    enumerated_questions = list(enumerate(session['random_questions']))
    return render_template('index.html', quiz_questions=enumerated_questions)


@app.route('/submit', methods=['POST'])
def submit():
    global score
    score = 0
    results = []
    for i, question in enumerate(session['random_questions']):
        answer = request.form[f'question_{i}']
        is_correct = answer == question['answer']
        if is_correct:
            score += 1
        results.append({
            "question": question['question'],
            "image": question['image'],
            "user_answer": answer,
            "correct_answer":question['answer'],
            "is_correct": is_correct
        })
    return render_template('result.html', score=score, total=num_questions, results=results)

if __name__ == '__main__':
    app.run(debug=True)