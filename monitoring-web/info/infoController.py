import cherrypy
from info.models.infoService import infoService
import os

class infoController():

    def __init__(self) :
        self.svc = infoService()
        self.path = os.path.dirname(os.path.abspath(__file__))


    @cherrypy.expose
    def index(self) : 
        return open(self.path + '/index.html')
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getInfo(self) :
        data = self.svc.getInfoSVC()
        return data
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAllInfo(self) :
        data = self.svc.getAllInfo()
        return data