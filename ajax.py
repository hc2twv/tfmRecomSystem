#!/usr/bin/env python
# -*- conding:utf-8 -*--

print "Content-type: text/html\n\n"
import cgi, cgitb; cgitb.enable()

# Some hosts will need to have document_root appended
# to sys.path to be able to find user modules
import sys, os
sys.path.append(os.environ['DOCUMENT_ROOT']+"/recomenTFM")
from graphbase.conexion import Conexion
import Cookie, os, shelve
# Creamos instancia de Variables
form = cgi.FieldStorage()
con = Conexion()

def getCookieUser():
    string_cookie = os.environ.get('HTTP_COOKIE', '')
    cookie = Cookie.SimpleCookie()
    cookie.load(string_cookie)
    sid = cookie['sid'].value;
    session_dir = os.environ['DOCUMENT_ROOT'] + '/recomenTFM/session'
    data = shelve.open(session_dir + '/sess_' + sid, writeback=True)
    return data['cookie']['usuario'] 

method = form.getvalue("method")

if (method == "relUserItem"):
    idNodoItem = form.getvalue("id")
    con.doRelationsUserItem(getCookieUser(),idNodoItem)

                
        
        
#print con.getNodeUser(getCookieUser())
    
    
    
