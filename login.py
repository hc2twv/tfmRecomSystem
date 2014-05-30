#!/usr/bin/env python

import cgi, cgitb; cgitb.enable()

# Some hosts will need to have document_root appended
# to sys.path to be able to find user modules
import sys, os
sys.path.append(os.environ['DOCUMENT_ROOT']+"/recomenTFM")

import time
from graphbase.session import Session
from graphbase.conexion import Conexion

con = Conexion()
# Creamos instancia de FieldStorage
form = cgi.FieldStorage()
user = form.getvalue("user")
if user!= None:
    if (con.existNodeUser(user) == 1):
        sess = Session(expires=30*24*60*60, cookie_path='/', usuario=user)
               
        # Session data is a dictionary like object
        lastvisit = sess.data.get('lastvisit')
        if lastvisit:
            message = 'Welcome back. Your last visit was at ' + \
              time.asctime(time.gmtime(float(lastvisit)))
        else:
            message = 'New session'
        
        # Save the current time in the session
        sess.data['lastvisit'] = repr(time.time())
        #print """\%s       
        #Content-Type: text/plain\n
        #sess.cookie = %s
        #sess.data = %s
        #%s
        #""" % (sess.cookie, sess.cookie, sess.data, message)
        #sess.close()
        print "Status: 302 Moved"
        print "Location: indexlogin.html?user="+user 
        print
    else:
        # -*- conding:utf-8 -*--
        print "Content-type: text/html\n\n" 
        print "EL Usuario: %s <b>NO</b> Existe en la Base de Datos, Consultar al Administrador... =P<br />" % user
        print "<a href='index.html'style='color:blue'>Atr&aacute;s</a>"
else:
    # -*- conding:utf-8 -*--
    print "Content-type: text/html\n\n" 
    print "EL Usuario: %s <b>NO</b> Existe en la Base de Datos, Consultar al Administrador... =P<br />" % user
    print "<a href='index.html'style='color:blue'>Atr&aacute;s</a>"