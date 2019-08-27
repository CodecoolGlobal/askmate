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

        if util.isitUpdate("question",request.form.get("id")):
            data_handler.edit_row("question",request.form)
        else:
            data_handler.add_new_row_to_table(request.form,"question")
        return redirect(url_for("route_question", question_id=request.form.get("id")))

    else:
        search_options = data_handler.SEARCH_OPTIONS
        order_options = data_handler.ORDER_OPTIONS
        questions = data_handler.get_all_data('question')
        selected_o_option = request.args.get("order_direction")#ezt megtudja tartani
        selected_s_option = request.args.get("ordered_by")#ezt nem tudja valszeg a láthatatlan whitespace a string végén nem tudom biztosan
        try:
            
            order_direction = util.OPTIONS[request.args.get("order_direction")]
            print(order_direction)
            print(request.args.get("ordered_by"))
            ordered_by = util.OPTIONS[request.args.get("ordered_by")]
            print(ordered_by)
        except KeyError:
            ordered_by = "submission_time"
            order_direction = True

        for question in questions:
            question["vote_number"] = int(question["vote_number"])
            question["view_number"] = int(question["view_number"])#itt lehet valami intes baja van
            question["title"] = question["title"].lower() #a nagybetűk miatt nem tudja sortolni

        sorted_questions = sorted(questions, key=lambda question: question[ordered_by], reverse=order_direction)
        #for question in questions:
         #   question["submission_time"] = time.ctime(int(question["submission_time"]))
        print(order_direction,ordered_by)
        return render_template("list.html", questions=sorted_questions, s_options=search_options, o_options=order_options, selected_s_option=selected_s_option,selected_o_option=selected_o_option)

@app.route("/question/<question_id>", methods=["GET", "POST"])
def route_question(question_id):
    question = data_handler.get_data_by_id(question_id,'question')[0]
    print(question)
    if request.method == "GET":

        question["view_number"] = int(question["view_number"]) + 1
        data_handler.edit_row('question',question)

    a_s = data_handler.get_all_data('answer')
    id = data_handler.get_next_id(a_s)

    #question["submission_time"] = time.ctime(int(question["submission_time"]))
    answers = data_handler.get_answers_by_qid(question_id)
    return render_template("question.html", question=question, answers=answers, id=str(id))


@app.route("/add-question", methods=["GET", "POST"])
def route_add_question():
    qs = data_handler.get_all_data("question")
    id = data_handler.get_next_id(qs)
    empty_question = {}
    return render_template("add-question.html", id=str(id), question=empty_question)


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def route_new_answer(question_id):
    data_handler.add_new_row_to_table(request.form,"answer")
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def route_delete_question(question_id):
    data_handler.delete_data_by_id(question_id,"question")
    answers_to_question = data_handler.get_answers_by_qid(question_id)
    for answer in answers_to_question:
        data_handler.delete_data_by_id(answer.get("id"),"answer")
    return redirect(url_for("route_list"))


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def route_delete_answer(answer_id):
    answer = data_handler.get_data_by_id(answer_id,'answer')
    question_id = answer.get('question_id')
    data_handler.delete_data_by_id(answer.get("id"),"answer")
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def route_edit(question_id):
    question = data_handler.get_data_by_id(question_id,'question')
    return render_template("add-question.html", question=question)


@app.route("/question/<question_id>/vote-up", methods=["GET", "POST"])
def route_question_vote_up(question_id):
    question = data_handler.get_data_by_id(question_id,'question')
    question["vote_number"] = int(question["vote_number"]) + 1
    question["view_number"] = int(question["view_number"]) - 1
    data_handler.edit_row("question",question)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/question/<question_id>/vote-down", methods=["GET", "POST"])
def route_question_vote_down(question_id):
    question = data_handler.get_data_by_id(question_id,'question')
    question["vote_number"] = int(question["vote_number"]) - 1
    question["view_number"] = int(question["view_number"]) - 1
    data_handler.edit_row("question",question)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/answer/<answer_id>/vote-up", methods=["GET", "POST"])
def route_answer_vote_up(answer_id):
    answer = data_handler.get_data_by_id(answer_id,'answer')
    question_id = answer["question_id"]
    answer["vote_number"] = int(answer["vote_number"]) + 1
    question = data_handler.get_data_by_id(question_id,'question')
    question["view_number"] = int(question["view_number"]) - 1
    data_handler.edit_row("question",question)
    data_handler.edit_row("answer",answer)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/answer/<answer_id>/vote-down", methods=["GET", "POST"])
def route_answer_vote_down(answer_id):
    answer = data_handler.get_data_by_id(answer_id,'answer')
    question_id = answer["question_id"]
    answer["vote_number"] = int(answer["vote_number"]) - 1
    question = data_handler.get_data_by_id(question_id,'question')
    question["view_number"] = int(question["view_number"]) - 1
    data_handler.edit_row("question", question)
    data_handler.edit_row("answer", answer)
    return redirect(url_for("route_question", question_id=question_id))


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
