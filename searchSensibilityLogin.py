#!/usr/bin/env python
# -*- conding:utf-8 -*--

print "Content-type: text/html\n\n"

import flickr
import soundcloud
import cgi, cgitb 
cgitb.enable()
import gdata.youtube
from graphbase.conexion import Conexion
import gdata.youtube.service
import sys, os
sys.path.append(os.environ['DOCUMENT_ROOT']+"/recomenTFM")
import Cookie, os, shelve
# Creamos instancia de FieldStorage
form = cgi.FieldStorage()
txtsch = form.getvalue("search")
#Variable para interactuar con la bdog
con = Conexion()

def getCookieUser():
    string_cookie = os.environ.get('HTTP_COOKIE', '')
    cookie = Cookie.SimpleCookie()
    cookie.load(string_cookie)
    sid = cookie['sid'].value;
    session_dir = os.environ['DOCUMENT_ROOT'] + '/recomenTFM/session'
    data = shelve.open(session_dir + '/sess_' + sid, writeback=True)
    return data['cookie']['usuario'] 


con.setWordUser(getCookieUser(), txtsch)

#Busqueda en Base
print "-"
print "<ol>"
palabras = txtsch.split()
for palabra in palabras:
    nodos = con.searchNodesFlickr(palabra)
    for nodo in nodos:
        print "<li><p>Title: %s" % nodo.values[0]['title'].encode('utf-8') 
        print "<br />Publicado en: %s" % nodo.values[0]['datetaken']
        print "<br />Tags: %s" % nodo.values[0]['tags'].encode('utf-8')
        print "<br />URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" % (nodo.values[0]['url'],nodo.values[0]._id,nodo.values[0]['url'])
        print "</p></li>"

#Busqueda en SoundCloud
for palabra in palabras:
    nodos = con.searchNodesSoundCloud(palabra)
    for nodo in nodos:
        print "<li><p>Title: %s" % nodo.values[0]['title'].encode('utf-8') 
        print "<br />URL: <a href=%s target='_blank'alt='%s'onclick='javascript:doRelation(this)' >%s</a>" % (nodo.values[0]['url'],nodo.values[0]._id,nodo.values[0]['url'])
        print "<br />Tags: %s" % nodo.values[0]['tags'].encode('utf-8')
        print "</p></li>"

#Busqueda en Youtube
for palabra in palabras:
    nodos = con.searchNodesYoutube(palabra)
    for nodo in nodos:
        print "<li><p>Title: %s" % nodo.values[0]['title'].encode('utf-8') 
        print "<br />Publicado en: %s" % nodo.values[0]['datepublished']
        print "<br />URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" % (nodo.values[0]['url'],nodo.values[0]._id,nodo.values[0]['url'])
        print "</p></li>"

print "</ol>"