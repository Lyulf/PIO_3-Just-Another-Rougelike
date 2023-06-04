import pygame
import threading

__local_data = threading.local()
__local_data.__CURRENT_BORDER = None

def get_border():
    global __local_data
    return __local_data.__CURRENT_BORDER

def set_border(value):
    global __local_data
    __local_data.__CURRENT_BORDER = value
