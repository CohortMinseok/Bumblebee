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
# import random
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
# from configparser import ConfigParser

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

async def goleftattack():
    await leftp()
    await jumpp()
    await jumpr()    
    await jumpp()
    await jumpr()
    await attackp()
    await attackr()
    await leftr()



