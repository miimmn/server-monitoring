from database import dbConfig as db


class infoDAO():

    def __init__(self) :
        self.db = db()

    #  가장 최근 값만 가져오기 (업데이트용)
    def getInfoDAO(self, ip) :

        qry = f'''
			SELECT 
				DATE_FORMAT(cpu.origin_time, '%Y-%m-%d %H:%i:%S') as origin_time, cpu.value cpuval, 
				mem.ram_usage ram,  
				disk.disk_read disk_read, disk.disk_write disk_write, 
				net.netin netin, net.netout netout
			FROM    
				perform_check_cpuperform cpu
			JOIN
				perform_check_memperform mem
			ON 
				cpu.ip = mem.ip 
				AND cpu.origin_time = mem.origin_time
			JOIN
				perform_check_diskperform disk
			ON
				cpu.ip = disk.ip
				AND cpu.origin_time = disk.origin_time
			JOIN
				perform_check_networkperform net
			ON
				cpu.ip = net.ip
				AND cpu.origin_time = net.origin_time
			WHERE 
				cpu.origin_time = 
					(
						SELECT MAX(cpu.origin_time)
						FROM 
							perform_check_cpuperform cpu
						WHERE
							cpu.ip = '{ip}'	
					)
				AND cpu.ip = '{ip}'
        '''
        return self.db.read(qry)
    

    # 전체 기록 가져오기 (그래프 초기 데이터 세팅) - 최대 10분 분량
    def getAllInfo(self, ip) :

        qry = f'''
            SELECT 
                DATE_FORMAT(cpu.origin_time, '%Y-%m-%d %H:%i:%S') as origin_time, cpu.value cpuval, 
                mem.ram_usage ram,  
				disk.disk_read disk_read, disk.disk_write disk_write, 
				net.netin netin, net.netout netout
            FROM    
				perform_check_cpuperform cpu
			JOIN
				perform_check_memperform mem
			ON 
				cpu.ip = mem.ip 
				AND cpu.origin_time = mem.origin_time
			JOIN
				perform_check_diskperform disk
			ON
				cpu.ip = disk.ip
				AND cpu.origin_time = disk.origin_time
			JOIN
				perform_check_networkperform net
			ON
				cpu.ip = net.ip
				AND cpu.origin_time = net.origin_time
			WHERE 
				cpu.ip = '{ip}'
			LIMIT 120; 
        '''
		
        return self.db.read(qry)
    
	# ip 목록 가져오기
    def getIpList(self) : 
        qry = 'SELECT ip FROM monitoring_ip'
        return self.db.readForList(qry)
		
	