import pymysql
import telegram
import asyncio
import time

token = "6436327478:AAH9Tsu_o2xGMI7NlZ8uF6lAmdrsYu3ZPRs"
bot = telegram.Bot(token)


####################### 텔레그램 API -- 알림 메시지 발송 ##########################


# 경고 알람
async def warningAlarm(cpuInfo):

    text = f'''
            [경고 알림] 
    IP : {cpuInfo['ip']}  CPU 사용률 : {cpuInfo['value']*100}%
    cpu가 80% 이상 사용되고 있습니다.
    '''
    await bot.send_message(chat_id="6929976577", text=text)

# 심각 알람
async def seriousAlarm(cpuInfo):

    text = f'''
            [심각 알림]
    IP : {cpuInfo['ip']}  CPU 사용률 : {cpuInfo['value']*100}%
    cpu가 지속적으로 과부하되고 있습니다.
    '''
    await bot.send_message(chat_id="6929976577", text=text)



############################# DB 조회 & cpu 사용률 확인 #############################

con = pymysql.connect(host='192.168.56.10', user='root', password='nb1234', db='django_project', charset='utf8')

# ip목록 받기
qry = "SELECT ip FROM monitoring_ip"

# tuple형
cursor = con.cursor()
cursor.execute(qry)
ipList = [item[0] for item in cursor.fetchall()]

# dict형
cursor = con.cursor(pymysql.cursors.DictCursor)
cnt = {}

# ip별 경고 count 초기화
for ip in ipList :
    cnt[ip] = 0
print(ipList)

try:
    while True : 
        for ip in ipList :
            qry = f'''
                SELECT
                    id, value, ip, origin_time  
                FROM
                    perform_check_cpuperform cpu 
                WHERE 
                    cpu.id = 
                        (
                            SELECT MAX(id) 
                            FROM perform_check_cpuperform cpu 
                            WHERE cpu.ip = '{ip}')
                        '''
            cursor.execute(qry)
            cpu = cursor.fetchone()
            con.commit()
            
            print(
            f''' 
                ip :: {ip}\n 
                value :: {cpu['value']}\n 
                시간 ::  {cpu['origin_time']}
                --------------------------------------
            ''')

            if cpu['value'] >= 0.8 :
                cnt[ip] += 1
                loop = asyncio.get_event_loop()

                if cnt[ip] == 3 :
                    print( f"           >>>---- 심각 알림 메시지 발송 ---- ip : {ip}")
                    loop.run_until_complete(seriousAlarm(cpu))
                    cnt[ip] = 0      
                else :
                    print( f"           >>>---- 경고 알림 메시지 발송 ---- ip : {ip}")
                    loop.run_until_complete(warningAlarm(cpu))
            else :
                cnt[ip] = 0 # 연속으로 80% 이상이어야 [심각] 메시지 발송

        # time.sleep(60) # 1분에 한 번 씩 확인
        time.sleep(5) # 테스트용 5초씩 확인

except:
    print(" alarm.py :: 메시지 발송 처리 에러 ")

finally:
    con.close()








        






