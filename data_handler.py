import connection
from datetime import datetime

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
    query = f'SELECT * FROM answer WHERE question_id={question_id}'

    cursor.execute(query)
    data = cursor.fetchall()
    return data

@connection.connection_handler
def add_new_row_to_table(cursor,data,table):
    data = dict(data)
    data = replace_values(data)
    data = add_current_time(data)

    data["submission_time"] = f"""'{data["submission_time"]}'"""
    data["message"] = f"""'{data["message"]}'"""
    data["image"] = f"""'{data["image"]}'"""

    if table == "questions":
        data["title"] = f"""'{data["title"]}'"""

    columns=[column for column in data]
    values = [data[column] for column in columns]
    query = 'INSERT INTO '+table+' ('+','.join(columns)+')'+' VALUES '+'('+','.join(values)+')'
    cursor.execute(query)


@connection.connection_handler
def delete_data_by_id(cursor,id,table):
    query='DELETE FROM '+table+' WHERE id='+id
    cursor.execute(query)

@connection.connection_handler
def delete_answers_by_qid(cursor,qid):
    query='DELETE FROM answer WHERE question_id='+qid
    cursor.execute(query)

def add_current_time(data):
    print(data)
    data['submission_time'] = datetime.now()
    return data

@connection.connection_handler
def edit_row(cursor,table,new_row):
    query=""
    print(new_row)
    if table == "question":
        query=f"""UPDATE question SET submission_time='{new_row["submission_time"]}',view_number={new_row["view_number"]},vote_number={new_row["vote_number"]},title='{new_row["title"]}', message= '{new_row["message"].replace("'","''")}', image='{str(new_row["image"]).replace("None","")}' WHERE id={new_row["id"]}"""

    elif table == "answer":
        query=f"""UPDATE answer SET submission_time='{new_row["submission_time"]}',vote_number={new_row["vote_number"]},question_id={new_row["question_id"]},message='{new_row["message"]}',image='{str(new_row["image"]).replace("None","")}' WHERE id={new_row["id"]}"""

    cursor.execute(query)

@connection.connection_handler
def sort_questions(cursor,order_by,order_direction):
    query = f'SELECT * FROM question ORDER BY {order_by} {order_direction}'
    cursor.execute(query)
    questions = cursor.fetchall()
    return questions

def replace_values(data):
    data = dict(data)
    for column in data:
        print(column)
        print(data[column])
        print(type(data[column]))
        data[column]=data[column].replace("'","''")
    data["image"] = str(data["image"]).replace("", "")
    return data


@connection.connection_handler
def get_next_id(cursor,table):
    query = 'SELECT id FROM '+table+' ORDER BY id DESC LIMIT 1'
    cursor.execute(query)
    last_id = cursor.fetchone()
    next_id = last_id["id"]+1
    return next_id
