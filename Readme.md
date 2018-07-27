# Project Title

Simple script to read cvs url from mysql download the cvs and import into database, then the script do the sanity check to check if the cvs has been imported 
if there is some error, the script make update with value 1 on field into mysql table called nagios and Nagios get the status Critical
if there is not error the vlue will be 0

### Prerequisites
```
import MySQLdb
import string
import subprocess
import re
import os
import sys
import datetime

```

### Installing

Download the file with git 

git@github.com:micheleberardi/feeds_cvs.py.git


## Running

python feeds_cvs.py


## Authors

* **Michele Berardi** -- [MicheleBerardi](https://github.com/micheleberardi)

* Please feel free to reach out with any questions
