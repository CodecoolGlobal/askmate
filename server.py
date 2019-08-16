from flask import Flask, render_template, request, redirect, url_for
import data_handler, time
import util

app = Flask(__name__)
QUESTION_PATH = data_handler.QUESTION_PATH
ANSWER_PATH = data_handler.ANSWER_PATH


@app.route("/")
@app.route('/list', methods=["GET", "POST"])
def route_list():
    if request.method == "POST":

        new_q_dict = {}
        if util.isitUpdate(data_handler.get_all_data(QUESTION_PATH), request.form.get("id")):
            for key in request.form:
                new_q_dict[key] = request.form.get(key)
            data_handler.edit_question(data_handler.get_all_data(QUESTION_PATH), new_q_dict, QUESTION_PATH)
        else:
            new_q_dict = data_handler.add_new_question(request.form)
        return redirect(url_for("route_question", question_id=new_q_dict["id"]))

    else:
        s_options = data_handler.SEARCH_OPTIONS
        o_options = data_handler.ORDER_OPTIONS
        questions = data_handler.get_all_data(QUESTION_PATH)
        sorted_questions = sorted(questions, key=lambda question: question["submission_time"], reverse=True)
        for question in questions:
            question["submission_time"] = time.ctime(int(question["submission_time"]))
        return render_template("list.html", questions=sorted_questions, s_options=s_options, o_options=o_options)


@app.route("/question/<question_id>", methods=["GET", "POST"])
def route_question(question_id):
    question = data_handler.get_data_by_id(question_id, QUESTION_PATH, "id")

    if request.method == "GET":
        question["view_number"] = int(question["view_number"]) + 1
        data_handler.edit_question(data_handler.get_all_data(QUESTION_PATH), question, QUESTION_PATH)

    a_s = data_handler.get_all_data(ANSWER_PATH)
    id = data_handler.get_next_id(a_s)

    question["submission_time"] = time.ctime(int(question["submission_time"]))
    answers = data_handler.get_answers_by_qid(question_id)
    return render_template("question.html", question=question, answers=answers, id=str(id))


@app.route("/add-question", methods=["GET", "POST"])
def route_add_question():
    qs = data_handler.get_all_data(QUESTION_PATH)
    id = data_handler.get_next_id(qs)
    empty_question = {}
    return render_template("add-question.html", id=str(id), question=empty_question)


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def route_new_answer(question_id):
    data_handler.add_new_answer(request.form)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def route_delete_question(question_id):
    data_handler.write_to_file(data_handler.delete_data_by_id(question_id, QUESTION_PATH, "id"), QUESTION_PATH, "w")
    data_handler.write_to_file(data_handler.delete_data_by_id(question_id, ANSWER_PATH, "question_id"), ANSWER_PATH,
                               "w")
    return redirect(url_for("route_list"))


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def route_delete_answer(answer_id):
    answer = data_handler.get_data_by_id(answer_id, ANSWER_PATH, "id")
    question_id = answer["question_id"]
    data_handler.write_to_file(data_handler.delete_data_by_id(answer_id, ANSWER_PATH, "id"), ANSWER_PATH, "w")
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def route_edit(question_id):
    question = data_handler.get_data_by_id(question_id, QUESTION_PATH, "id")
    return render_template("add-question.html", question=question)


@app.route("/question/<question_id>/vote-up", methods=["GET", "POST"])
def route_question_vote_up(question_id):
    question = data_handler.get_data_by_id(question_id, QUESTION_PATH, "id")
    question["vote_number"] = int(question["vote_number"]) + 1
    question["view_number"] = int(question["view_number"]) - 1
    data_handler.edit_question(data_handler.get_all_data(QUESTION_PATH), question, QUESTION_PATH)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/question/<question_id>/vote-down", methods=["GET", "POST"])
def route_question_vote_down(question_id):
    question = data_handler.get_data_by_id(question_id, QUESTION_PATH, "id")
    question["vote_number"] = int(question["vote_number"]) - 1
    question["view_number"] = int(question["view_number"]) - 1
    data_handler.edit_question(data_handler.get_all_data(QUESTION_PATH), question, QUESTION_PATH)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/answer/<answer_id>/vote-up", methods=["GET", "POST"])
def route_answer_vote_up(answer_id):
    answer = data_handler.get_data_by_id(answer_id, ANSWER_PATH, "id")
    question_id = answer["question_id"]
    answer["vote_number"] = int(answer["vote_number"]) + 1
    question = data_handler.get_data_by_id(question_id, QUESTION_PATH, "id")
    question["view_number"] = int(question["view_number"]) - 1
    data_handler.edit_question(data_handler.get_all_data(QUESTION_PATH), question, QUESTION_PATH)
    data_handler.edit_question(data_handler.get_all_data(ANSWER_PATH), answer, ANSWER_PATH)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/answer/<answer_id>/vote-down", methods=["GET", "POST"])
def route_answer_vote_down(answer_id):
    answer = data_handler.get_data_by_id(answer_id, ANSWER_PATH, "id")
    question_id = answer["question_id"]
    answer["vote_number"] = int(answer["vote_number"]) - 1
    question = data_handler.get_data_by_id(question_id, QUESTION_PATH, "id")
    question["view_number"] = int(question["view_number"]) - 1
    data_handler.edit_question(data_handler.get_all_data(QUESTION_PATH), question, QUESTION_PATH)
    data_handler.edit_question(data_handler.get_all_data(ANSWER_PATH), answer, ANSWER_PATH)
    return redirect(url_for("route_question", question_id=question_id))


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
