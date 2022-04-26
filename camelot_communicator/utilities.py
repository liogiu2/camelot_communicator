import json
import importlib.resources as pkg_resources
import camelot_communicator.json_data as json_data

def parse_json(jsonfile):
    with pkg_resources.open_text(json_data, jsonfile+'.json') as json_file:
        json_data_parsed = json.load(json_file)
    return json_data_parsed
    
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def get_action_list():
    """
    This method is used to get the action list from the action list file.
    """
    action_list_parsed = parse_json("Actionlist")
    action_list = []
    for action in action_list_parsed:
        action_list.append(action['name'])
    return action_list

def str2bool(v):
    """
    This method is used to convert a string to a boolean.
    """
    return str(v).lower() in ("yes", "true", "t", "1")