"""
Tools for reading PHP arrays into python objects.
"""

import os, sys
from subprocess import check_output
import json


def read_php(php_filename, *, variable=None, modify_command=lambda x: x):
    """
    Given a php file denoted by the filename, return the array, or an array from the file.
    :type php_filename: str
    :type variable: str
    :return: list|dict
    """
    command = modify_command(
        f'echo json_encode(include "{php_filename}");' 
        if not variable else
        f'@include "{php_filename}"; echo json_encode(${variable});'
    )
    result = check_output([
        'php', 
        '-r', 
        command
    ])
    return json.loads(result)

def combine_and_read(filenames, *, variable):
    """
    Given a list of php filenames, include them in the document and then capture the variable output.
    :type filenames: list
    :type variable: str
    :return: list|dict
    """
    initial_definition = '';
    result = check_output(['php', '-r', f'{initial_definition} ' + " ".join([
        '@include "{fn}";' for fn in filenames]) + ' echo json_encode(${variable});'])

