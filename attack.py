# import socket
# import pyautogui
# import signal
# import win32gui
# import win32api
# import win32con
# import json
# import os
# import sys
# import requests
# import uuid
import random
# import cv2
# import time
# from math import log10, floor
from time import perf_counter
# import numpy as np
# import threading
# from pynput import keyboard
# from PIL import ImageGrab
# from datetime import datetime
# from game import Game
# import asyncio
# import tkinter as tk
# from tkinter import messagebox
# from tkinter import *
# import gdi_capture
# from PIL import Image, ImageTk   
from configparser import ConfigParser

from theinterception import Interception
from theinterception import KEYBOARD_MAPPING
from theinterception import _utils
from theinterception import exceptions
from theinterception import KeyStroke, MouseStroke, Stroke
from theinterception import (FilterKeyState, FilterMouseState, KeyState, MouseFlag,
                      MouseRolling, MouseState)

try:
    interception = Interception()
    INTERCEPTION_INSTALLED = True
except Exception:
    INTERCEPTION_INSTALLED = False
print(f'{INTERCEPTION_INSTALLED = }')

async def sleep(dur):
    now = perf_counter()
    end = now + dur
    while perf_counter() < end:
        pass

# to convert keycode
def _get_keycode(key: str) -> int:
    try:
        return KEYBOARD_MAPPING[key]
    except KeyError:
        raise exceptions.UnknownKeyError(key)

# key press down function
def keydown(key):
    keycode = _get_keycode(key)
    stroke = KeyStroke(keycode, KeyState.KEY_DOWN, 0)
    interception.send_key(stroke)

# key release function
def keyup(key):
    keycode = _get_keycode(key)
    stroke = KeyStroke(keycode, KeyState.KEY_UP, 0)
    interception.send_key(stroke)


# read player key settings on startup. 

config = ConfigParser()
config.read('keysettings.ini')
atk = config.get('main', 'attack')
jump = config.get('main', 'jump')
teleport = config.get('main', 'teleport')
ropeconnect = config.get('main', 'ropeconnect')

async def leftp(x=31,y=101):
    keydown('left')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def leftr(x=31,y=101):
    keyup('left')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def rightp(x=31,y=101):
    keydown('right')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def rightr(x=31,y=101):
    keyup('right')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def upp(x=31,y=101):
    keydown('up')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def upr(x=31,y=101):
    keyup('up')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def downp(x=31,y=101):
    keydown('down')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def downr(x=31,y=101):
    keyup('down')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def jumpp(x=31,y=101):
    keydown(jump)
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def jumpr(x=31,y=101):
    keyup(jump)
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def teleportp(x=31,y=101):
    keydown(teleport)
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def teleportr(x=31,y=101):
    keyup(teleport)
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def attackp(x=31,y=101):
    keydown(atk)
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def attackr(x=31,y=101):
    keyup(atk)
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def ropeconnectp(x=31,y=101):
    keydown(ropeconnect)
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def ropeconnectr(x=31,y=101):
    keyup(ropeconnect)
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def goleftattack():
    print(f'goleftattack')
    await leftp()
    await jumpp()
    await jumpr()    
    await jumpp()
    await jumpr()
    await attackp()
    await attackr()
    await leftr()

async def gorightattack():
    print(f'gorightattack')
    await rightp()
    await jumpp()
    await jumpr()    
    await jumpp()
    await jumpr()
    await attackp()
    await attackr()
    await rightr()

async def goupattack():
    print(f'goupattack')
    await rightp()
    await ropeconnectp()
    await ropeconnectr()
    await attackp()
    await attackr()
    await rightr()

async def godownattack():
    print(f'godownattack')
    await downp()    
    await jumpp()
    await jumpr()
    await attackp()
    await attackr()
    await downr()



