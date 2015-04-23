#!/usr/bin/python
import os
import site

site.addsitedir('/home/greggjs/.virtualenvs/flask/local/lib/python2.7/site-packages')

activate_this = os.path.expanduser('/home/greggjs/.virtualenvs/flask/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from main import app as application
