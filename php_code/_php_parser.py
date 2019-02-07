import json
from subprocess import check_output
import os



def parse_php_file(fn):
    includes = ['php_objects.php', 'bst.php', 'generate_tokens.php']
    include_str = "; ".join([f"include \'{os.path.dirname(os.path.realpath(__file__))}/{fn}\'" for fn in includes])
    tokens = check_output(['php', '-r', f'$pfile = \'{fn}\'; {include_str};']).decode('utf-8')
    tokens = json.loads(tokens)
    return tokens



if __name__ == '__main__':
    import pprint
    print(pprint.PrettyPrinter(indent=4).pprint(parse_php_file('tests/test_load_complex_array.php')))