_CNTRL_CHARS = map(chr, list(range(0x0, 0x1f)) + [0x7f])

def _has_cntrl_chars(val):
    for char in val:
        if char in _CNTRL_CHARS:
            return True

def determine_quoting(val):
    return '"' if _has_cntrl_chars(val) else "'"



def generate_scalar(scalar_val, upper_keywords=False):
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
    val = indent
    if last_level > 0:
        val *= last_level
        val += indent

    return [indent, 0] if last_level == 0 else [indent*last_level+indent, indent*last_level]

def generate_array(list_or_array, indent=2, last_level=0, end=';'):
    spaces, end_bracket_spaces = [' '*x for x in calculate_array_indents(indent, last_level)]
    parts = ['array (']

    indexed_array = type(list_or_array) is not dict
    arr_items = enumerate(list_or_array) if indexed_array else list_or_array.items()

    for (key, item) in arr_items:
        current_item_is_scalar = type(item) not in (tuple, list, set, dict)
        key_quote_type = determine_quoting(key) if not indexed_array else ''

        if current_item_is_scalar:
            value = generate_scalar(item)
            prefix_return = ""
        else:
            value = generate_array(item, indent=indent, end=',', last_level=last_level + 1)
            prefix_return = f"\n{spaces}"

        prefix = f"{key_quote_type}{key}{key_quote_type} => {prefix_return}"
        parts.append(f'{spaces}{prefix}{value},')

    parts.append('%s)' % (end_bracket_spaces))

    return '\n'.join(parts) + (";" if last_level == 0 else "")
