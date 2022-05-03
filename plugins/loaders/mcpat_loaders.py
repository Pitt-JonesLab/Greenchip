__author__ = 'nbp3'

import ast
import xml.etree.ElementTree
import os.path


def mcpat_dict_loader(file_path):
    item = {}
    if not os.path.isfile(file_path):
        return None
    with open(file_path, 'r') as f:
        string_dict = f.read()
        item = ast.literal_eval(string_dict[8:])
    return item


def mcpat_cfg_loader(file_path):
    return xml.etree.ElementTree.parse(file_path).getroot()