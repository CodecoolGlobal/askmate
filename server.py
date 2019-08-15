from flask import Flask, render_template, request, redirect, url_for
import data_handler, time
import util

app = Flask(__name__)


@app.route("/")
@app.route('/list', methods=["GET","POST"])
def route_list():
    if request.method == "POST":
        new_q_list = []
        new_q_dict = {}
        if util.isitUpdate(data_handler.get_all_data(data_handler.QUESTION_PATH),request.form.get("id")):
            for key in request.form:
                new_q_dict[key] = request.form.get(key)
            data_handler.edit_question(data_handler.get_all_data(data_handler.QUESTION_PATH),new_q_dict, data_handler.QUESTION_PATH)

        else:
            for key in request.form:
                if key =="submission_time":
                    new_q_dict[key] = int(time.time())
                else:
                    new_q_dict[key] = request.form.get(key)
            new_q_list.append(new_q_dict)
            data_handler.write_to_file(new_q_list,data_handler.QUESTION_PATH,"a")
        return redirect(url_for("route_question",question_id=new_q_dict["id"]))

    else:
        s_options = data_handler.SEARCH_OPTIONS
        o_options = data_handler.ORDER_OPTIONS
        questions = data_handler.get_all_data(data_handler.QUESTION_PATH)
        ordered_by = util.option_converter(request.args.get("ordered_by"))
        print(ordered_by)
        order_direction = util.option_converter(request.args.get("order_direction"))
        if ordered_by is None:
            ordered_by = "submission_time" #NEMJÓ
            order_direction = True
        print(order_direction,ordered_by)
        print(questions)
        sorted_questions = sorted(questions, key= lambda question: question[ordered_by],reverse=order_direction)
        return render_template("list.html", questions=sorted_questions, s_options=s_options, o_options=o_options,selected_s_option=ordered_by,selected_o_option=order_direction)



@app.route("/question/<question_id>", methods=["GET","POST"])
def route_question(question_id):
    a_s = data_handler.get_all_data(data_handler.ANSWER_PATH)
    id = int(a_s[-1]["id"]) + 1
    question= data_handler.get_data_by_id(question_id,data_handler.QUESTION_PATH,"id")
    question["submission_time"] = time.ctime(int(question["submission_time"]))
    answers = data_handler.get_answers_by_qid(question_id)
    return render_template("question.html", question = question,answers=answers, id=str(id))

@app.route("/add-question", methods=["GET", "POST"])
def route_add_question():
    qs=data_handler.get_all_data(data_handler.QUESTION_PATH)
    id=int(qs[-1]["id"])+1
    empty_question = {}
    return render_template("add-question.html",id=str(id),question=empty_question)

@app.route("/question/<question_id>/new-answer" ,methods=["GET","POST"])
def route_new_answer(question_id):
    new_a_dict = {}
    new_a_list = []
    for key in request.form:
        if key == "submission_time":
            new_a_dict[key] = int(time.time())
        else:
            new_a_dict[key] = request.form.get(key)
    new_a_list.append(new_a_dict)
    data_handler.write_to_file(new_a_list, data_handler.ANSWER_PATH,"a")
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/question/<question_id>/delete",methods=["GET","POST"])
def route_delete_question(question_id):
    data_handler.write_to_file(data_handler.delete_data_by_id(question_id,data_handler.QUESTION_PATH,"id"),data_handler.QUESTION_PATH,"w")
    data_handler.write_to_file(data_handler.delete_data_by_id(question_id,data_handler.ANSWER_PATH,"question_id"),data_handler.ANSWER_PATH,"w")
    return redirect(url_for("route_list"))


@app.route("/answer/<answer_id>/delete", methods=["GET","POST"])
def route_delete_answer(answer_id):
    answer = data_handler.get_data_by_id(answer_id,data_handler.ANSWER_PATH,"id")
    question_id = answer["question_id"]
    data_handler.write_to_file(data_handler.delete_data_by_id(answer_id,data_handler.ANSWER_PATH,"id"),data_handler.ANSWER_PATH,"w")
    return redirect(url_for("route_question", question_id=question_id))

@app.route("/question/<question_id>/edit", methods=["GET","POST"])
def route_edit(question_id):
    question = data_handler.get_data_by_id(question_id,data_handler.QUESTION_PATH,"id")
    return render_template("add-question.html",question = question)

@app.route("/question/<question_id>/vote-up", methods=["GET","POST"])
def route_question_vote_up(question_id):
    question = data_handler.get_data_by_id(question_id, data_handler.QUESTION_PATH, "id")
    question["vote_number"] = int(question["vote_number"]) + 1
    data_handler.edit_question(data_handler.get_all_data(data_handler.QUESTION_PATH), question, data_handler.QUESTION_PATH)
    return redirect(url_for("route_question", question_id=question_id))

@app.route("/question/<question_id>/vote-down", methods=["GET","POST"])
def route_question_vote_down(question_id):
    question = data_handler.get_data_by_id(question_id, data_handler.QUESTION_PATH, "id")
    question["vote_number"] = int(question["vote_number"]) - 1
    data_handler.edit_question(data_handler.get_all_data(data_handler.QUESTION_PATH), question, data_handler.QUESTION_PATH)
    return redirect(url_for("route_question", question_id=question_id))

@app.route("/answer/<answer_id>/vote-up", methods=["GET","POST"])
def route_answer_vote_up(answer_id):
    answer = data_handler.get_data_by_id(answer_id, data_handler.ANSWER_PATH, "id")
    question_id = answer["question_id"]
    answer["vote_number"] = int(answer["vote_number"]) + 1
    data_handler.edit_question(data_handler.get_all_data(data_handler.ANSWER_PATH), answer, data_handler.ANSWER_PATH)
    return redirect(url_for("route_question", question_id=question_id))


@app.route("/answer/<answer_id>/vote-down", methods=["GET","POST"])
def route_answer_vote_down(answer_id):
    answer = data_handler.get_data_by_id(answer_id, data_handler.ANSWER_PATH, "id")
    question_id = answer["question_id"]
    answer["vote_number"] = int(answer["vote_number"]) - 1
    data_handler.edit_question(data_handler.get_all_data(data_handler.ANSWER_PATH), answer, data_handler.ANSWER_PATH)
    return redirect(url_for("route_question", question_id=question_id))

if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
