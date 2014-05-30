#!/usr/bin/env python


import cgi, cgitb; cgitb.enable()

# Some hosts will need to have document_root appended
# to sys.path to be able to find user modules
import sys, os
sys.path.append(os.environ['DOCUMENT_ROOT']+"/recomenTFM")

from graphbase.session import Session

sess = Session()
sess.cookie.clear() 
sess.close()
print "Status: 302 Moved"
print "Location: index.html" 
print
