import csv

ANSWER_PATH = "data/answer.csv"
QUESTION_PATH = "data/question.csv"

def get_all_data(path):
    rows = []
    with open(path,"r") as f:
        csv_reader = csv.DictReader(f, delimiter = ',',restval="")
        for row in csv_reader:
            row_dict = {}
            for header in row:
                row_dict[header] = row[header]
            rows.append(row_dict)
        return rows

def get_q_by_id(qid):
    with open(QUESTION_PATH,"r") as f:
        csv_reader = csv.DictReader(f, delimiter = ',',restval="")
        question_dict = {}
        for row in csv_reader:
            if row["id"] == qid:
                for header in row:
                    question_dict[header] = row[header]
        return question_dict

def get_answers_by_qid(qid):
    answers = []
    with open(ANSWER_PATH,"r") as f:
        csv_reader = csv.DictReader(f, delimiter = ',',restval="")
        for answer in csv_reader:
            if answer["question_id"] == qid:
                answer_dict = {}
                for header in answer:
                    answer_dict[header] = answer[header]
                answers.append(answer_dict)
        return answers