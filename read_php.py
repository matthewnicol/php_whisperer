"""
Tools for reading PHP arrays into python objects.
"""


from subprocess import check_output
import json


def read_php(php_filename, *, variable=None):
    """
    Given a php file denoted by the filename, return the array, or an array from the file.
    :type php_filename: str
    :type variable: str
    :return: list|dict
    """
    if not variable:
        result = check_output(['php', '-r', f'echo json_encode(include "{php_filename}");'])
    else:
        result = check_output(['php', '-r', f'include "{php_filename}"; echo json_encode(${variable});'])
    return json.loads(result)