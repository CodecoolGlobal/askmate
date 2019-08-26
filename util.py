import data_handler

def dict_converter(ordereddict):
    """ Converts ordered dict into regular dict
    :rtype: anyád
    """
    dict = {}
    for key in ordereddict:
        dict[key] = ordereddict[key]
    return dict


OPTIONS = {
    "View": "view_number",
    "Vote": "vote_number",
    "Title": "title",
    "Date": "submission_time",
    "Descending": True,
    "Ascending": False,
}

def option_converter(option):
    if option == "View ":
        return "view_number"

    elif option == "Vote ":
        return "vote_number"

    elif option == "Title ":
        return "title"

    elif option == "Date ":
        return "submission_time"

    elif option == "Descending":
        return True
    elif option == "Ascending":
        return False

def isitUpdate(all_qs, id):
    for q in all_qs:
        if id == q["id"]:
            return True
    return False