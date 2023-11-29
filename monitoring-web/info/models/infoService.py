from info.models.infoDAO import infoDAO

class infoService():

    def __init__(self) :
        self.dao = infoDAO()

    
    # 그래프 업데이트용 (5초에 한 번 씩 가져오는 거)
    def getInfoSVC(self) :
        
        ipList = self.dao.getIpList()
        result = {}

        # ip별로 그래프 데이터 담기
        for ip in ipList :
            data = self.dao.getInfoDAO(ip)
            result[ip] = self.classify(data)

        return result


    # 초기 그래프 세팅용 (10분 분량 데이터)
    def getAllInfo(self) :

        ipList = self.dao.getIpList()
        result = {}

        for ip in ipList : 
            data = self.dao.getAllInfo(ip)
            result[ip] = self.classify(data)

        return result
    

    # cpu, mem, disk, net으로 분류하기
    def classify(self, dataByIp) :
        
        classifyData = {}
        classifyData['cpuData'] = []
        classifyData['memData'] = []
        classifyData['diskData'] = []
        classifyData['netData'] = []

        
        for data in dataByIp :
            cpuTmp, memTmp, diskTmp, netTmp = {}, {}, {}, {}

            cpuTmp['origin_time'] = memTmp['origin_time'] = diskTmp['origin_time'] = netTmp['origin_time'] = data['origin_time']
            
            cpuTmp['value'] = data['cpuval']

            memTmp['ram_usage'] = data['ram']

            diskTmp['disk_read'] = data['disk_read']
            diskTmp['disk_write'] = data['disk_write']

            netTmp['netin'] = data['netin']
            netTmp['netout'] = data['netout']

            classifyData['cpuData'].append(cpuTmp)
            classifyData['memData'].append(memTmp)
            classifyData['diskData'].append(diskTmp)
            classifyData['netData'].append(netTmp)

        return classifyData