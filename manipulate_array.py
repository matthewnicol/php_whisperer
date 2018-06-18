"""
Tools for manipulating PHP arrays that have been parsed into python.
"""


def extract_tree(array, extraction_path):
    """
    Pull a tree out from a python list or dictionary. Return that tree
    :param array: A Python list or dictionary
    :param extraction_path:  "level1.level2.0.3.level5" <-- map for traversing the array
    :return: The subtree at the path
    """
    path = extraction_path.split(".")
    cursor = array
    for loc in path:
        # Handle extraction if this tree is an ordered array
        if all([x in "0123456789" for x in loc]):
            cursor = cursor[int(loc)]
        # Handle extraction if this tree is an associative array
        else:
            cursor = cursor[loc]
    return cursor


def erase_tree(array, extraction_path):
    """

    :param array: A Python list or dictionary
    :param extraction_path: "level1.level2.0.3.level5" <-- map for traversing the array
    :return: None
    """
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
