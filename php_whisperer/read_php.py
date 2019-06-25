"""
Tools for reading PHP arrays into python objects.
"""

import os, sys
from subprocess import check_output
import json


def read_many(*php_filenames, variable=None, modify_command=lambda x: x):
    command = modify_command(
        "\n".join(
            ["\n".join([
                f'echo json_encode(include "{x}");' 
                if not variable else
                f'@include "{x}";' for x in php_filenames]),
            f"echo json_encode(${variable});"])
    )
    result = check_output([
        'php', 
        '-r', 
        command
    ])
    return json.loads(result)

def alter_source_and_read_php(php_filename, *, 
        variable=None, 
        modify_command=lambda x: x, alter_source=lambda x: x):
    with open(php_filename, 'r') as rf:
        with open('/tmp/modphp.php', 'w') as wf:
            wf.write(alter_source(rf.read()))

    return read_php('/tmp/modphp.php', variable=variable, modify_command=modify_command)


def read_php(php_filename, *, variable=None, modify_command=lambda x: x, debug=False):
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
    if debug:
        print(command)
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

