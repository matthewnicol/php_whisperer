class Positioning:
    NEXT_SIBLING, PREVIOUS_SIBLING = range(2)

def manipulate_array(array, operation, new_value):
    pass


def extract_tree(array, extraction_path):
    path = extraction_path.split(".")
    cursor = array
    for loc in path:
        if all([x in "0123456789" for x in loc]):
            cursor = cursor[int(loc)]
        else:
            cursor = cursor[loc]
    return cursor

def erase_tree(array, extraction_path):
    if isinstance(extraction_path, str):
        extraction_path = extraction_path.split(".")
    loc = extraction_path[0]
    rest = extraction_path[1:] if len(extraction_path) > 1 else None

    # Handle extract if this tree is an ordered array
    if all([x in "0123456789" for x in loc]):
        ret_arr = []
        for num, el in enumerate(array):
            if num != int(loc):
                ret_arr.append(el)
            else:
                if rest:
                    ret_arr.append(erase_tree(el, rest))
        return ret_arr

    # Handle extract if this tree is an associative array
    else:
        ret_arr = {}
        for k, v in array.items():
            if k == loc:
                if rest:
                    ret_arr[k] = erase_tree(array[k], rest)
            else:
                ret_arr[k] = v
        return ret_arr
