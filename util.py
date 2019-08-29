from datetime import datetime

OPTIONS = {
    "View": "view_number",
    "Vote": "vote_number",
    "Title": "title",
    "Date": "submission_time",
    "Descending": "DESC",
    "Ascending": "ASC",
}


def replace_values(data):
    data = dict(data)
    for column in data:
        print(column)
        print(data[column])
        print(type(data[column]))
        data[column] = data[column].replace("'", "''")
    if "image" in data:
        data["image"] = str(data["image"]).replace("", "")
    return data


def add_current_time(data):
    print(data)
    data['submission_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return data
