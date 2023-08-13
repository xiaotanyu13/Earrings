import time,copy
import random
import math


import zlib


UsingFuctionDict = {
                    101:{'X':(1780,1780+28),'Y':(758,758+28),'URL':'https://kuajing.pinduoduo.com/main/order-manager/shipping-desk'},#查询商品详情
                    102:{'X':(920,1280),'Y':(580,720),'URL':'https://mms.pinduoduo.com/sycm/goods_effect/detail'},#查询买家数
                    103:{'X':(780,880),'Y':(390,450),'URL':'https://mms.pinduoduo.com/goods/goods_list'},#下架商品
                    }

n = [0,1996959894,-301047508,-1727442502,124634137,1886057615,-379345611,-1637575261,249268274,2044508324,-522852066,-1747789432,162941995,2125561021,-407360249,-1866523247,498536548,1789927666,-205950648,-2067906082,450548861,1843258603,-187386543,-2083289657,325883990,1684777152,-43845254,-1973040660,335633487,1661365465,-99664541,-1928851979,997073096,1281953886,-715111964,-1570279054,1006888145,1258607687,-770865667,-1526024853,901097722,1119000684,-608450090,-1396901568,853044451,1172266101,-589951537,-1412350631,651767980,1373503546,-925412992,-1076862698,565507253,1454621731,-809855591,-1195530993,671266974,1594198024,-972236366,-1324619484,795835527,1483230225,-1050600021,-1234817731,1994146192,31158534,-1731059524,-271249366,1907459465,112637215,-1614814043,-390540237,2013776290,251722036,-1777751922,-519137256,2137656763,141376813,-1855689577,-429695999,1802195444,476864866,-2056965928,-228458418,1812370925,453092731,-2113342271,-183516073,1706088902,314042704,-1950435094,-54949764,1658658271,366619977,-1932296973,-69972891,1303535960,984961486,-1547960204,-725929758,1256170817,1037604311,-1529756563,-740887301,1131014506,879679996,-1385723834,-631195440,1141124467,855842277,-1442165665,-586318647,1342533948,654459306,-1106571248,-921952122,1466479909,544179635,-1184443383,-832445281,1591671054,702138776,-1328506846,-942167884,1504918807,783551873,-1212326853,-1061524307,-306674912,-1698712650,62317068,1957810842,-355121351,-1647151185,81470997,1943803523,-480048366,-1805370492,225274430,2053790376,-468791541,-1828061283,167816743,2097651377,-267414716,-2029476910,503444072,1762050814,-144550051,-2140837941,426522225,1852507879,-19653770,-1982649376,282753626,1742555852,-105259153,-1900089351,397917763,1622183637,-690576408,-1580100738,953729732,1340076626,-776247311,-1497606297,1068828381,1219638859,-670225446,-1358292148,906185462,1090812512,-547295293,-1469587627,829329135,1181335161,-882789492,-1134132454,628085408,1382605366,-871598187,-1156888829,570562233,1426400815,-977650754,-1296233688,733239954,1555261956,-1026031705,-1244606671,752459403,1541320221,-1687895376,-328994266,1969922972,40735498,-1677130071,-351390145,1913087877,83908371,-1782625662,-491226604,2075208622,213261112,-1831694693,-438977011,2094854071,198958881,-2032938284,-237706686,1759359992,534414190,-2118248755,-155638181,1873836001,414664567,-2012718362,-15766928,1711684554,285281116,-1889165569,-127750551,1634467795,376229701,-1609899400,-686959890,1308918612,956543938,-1486412191,-799009033,1231636301,1047427035,-1362007478,-640263460,1088359270,936918000,-1447252397,-558129467,1202900863,817233897,-1111625188,-893730166,1404277552,615818150,-1160759803,-841546093,1423857449,601450431,-1285129682,-1000256840,1567103746,711928724,-1274298825,-1022587231,1510334235,755167117]
def three(a:int,b:int):
    if a <0:
        #补码形式
        binary_number2 = bin(a)[3:]
        binary_number = '0'*(32 -len(binary_number2)) + binary_number2
        x = []
        for i in binary_number:  #取反
            I = 1 if not int(i) else 0
            x.append(str(I))
        flipped_number1 = ''.join(x)
        L = len(flipped_number1)
        X = bin(~int(flipped_number1, 2))[3:]  #取反后+1
        flipped_number = '0'*(L-len(X)) + X    #补回原来的长度   原理是要在取反后的二进制+1,
        return int('0' * b + flipped_number[:-b],2) if b else int( flipped_number,2)
    else:
        return int('0' * b + (bin(a)[2:])[:-b],2)   if b else a

