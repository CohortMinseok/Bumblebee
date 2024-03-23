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

from initinterception import interception, move_to, move_relative, left_click, keydown, keyup, sleep


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

async def leftattack():
    print(f'leftattack')
    await leftp()
    await attackp()
    await attackr()
    await leftr()

async def rightattack():
    print(f'rightattack')
    await rightp()
    await attackp()
    await attackr()
    await rightr()

async def goleftattack():
    print(f'goleftattack')
    await leftp()
    await teleportp()
    await teleportr()
    await attackp()
    await attackr()
    await leftr()

async def goleftattackk():
    print(f'goleftattackk')
    await leftp()
    await teleportp()
    await teleportr()
    await attackp()
    await attackr()
    await attackp()
    await attackr()
    await leftr()

async def goleftattackv2():
    print(f'goleftattackv2')
    await leftp()
    await jumpp()
    await jumpr()    
    await jumpp()
    await jumpr()
    await attackp()
    await attackr()
    await leftr()

async def gorightattackk():
    print(f'gorightattackk')
    await rightp()
    await teleportp()
    await teleportr()
    await attackp()
    await attackr()
    await attackp()
    await attackr()
    await rightr()

async def gorightattack():
    print(f'gorightattack')
    await rightp()
    await teleportp()
    await teleportr()
    await attackp()
    await attackr()
    await rightr()

async def gorightattackv2():
    print(f'gorightattackv2')
    await rightp()
    await jumpp()
    await jumpr()    
    await jumpp()
    await jumpr()
    await attackp()
    await attackr()
    await rightr()

async def goupattackv2():
    print(f'goupattackv2')
    await rightp()
    await ropeconnectp()
    await ropeconnectr()
    await attackp()
    await attackr()
    await rightr()

async def goupattack():
    print(f'goupattack')
    await sleep(.1)
    await upp()
    await teleportp()
    await teleportr()
    await upr()
    await attackp()
    await attackr()
    await sleep(.1)

async def goupattackv3():
    print(f'goupattackv3')
    await sleep(.1)
    await jumpp()
    await jumpr()
    await ropeconnectp(31,101)
    await ropeconnectr(31,101)
    await sleep(.333)
    await attackp()
    await attackr()
    await attackp()
    await attackr()
    await sleep(.1)

async def upjumpattack():
    print(f'upjumpattack')
    await sleep(.1)
    await upp()
    await teleportp()
    await teleportr()
    await upr()
    await attackp()
    await attackr()
    await sleep(.1)

async def upjumpattackv2(): # adele upjump
    print(f'upjumpattackv2')
    await sleep(.1)
    await jumpp()
    await jumpr()
    await upp()
    await jumpp()
    await jumpr()
    await upr()
    await attackp()
    await attackr()
    await attackp()
    await attackr()
    await sleep(.1)

async def godownattack():
    print(f'godownattack')
    await downp()
    await teleportp()
    await teleportr()
    await downr()
    await attackp()
    await attackr()
    await sleep(.1)

async def godownattackv2():
    print(f'godownattackv2')
    await downp()    
    await jumpp()
    await jumpr()
    await attackp()
    await attackr()
    await downr()


# polo portal hunting map rotation patch

async def upjumpup():
    print(f'upjumpup')
    await jumpp()
    await jumpr()
    await upp()
    await jumpp()
    await jumpr()
    await upr()

async def bountyhuntrotation():
    print(f'bountyhuntrotation')
    for i in range(5):
        await goleftattack()
        time.sleep(.502)
    for i in range(5):
        await gorightattack()
        time.sleep(.502)

async def bountyhuntrotationv2(): # adele flash jump
    print(f'bountyhuntrotationv2')
    for i in range(4):
        await goleftattack()
        time.sleep(.502)
    for i in range(4):
        await gorightattack()
        time.sleep(.502)

async def castlewallrotation():
    print(f'castlewallrotation')
    await leftattack()
    time.sleep(.5)
    await rightattack()
    time.sleep(.5)
    # await goleftattack()
    # time.sleep(.502)
    await upjumpup()
    time.sleep(.802)
    await leftattack()
    time.sleep(.5)
    await rightattack()
    time.sleep(.5)
    # await gorightattack()
    # time.sleep(.502)
    await downjump()
    time.sleep(.702)

async def castlewallrotationv3():
    print(f'castlewallrotationv3')
    await leftattack()
    time.sleep(.5)
    await rightattack()
    time.sleep(.5)
    # await goleftattack()
    # time.sleep(.502)
    await ropeconnectpr()
    time.sleep(.802)
    await leftattack()
    time.sleep(.5)
    await rightattack()
    time.sleep(.5)
    # await gorightattack()
    # time.sleep(.502)
    await downjump()
    time.sleep(.702)

async def castlewallrotationv2():
    print(f'castlewallrotationv2')
    for i in range(2):
        await goleftattack()
        time.sleep(.502)
    await ropeconnectpr()
    time.sleep(.802)
    for i in range(2):
        await gorightattack()
        time.sleep(.502)
    await downjump()
    time.sleep(.702)
    await attackp()
    await attackr()
    time.sleep(.502)

async def stormwingrotation():
    print(f'stormwingrotation')
    for i in range(5):
        await goleftattack()
        time.sleep(.502)
    await ropeconnectpr()
    time.sleep(.602)
    for i in range(5):
        await gorightattack()
        time.sleep(.502)
    for i in range(5):
        await downjump()
        time.sleep(.302)

# randomiser patch

async def send2(code):
    keydown(code)
    r = random.randint(31, 131)
    r /= 1000
    await sleep(r)

async def send3(code):
    keyup(code)
    r = random.randint(31, 131)
    r /= 1000
    await sleep(r)


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
    await leftp()
    await jumpp()
    await jumpr()
    # await jumpp()
    # await jumpr()
    await jumpp()
    await jumpr()
    # await shikigamip()
    # await shikigamir()
    await attackp()
    await attackr()
    await leftr()

async def rightjumpjumpattack(x=31, y=101):
    await rightp()
    await jumpp()
    await jumpr()
    # await jumpp()
    # await jumpr()
    await jumpp()
    await jumpr()
    # await shikigamip()
    # await shikigamir()
    await attackp()
    await attackr()
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