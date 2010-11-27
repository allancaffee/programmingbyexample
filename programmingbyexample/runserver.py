#!/usr/bin/python

import os
import sys

# Make everything relative to our parent directory
sys.path.insert(0, os.pardir)
sys.path.append(os.getcwd())

from programmingbyexample import app
app.run(debug=True)
