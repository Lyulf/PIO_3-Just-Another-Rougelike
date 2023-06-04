import threading

__local_data = threading.local()
__local_data.__DT = 0

def current_dt():
    global __local_data
    return __local_data.__DT

def update_dt(value):
    global __local_data
    __local_data.__DT = value