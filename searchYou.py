#!/usr/bin/env python
# -*- conding:utf-8 -*--

print "Content-type: text/html\n\n"

import cgi, cgitb 
from graphbase.conexion import Conexion
import gdata.youtube
import gdata.youtube.service

cgitb.enable()
#Instanciamos la API de Youtube
client = gdata.youtube.service.YouTubeService()
query = gdata.youtube.service.YouTubeVideoQuery()

# Creamos instancia de FieldStorage
form = cgi.FieldStorage()

con = Conexion()    
# Obtenemos la palabra de busqueda
query.vq = form.getvalue("search")
query.max_results = 5
query.start_index = 1
query.racy = "exclude"
query.format = '5'
query.orderby = "relevance"

feed = client.YouTubeQuery(query)

#Variable para enumerar los archivos
print "-"
print "<ol>"
palabras = query.vq.split()
for palabra in palabras:
    nodos = con.searchNodesYoutube(palabra)
    for nodo in nodos:
        print "<li><p>Title: %s" % nodo.values[0]['title'].encode('utf-8') 
        print "<br />Publicado en: %s" % nodo.values[0]['datepublished']
        print "<br />URL: <a href=%s target='_blank'>%s</a>" % (nodo.values[0]['url'],nodo.values[0]['url'])
        print "</p></li>"

print "<br />-"
for entry in feed.entry:
    url = entry.GetSwfUrl()
    op = con.searchNodeDuplicated(url, "Video")
    if (op == 0) :
        print "<li><p>Titulo: %s" % entry.media.title.text 
        print "<br />Publicado en: %s" % entry.published.text
        #print "<br />description: %s" % entry.media.description.text
        print "<br />URL: <a href=%s target='_blank'>%s</a>" % (url,url)
        print "</p></li>"
        con.createNodeVideoYoutube(entry.media.title.text,entry.published.text, url)

print "</ol>"