#!/usr/bin/env python
# -*- conding:utf-8 -*--

print "Content-type: text/html\n\n"


import soundcloud
from graphbase.conexion import Conexion
import cgi, cgitb 
cgitb.enable()
# create a client object with your app credentials
client = soundcloud.Client(client_id='529295acc334c5fea23d339ac03300bc')

# Creamos instancia de FieldStorage
form = cgi.FieldStorage()
palsch = form.getvalue("search")
con = Conexion()
print "-"
print "<ol>"
palabras = palsch.split()
for palabra in palabras:
    nodos = con.searchNodesSoundCloud(palabra)
    for nodo in nodos:
        print "<li><p>Title: %s" % nodo.values[0]['title'].encode('utf-8') 
        print "<br />URL: <a href=%s target='_blank'>%s</a>" % (nodo.values[0]['url'],nodo.values[0]['url'])
        print "<br />Tags: %s" % nodo.values[0]['tags'].encode('utf-8')
        print "</p></li>"


# find all sounds of buskers licensed under 'creative commons share alike'
tracks = client.get('/tracks', q=palsch, license='cc-by-sa')

print "-"
for track in tracks:
    var = "/tracks/"+ str(track.id)
    trackdef = client.get(var)
    op = con.searchNodeDuplicated(trackdef.permalink_url, "Music")
    if (op == 0) :
        try:
            print "<li><p>Title:  %s <br />" % (track.title)            
            # get the tracks streaming URL
            print "URL: <a href=%s target='_blank'>%s</a> <br />" % (trackdef.permalink_url,trackdef.permalink_url)
            #print "Descripcion: %s </p>" % track.description
            print "Tags: %s" % track.tag_list
            print "</li>"
            con.createNodeMusicSoundCloud(track.id, track.title, trackdef.permalink_url,track.tag_list.encode('utf-8'))
        except:
            continue
print "</ol>"