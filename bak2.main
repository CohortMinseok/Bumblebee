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
import cv2
import time
from math import log10, floor
from time import perf_counter
import numpy as np
import threading
from pynput import keyboard
from PIL import ImageGrab
from datetime import datetime
from game import Game
import asyncio
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import gdi_capture
from PIL import Image, ImageTk   
from configparser import ConfigParser

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
        for i in range(1):
            keydown('a')
            await sleep(.002)
            keyup('a')
            await sleep(.002)
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
            print(f'script resume ..')




if __name__ == "__main__":
    

    config = ConfigParser()
    config.read('config.ini')
    minimapX = int(config.get('main', 'minimapX'))
    minimapY = int(config.get('main', 'minimapY'))
    initial_line_position = float(config.get('main', 'initial_line_position'))
    initial_line_position2 = float(config.get('main', 'initial_line_position2'))
    initial_line_position3 = float(config.get('main', 'initial_line_position3'))
    print(f'{minimapX}, {minimapY}, {initial_line_position}, {initial_line_position2}, {initial_line_position3}')
    g = None

    
    def on_close():
        print("Closing the window")
        # Add your code here to run before closing the window
        # config.add_section('main')
        config.set('main', 'key1', 'value1')
        config.set('main', 'key2', 'value2')
        config.set('main', 'key3', 'value3')
        config.set('main', 'minimapX', str(minimapX))
        config.set('main', 'minimapY', str(minimapY))
        config.set('main', 'initial_line_position', str(line_position_slider.get()))
        config.set('main', 'initial_line_position2', str(line_position_slider2.get()))
        config.set('main', 'initial_line_position3', str(line_position_slider3.get()))
        with open('config.ini', 'w') as f:
            config.write(f)            
        for _, stop_event in threads:
            stop_event.set()
        for thread, _ in threads:
            thread.join()
        root.destroy()

    def on_button_click():
        stop_event = threading.Event()
        thread = threading.Thread(target=start_the_main, args=(stop_event,))
        thread.start()
        threads.append((thread, stop_event))
        # label.config(text="Working...")
        # root.after(0, lambda: update_label("Task completed!"))

    def update_label(text):
        # label.config(text=text)
        pass

    def thepause():
        # messagebox.showinfo("Hello", "Hello, GUI!")
        global pause
        # print(f'{pause=}')
        pause = not pause
        print(f'{pause=}')

    def start_the_main(stop_event):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main(stop_event))
        loop.close()

    def button_adjustminimap():    
        global minimapX    
        global minimapY
        global vertical_line
        global vertical_line2
        global vertical_line3
        global initial_line_position
        global canvas_width
        global canvas_height
        minimapX = int(entry1.get())
        minimapY = int(entry2.get())
        hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
        top, left, bottom, right = 8, 63, minimapX, minimapY
        with gdi_capture.CaptureWindow(hwnd) as img:            
            img_cropped = img[left:right, top:bottom]
            # height, width = img_cropped.shape[0], img_cropped.shape[1]
            img_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)
            img_cropped = Image.fromarray(img_cropped)
            tk_image = ImageTk.PhotoImage(img_cropped)
            # image_label.config(image=tk_image)
            # image_label.image = tk_image     
            canvas.delete("all")
            canvas.config(width=minimapX-8,height=minimapY-63)
            canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)        
            canvas.image = tk_image
            
            canvas_width=minimapX-8
            canvas_height=minimapY-63
            initial_line_position = canvas_width / 2

            vertical_line = canvas.create_line(initial_line_position, 2, initial_line_position, canvas_height, fill="red", width=2)
            line_position_slider.config(to=canvas_width, length=canvas_width)
            update_line_position(line_position_slider.get())
            
            vertical_line2 = canvas.create_line(initial_line_position, 2, initial_line_position, canvas_height, fill="yellow", width=2)
            line_position_slider2.config(to=canvas_width, length=canvas_width)
            update_line_position2(line_position_slider2.get())
            
            vertical_line3 = canvas.create_line(2, initial_line_position, canvas_height, initial_line_position, fill="lime", width=2)
            line_position_slider3.config(to=canvas_height, length=canvas_height*2)
            update_line_position3(line_position_slider3.get())


    def update_line_position(value):
        canvas.coords(vertical_line, float(value), 0, float(value), canvas_height)
    
    def update_line_position2(value):
        canvas.coords(vertical_line2, float(value), 0, float(value), canvas_height)

    def update_line_position3(value):
        canvas.coords(vertical_line3, 0, float(value), canvas_width, float(value))


    # def update_label(value):
    #     valuestr = f"Horizontal: {horizontal_slider.get()}, Vertical: {vertical_slider.get()}"
    #     label.config(text=valuestr)

    root = tk.Tk()
    root.title("Bumblebee")
    photo=PhotoImage(file='icon.ico')
    root.iconphoto(False,photo)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 600
    window_height = 800
    window_x = screen_width - window_width
    window_y = 0
    root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
    # button = tk.Button(root, text="Start", command=on_button_click, width=10, height=2, bg='lightblue')
    # button.pack(pady=(10,5))
    button = tk.Button(root, text="Pause", command=thepause, width=30, height=8, bg='lightblue')
    button.pack(pady=(10,20))
    # button = tk.Button(root, text="Adjust Minimap", command=button_adjustminimap, width=30, height=8, bg='lightblue')
    # button.pack(pady=(10,20))

    # image_label = tk.Label(root)
    # image_path = "minimap.PNG"
    # img = PhotoImage(file=image_path)
    # image_label.config(image=img)
    # image_label.image = img
    # image_label.pack(pady=20)    

    # # Horizontal Slider
    # horizontal_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=update_label)
    # horizontal_slider.pack(pady=10)
    # # Vertical Slider
    # vertical_slider = tk.Scale(root, from_=0, to=100, orient=tk.VERTICAL, command=update_label)
    # vertical_slider.pack(side=tk.LEFT, padx=10)
    # # Label to display slider values
    # label = tk.Label(root, text="Horizontal: 0, Vertical: 0")
    # label.pack(pady=10)
    # entry = tk.Entry(root, width=30)
    # entry.pack(pady=10)   

    frame = tk.Frame(root, bg='#ADD8E6')
    frame.pack(padx=0, pady=0)
    label1 = tk.Label(frame, text="x:", bg="#ADD8E6", fg="black")
    label1.grid(row=0, column=0, padx=(5,0), pady=0, sticky=tk.E)
    entry1 = tk.Entry(frame, width=10)
    entry1.grid(row=0, column=1, padx=(0,0), pady=(5,0))
    label2 = tk.Label(frame, text="y:", bg="#ADD8E6", fg="black")
    label2.grid(row=1, column=0, padx=(5,0), pady=0, sticky=tk.E)
    entry2 = tk.Entry(frame, width=10)
    entry2.grid(row=1, column=1, padx=(0,0), pady=0)
    button = tk.Button(frame, text="adjust minimap", command=button_adjustminimap)
    button.grid(row=2, column=0, pady=(2,4), padx=(5,0), columnspan=2)
    # result_label = tk.Label(frame, text="")
    # result_label.grid(row=0, column=1, rowspan=3, padx=10)
    image_path = "minimap.png"  # Replace with the actual path to your image
    img = PhotoImage(file=image_path)
    # image_label = tk.Label(frame, image=img)
    # image_label.image = img  # Keep a reference to the image to prevent it from being garbage collected
    # image_label.grid(row=0, column=2, rowspan=3, padx=5, pady=5)
    # canvas = tk.Canvas(frame, width=200, height=50, bg="#ADF8A6")
    canvas = tk.Canvas(frame, width=minimapX-8, height=minimapY-63, bg="#ADF8A6")
    canvas.grid(row=0, column=2, rowspan=3, padx=10)
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    
    hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
    top, left, bottom, right = 8, 63, minimapX, minimapY
    with gdi_capture.CaptureWindow(hwnd) as gdiimg:            
        # img_cropped = gdiimg[63:111, 8:333]
        img_cropped = gdiimg[left:right, top:bottom]
        img_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)
        img_cropped = Image.fromarray(img_cropped)
        tk_image = ImageTk.PhotoImage(img_cropped)
        # image_label.config(image=tk_image)
        # image_label.image = tk_image    
        canvas.delete("all")
        canvas.config(width=minimapX-8,height=minimapY-63) 
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)        
        canvas.image = tk_image 

    canvas_width=minimapX-8
    canvas_height=minimapY-63
    # initial_line_position = (minimapX-8) / 2

    vertical_line = canvas.create_line(initial_line_position, 0, initial_line_position, minimapY-63, fill="red", width=2)    
    slider_label = tk.Label(frame, text="left threshold:", bg="#ADD8E6")
    slider_label.grid(row=3, column=1, pady=5, padx=5)
    line_position_slider = tk.Scale(frame, from_=2, to=canvas_width, orient=tk.HORIZONTAL, length=canvas_width, resolution=1, command=update_line_position)
    line_position_slider.set(initial_line_position)
    line_position_slider.grid(row=3, column=2, pady=5, padx=5)
    
    vertical_line2 = canvas.create_line(initial_line_position2, 0, initial_line_position2, minimapY-63, fill="yellow", width=2)    
    slider_label2 = tk.Label(frame, text="right threshold:", bg="#ADD8E6")
    slider_label2.grid(row=4, column=1, pady=5, padx=5)
    line_position_slider2 = tk.Scale(frame, from_=2, to=canvas_width, orient=tk.HORIZONTAL, length=canvas_width, resolution=1, command=update_line_position2)
    line_position_slider2.set(initial_line_position2)
    line_position_slider2.grid(row=4, column=2, pady=5, padx=5)

    vertical_line3 = canvas.create_line(2, initial_line_position, canvas_height, initial_line_position, fill="lime", width=2)
    # vertical_line3 = canvas.create_line(initial_line_position3, 0, initial_line_position3, minimapY-63, fill="blue", width=2)    
    # slider_label3 = tk.Label(frame, text="rope connect:", bg="#ADD8E6")
    # slider_label3.grid(row=5, column=1, pady=5, padx=5)
    line_position_slider3 = tk.Scale(frame, from_=2, to=canvas_height, orient=tk.VERTICAL, length=canvas_height*2, resolution=1, command=update_line_position3)
    line_position_slider3.set(initial_line_position3)
    line_position_slider3.grid(row=0, column=3, rowspan=3, pady=5, padx=5)

    root.protocol("WM_DELETE_WINDOW", on_close)
    threads = []
    
    # start_the_main
    stop_event = threading.Event()
    thread = threading.Thread(target=start_the_main, args=(stop_event,))
    thread.start()
    threads.append((thread, stop_event))
    
    root.mainloop()


