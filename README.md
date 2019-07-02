# php_whisperer
*"I heard you help people with PHP problems?" "Truth is, I help PHP with people problems."*

Convert PHP arrays to Python objects using read_php

```
from php_whisperer import read_php
read_php('/tmp/a_php_file.py', variable='data')
>>> {'My Php Array': ['You', 'get', 'the', 'point']}
```

Convert Python lists and dictionaries to PHP using generate_php

```from php_whisperer import generate_php
generate_php([1, 2, 3, 4])

array(1, 2, 3, 4);
```

