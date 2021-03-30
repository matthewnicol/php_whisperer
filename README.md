# php_whisperer
*"I heard you help people with PHP problems?" "Truth is, I help PHP with people problems."*

## Read PHP
Convert PHP arrays to Python objects using read_php

```
from php_whisperer import read_php
read_php('/tmp/a_php_file.php', variable='data')
```
Result:
```
{'My Php Array': ['You', 'get', 'the', 'point']}
```
Read many php files:
```
from php_whisperer import read_many

file1 = open('/tmp/php_file.php')
file2 = open('/tmp/php_file2.php')
file3 = open('/tmp/php_file3.php')
read_many(file1, file2, "$x = File1::doSomethingWith($something_from_file2)", file3, variable='x')
```
Result:
```
{'My Php Array': ['You', 'get', 'the', 'point']}
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
