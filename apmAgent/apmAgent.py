import pymysql
import psutil
from datetime import datetime as dt
import time
import socket

con = pymysql.connect(host='192.168.56.10', user='root', password='nb1234', db='django_project', charset='utf8')

netUtil = psutil.net_io_counters()
prev_netin = netUtil.bytes_recv/1024**2
prev_netout = netUtil.bytes_sent/1024**2 
# myIp = socket.gethostbyname(socket.getfqdn()) # ip 주소

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
myIp = s.getsockname()[0]


def insert(cpu, mem, io, net) :
    cursor = con.cursor(pymysql.cursors.DictCursor)
    qry = '''
        INSERT INTO
            perform_check_cpuperform(origin_time, value, ip)
        VALUES
            ( %(origin_time)s, %(value)s, %(ip)s )
    '''
    cursor.execute(qry, cpu)
     
    qry = '''
        INSERT INTO 
            perform_check_memperform(origin_time, ram_usage, ip)
        VALUES
            ( %(origin_time)s, %(ram_usage)s, %(ip)s )
    '''
    cursor.execute(qry, mem)

    qry = '''
        INSERT INTO 
            perform_check_diskperform(origin_time, disk_read, disk_write, ip)
        VALUES
            ( %(origin_time)s, %(disk_read)s, %(disk_write)s, %(ip)s )
    '''
    cursor.execute(qry, io)

    qry = '''
        INSERT INTO 
            perform_check_networkperform(origin_time, netin, netout, ip)
        VALUES
            ( %(origin_time)s, %(netin)s, %(netout)s, %(ip)s )
    '''
    cursor.execute(qry, net)
    con.commit()
    

try:
    while True :
        memUtil = psutil.virtual_memory()
        ioUtil  = psutil.disk_io_counters()
        net = psutil.net_io_counters() 

        origin_time = dt.now().strftime('%Y-%m-%d %H:%M:%S') # 측정된 시간

        cpu = {
            "value" : psutil.cpu_percent(0.1)/100,
            "origin_time" : origin_time,
            "ip" : myIp
        }
        mem = {
            "ram_usage" : (memUtil.used)/(memUtil.total),
            "origin_time" : origin_time,
            "ip" : myIp
        }
        io = {
            "disk_read" : ioUtil.read_bytes,
            "disk_write" : ioUtil.write_bytes, 
            "origin_time" : origin_time,
            "ip" : myIp
        }

        time.sleep(2)
        netDict = {
            "netin" : round(net.bytes_recv/1024**2 - prev_netin, 1),
            "netout" : round(net.bytes_sent/1024**2 - prev_netout, 1),
            "origin_time" : origin_time,
            "ip" : myIp
        }
        
        prev_netin = round(net.bytes_recv/1024**2, 1) 
        prev_netout = round(net.bytes_sent/1024**2, 1)

        insert(cpu, mem, io, netDict)
        
        time.sleep(3)
        print("SUCCESS ... ...")
except:
    print(" \n------- DB INSERT 쿼리 처리 과정 중 오류 -------\n ")
finally:
    con.close()