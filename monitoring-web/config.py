import cherrypy
import logging

CP_CONF = {
    '/css': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static/css',
        'tools.staticdir.root': '/opt/monitoring-web'
    },

    '/js': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static/js',
        'tools.staticdir.root': '/opt/monitoring-web'
    },

    '/assets': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static/assets',
        'tools.staticdir.root': '/opt/monitoring-web'
    },

    '/font': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static/font',
        'tools.staticdir.root': '/opt/monitoring-web'
    },

    

}

SERVER_CONF = {
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8081,
    
    'tools.sessions.on': True,
    'tools.sessions.storage_type': "File",
    'tools.sessions.storage_path': 'sessions',
    'tools.sessions.timeout': 3600
}


# URL 접근 제어용 데코레이터
def access_check(func):
    def access_check_decorator(*args, **kwargs):
        user_info = cherrypy.session.get('userEmail', '사용자 없음')
        if user_info == '사용자 없음':
            logger = getLogger()
            logger.info("   로그인 데코레이터 진입   ")
            raise cherrypy.HTTPError(403, "로그인 후 이용가능합니다.")
            # raise cherrypy.HTTPRedirect("/user/loginview")
        return func(*args, **kwargs)
    return access_check_decorator


# 로그용
def getLogger() :
    logger = logging.getLogger(name='Django_project_server_performance-WEB')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '|%(asctime)s||%(name)s||%(levelname)s|\n%(message)s',datefmt='%Y-%m-%d %H:%M:%S'
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter) 
    logger.addHandler(stream_handler)

    return logger
    