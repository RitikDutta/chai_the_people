from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/questions', methods=['GET', 'POST'])
def questions():
    questions = {
        1: {'text': 'What is your name?', 'options': ['John', 'Mary', 'Tom']},
        2: {'text': 'What is your age?', 'options': ['18-25', '26-35']},
        3: {'text': 'What is your favorite color?', 'options': ['Red', 'Green', 'Blue']}
    }
    args = request.args
    print(args.get("id"))

    if request.method == 'POST':
        answers = {}
        for question_id in questions:
            answers[question_id] = request.form.get(str(question_id))
        # return str(answers)
        print(answers)
    return render_template('questions.html', questions=questions)


if __name__ == "__main__":
    app.run(debug=True)
