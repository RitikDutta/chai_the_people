from flask import Flask, request, render_template
from database_operations import CassandraCRUD
import datetime
app = Flask(__name__)





@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    options=''
    crud = CassandraCRUD("test_key")
    question = request.form.get('question')
    options = request.form.get('options')
    # txt = question.upper()
    print("questio ", question)
    print("options", options)
    if question is not None:
        if options is not None:
            crud.insert_survey_data(max(list(map(max, crud.last("survey").values)))+1, datetime.datetime.now().date(),  question, options)

    return render_template('add_question.html')






@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    crud = CassandraCRUD("test_key")
    args = request.args
    user_id = str(args.get("id"))
    
    name = request.form.get('name')
    age = request.form.get('age')
    annual_income = request.form.get('annual_income')
    city = request.form.get('city')
    gender = request.form.get('gender')
    marital_status = request.form.get('marital status')
    qualification = request.form.get('qualification')
    occupation = request.form.get('occupation')

    # txt = question.upper()
    print("name ", name)
    print("age ", age)
    print("annual_income ", annual_income)
    print("city ", city)
    print("gender ", gender)
    print("marital_status ", marital_status)
    print("qualification ", qualification)
    print('occupation ', occupation)
    if not (name ==None or age ==None or annual_income ==None or city ==None or gender ==None or marital_status ==None or qualification ==None or occupation ==None):
        crud.insert_user_data(user_id, datetime.datetime.now().date(), name, gender, age, annual_income, city, marital_status, qualification)
        print("No NONE Values")
    else:
        print("NONE VALUES")
    return render_template('add_user.html')


@app.route("/user_chart")
def show_tables2():
    crud = CassandraCRUD("test_key")
    data = crud.get_db("user")
    data.set_index(['user_id'], inplace=True)
    data.index.name=None
    return render_template('user_chart.html',tables=[data.to_html()],
    titles = ["User Activity"])

@app.route("/questions_chart")
def show_tables3():
    crud = CassandraCRUD("test_key")
    data = crud.get_db("survey")
    # data.set_index(['user_id'], inplace=False)
    data.index.name=None
    return render_template('questions_chart.html',tables=[data.to_html()],
    titles = ["questions_chart"])

@app.route("/responses_chart")
def show_tables4():
    crud = CassandraCRUD("test_key")
    data = crud.get_db("response")
    data.set_index(['user_id'], inplace=True)
    data.index.name=None
    return render_template('responses_chart.html',tables=[data.to_html()],
    titles = ["responses_chart"])




@app.route('/questions', methods=['GET', 'POST'])
def survey():
    crud = CassandraCRUD("test_key")
    dictionary_fields = {'text': ' ', 'options': ' '}
    db = db = crud.get_db("survey")
    
    question_id = []
    for i in range(len(db)):
        question_id.append(i+1)
    question_id

    student_record = {}
    #To create 5 records: We will run loop for 5 times
    for i in range(0, len(db)):
        student_record.update({question_id[i]: dict(dictionary_fields)})
    #Add two items to 2D dictionary
    for i in range(1, len(db)+1):
        options = db.iloc[i-1].options.split(",")
        student_record[i]['text'] = db.iloc[i-1].question
        student_record[i]['options'] = options

    # for i in range(1, 3):
    #     print(student_record[i])
        
    student_record
    questions = student_record
    args = request.args
    uid = args.get("id")
    # chk = args.get("chk")
    print(uid)
    # print(chk)
    # if args.get("chk") == "no":


    if request.method == 'POST':
        answers = {}
        for question_id in questions:
            answers[question_id] = request.form.get(str(question_id))
        # return str(answers)
        print(answers)
        print(type(answers))

        if not (uid == None or question_id == None):
            for i in range(len(answers)):
                if not answers[i+1]==None:
                    crud.insert_response_data(uid, i, answers[i+1], datetime.datetime.now().date())


    return render_template('questions.html', questions=questions)

    # else:
        # return render_template('add_user.html', uid=uid)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
