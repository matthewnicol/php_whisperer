"""
Convert python dicts and lists into PHP arrays
"""
import re

# This existed in langutil along with a lot of other crap.
# I've cut most of it out but I'm not sure if this is needed yet.
_CNTRL_CHARS = map(chr, list(range(0x0, 0x1f)) + [0x7f])


def _has_cntrl_chars(val):
    if isinstance(val, int):
        return False
    for char in val:
        if char in _CNTRL_CHARS:
            return True


def get_quote_type(val):
    """
    Should we use single quotes or double quotes?
    :param val: The value that we need to enclose in quotes
    :return: str - the type of quote we need to use
    """
    return '"' if _has_cntrl_chars(val) else "'"


def generate_scalar(scalar_val, upper_keywords=False):
    """
    Convert a non-array & non-list python value into its PHP equivelant
    :param scalar_val: value to convert
    :param upper_keywords: should we convert true and false to uppercase?
    :return: string representation of php value
    """
    mod_case = lambda x: x.upper() if upper_keywords else x.lower()

    if scalar_val is None:
        return mod_case('null')

    elif type(scalar_val) is bool:
        return mod_case('TRUE' if scalar_val else 'FALSE')

    elif type(scalar_val) is str:
        quote_type = '"' if _has_cntrl_chars(scalar_val) else '\''
        scalar_val = scalar_val.replace(quote_type, f'\\{quote_type}')
        return f"{quote_type}{scalar_val}{quote_type}"

    elif type(scalar_val) is int:
        return '%d' % scalar_val

    elif type(scalar_val) is float:
        return ('%f' % scalar_val).rstrip('0')

    raise ValueError(f'Cannot parse scalar: {scalar_val}')


def calculate_array_indents(indent=2, last_level=0):
    """
    Determine the start and end indents for a sub-array.
    :param indent: How much are we indenting on each go
    :param last_level: Recursion depth of the calling function
    :return: [int, int]
    """
    val = indent
    if last_level > 0:
        val *= last_level
        val += indent

    return [indent, 0] if last_level == 0 else [indent*last_level+indent, indent*last_level]


def generate_array(list_or_array, indent=2, last_level=0):
    """
    Given a python array (or sub-array), convert it into a PHP array.
    :type list_or_array: list|dict
    :type indent: int
    :type last_level: int
    :return: string representation of a php array
    """
    spaces, end_bracket_spaces = [' '*x for x in calculate_array_indents(indent, last_level)]
    parts = ['array (']

    indexed_array = type(list_or_array) is not dict
    arr_items = enumerate(list_or_array) if indexed_array else list_or_array.items()

    for (key, item) in arr_items:
        current_item_is_scalar = type(item) not in (tuple, list, set, dict)
        key_quote_type = get_quote_type(key) if not indexed_array else ''

        if current_item_is_scalar:
            value = generate_scalar(item)
            prefix_return = ""
        else:
            value = generate_array(item, indent=indent, last_level=last_level + 1)
            prefix_return = f"\n{spaces}"

        prefix = f"{key_quote_type}{key}{key_quote_type} => {prefix_return}"
        parts.append(f'{spaces}{prefix}{value},')

    parts.append('%s)' % (end_bracket_spaces))

    return '\n'.join(parts) + (";" if last_level == 0 else "")

def generate_php(list_or_array, *, variable=None, modern=False, return_=None):
    data = generate_array(list_or_array)
    if modern:
        data = data.replace("),\n", "],\n")
        data = data.replace(");", "];")
        data = re.sub(r'=>.*\n.*?array \(', "=> [", data, flags=re.MULTILINE)
        data = data.replace('array (', '[')

    if variable:
        return f"${variable} = " + data
    elif return_:
        return f"return " + data
    else:
        return data
