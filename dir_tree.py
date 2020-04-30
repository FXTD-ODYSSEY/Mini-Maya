# coding:utf-8
from __future__ import print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-30 09:30:41'

"""

"""


import os
import json
DIR = os.path.dirname(__file__)

def path_to_dict(path):
    """
    https://stackoverflow.com/questions/25226208/represent-directory-tree-as-json
    """
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir(path)]
    else:
        d['type'] = "file"
    return d

target_dir = os.path.realpath(os.path.join('.','mini_maya'))

with open(__file__.replace('.py','.json'),'w') as f:
    json.dump(path_to_dict(target_dir),f,indent=4)


# def list_files(startpath):
#     """
#     https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
#     """
#     for root, dirs, files in os.walk(startpath):
#         level = root.replace(startpath, '').count(os.sep)
#         indent = ' ' * 4 * (level)
#         print('{}{}/'.format(indent, os.path.basename(root)))
#         subindent = ' ' * 4 * (level + 1)
#         for f in files:
#             print('{}{}'.format(subindent, f))
# list_files(DIR)