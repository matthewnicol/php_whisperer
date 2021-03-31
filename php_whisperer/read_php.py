"""
Tools for reading PHP arrays into python objects.
"""

import os, sys
import io
from subprocess import check_output, CalledProcessError
import json
import shlex


def read_many(*php_data, variable=None, include_path=None, cwd=".", modify_command=lambda x: x):
    """
    Includes variadic list of php data, in the form of files or raw php strings, executes the php code
    then returns the value from the php compiler.

    :type php_data: str or file-like object
    :type variable: str
    :type include_path: list
    :type cwd: list
    :type modify_command: function

    """
    command = ""
    for x in php_data:
        if isinstance(x, io.TextIOBase):
            command = f"{command} \n if (file_exists('{x.name}')) @include '{x.name}';"
        else:
            command = f"{command} \n {x}"

    command = f'{command} \n if(isset(${variable})) \n\t echo json_encode(${variable}); \n else \n\t echo json_encode(array());'
           
    if include_path:
        include_path = ["-d ", ",".join(include_path)]
    else:
        include_path = []

    try:
        result = check_output(['php', *include_path, '-r', modify_command(command)])
        
    except CalledProcessError as err:
        with open('/tmp/php_whisperer_command', 'w') as wf:
            wf.write(modify_command(command))
        print(err.output)
        raise IOError(f"Error when executing PHP command. See generated php in /tmp/php_whisperer_command.")

    try:
        return json.loads(result.decode('utf-8').replace("?>", ""))
    except Exception as err:
        print(" ".join(['php', *include_path, '-r', modify_command(command)]))
        with open('/tmp/php_whisperer_command', 'w') as wf:
            wf.write(modify_command(command))
        raise IOError(f"Could not parse PHP into json: {result}. See generated php in /tmp/php_whisperer_command.")

def alter_source_and_read_php(php_filename, *, 
        variable=None, 
        modify_command=lambda x: x, 
        alter_source=lambda x: x,
        debug=False,
        ):
    with open(php_filename, 'r') as rf:
        with open('/tmp/modphp.php', 'w') as wf:
            wf.write(alter_source(rf.read()))

    return read_php('/tmp/modphp.php', variable=variable, modify_command=modify_command, debug=debug)


def read_php(php_filename, *, variable=None, cwd=None, include_path=None, modify_command=lambda x: x, debug=False):
    """
    Given a php file denoted by the filename, return the array, or an array from the file.
    :type php_filename: str
    :type variable: str
    :return: list|dict
    """
    command = modify_command(
        f'echo json_encode(include "{php_filename}");' 
        if not variable else
        f'@include "{php_filename}"; if(!isset(${variable})) echo json_encode(array()); else echo json_encode(${variable});'
    )
    if include_path:
        include_path = ["-d ", ",".join(include_path)]
    else:
        include_path = []
    if debug:
        print(command)
        print(f"Include Path: {include_path}")
    result = check_output(['php']+include_path+['-r', command], cwd=cwd)
    return json.loads(result)

def cp_php(lhs_ref, rhs_ref):
    pass

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


def read_php_stdin():
    with open("/tmp/.php_out", "w") as wf:
        for x in sys.stdin:
            wf.write(x)

    if len(sys.argv) > 2:
        variable = sys.argv[1]
    else:
        variable = None
    print(read_php("/tmp/.php_out", variable=variable, debug="--debug" in sys.argv))

