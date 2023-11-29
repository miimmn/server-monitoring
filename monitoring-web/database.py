# DB 연결
import pymysql


class dbConfig() :
    
    def __init__(self) -> None:
        pass


    def db_connect(self) :
        con = pymysql.connect(host='192.168.56.10', user='root', password='nb1234', db='django_project', charset='utf8')
        return con

    # SELECT - dictionary
    def read(self, qry) :
        conn = self.db_connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(qry)
        result = cursor.fetchall()
        conn.close()

        return result


    # SELECT - 리스트로 받기 
    def readForList(self, qry) :
        conn = self.db_connect()
        cursor = conn.cursor()
        cursor.execute(qry)
        result = [item[0] for item in cursor.fetchall()]
        conn.close()

        return result
    



