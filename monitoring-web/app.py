import cherrypy
import config
# from user.userController import userController
from info.infoController import infoController


class MyApp:
    def __init__(self):
        self.infoController = infoController()

    def configure(self):
        # 애플리케이션 루트 URL 경로 설정
        cherrypy.tree.mount(self.infoController, '/info', config=None)

        cherrypy.config.update(config.SERVER_CONF)


if __name__ == '__main__':
    my_app = MyApp()
    my_app.configure()

    cherrypy.quickstart(my_app, '/', config=config.CP_CONF)


