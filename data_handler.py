import connection
from util import replace_values, add_current_time

SEARCH_OPTIONS = ["Date", "Vote", "View", "Title"]
ORDER_OPTIONS = ["Ascending", "Descending"]


@connection.connection_handler
def get_all_data(cursor, table):
    query = 'SELECT * FROM ' + table
    cursor.execute(query)
    data = cursor.fetchall()
    return data


@connection.connection_handler
def get_data_by_id(cursor, id, table):
    query = 'SELECT * FROM ' + table + ' WHERE id =' + id
    cursor.execute(query)
    data = cursor.fetchall()
    return data


@connection.connection_handler
def get_answers_by_qid(cursor, question_id):
    query = f'SELECT * FROM answer WHERE question_id={question_id} ORDER BY submission_time DESC'

    cursor.execute(query)
    data = cursor.fetchall()
    return data


@connection.connection_handler
def add_new_row_to_table(cursor, data, table):
    data = dict(data)
    data = replace_values(data)
    data = add_current_time(data)

    data["submission_time"] = f"""'{data["submission_time"]}'"""
    data["message"] = f"""'{data["message"]}'"""

    if table == "question" or table == "answer":
        data["image"] = f"""'{data["image"]}'"""
        if table == "question":
            data["title"] = f"""'{data["title"]}'"""

    columns = [column for column in data]
    values = [data[column] for column in columns]
    query = 'INSERT INTO ' + table + ' (' + ','.join(columns) + ')' + ' VALUES ' + '(' + ','.join(values) + ')'
    cursor.execute(query)


@connection.connection_handler
def delete_data_by_id(cursor, id, table):
    query = 'DELETE FROM ' + table + ' WHERE id=' + id
    cursor.execute(query)


@connection.connection_handler
def delete_answers_by_qid(cursor, qid):
    query = 'DELETE FROM answer WHERE question_id=' + qid
    cursor.execute(query)


@connection.connection_handler
def edit_row(cursor, table, new_row):
    query = ""
    if table == "question":
        query = f"""UPDATE question SET submission_time='{new_row["submission_time"]}',view_number={new_row[
            "view_number"]},vote_number={new_row["vote_number"]},title='{new_row["title"]}', message= '{new_row[
            "message"].replace("'", "''")}', image='{str(new_row["image"]).replace("None", "")}' WHERE id={new_row[
            "id"]}"""

    elif table == "answer":
        query = f"""UPDATE answer SET submission_time='{new_row["submission_time"]}',vote_number={new_row[
            "vote_number"]},question_id={new_row["question_id"]},message='{new_row["message"]}',image='{str(
            new_row["image"]).replace("None", "")}' WHERE id={new_row["id"]}"""
    elif table == "comment":
        query = f"""UPDATE comment SET question_id={new_row["question_id"]},answer_id={new_row["answer_id"]},message='{
        new_row["message"]}',submission_time='{new_row["submission_time"]}',edited_count={new_row[
            "edited_count"]} WHERE id={new_row["id"]}"""

    cursor.execute(query)


@connection.connection_handler
def sort_questions(cursor, order_by, order_direction):
    query = f'SELECT * FROM question ORDER BY {order_by} {order_direction}'
    cursor.execute(query)
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_next_id(cursor, table):
    query = 'SELECT id FROM ' + table + ' ORDER BY id DESC LIMIT 1'
    cursor.execute(query)
    last_id = cursor.fetchone()
    next_id = last_id["id"] + 1
    return next_id


@connection.connection_handler
def search(cursor, search_phrase):
    query = f"""SELECT id FROM question WHERE message LIKE '%{search_phrase}%' OR title LIKE '%{search_phrase}%' UNION SELECT question_id FROM answer WHERE message LIKE '%{search_phrase}%'"""
    cursor.execute(query)
    ids = cursor.fetchall()
    ids_list = [f'id={id["id"]}' for id in ids]

    query = f"""SELECT * FROM question WHERE {' OR '.join((ids_list))}"""
    cursor.execute(query)
    results = cursor.fetchall()
    return results


@connection.connection_handler
def get_latest_five_questions(cursor):
    query = f'SELECT * FROM question ORDER BY submission_time DESC LIMIT 5'
    cursor.execute(query)
    data = cursor.fetchall()
    return data


@connection.connection_handler
def get_comments_by_question(cursor, question):
    answer_ids = [answer['id'] for answer in get_answers_by_qid(question['id'])]
    answer_ids_list = [f'answer_id={answer_id}' for answer_id in answer_ids]
    columns = """id, question_id, answer_id, message, submission_time, CASE WHEN edited_count IS NULL THEN 0 ELSE edited_count END"""
    query = f"""SELECT {columns} FROM comment WHERE question_id = {question["id"]}"""
    if answer_ids:
        query += f" OR {' OR '.join((answer_ids_list))} ORDER BY submission_time DESC"
    cursor.execute(query)
    data = cursor.fetchall()
    return data


@connection.connection_handler
def add_new_user(cursor,username,password,registration_date):
    cursor.execute(
        """INSERT INTO "user" (username,password,registration_date)
        VALUES (%(username)s,%(password)s,%(registration_date)s);""",{'username':username,'password':password,'registration_date':registration_date})

@connection.connection_handler
def get_data_by_username(cursor, username):
    cursor.execute("""SELECT * FROM "user" WHERE username = %(username)s;""",{"username":username})
    data = cursor.fetchall()
    return data