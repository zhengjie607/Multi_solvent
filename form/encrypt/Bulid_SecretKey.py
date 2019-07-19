
import datetime
from encrypt.MyCryptoAMSlicer import PrpCrypt#整体调试用
#from MyCryptoAMSlicer import PrpCrypt#单独调试用
def authorization(serialnumber,days1,key):
    if len(serialnumber.strip())!=36:
        return -1#序列号长度有误
    tmp_serialnumber=serialnumber.replace('-','')
    #print(tmp_serialnumber)
    serialnumber1=tmp_serialnumber[0:8]
    serialnumber2=tmp_serialnumber[8:16]
    serialnumber3=tmp_serialnumber[16:24]
    serialnumber4=tmp_serialnumber[24:32]


    now_day=datetime.datetime.now()
    new_day=now_day+datetime.timedelta(days=days1)
    
    beforeAes=str(now_day.year)+stringday(now_day.day)+ serialnumber2+tohex(new_day.month)+serialnumber1+stringday(new_day.day)+serialnumber4+str(new_day.year)+serialnumber3+tohex(now_day.month)
    
    #print(beforeAes)
    return PrpCrypt(key).encrypt(beforeAes)
def deauthorization(serialnumber,key):
    beforeAes=PrpCrypt(key).decrypt(serialnumber)
    serialnumber1=beforeAes[15:23]
    serialnumber2=beforeAes[6:14]
    serialnumber3=beforeAes[37:45]
    serialnumber4=beforeAes[25:33]

    SN=serialnumber1+'-'+serialnumber2[0:4]+'-'+serialnumber2[4:8]+'-'+serialnumber3[0:4]+'-'+serialnumber3[4:8]+serialnumber4

    re_day=beforeAes[23:25]
    re_month=beforeAes[14]
    if re_month=='A':
        re_month=10
    elif re_month=='B':
        re_month=11
    elif re_month=='C':
        re_month=12
    re_year=beforeAes[33:37]
    re_day=int(re_day)
    re_month=int(re_month)
    re_year=int(re_year)
    re_date=datetime.datetime(re_year,re_month,re_day)
    now_day=beforeAes[4:6]
    now_month=beforeAes[45]
    if now_month=='A':
        now_month=10
    elif now_month=='B':
        now_month=11
    elif now_month=='C':
        now_month=12
    now_year=beforeAes[0:4]
    now_day=int(now_day)
    now_month=int(now_month)
    now_year=int(now_year)
    now_date=datetime.datetime(now_year,now_month,now_day)
    return SN,re_date,now_date
def stringday(day):
    if day<10:
        tmp='0'+str(day)
    else:
        tmp=str(day)
    return tmp   
def tohex(be):
    tmp=""
    if be==10:
        tmp="A"
    elif be==11:
        tmp="B"
    elif be==12:
        tmp='C'
    else:
        tmp=str(be)
    return tmp
def getSerialNum():
    f=open('store.kd','r')
    serial_num=f.read()
    f.close()
    
    if serial_num=='':
        import uuid
        serial_num=uuid.uuid1()
        f=open('store.kd','w')
        f.write(str(serial_num))
        f.close()
    return str(serial_num)        
       
if __name__=='__main__':
    key1="djjwiw38dn43wx1q"
    a=authorization("8269974a-a9f2-11e9-8199-6c4b90a65841",1,key1)
    print(a)
    b,c,d=deauthorization(a,key1)
    print(b)
    print(c)
    print(d)
    print(getSerialNum())
    