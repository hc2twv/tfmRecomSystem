#! /usr/bin/env python
# -*- conding:utf-8 -*--

from graphbase.conexion import Conexion
import numpy as np
import random
# Copyright 2006 Bryan O'Sullivan <bos@serpentine.com>.
#
# This software may be used and distributed according to the terms
# of the GNU General Public License, version 2 or later, which is
# incorporated herein by reference.

con = Conexion()
#Match (u:User{user : "silkend"})-[r]->(n) Where n.title=~ '.*(?i)celu.*' or n.tags=~ '.*(?i)celula.*'  return r

nodesItems = con.getRelationshipNodeUser('silkend')
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
    print "<li><p>Title: "+dataN['title']+ "<br />"
    print "<br />URL: <a href=%s target='_blank' alt='%s' >%s</a>" %  (dataN['url'],nodoI._id,dataN['url'])  
    print "</li>" 
            


