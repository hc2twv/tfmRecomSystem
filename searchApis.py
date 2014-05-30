#!/usr/bin/env python
# -*- conding:utf-8 -*--

print "Content-type: text/html\n\n"

import flickr
import soundcloud
import cgi, cgitb 
import gdata.youtube
from graphbase.conexion import Conexion
import gdata.youtube.service

cgitb.enable()
# Creamos instancia de FieldStorage
form = cgi.FieldStorage()
txtsch = form.getvalue("search")
#Variable para interactuar con la bdog
con = Conexion()
print "<p><b>Nuevos Archivos Encontrados</b></p>"
print "<ol>"
#Busqueda en las APIS
#Busqueda en Flickr
photos = flickr.photos_search(tags=txtsch, tag_mode='all', per_page=5)
for photo in photos:
    op = con.searchNodeDuplicated(photo.url, "Image")
    if (op == 0) :
        try:
            tagsc = ""
            for tag in photo.tags:
                    tagsc = tagsc + tag.text +" "
            nodo = con.createNodeImageFlickr(photo.id, photo.title, photo.url, photo.datetaken, tagsc.encode('utf-8'))            
            print "<li><p>Title: "+photo.title+ "<br />"
            print "Publicado en: "+photo.datetaken + "<br />"
            print "Tags: "
            print tagsc.encode('utf-8')
            print "<br />URL: <a href=%s target='_blank' alt='%s' >%s</a>" %  (photo.url,nodo._id,photo.url)  
            print "</li>"  
        except:
            continue


#Instanciamos la API de Youtube
#Busqueda en Youtube
clienty = gdata.youtube.service.YouTubeService()
query = gdata.youtube.service.YouTubeVideoQuery()
query.vq = txtsch
query.max_results = 5
query.start_index = 1
query.racy = "exclude"
query.format = '5'
query.orderby = "relevance"
try:
    feed = clienty.YouTubeQuery(query)
    
    for entry in feed.entry:
        url = entry.GetSwfUrl()
        op = con.searchNodeDuplicated(url, "Video")
        if (op == 0) :
            nodo= con.createNodeVideoYoutube(entry.media.title.text,entry.published.text, url)
            print "<li><p>Titulo: %s" % entry.media.title.text 
            print "<br />Publicado en: %s" % entry.published.text
            #print "<br />description: %s" % entry.media.description.text
            print "<br />URL: <a href=%s target='_blank'alt='%s'>%s</a>" % (url,nodo._id,url)
            print "</p></li>"
            
except:
    print ""

#Busqueda en SoundCLoud
# create a client object with your app credentials
client = soundcloud.Client(client_id='529295acc334c5fea23d339ac03300bc')
# find all sounds of buskers licensed under 'creative commons share alike'
try:
    tracks = client.get('/tracks', q=txtsch, license='cc-by-sa')
    for track in tracks:
        var = "/tracks/"+ str(track.id)
        trackdef = client.get(var)
        op = con.searchNodeDuplicated(trackdef.permalink_url, "Music")
        if (op == 0) :
            try:
                nodo = con.createNodeMusicSoundCloud(track.id, track.title, trackdef.permalink_url,track.tag_list.encode('utf-8'))
                print "<li><p>Title:  %s <br />" % (track.title)            
                # get the tracks streaming URL
                print "URL: <a href=%s target='_blank' alt='%s'>%s</a> <br />" % (trackdef.permalink_url,nodo._id,trackdef.permalink_url)
                #print "Descripcion: %s </p>" % track.description
                print "Tags: %s" % track.tag_list
                print "</li>"
            except:
                continue
except:
    print ""
print "</ol>"