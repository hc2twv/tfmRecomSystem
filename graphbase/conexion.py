#!/usr/bin/env python

from py2neo import neo4j
from py2neo import node, rel
import time


class Conexion:
    
    graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    

    def createNodeImageFlickr(self, idf, title, url, datetaken, tags):
        #query_string = "Create (f:Image {name: 'flickr"+idf+"', idf:"+idf+", title:'"+title+"', url:'"+url+"', datetaken:'"+datetaken+"', tags:'"+tags+"'})"
        #query = neo4j.CypherQuery(self.graph_db,query_string)
        #query.execute()
        ndo, = self.graph_db.create(node({"idf":idf,"title":title,"url":url,"datetaken":datetaken,"tags":tags}))
        ndo.add_labels("Image")
        return ndo
         
    def createNodeVideoYoutube(self,title,datepublished,url):
        ndo, = self.graph_db.create(node({"title":title,"datepublished":datepublished,"url":url}))
        ndo.add_labels("Video")
        return ndo
    
    def createNodeMusicSoundCloud(self,idm, title, url,tags):
        ndo, = self.graph_db.create(node({"idm":idm,"title":title,"url":url,"tags":tags}))
        ndo.add_labels("Music")
        return ndo
    
    #Metodos de Busqueda 
    def searchNodesFlickr(self, tag):
        query = neo4j.CypherQuery(self.graph_db, "Match (f:Image) Where f.tags=~ '.*(?i)"+tag+".*' Return f ")
        return query.execute()
        
            
    def searchNodesYoutube(self, title):
        query = neo4j.CypherQuery(self.graph_db, "Match (y:Video) Where y.title=~ '.*(?i)"+title+".*' Return y ")
        return query.execute()
    
    def searchNodesSoundCloud(self, title):
        query = neo4j.CypherQuery(self.graph_db, "Match (s:Music) Where s.title=~ '.*(?i)"+title+".*' OR s.tags=~ '.*(?i)"+title+".*' Return s ")
        return query.execute()
        
    def searchNodeDuplicated(self, url, tipo):
        query = neo4j.CypherQuery(self.graph_db,"Match (f:"+tipo+") Where f.url='"+url+"' Return f")
        valor = query.execute()
        for val in valor:
            if val.values[0]['url'] == url:
                return 1
        return 0
    
    def existNodeUser(self, user):
        query = neo4j.CypherQuery(self.graph_db,"Match (u:User) Where u.user='"+user+"' Return u")
        valor = query.execute()
        for val in valor:
            if val.values[0]['user'] == user:
                return 1
        return 0
        
    def getNodeUserId(self,user):
        query = neo4j.CypherQuery(self.graph_db,"Match (u:User) Where u.user='"+user+"' Return u Limit 1")
        valor = query.execute()
        for val in valor:
            return val.values[0]._id
        return None
    
    def getUserFromNode(self,idNode):
        nodeU = self.graph_db.node(idNode)
        return nodeU.get_properties()['user']
         
    def doRelationsUserItem(self,user,idNItem):
        nodeI = self.graph_db.node(idNItem)
        idUser = self.getNodeUserId(user)
        nodeU = self.graph_db.node(idUser) 
        date = time.asctime(time.localtime(time.time())) 
        query_string = "Start n1=node("+str(idUser)+"), n2=node("+str(idNItem)+") Match (n1)-[r:LOOKED]->(n2) Return Count(*)"
        query = neo4j.CypherQuery(self.graph_db,query_string)
        num = query.execute()
        if (num._data[0].values[0]==0):        
            relacion = rel((nodeU,("LOOKED", {"date": date,"numVeces": 1}),nodeI))        
            self.graph_db.create(relacion)
        else:
            query_string = "Start n1=node("+str(idUser)+"), n2=node("+str(idNItem)+") Match (n1)-[r:LOOKED]->(n2) Set r.numVeces=r.numVeces +1 "
            query = neo4j.CypherQuery(self.graph_db,query_string)
            return query.execute()
            
    
    def getNodeUser(self,user):
        return self.graph_db.node(self.getNodeUserId(user))
    
    def getNodeItem(self,idItem):
        return self.graph_db.node(idItem)
    
    def setWordUser(self,user,word1):
        nodeU = self.getNodeUser(user)
        sch = nodeU.get_properties()
        query_string = "Match (u:User) Where u.user='"+user+"' Set u.searchWord='"+word1+"', u.searchWordAnt='"+sch['searchWord']+"' Return u"
        query = neo4j.CypherQuery(self.graph_db,query_string)
        query.execute()
    
    def getRelationshipNodeUser(self,user):
        nodeU = self.getNodeUser(user)
        sch = nodeU.get_properties()
        query_string = "Match (u:User{user:'"+user+"'})-[r:LOOKED]->(n) Where n.title=~ '.*(?i)"+sch['searchWord']+".*' or n.tags=~ '.*(?i)"+sch['searchWordAnt']+".*'  Return n"
        query = neo4j.CypherQuery(self.graph_db,query_string)
        return query.execute()
    
    def getRelationshipNodeItem(self,idItem):
        query_string = "Start n1=node("+str(idItem)+"), n2=node(*) Match (n1)<-[r:LOOKED]-(n2) Return n2 "
        query = neo4j.CypherQuery(self.graph_db,query_string)
        return query.execute()

        