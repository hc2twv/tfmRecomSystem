#!/usr/bin/env python
# -*- conding:utf-8 -*--

print "Content-type: text/html\n\n"

from graphbase.conexion import Conexion
import flickr
import cgi, cgitb
import gdata.youtube
import numpy as np
import random
import gdata.youtube.service
cgitb.enable()
form = cgi.FieldStorage()
#Algoritmo basado en Filtrado Colaborativo
con = Conexion()
#Match (u:User{user : "silkend"})-[r]->(n) Where n.title=~ '.*(?i)celu.*' or n.tags=~ '.*(?i)celula.*'  return r
us = form.getvalue("user")

nodesItems = con.getRelationshipNodeUser(us)
if (nodesItems.__len__() > 0):
    Items = []
    ItemsUser = []
    for nodeI in nodesItems:
        ItemsUser.append(nodeI.values[0]._id)
        Items.append(nodeI.values[0]._id)
    
    
    Users = []
    for item in Items:
        nodesUsersofItem = con.getRelationshipNodeItem(item)
        for nodeU in nodesUsersofItem:                    
            Users.append(nodeU.values[0].get_properties()['user'])
    
    
    #print Users
    Users = list(set(Users))
    
    
    for user in Users:
        #print user
        nodesItems = con.getRelationshipNodeUser(user)
        for nodeI in nodesItems:
            Items.append(nodeI.values[0]._id)
        
    Items = list(set(Items))
    
    #print Users
    #print Items
    
    valores = np.zeros((Items.__len__(),Users.__len__()))
    
    i = 0
    for user in Users:
        nodesItems = con.getRelationshipNodeUser(user)
        for nodeI in nodesItems:
            if (Items.__contains__(nodeI.values[0]._id)):
                idx = Items.index(nodeI.values[0]._id, )
                valores[idx][i] = 1
        i= i+1
        
    cosenos = np.zeros((ItemsUser.__len__(),Items.__len__())) 
    #print cosenos   
    val = Items.__len__() - 1
    for i in range(ItemsUser.__len__()):
        for j in range(Items.__len__()):
            cosenos[i][j] = (valores[i].dot(valores[j]))/(np.linalg.norm(valores[i]) * np.linalg.norm(valores[j]))
    
    fila = random.randrange(ItemsUser.__len__())
    ItemsRecom = []
    for i in range(cosenos[fila].__len__()):
        if (cosenos[fila][i] > 0):
            ItemsRecom.append(Items[i])
    
    #print ItemsRecom
    #print ItemsUser
    ItemsRecomFinales = set(ItemsRecom) - set(ItemsUser)
    
    #print ItemsRecomFinales
    for recom in ItemsRecomFinales:
        nodoI = con.getNodeItem(recom)
        dataN = nodoI.get_properties()
        print "<li><p>Title: "+dataN['title'].encode('utf-8')+ "<br />"
        print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (dataN['url'],nodoI._id,dataN['url'])  
        print "</li>" 
    print ""
    if (len(ItemsRecomFinales) == 0):
        userB = con.getNodeUser(us)
        nodeF = con.searchNodesFlickr(userB.get_properties()['searchWord'])
        for n in nodeF:
            if not (ItemsUser.__contains__(n.values[0]._id)):
                print "<li><p>Title: "+n.values[0]['title'].encode('utf-8')+ "<br />"
                print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (n.values[0]['url'],n.values[0]._id,n.values[0]['url'])  
                print "</li>"
        nodeF = con.searchNodesFlickr(userB.get_properties()['searchWordAnt'])
        for n in nodeF:
            if not (ItemsUser.__contains__(n.values[0]._id)):
                print "<li><p>Title: "+n.values[0]['title'].encode('utf-8')+ "<br />"
                print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (n.values[0]['url'],n.values[0]._id,n.values[0]['url'])  
                print "</li>"
        nodeF = con.searchNodesYoutube(userB.get_properties()['searchWord'])
        for n in nodeF:
            if not (ItemsUser.__contains__(n.values[0]._id)):
                print "<li><p>Title: "+n.values[0]['title'].encode('utf-8')+ "<br />"
                print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (n.values[0]['url'],n.values[0]._id,n.values[0]['url'])  
                print "</li>"
        nodeF = con.searchNodesYoutube(userB.get_properties()['searchWordAnt'])
        for n in nodeF:
            if not (ItemsUser.__contains__(n.values[0]._id)):
                print "<li><p>Title: "+n.values[0]['title'].encode('utf-8')+ "<br />"
                print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (n.values[0]['url'],n.values[0]._id,n.values[0]['url'])  
                print "</li>"
        nodeF = con.searchNodesSoundCloud(userB.get_properties()['searchWord'])
        for n in nodeF:
            if not (ItemsUser.__contains__(n.values[0]._id)):
                print "<li><p>Title: "+n.values[0]['title'].encode('utf-8')+ "<br />"
                print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (n.values[0]['url'],n.values[0]._id,n.values[0]['url'])  
                print "</li>"
        nodeF = con.searchNodesSoundCloud(userB.get_properties()['searchWordAnt'])
        for n in nodeF:
            if not (ItemsUser.__contains__(n.values[0]._id)):
                print "<li><p>Title: "+n.values[0]['title'].encode('utf-8')+ "<br />"
                print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (n.values[0]['url'],n.values[0]._id,n.values[0]['url'])  
                print "</li>"
else:
    userB = con.getNodeUser(us)
    nodeF = con.searchNodesFlickr(userB.get_properties()['searchWord'])
    for n in nodeF:
        print "<li><p>Title: "+n.values[0]['title'].encode('utf-8')+ "<br />"
        print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (n.values[0]['url'],n.values[0]._id,n.values[0]['url'])  
        print "</li>"
    nodeF = con.searchNodesFlickr(userB.get_properties()['searchWordAnt'])
    for n in nodeF:
        print "<li><p>Title: "+n.values[0]['title'].encode('utf-8')+ "<br />"
        print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (n.values[0]['url'],n.values[0]._id,n.values[0]['url'])  
        print "</li>"
    nodeF = con.searchNodesYoutube(userB.get_properties()['searchWord'])
    for n in nodeF:
        print "<li><p>Title: "+n.values[0]['title'].encode('utf-8')+ "<br />"
        print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (n.values[0]['url'],n.values[0]._id,n.values[0]['url'])  
        print "</li>"
    nodeF = con.searchNodesYoutube(userB.get_properties()['searchWordAnt'])
    for n in nodeF:
        print "<li><p>Title: "+n.values[0]['title'].encode('utf-8')+ "<br />"
        print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (n.values[0]['url'],n.values[0]._id,n.values[0]['url'])  
        print "</li>"
    nodeF = con.searchNodesSoundCloud(userB.get_properties()['searchWord'])
    for n in nodeF:
        print "<li><p>Title: "+n.values[0]['title'].encode('utf-8')+ "<br />"
        print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (n.values[0]['url'],n.values[0]._id,n.values[0]['url'])  
        print "</li>"
    nodeF = con.searchNodesSoundCloud(userB.get_properties()['searchWordAnt'])
    for n in nodeF:
        print "<li><p>Title: "+n.values[0]['title'].encode('utf-8')+ "<br />"
        print "URL: <a href=%s target='_blank' alt='%s' onclick='javascript:doRelation(this)' >%s</a>" %  (n.values[0]['url'],n.values[0]._id,n.values[0]['url'])  
        print "</li>"