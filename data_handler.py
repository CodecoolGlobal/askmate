import csv
import time
import connection
from datetime import datetime

ANSWER_PATH = "data/answer.csv"
QUESTION_PATH = "data/question.csv"
SEARCH_OPTIONS = ["Date", "Vote", "View", "Title"]
ORDER_OPTIONS = ["Ascending", "Descending"]

@connection.connection_handler
def get_all_data(cursor,table):
    query = 'SELECT * FROM '+table
    cursor.execute(query)
    data = cursor.fetchall()
    return data

@connection.connection_handler
def get_data_by_id(cursor,id,table):
    query = 'SELECT * FROM '+table+' WHERE id ='+ id
    cursor.execute(query)
    data = cursor.fetchall()
    return data

@connection.connection_handler
def get_answers_by_qid(cursor,question_id):
    cursor.execute("""
                            SELECT * FROM answer WHERE question_id = %s;
                           """,question_id)
    data = cursor.fetchall()
    return data

@connection.connection_handler
def write_to_table(cursor,data,table):
    data = replace_values(data)
    columns=[column for column in data]
    values = [data[column] for column in columns]
    query = 'INSERT INTO'+table+'('+','.join(columns)+')'+'VALUES'+'('+','.join(values)+')'
    cursor.execute(query)

@connection.connection_handler
def add_new_row_to_table(cursor,data,table):
    data = replace_values(data)
    data = add_current_time(data)
    columns=[column for column in data]
    values = [data[column] for column in columns]
    query = 'INSERT INTO'+table+'('+','.join(columns)+')'+'VALUES'+'('+','.join(values)+')'
    cursor.execute(query)
"""
def write_to_file(data, path, mode):
    fieldnames = [key for key in data[0]]
    with open(path, mode) as f:
        writer = csv.DictWriter(f, fieldnames, delimiter=',', restval="")
        if mode == "w":
            writer.writeheader()

        writer.writerows(data)
"""
@connection.connection_handler
def delete_data_by_id(cursor,id,table):
    query='DELETE FROM '+table+' WHERE id='+id
    cursor.execute(query)

"""
def delete_data_by_id(id, path, key):
    data_to_remain = []
    all_data = get_all_data(path)
    for data in all_data:
        if data[key] == id:
            continue
        else:
            data_to_remain.append(data)
    return data_to_remain"""

def add_current_time(data):
    data['submission_time'] = datetime.now()
    return data

@connection.connection_handler
def edit_row(cursor,table,new_row):
    query=""
    if table == "question":
        query='UPDATE question SET submission_time=%s,view_number=%d,vote_number=%d,title=%s,message=%s,image=%s WHERE id=%s;'
    elif table == "answer":
        query='UPDATE answer SET submission_time=%s,vote_number=%d,question_id=%d,message=%s,image=%s WHERE id=%s;'
    #FELADOM
    cursor.execute(query,value)


def replace_values(data):
    ret_data = []
    for elem in data:

        elem = elem.replace("'","''")
        ret_data.append(elem)
    return ret_data


@connection.connection_handler
def get_next_id(table):
    query = 'SELECT id FROM '+table+' '

def get_next_id(all_data):
    return int(all_data[-1]["id"]) + 1

"""
def add_new_answer(request_form):
    new_a_dict = {}
    new_a_list = []
    for key in request_form:
        if key == "submission_time":
            new_a_dict[key] = int(time.time())
        else:
            new_a_dict[key] = request_form.get(key)
    new_a_list.append(new_a_dict)
    write_to_file(new_a_list, ANSWER_PATH, "a")
"""