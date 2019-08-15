import csv

ANSWER_PATH = "data/answer.csv"
QUESTION_PATH = "data/question.csv"
SEARCH_OPTIONS = ["Date", "Vote", "View", "Title"]
ORDER_OPTIONS = ["Ascending", "Descending"]

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

def get_data_by_id(id,path,key):
    with open(path,"r") as f:
        csv_reader = csv.DictReader(f, delimiter = ',',restval="")
        data_dict = {}
        for row in csv_reader:
            if row[key] == id:
                for header in row:
                    data_dict[header] = row[header]
        return data_dict

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

def write_to_file(data,path,mode):
    fieldnames=[key for key in data[0]]
    with open(path,mode) as f:
        writer = csv.DictWriter(f,fieldnames,delimiter = ',',restval="")
        if mode == "w":
            writer.writeheader()

        writer.writerows(data)

def delete_data_by_id(id,path,key):
    data_to_remain = []
    all_data = get_all_data(path)
    for data in all_data:
        if data[key] == id:
            continue
        else:
            data_to_remain.append(data)
    return data_to_remain


def edit_question(all_qs, new_q, path):
    for row in all_qs:
        if row["id"] == new_q["id"]:
            index = all_qs.index(row)
            all_qs.remove(row)
            all_qs.insert(index, new_q)
    write_to_file(all_qs,path,"w")