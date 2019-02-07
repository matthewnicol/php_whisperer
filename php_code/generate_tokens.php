<?php
$f = fopen($pfile, 'r');
$data = fread($f, filesize($pfile));
$tokens = array();

$tmappings = array(
    "." => "PERIOD",
    "," => "COMMA",
    "(" => "OPEN_PAREN",
    ")" => "CLOSE_PAREN",
    "[" => "OPEN_SQUARE_BRACKET",
    "]" => "CLOSE_SQUARE_BRACKET",
    "=" => "EQUALS",
    "{" => "OPEN_BLOCK",
    "}" => "CLOSE_BLOCK",
    ";" => "END_STATEMENT",
);

$tstrings = array(
    "true" => "BOOL_TRUE",
    "false" => "BOOL_FALSE",
);

$tokens = token_get_all($data);
$tokens_out = array();
$skip = 0;

$classify_char_token = function($t) use ($tmappings) {
    if (in_array($t, array_keys($tmappings))) {
        return array('name' => $tmappings[$t], 'val' => $t);
    }
    else {
        return array('name' => 'UNKNOWN', 'val' => $t);
    }
};

$classify_token = function ($t) use ($bst, $tstrings, $classify_char_token) {
    if (is_array($t)) {
        $meta = array('name' => token_name($t[0]), 'val' => $t[1]);
        if ($meta['name'] == 'T_STRING') {
            $meta['builtin'] = $bst->find($meta['val']);
            if (in_array($meta['val'], array_keys($tstrings))) {
                $meta['name'] = $tstrings[$meta['val']];
            }
        }
        return $meta;
    }
    else return $classify_char_token($t);
};

$arr = array();

$pop_latest_token = function() use (&$arr, &$tokens_out) {
    if (count($arr) == 0) {
        if (count($tokens_out) > 0) {
            return array_pop($tokens_out);
        }
        else {
            return false;
        }
    }
    else {
        if (count($arr[count($arr)-1]['inner']) == 0) {
            return false;
        }
        else {
            return array_pop($arr[count($arr)-1]['inner']);
        }
    }
};

$push_latest_token = function($token) use (&$arr, &$tokens_out) {
    if (count($arr) > 0) array_push($arr[count($arr)-1]['inner'], $token);
    else array_push($tokens_out, $token);
};



for ($i = 0; $i < count($tokens); $i++) {

    if ($skip > 0) {
        $skip -= 1;
        continue;
    }

    $meta = $classify_token($tokens[$i]);

    if ($meta['name'] == 'T_ARRAY') {
        array_push($arr, array('name' => 'T_COMPOUND_ARRAY', 'inner' => array(), 'start_code' => 'array'));
        $j = $i+1;
        while (in_array($classify_token($tokens[$j])['name'], array('T_WHITESPACE', 'OPEN_PAREN'))) {
            $push_latest_token($classify_token($tokens[$j]));
            $skip +=1;
            $j +=1;
        }
        continue;
    }

    if ($meta['name'] == 'OPEN_SQUARE_BRACKET') {
        if (count($arr) > 0) {

        }
    }

    if ($meta['name'] == 'T_DOUBLE_COLON') {
        $prev_token = $pop_latest_token();
        $next_token = $classify_token($tokens[$i+1]);
        $compound = $prev_token['val'] . $meta['val'] . $next_token['val'];
        $inner = array($prev_token, $meta, $next_token);
        $topush = array('name' => 'COMPOUND_REFERENCE', 'val' => $compound, 'inner' => $inner, 'builtin' => $bst->find($compound));

        $push_latest_token($topush);
        $skip += 1;
        continue;
    }

    if ($meta['name'] == "CLOSE_PAREN") {
        if (count($arr) > 0) {
            $ar = array_pop($arr);
            $push_latest_token($ar);
            continue;
        }
    }

    $push_latest_token($meta);
}

echo json_encode($tokens_out);