def crc32(href:str,I = None):
    e = I if I else 0
    e ^= -1
    for H in href:
        e1 = three(e,8)
        e = e1 ^ n[ 255 & (e ^ ord(H))]
    remainder_list = []
    reNumber = three((-1^e),0)
    while reNumber > 0:
        remainder = reNumber % 256
        remainder_list.append(remainder)
        reNumber //= 256
    remainder_list.reverse()
    return  remainder_list


def int_to_bytes(n):
    if not n:
        return [0]
    binary_str =bin(n)[2:].zfill((len(bin(n)[2:]) + 7) // 7* 7)
    binary_str = [binary_str[i:i + 7] for i in range(0, len(binary_str), 7)]
    byteList = []
    if not int(binary_str[0],2):
        binary_str.remove(binary_str[0])
    for b,_byte in enumerate(binary_str):
        _byte = int('0' + _byte,2)  if not b  else  int('1' + _byte,2)
        byteList.append(_byte)
    byteList.reverse()
    return byteList



def butget(t=0,e=0):
    if t == 64:
        return 64
    elif t == 63:
        return e
    elif t >= e:
        return t + 1
    else:
        return t


class PDD_Cracking:
    def __init__(self):
        self.V = '9240gsB6PftGXnlQTw_pdvz7EekDmuAWCVZ5UF-MSK1IHOchoaxqYyj8Jb3LrNiR='
        self.d = {'_bK': 0}
        self.h = {'_xea': [v for v in self.V],
             '_bÌ': 64,
             }
    def StartTask(self,data):
        self.t = data
        self.T = self.handler_data()
        anti_content = self.PDD_encode()
        return anti_content

    def p_(self):
        compressed = zlib.compress(bytes(self.t))  #把i2转 字节序列的形式   然后压缩,得到  compressed
        return compressed

    def handler_data(self):
        P = self.p_()
        decompressed_list = bytearray(P)  #内置类型bytearray存储二进制数据，相当于C语言中的char类型
        new_arr = [int(byte)  for byte in decompressed_list]
        print([chr(ii) for ii in [102, 36, 67, 120]])
        new_h = [chr(i) for  i  in new_arr] + [chr(ii) for ii in [102, 36, 67, 120]]
        h2 = ''.join(new_h)
        return  h2


    def isNaN(self,value):
        if isinstance(value, (int, float)):
            return math.isnan(value)
        elif isinstance(value, str):
            try:
                float(value)
                return False
            except ValueError:
                return True
        elif isinstance(value, list):
            if len(value) != 1:
                return True
            else:
                try:
                    float(value[0])
                    return False
                except ValueError:
                    return True
        else:
            return True


#管理h的,属于h方法里的
    def _xe1(self,t):
        self.h['_bÌ'] += 1
        if  len(self.h['_xea']) <= self.h['_bÌ']:
            self.h['_xea'].append(t)
        else:
            self.h['_xea'][self.h['_bÌ']] = t

#d方法
    def _bf(self):
        try:
            char_code = ord(self.d['_bÇ'][self.d['_bK']])
        except:
            char_code = 0
        self.d['_bK'] += 1
        return char_code
    def PDD_encode(self):
        P = ""
        y = int(random.random()*64)
        ##print(66666666,self.T == "x\x9Ccfd``ê\x16ÜÉñ\x88ùÁ\x91'r\f'äî³?b\x99º\x1FÈ|Èþ\x90e)\x88ñ\x14ÈØ\nb¼b\x7FÀr\x14ÄxÇ~\x9Få*\x88ñ\x85ý.ËS\x10ã\x07û\x1D\x96¯ Æoö\x9B,­\x07\x80\x8C¿ì7X¦\x82\x18\r\x1C×XÖ\x82\x18m\x1C\x97Xö\x82\x18\x138N²\x9C\x051æqìf¹\vb¬àXÅò\x16ÄXÇ1\x9Bå/\x88±\x9Ec2KïA c\x03G/Ë\\\x10c\x13G;ËZ\x10c+G\x03Ë^\x10c;Ç/æ³ ÆN\x8E/Ìw!\x8C\x0FÌo!\x8CwÌ\x7F!\x8C·Ì}\x87À\x8C×Ì?!\x8C\x97Ì«\x0E\x83\x19Ï\x99¯C\x18O\x99'\x1E\x013\x1E1/\x831^\x82\x18\x8A Ö¶£@\x96¿ß='éó\x1C³\x81\x9E¼É±\x06HÞåØ\x03$-´2JJ\n\x8A­ôõss\x8Bõ\n2óRJó\x81H/9?W?=??¥\x18BÆçd\x16\x970ô·d¸;4ðOàð\x903634´0³´0503041°Ð54³0007751547\bhp\x888»BéVbefe\x91À±\x8A|ßüªÌ\x9C\x9CD}S=\x03\x05\x8Dp -ùåÅ\n~!\n\x86\x06z\x06Ö\n@\x013\x13k\x85\n3\x13M\x05Ç\x82\x82\x9CÔðÔ$ïÌ\x12}Scs=c3\x05\ro\x8F\x10_\x1F\x1D\x85\x9CÌìT\x05÷Ôäì|M\x05ç\x8C¢üÜT}C\x90\x01 ¨\x10\x9C\x98\x96X\x94\tÕÒ \x11Qàj\x91c\x10\x12\x99Sà\x1C\x19a\x10\x92\x14\x11\x12\x1Fä\x99\x15\x9A\x96\x15a\x94\x97nXà[á\x16\x9C\x15ï\x13ïÛA´Ê\x05\x12EN\x11~Nî\x81®\x81\x95\x15Y9Ùa\x1E\x81ÎI\x85\x8Eé¶¶«\x98$·1¶kLÞ{õ\x02\x03\x00æüþ\x12£øCE")
        self.d['_bÇ'] = self.T
        GG =  0
        while self.d['_bK'] < len(self.T):
            ###print(111,len(T),d['_bK'])
            #9
            GG+=1
            self._xe1(self._bf()) #9
            #2
            self._xe1(self._bf())#2
            #5
            self._xe1(self._bf()) #5
            ##print(self.d['_bK'], self.h['_xea'][-3:])

            #3
            ###print(d['_bK'],h['_bÌ'],h['_xea'],h['_xea'][h['_bÌ']-2])
            i = int(self.h['_xea'][self.h['_bÌ']-2]) >> 2

            #0
            a0 = int(self.h['_xea'][(self.h['_bÌ']-2)])
            a0 = a0 & 3
            a0 = a0 << 4
            a1 = int(self.h['_xea'][self.h['_bÌ']-1]) >> 4
            a = a0 | a1
            #a = ( ([h['_xea'][(h['_bÌ']-2)] & 3 )<<4  ],h['_xea'][h['_bÌ']-1] >> 4)

            #7
            u0 =  int(self.h['_xea'][self.h['_bÌ']-1])
            u0 = u0 & 15
            u0 = u0 << 2
            u1 = int(self.h['_xea'][self.h['_bÌ']]) >> 6
            u =  u0 | u1

            #1
            c =  int(self.h['_xea'][self.h['_bÌ']]) & 63


            ##print(f'第{GG}次变动前   i:{i}   a:{a}    u:{u}    c:{c}')
            #4
            if self.isNaN(self.h['_xea'][(self.h['_bÌ'] - 1)]):
                u = c = 64
            else:
               c = 64 if self.isNaN(self.h['_xea'][self.h['_bÌ']])  else c



            #6
            i = butget(i ,y)
            a = butget(a,y)
            u = butget(u, y)
            c = butget(c, y)

            ##print(f'第{GG}次变动后   i:{i}   a:{a}    u:{u}    c:{c}')

            #10
            self.h['_bÌ'] -= 3
            #8
            #c_0 = h["_xea"][c]


            p =  str(self.h["_xea"][i]) + str(self.h["_xea"][a]) + str(self.h["_xea"][u]) +str(self.h["_xea"][c])
            P +=p
            ###print('完成',P)

            if  self.d['_bK'] > len(self.T) and P[-2:] == '99':
                P = P[0:-2] + '=='
            ##print('###########################')

            ##print()
            ##print()
        ##print('完整:', '0ap' + P.replace('=','') + self.V[y])
        return '0ap' + P.replace('=','') + self.V[y]
class Create_list:
    def __init__(self,UsingFuction=None,Cookie=None,JoinUrl=None,Count=None):
        self.UsingFuction = UsingFuction if UsingFuction else None
        if Cookie:
            CookieDict = self.cookieHandler(Cookie)
            if 'api_uid' in CookieDict and '_nano_fp' in CookieDict:
                self.api_uid = CookieDict['api_uid']
                self._nano_fp = CookieDict['_nano_fp']
                self.join_time = int(CookieDict['x-visit-time']) + 1000 if 'x-visit-time' in CookieDict else None
            else:
                self.api_uid = None
                self._nano_fp = None
                self.join_time = None
        else:
            self.api_uid = None
            self._nano_fp = None
            self.join_time = None
        self.count = Count if Count else None
        JoinUrl = JoinUrl if JoinUrl else "https://mms.pinduoduo.com/home"

        if not self.api_uid or  not self._nano_fp:
            self.CookieErroe = 'cookie没检测api_uid,_nano_fp.请检查你的cookie'
        else:
            self.CookieErroe = None
        self.total = []
        method_list = ['xt','wt','mt','kt','ct','pt',
                       'Et','At','Lt_qt','Nt','Bt','It',
                       'Jt','zt','Kt','Zt','Yt','Re',
                       ]
        self.StartTime = int(time.time()*1000)
        self.join_time = self.join_time if self.join_time and self.StartTime - self.join_time < 3*3600*1000 else self.StartTime - 14124991
        #获取cookie 访问时间
            #if 访问时间 在当前时间的3个小时以内  就认定 访问时间+1000毫秒就是进入页面的时间
            #else 执行方法时间 - 14124991(常量)为访问时间
        ##print(self.join_time)

        for method_name in method_list:
            attr = getattr(self,method_name)
            if method_name =='kt':
                self.total += attr(JoinUrl)
            elif method_name == 'Jt':
                self.total += attr("https://mms.pinduoduo.com/login/")
            else:
                self.total += attr()
        #print(self.total)
        total_len = bin(len(self.total))[2:]
        totalLen = '0' * (16 - len(total_len)) + str(total_len)
        self.total = [3] + [1,0,0] + [int(totalLen[0:8],2),int(totalLen[8:16],2)] +self.total
        self.anti_content = PDD_Cracking().StartTask(self.total)

    def xt(self):
        #self.StartTime
        if self.UsingFuction and self.UsingFuction in UsingFuctionDict:
            X1 = UsingFuctionDict[self.UsingFuction]['X'][0]
            X2 = UsingFuctionDict[self.UsingFuction]['X'][1]
            Y1 = UsingFuctionDict[self.UsingFuction]['Y'][0]
            Y2 = UsingFuctionDict[self.UsingFuction]['Y'][1]
            clientX = random.randint(X1, X2)
            clientY = random.randint(Y1, Y2)
        else:
            clientX = random.randint(920, 1280)
            clientY = random.randint(580, 720)
        timeStampe = self.StartTime - self.join_time
        elementId = [0]
        self.randomSeedDict = {'clientX':  clientX, 'clientY': clientY, 'timeStampe':  timeStampe, 'elementId': ""}
        x = [17] + int_to_bytes(clientX) + int_to_bytes(clientY) +  int_to_bytes(timeStampe) + elementId
        return  x


    def wt(self):
        similar_dicts_ = []
        timeStampe = self.StartTime - self.join_time - 100
        RandomRangeSeconds_Start =  timeStampe - 10000 if timeStampe - 10000 < 0 else 12
        RandomRangeSeconds_End   =  timeStampe - 100   if timeStampe - 10000 < 0 else 80
        TimeStampe = 0
        while len(similar_dicts_) < 30:
            new_dict = copy.deepcopy(self.randomSeedDict)
            timestampe =random.randint(RandomRangeSeconds_Start, RandomRangeSeconds_End)
            randomRange = timestampe//10 if  timestampe//10 else 2
            new_dict['clientX'] += random.randint(-randomRange, randomRange)
            new_dict['clientY'] += random.randint(-randomRange, randomRange)
            TimeStampe += timestampe
            new_dict['timeStampe'] -= TimeStampe
            if set(new_dict.values()) not in [set(d.values()) for d in similar_dicts_]:
                similar_dicts_.append(new_dict)
        similar_dicts = sorted(similar_dicts_, key=lambda x: x['timeStampe'])
        similar_dicts[-2]['clientX'] = similar_dicts[-1]['clientX'] = self.randomSeedDict['clientX']
        similar_dicts[-2]['clientY'] = similar_dicts[-1]['clientY'] = self.randomSeedDict['clientY']
        #print(similar_dicts)
        bytesList = [200,30]
        for similar_dict in  similar_dicts:
            for dict_value in list(similar_dict.values()):
                bytesList +=  int_to_bytes(dict_value)
        return  bytesList

    def mt(self):
        new_dict = copy.deepcopy(self.randomSeedDict)
        for key in self.randomSeedDict.keys():
            if key == 'timeStampe':
                new_dict[key] += random.randint(10, 100)
        bytesList = [33]
        for dict_value in list(new_dict.values()):
            bytesList += int_to_bytes(dict_value)
        return  bytesList + [79, 78, 222, 66]

    def kt(self,Api):
        return  [56]+[len(Api)]+[ord(A) for A in Api]+[0,143,132,104,71]#[0,207,29,38,184]
    def ct(self):
        #页面大小
        return [64] + int_to_bytes(1920) + int_to_bytes(1040)
    def pt(self):
        #self.time0 = int(time.time()*1000)
        random.seed(self.StartTime)
        random_folat = ["{:.16f}".format(random.random()) for i in range(2)]
        #print(888888,int(int(2**52+1) * float(random_folat[0])),int(2**52+1) * float(random_folat[0]))
        x_time = str(int(int(2**52+1) * float(random_folat[0]) + int(2**30+1) * float(random_folat[1]))) + '-' + str(self.StartTime)
        X = [ord(i) for  i in  x_time]
        return  [72] +  [len(X)] + X  #'2897766349955370-1679981736461'  1679981736893
    def Et(self): #10*8  + n(8192)转二进制
        return [80, 128, 64]
    def At(self): #11*8 + 当前页面
        if self.UsingFuction and self.UsingFuction in UsingFuctionDict:
            return  [88] + crc32(UsingFuctionDict[self.UsingFuction]['URL'])
        return [88,205,168,34,218]
    def Lt_qt(self):  #97 + ord("y")
        return [97,121,105,121]



    def Nt(self):
        time_subtraction = int(time.time()*1000) - self.StartTime
        time_subtraction = time_subtraction if 5 > time_subtraction > 0 else random.randint(1, 5)
        remainder_list = []
        while time_subtraction > 0:
            remainder = time_subtraction % 256
            remainder_list.append(remainder)
            time_subtraction //= 256
        remainder_list.reverse()
        n = 112 + len(remainder_list)
        return [n] + remainder_list

    def Bt(self):
        agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        return [120] + [len(agent)] + [ord(i) for i in agent]


    def It(self):
        if self._nano_fp:
            nanoFp = [ord(i) for i in self._nano_fp]
            return [128,len(nanoFp)] + nanoFp +[136,len(nanoFp)] + nanoFp
        else:
            return [128,40,88,112,69,56,108,48,84,89,108,112,67,89,88,48,84,98,88,84,95,82,73,106,85,102,106,88,50,110,103,49,112,77,120,70,83,106,95,76,95,77]+[136,40,88,112,69,56,108,48,84,89,108,112,67,89,88,48,84,98,88,84,95,82,73,106,85,102,106,88,50,110,103,49,112,77,120,70,83,106,95,76,95,77]
    def Jt(self,LoginApi):  #"https://mms.pinduoduo.com/login/"
        return []#[18*8] + [ord(i) for i in str(LoginApi)]
    def zt(self):
        return []#[169, 153]
    def Kt(self):
        if self.api_uid:
            api_uid = [ord(i) for i in self.api_uid]
            return [160,len(api_uid)] + api_uid
        else:
            return [160,24] + [ord(i) for i in str("rBXNBGQEQyxjlkVHQCbqAg==")]

    def Zt(self):
        self.count = int(self.count) if self.count else random.randint(180,1800)
        remainder_list = []
        while self.count > 0:
            remainder = self.count % 256
            remainder_list.append(remainder)
            self.count //= 256
        remainder_list.reverse()
        n = 168 + len(remainder_list)
        return [n] + remainder_list

    def Yt(self):
        timestamp =  self.join_time # 13位,初次进入页面的时间
        binary_str = bin(timestamp)[2:]
        l = len(binary_str) // 6
        binary_str = '0' * (l * 8 - len(binary_str)) + str(binary_str)
        u = []
        for  c  in range(l):
            d = int(binary_str[c*8:(c+1)*8],2)
            u.append(d)
        return [182] + u

    def Re(self):
        return [208,0]

    def cookieHandler(self,cookie_str):
        cookie_dict = {}
        cookie_pairs = cookie_str.split(';')
        for pair in cookie_pairs:
            pair = pair.strip()
            if pair:
                key, value = pair.split('=', 1)
                cookie_dict[key] = value
        return cookie_dict


if __name__ == '__main__':
    #cookie 你的店铺cookie
    #count 调用次数
    cookie = '_bee=Raljnq0b6aKyFua6R5gwQ9p8vDJQr42l; _f77=6f8352db-3d3b-4d22-840b-a7ea88876cc2; _a42=4f526040-7d9d-4151-bcec-b86be9d48bf9; api_uid=CmlqNWRGQQUDawBThno0Ag==; _nano_fp=XpEJX5Xxnpmjn0d8nC_gtoIgd1lWrNnWYuYin1UJ; rckk=Raljnq0b6aKyFua6R5gwQ9p8vDJQr42l; ru1k=6f8352db-3d3b-4d22-840b-a7ea88876cc2; ru2k=4f526040-7d9d-4151-bcec-b86be9d48bf9; SUB_PASS_ID=eyJ0IjoiejJvb3V6TkMzVS9oM0NKT1dNMkZrKzJ4UmZrcEh2RnRzV1QvYUlEWWM5di9FclFIbWk0NXBPOWZvWGltZXFhTyIsInYiOjEsInMiOjEwMDAwLCJ1Ijo5MDQ2ODAyNDAxMzI5fQ=='
    count = 1
    Create_list = Create_list(UsingFuction=101,Cookie = cookie,JoinUrl=None,Count=count)
    print(Create_list.anti_content)

#鼠标加密参数,cookie,api_uid  zlib