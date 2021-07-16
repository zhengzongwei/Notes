import time
import os

def execute_time(func):
    """
    compute function execute time
    """
    def wrapper(*args,**kwargs):
        start_time = time.time()
        func_return = func(*args,**kwargs)
        end_time = time.time()
        formet_str = ("[%s] execute time: %s " % (func.__name__,end_time-start_time))
        print(formet_str)
        os.system("echo %s >> %s-esexute-time" % (formet_str,func.__name__))
        return func_return
    return wrapper


def now_time(nowtime=None)->str:
    """
    formatting time
    """
    if nowtime is None:
        nowtime = time.time()
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(nowtime))

def now_timestrap():
    return time.time()

def timestrap(str_time:str)->int:
    """
    formatting time to timestrap
    """
    return time.mktime(str_time,"%Y-%m-%d %H:%M:%S")
   




