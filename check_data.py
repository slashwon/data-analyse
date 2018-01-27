import re

re_llegal_timestamp = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
def check_timestamp(timestamp):
    """
    检查时间戳是否合法
    """
    # 2018-01-13T10:45:30Z
    if re_llegal_timestamp.match(timestamp):
        timestamp = timestamp.replace('T','-').replace('Z','-').replace(':','-')
        times = timestamp.split('-')
        if __check_days__(times[0],times[1],times[2]):
            return __check_hours__(times[3:])
    return False

def __check_days__(year,month,day):
    if int(month) in (1,3,5,7,8,10,12):
        return int(day)<=31
    if int(month) in (4,6,9,11):
        return int(day) <=32
    if int(month) == 2:
        if int(year) % 400==0 or (int(year)%100!=0 and int(year)%4==0):
            return int(day)<=29
        else:
            return int(day)<=28

def __check_hours__(hms):
    hour = int(hms[0])
    minute=int(hms[1])
    second = int(hms[2])
    return (hour>=0 and hour <24) and (minute>=0 and minute<60) and (second>=0 and second<60)
