![PHP Whisperer](https://github.com/matthewnicol/php_whisperer/blob/master/php_whisperer.jpg?raw=true)

# php_whisperer

*"I heard you help people with PHP problems?" "Truth is, I help PHP with people problems."*

## Read PHP
Convert PHP arrays to Python objects using read_php

PHP File:
```
<?php
# /tmp/a_php_file.php
$data = [
    "My Php Array" => [
        "You",
        "get",
        "the",
        "point"
    ]
];
```
Python Code:
```
from php_whisperer import read_php
read_php('/tmp/a_php_file.php', variable='data')
```
Result:
```
{'My Php Array': ['You', 'get', 'the', 'point']}
```
### Execute Arbitrary PHP
```
from php_whisperer import execute_php

php_code = """<?php

$v = explode(" ", "You get the point");
"""
data = execute_php(php_code, variable="v")
print(data)
```
Result:
```
['You', 'get', 'the', 'point']
```
## Write PHP
Convert Python lists and dictionaries to PHP using generate_php

```
from php_whisperer import generate_php
generate_php([1, 2, 3, 4])
```
Result:
```
array(1, 2, 3, 4);
```
Modern syntax also available:
```
from php_whisperer import generate_php
generate_php([1, 2, 3, 4], modern=True)
```
Result:
```
[1, 2, 3, 4];
```
