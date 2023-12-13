import socket
import pyautogui
import signal
import time
import win32gui
import win32api
import win32con
import json
import os
import sys
from math import log10, floor
import random
from time import perf_counter
import numpy as np
import cv2
import threading
from pynput import keyboard
from PIL import ImageGrab
import requests
import uuid
from datetime import datetime
from game import Game
import asyncio

import tkinter as tk
from tkinter import messagebox
from tkinter import *

# from theinterception.interception import Interception
# from theinterception._keycodes import KEYBOARD_MAPPING
# import theinterception._utils as _utils
# import theinterception.exceptions as exceptions
# from theinterception.strokes import KeyStroke, MouseStroke, Stroke
# from theinterception._consts import (FilterKeyState, FilterMouseState, KeyState, MouseFlag,
#                       MouseRolling, MouseState)

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


# global variables
pause = False


# essential functions
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


async def main(stop_event):
    print(f'script starting ..')
    time.sleep(1)
    
    while True:
        #
        # time.sleep(1)
        now=perf_counter()
        # for i in range(1):
        #     keydown('a')
        #     await sleep(.002)
        #     keyup('a')
        #     await sleep(.002)
        print(f'{perf_counter()-now:.10f}')
        keydown('enter')
        await sleep(.002)
        keyup('enter')
        await sleep(.002)
        #
        print(f'time.sleep ..')
        await sleep(2.002)
        if pause:
            print(f'script paused ..')
            while pause:
                # do nothing
                time.sleep(1)
                if stop_event.is_set():
                    return
            print(f'resume script ..')




if __name__ == "__main__":
    

    
    def on_close():
        print("Closing the window")
        # Add your code here to run before closing the window
        for _, stop_event in threads:
            stop_event.set()
        for thread, _ in threads:
            thread.join()
        root.destroy()

    def on_button_click():
        stop_event = threading.Event()
        thread = threading.Thread(target=between_main, args=(stop_event,))
        thread.start()
        threads.append((thread, stop_event))
        # label.config(text="Working...")
        root.after(0, lambda: update_label("Task completed!"))

    def update_label(text):
        # label.config(text=text)
        pass

    def thepause():
        # messagebox.showinfo("Hello", "Hello, GUI!")
        global pause
        # print(f'{pause=}')
        pause = not pause
        print(f'{pause=}')

    def between_main(stop_event):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main(stop_event))
        loop.close()

    root = tk.Tk()
    root.title("Bumblebee")
    photo=PhotoImage(file='icon.ico')
    root.iconphoto(False,photo)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 300
    window_height = 200
    window_x = screen_width - window_width
    window_y = 0
    root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
    button = tk.Button(root, text="Start", command=on_button_click, width=10, height=2, bg='lightblue')
    button.pack(pady=(10,5))
    button = tk.Button(root, text="Pause", command=thepause, width=30, height=8, bg='lightblue')
    button.pack(pady=(10,20))
    label = tk.Label(root, text="Click the button to start a task.")
    label.pack(pady=20)
    root.protocol("WM_DELETE_WINDOW", on_close)
    threads = []
    root.mainloop()
