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
import time
# from math import log10, floor
from time import perf_counter
# import numpy as np
# import threading
# from pynput import keyboard
from pynput.keyboard import Listener as KeyListener  # type: ignore[import]
from pynput.mouse import Listener as MouseListener  # type: ignore[import]
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
from typing import Literal, Optional
_TEST_MOUSE_STROKE = MouseStroke(MouseState.MOUSE_MIDDLE_BUTTON_UP, 0, 0, 0, 0, 0)
_TEST_KEY_STROKE = KeyStroke(KEYBOARD_MAPPING["space"], KeyState.KEY_UP, 0)
def auto_capture_devices2(*, keyboard: bool = True, mouse: bool = True, verbose: bool = False):
    mouse_listener = MouseListener(on_click=lambda *args: False)
    key_listener = KeyListener(on_release=lambda *args: False)
    for device in ("keyboard", "mouse"):
        if (device == "keyboard" and not keyboard) or (device == "mouse" and not mouse):
            continue
        print(f"Trying {device} device numbers...")
        stroke: Stroke
        if device == "mouse":
            listener, stroke, nums = mouse_listener, _TEST_MOUSE_STROKE, range(10, 20)
        else:
            listener, stroke, nums = key_listener, _TEST_KEY_STROKE, range(10)
        listener.start()
        for num in nums:
            interception.send(num, stroke)
            time.sleep(random.uniform(0.1, 0.3))
            if listener.is_alive():
                print(f"No success on {device} {num}...")
                continue
            print(f"Success on {device} {num}!")
            set_devices(**{device: num})
            break
    print("Devices set.")    
def set_devices(keyboard: Optional[int] = None, mouse: Optional[int] = None) -> None:
    """Sets the devices on the current context. Keyboard devices should be from 0 to 10
    and mouse devices from 10 to 20 (both non-inclusive).

    If a device out of range is passed, the context will raise a `ValueError`.
    """
    interception.keyboard = keyboard or interception.keyboard
    interception.mouse = mouse or interception.mouse
auto_capture_devices2()

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
config.read('settings.ini')
atk = config.get('keybind', 'attack')
jump = config.get('keybind', 'jump')
teleport = config.get('keybind', 'teleport')
ropeconnect = config.get('keybind', 'ropeconnect')
npc = config.get('keybind', 'npc')

def refreshkeybind():
    global atk
    global jump
    global teleport
    global ropeconnect
    global npc
    config.read('settings.ini')
    atk = config.get('keybind', 'attack')
    jump = config.get('keybind', 'jump')
    teleport = config.get('keybind', 'teleport')
    ropeconnect = config.get('keybind', 'ropeconnect')
    npc = config.get('keybind', 'npc')


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

async def npcp(x=31,y=101):
    keydown(npc)
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def npcr(x=31,y=101):
    keyup(npc)
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

async def ropeconnectpr():
    await ropeconnectp()
    await ropeconnectr()

# rectangular clockwise rotation

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

# temp (not organized) (please delete soon)


async def shiftp(x=31, y=119):
    # send2('01')
    keydown('shift')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)


async def shiftr(x=31, y=101):
    # send3('01')
    keyup('shift')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def shiftpr():
    await shiftp()
    await shiftr()

async def shikigamip(x=31,y=101):
    # send2('27')
    keydown('x')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def shikigamir(x=31,y=101):
    # send3('27')
    keyup('x')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def shikigamipr3(x=3,y=33):
    await shikigamip()
    await shikigamir(x,y)
    await shikigamip()
    await shikigamir(x,y)
    await shikigamip()
    await shikigamir(x,y)

async def jumpupjumpattack(x=31,y=101):
    print(f'jumpupjumpattack')
    # await ep()
    # await er()
    await jumpp(111,177)
    await jumpr()
    await upp()
    await jumpp(111,177)
    await jumpr(3,33)
    await upr(3,33)
    # await rp()
    # await rr()
    await shikigamip()
    await shikigamir()
    await sleep(.2)
    
async def downjump():
    await downp()
    await jumpp()
    await jumpr()
    await downr()
    # time.await sleep(3)
    # yinyangp()
    # yinyangr(555,999)

async def downjumpv2():
    await downp()
    await jumpp()
    await jumpr()
    await shiftpr()
    await downr(1333,1999)
    
async def yinyangp(x=31, y=101):
    keydown('s')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def yinyangr(x=31, y=101):
    keyup('s')
    r = random.randint(x, y)
    r /= 1000
    await sleep(r)

async def leftjumpjumpattack(x=31, y=101):
    await leftp(111,177)
    await jumpp()
    await jumpr(3,33)
    await jumpp()
    await jumpr()
    await jumpp()
    await jumpr(133, 255)
    await shikigamip()
    await shikigamir()
    await leftr()

async def rightjumpjumpattack(x=31, y=101):
    await rightp(111,177)
    await jumpp()
    await jumpr(3,33)
    await jumpp()
    await jumpr()
    await jumpp()
    await jumpr(133, 255)
    await shikigamip()
    await shikigamir()
    await rightr()

async def upjumpshift():
    await jumpp()
    await jumpr()
    await upp()
    await shiftp()
    await upr()
    await shiftr(333, 888)
    await yinyangp()
    await yinyangr(444, 777)