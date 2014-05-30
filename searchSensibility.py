#!/usr/bin/env python
# -*- conding:utf-8 -*--

print "Content-type: text/html\n\n"

import flickr
import soundcloud
import cgi, cgitb 
import gdata.youtube
from graphbase.conexion import Conexion
import gdata.youtube.service

# Creamos instancia de FieldStorage
form = cgi.FieldStorage()
palabra = form.getvalue("search")
#Variable para interactuar con la bdog
con = Conexion()

#Busqueda en Base
print "-"
print "<ol>"
nodos = con.searchNodesFlickr(palabra)
  
for nodo in nodos:
    print "<li><p>Title: %s" % nodo.values[0]['title'].encode('utf-8') 
    print "<br />Publicado en: %s" % nodo.values[0]['datetaken']
    print "<br />Tags: %s" % nodo.values[0]['tags'].encode('utf-8')
    print "<br />URL: <a href=%s target='_blank'>%s</a>" % (nodo.values[0]['url'],nodo.values[0]['url'])
    print "</p></li>"

#Busqueda en SoundCloud

nodos = con.searchNodesSoundCloud(palabra)
for nodo in nodos:
    print "<li><p>Title: %s" % nodo.values[0]['title'].encode('utf-8') 
    print "<br />URL: <a href=%s target='_blank'>%s</a>" % (nodo.values[0]['url'],nodo.values[0]['url'])
    print "<br />Tags: %s" % nodo.values[0]['tags'].encode('utf-8')
    print "</p></li>"

#Busqueda en Youtube
nodos = con.searchNodesYoutube(palabra)
for nodo in nodos:
    print "<li><p>Title: %s" % nodo.values[0]['title'].encode('utf-8') 
    print "<br />Publicado en: %s" % nodo.values[0]['datepublished']
    print "<br />URL: <a href=%s target='_blank'>%s</a>" % (nodo.values[0]['url'],nodo.values[0]['url'])
    print "</p></li>"

print "</ol>"