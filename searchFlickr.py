#!/usr/bin/env python
# -*- conding:utf-8 -*--

print "Content-type: text/html\n\n"

import flickr
import cgi, cgitb 
from graphbase.conexion import Conexion
cgitb.enable()

# Creamos instancia de FieldStorage
form = cgi.FieldStorage()
txtsch = form.getvalue("search")
#Variable para interactuar con la bdog
con = Conexion()

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
        print "<br />URL: <a href=%s target='_blank'>%s</a>" % (nodo.values[0]['url'],nodo.values[0]['url'])
        print "</p></li>"
        
#Busqueda en Flickr
print "-"
photos = flickr.photos_search(tags=txtsch, tag_mode='all', per_page=5)
for photo in photos:
    op = con.searchNodeDuplicated(photo.url, "Image")
    if (op == 0) :
        try:
            print "<li><p>Title: "+photo.title+ "<br />"
            print "Publicado en: "+photo.datetaken + "<br />"
            print "Tags: "
            tagsc = ""
            for tag in photo.tags:
                    tagsc = tagsc + tag.text +" "
                    print tag.text.encode('utf-8')
            print "<br />URL: <a href=%s target='_blank'>%s</a>" %  (photo.url,photo.url)  
            print "</li>"  
            con.createNodeImageFlickr(photo.id, photo.title, photo.url, photo.datetaken, tagsc.encode('utf-8'))          
        except:
            continue

print "</ol>"
