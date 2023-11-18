import json


def dict_array_as_json(dict_array):
    return json.dumps([d.as_dict() for d in dict_array], default=str)
