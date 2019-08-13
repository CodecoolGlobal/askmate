from flask import Flask, render_template, request, redirect, url_for
import data_handler
import connection

app = Flask(__name__)


@app.route("/")
@app.route('/list', methods=["GET","POST"])
def route_list():
    questions = data_handler.get_all_data(data_handler.QUESTION_PATH)
    return render_template("list.html", questions=questions)



@app.route("/question/<question_id>", methods=["GET","POST"])
def route_question(question_id):
    question= data_handler.get_q_by_id(question_id)
    answers = data_handler.get_answers_by_qid(question_id)
    return render_template("question.html", question = question,answers=answers)

@app.route("/add-question", methods=["GET", "POST"])
def route_add_question():
    return render_template("add-question.html")


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
