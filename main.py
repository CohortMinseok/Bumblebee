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
from tkinter import ttk
from tkinter import *
import gdi_capture
from PIL import Image, ImageTk
from configparser import ConfigParser
from attack import goleftattack, gorightattack, goupattack, godownattack

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


async def main(stop_event, left, right, top, btm, g):
    print(f'bot has started ..')
    time.sleep(.01)
    left=left/2+0
    right=right/2+0
    top=top/2-8
    btm=btm/2-8


    xynotfound=0
    global pause
    pause = True
    while True:
        if pause:
            print(f'script is paused .. click resume to resume. ')
            while pause:
                # do nothing
                time.sleep(1)
                if stop_event.is_set():
                    return
            print(f'script resumed ..')
        #
        time.sleep(.411) # when testing ..
        # time.sleep(.011) # when real botting ..
        g_variable = g.get_player_location()
        x, y = (None, None) if g_variable is None else g_variable
        if x == None or y == None:
            xynotfound+=1
            if xynotfound > 30:
                t = time.localtime()
                currenttime = time.strftime("%H:%M:%S", t)
                print(f'something is wrong .. character not found .. exiting .. {currenttime}')
                # stop_flag = True
                # randompicker_thread.join()
                return
            print(f'x==None, pass ..')
            time.sleep(.1)
            pass
        else:
            xynotfound=0
            if y > top and (y > btm-10 and y <= btm+5):
                if x > left+15:
                    await goleftattack()
                elif x < left-15:
                    await gorightattack()
                elif x >= left-15 and x <= left+15:
                    await goupattack()            
            elif y <= top+5 and y > top-10:
                if x < right-15:
                    await gorightattack()
                elif x > right+15:
                    await goleftattack()
                elif x >= right-15 and x <= right+15:
                    await godownattack()
            elif y > top and not (y > btm-10 and y <= btm+5):
                await godownattack()
            else:
                await godownattack()
        
        print(f'{x=}, {y=} | {left=}, {top=}, {right=} {btm=}')


        #
        #




if __name__ == "__main__":
    
    config = ConfigParser()
    config.read('config.ini')
    minimapX = int(config.get('main', 'minimapX'))
    minimapY = int(config.get('main', 'minimapY'))
    initial_line_position = float(config.get('main', 'initial_line_position'))
    initial_line_position2 = float(config.get('main', 'initial_line_position2'))
    initial_line_position3 = float(config.get('main', 'initial_line_position3'))
    initial_line_position4 = float(config.get('main', 'initial_line_position4'))
    print(f'{minimapX}, {minimapY}, {initial_line_position}, {initial_line_position2}, {initial_line_position3}, {initial_line_position4}')
    g = Game((8, 63, minimapX, minimapY)) # 

    
    def on_close():
        print("Closing the window")
        #
        global pause
        pause=True
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
        config.set('main', 'initial_line_position4', str(line_position_slider4.get()))
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

    def thepause():
        global pause
        pause = not pause
        if pause:
            button.config(text='Resume', bg='tomato')
        else:
            button.config(text='Pause', bg='lime')

    def start_the_main(stop_event):
        g = Game((8, 63, minimapX, minimapY)) # 
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main(
            stop_event, 
            float(line_position_slider.get()), 
            float(line_position_slider2.get()), 
            float(line_position_slider3.get()), 
            float(line_position_slider4.get()), 
            g
        ))
        loop.close()

    def entry_focus_in(event):
        if entry1.get()=="Enter x...":
            entry1.delete(0,'end')
            entry1.config(fg='Black')

    def entry_focus_out(event):
        if entry1.get()=="":
            entry1.insert(0,'Enter x...')
            entry1.config(fg='gray')

    def entry2_focus_in(event):
        if entry2.get()=="Enter y...":
            entry2.delete(0,'end')
            entry2.config(fg='Black')

    def entry2_focus_out(event):
        if entry2.get()=="":
            entry2.insert(0,'Enter y...')
            entry2.config(fg='gray')

    def button_adjustminimap():
        global minimapX    
        global minimapY
        global vertical_line
        global vertical_line2
        global vertical_line3
        global vertical_line4
        global initial_line_position
        global canvas_width
        global canvas_height
        minimapX = int(entry1.get())
        minimapY = int(entry2.get())
        if minimapX > 400:
            minimapX=400
        if minimapY > 300:
            minimapY=300
        if minimapX < 100:
            minimapX=100
        if minimapY < 100:
            minimapY=100
        hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
        top, left, bottom, right = 8, 63, minimapX, minimapY
        with gdi_capture.CaptureWindow(hwnd) as img:            
            img_cropped = img[left:right, top:bottom]
            height = (right-left)*2
            width = (bottom-top)*2
            img_cropped = cv2.resize(img_cropped, (width, height))
            img_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)
            img_cropped = Image.fromarray(img_cropped)
            tk_image = ImageTk.PhotoImage(img_cropped)
            canvas.delete("all")
            canvas.config(width=width,height=height)
            canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)        
            canvas.image = tk_image
            
            canvas_width=width
            canvas_height=height
            # canvas_width=minimapX-8
            # canvas_height=minimapY-63
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

            vertical_line4 = canvas.create_line(2, initial_line_position, canvas_height, initial_line_position, fill="lightblue", width=2)
            line_position_slider4.config(to=canvas_height, length=canvas_height*2)
            update_line_position4(line_position_slider4.get())
        
        g = Game((8, 63, minimapX, minimapY)) # 
        
        # background_image = Image.open("bumblebee.gif")
        # background_image = background_image.resize((window_width, window_height),  Image.Resampling.LANCZOS)
        # background_photo = ImageTk.PhotoImage(background_image)
        # background_label = tk.Label(root, image=background_photo)
        # background_label.place(relwidth=1, relheight=1)
        # background_label.image = background_photo
        # root.configure(bg='orange')
        # frame2.config(bg='', bd=0)


    def update_line_position(value):
        canvas.coords(vertical_line, float(value), 0, float(value), canvas_height)
    
    def update_line_position2(value):
        canvas.coords(vertical_line2, float(value), 0, float(value), canvas_height)

    def update_line_position3(value):
        canvas.coords(vertical_line3, 0, float(value), canvas_width, float(value))
    
    def update_line_position4(value):
        canvas.coords(vertical_line4, 0, float(value), canvas_width, float(value))

    def reset():        
        global pause
        pause=True
        for _, stop_event in threads:
            stop_event.set()
        for thread, _ in threads:
            thread.join()
        stop_event = threading.Event()
        thread = threading.Thread(target=start_the_main, args=(stop_event,))
        thread.start()
        threads.append((thread, stop_event))
        label_currentleft.config(text=f"current left: {line_position_slider.get()}")
        label_currentright.config(text=f"current right: {line_position_slider2.get()}")
        label_currenttop.config(text=f"current top: {line_position_slider3.get()}")
        label_currentbtm.config(text=f"current btm: {line_position_slider4.get()}")
            
    def on_tab_change(event):
        selected_tab = notebook.index(notebook.select())
        print("Selected Tab:", selected_tab)



    # root start
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
    # # background_image = tk.PhotoImage(file="bumblebee.gif")
    # background_image = Image.open("bumblebee.gif")
    # background_image = background_image.resize((window_width, window_height),  Image.Resampling.LANCZOS)
    # background_photo = ImageTk.PhotoImage(background_image)
    # background_label = tk.Label(root, image=background_photo)
    # background_label.place(relwidth=1, relheight=1)
    # background_label.image = background_photo
    
    # # very cool title bar
    # root.overrideredirect(True)  # Remove the title bar
    # # Create a frame for a custom title bar
    # title_bar = tk.Frame(root, bg="blue", height=30, relief="raised", bd=0)
    # title_bar.pack(fill="x")
    # # Create a custom font for title text
    # title_font = ("Helvetica", 14)
    # # Set the width and height of the button
    # button_width = 15
    # button_height = 3
    # # Choose a brighter green color
    # button_color = "lime"
    # # Create a button with the custom font, width, height, and color
    # button = tk.Button(title_bar, text="Click me!", command=on_button_click, font=title_font, width=button_width, height=button_height, bg=button_color)
    # button.pack(side="left", padx=10)
    # # Close button
    # close_button = tk.Button(title_bar, text="X", command=root.destroy, font=title_font, width=2, height=1, bg="red", relief="flat")
    # close_button.pack(side="right", padx=10)
    # # Make the window draggable
    # def start_drag(event):
    #     root.x = event.x
    #     root.y = event.y
    # def drag(event):
    #     deltax = event.x - root.x
    #     deltay = event.y - root.y
    #     x = root.winfo_x() + deltax
    #     y = root.winfo_y() + deltay
    #     root.geometry(f"+{x}+{y}")
    # title_bar.bind("<ButtonPress-1>", start_drag)
    # title_bar.bind("<B1-Motion>", drag)

    
    notebook = ttk.Notebook(root)
    # Create tabs (frames) to be added to the Notebook
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)
    tab4 = ttk.Frame(notebook)
    tab5 = ttk.Frame(notebook)
    tab6 = ttk.Frame(notebook)
    # Add tabs to the Notebook
    notebook.add(tab1, text="Tab 1")
    notebook.add(tab2, text="Tab 2")
    notebook.add(tab3, text="Tab 3")
    notebook.add(tab4, text="Tab 4")
    notebook.add(tab5, text="Tab 5")
    notebook.add(tab6, text="Tab 6")
    # Bind the tab change event
    notebook.bind("<<NotebookTabChanged>>", on_tab_change)
    # Pack the Notebook widget
    notebook.pack(expand=1, fill="both")
    # Add content to each tab
    label1 = tk.Label(tab1, text="Rectangular Rotation Method")
    label1.pack(padx=10, pady=10)
    label2 = tk.Label(tab2, text="Script Recording Method (Coming Soon .. )")
    label2.pack(padx=10, pady=10)
    label3 = tk.Label(tab3, text="Custom Map Rotation Design Method (Coming Soon ..)")
    label3.pack(padx=10, pady=10)
    label4 = tk.Label(tab4, text="Telegram Setup")
    label4.pack(padx=10, pady=10)
    label5 = tk.Label(tab5, text="Autoclicker (Monster Life)")
    label5.pack(padx=10, pady=10)
    label6 = tk.Label(tab6, text="Settings")
    label6.pack(padx=10, pady=10)


    button = tk.Button(tab1, text="Resume", command=thepause, width=20, height=5, bg='tomato', font=('Helvetica', 16))
    button.pack(pady=(10,20))

    frame = tk.Frame(tab1, bg='', bd=0)
    # frame = tk.Frame(root, bg='#ffbb29')
    frame.pack(padx=0, pady=0)
    # # label1 = tk.Label(frame, text="x:", fg="black", bg='#ffbb29')
    # # label1.grid(row=0, column=0, padx=(5,0), pady=0, sticky=tk.E)
    # entry1 = tk.Entry(frame, width=10, fg='Gray')
    # entry1.insert(0, 'Enter x...')
    # entry1.bind("<FocusIn>", entry_focus_in)
    # entry1.bind("<FocusOut>", entry_focus_out)
    # entry1.grid(row=0, column=0, padx=(0,1), pady=(0,1))
    # # label2 = tk.Label(frame, text="y:", fg="black", bg='#ffbb29')
    # # label2.grid(row=1, column=0, padx=(5,0), pady=0, sticky=tk.E)
    # entry2 = tk.Entry(frame, width=10, fg='Gray')
    # entry2.insert(0, 'Enter y...')
    # entry2.bind("<FocusIn>", entry2_focus_in)
    # entry2.bind("<FocusOut>", entry2_focus_out)
    # entry2.grid(row=0, column=1, padx=(1,0), pady=(0,1))
    entry1 = Spinbox(frame, from_=100, to=400, font=("Helvetica", 16), width=5, increment=10)
    entry1.delete(0,tk.END)
    entry1.insert(0,minimapX)
    entry1.grid(row=0,column=0, padx=(0,0), pady=(0,0))
    entry2 = Spinbox(frame, from_=100, to=300, font=("Helvetica", 16), width=5, increment=10)
    entry2.delete(0,tk.END)
    entry2.insert(0,minimapY)
    entry2.grid(row=0,column=1, padx=(0,0), pady=(0,0))
    button2 = tk.Button(frame, text="adjust minimap", command=button_adjustminimap)
    button2.grid(row=0, column=2, padx=(1,0), pady=(0,1))
    image_path = "minimap.png"  # Replace with the actual path to your image
    img = PhotoImage(file=image_path)


    frame2 = tk.Frame(tab1, bg='orange', bd=0)
    frame2.pack(padx=0, pady=0)
    canvas = tk.Canvas(frame2, width=minimapX-8, height=minimapY-63, bg='#fabb29')
    canvas.grid(row=0, column=0, rowspan=1, padx=10, pady=(10,0))
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    
    hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
    top, left, bottom, right = 8, 63, minimapX, minimapY
    with gdi_capture.CaptureWindow(hwnd) as gdiimg:
        img_cropped = gdiimg[left:right, top:bottom]
        img_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)
        height, width = img_cropped.shape[:2]
        width = width*2
        height = height*2
        # width = (right-left)*2
        # height = (bottom-top)*2
        img_cropped = cv2.resize(img_cropped, (width, height))
        img_cropped = Image.fromarray(img_cropped)
        tk_image = ImageTk.PhotoImage(img_cropped)
        canvas.delete("all")
        canvas.config(width=width,height=height)
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        canvas.image = tk_image 

    canvas_width=width
    canvas_height=height
    # canvas_width=minimapX-8
    # canvas_height=minimapY-63

    vertical_line = canvas.create_line(initial_line_position, 0, initial_line_position, minimapY-63, fill="red", width=2)    
    # slider_label = tk.Label(frame, text="left threshold:", bg='#ffbb29')
    # slider_label.grid(row=3, column=1, pady=5, padx=5)
    line_position_slider = tk.Scale(frame2, from_=2, to=canvas_width, orient=tk.HORIZONTAL, length=canvas_width, resolution=1, command=update_line_position)
    line_position_slider.set(initial_line_position)
    line_position_slider.grid(row=1, column=0, pady=1, padx=1)
    
    vertical_line2 = canvas.create_line(initial_line_position2, 0, initial_line_position2, minimapY-63, fill="yellow", width=2)    
    # slider_label2 = tk.Label(frame, text="right threshold:", bg='#ffbb29')
    # slider_label2.grid(row=4, column=1, pady=5, padx=5)
    line_position_slider2 = tk.Scale(frame2, from_=2, to=canvas_width, orient=tk.HORIZONTAL, length=canvas_width, resolution=1, command=update_line_position2)
    line_position_slider2.set(initial_line_position2)
    line_position_slider2.grid(row=2, column=0, pady=(0,10), padx=1)

    vertical_line3 = canvas.create_line(2, initial_line_position, canvas_height, initial_line_position, fill="lime", width=2)
    line_position_slider3 = tk.Scale(frame2, from_=2, to=canvas_height, orient=tk.VERTICAL, length=canvas_height*2, resolution=1, command=update_line_position3)
    line_position_slider3.set(initial_line_position3)
    line_position_slider3.grid(row=0, column=1, rowspan=3, pady=(10,10), padx=(0,10))

    vertical_line4 = canvas.create_line(2, initial_line_position, canvas_height, initial_line_position, fill="lightblue", width=2)
    line_position_slider4 = tk.Scale(frame2, from_=2, to=canvas_height, orient=tk.VERTICAL, length=canvas_height*2, resolution=1, command=update_line_position4)
    line_position_slider4.set(initial_line_position4)
    line_position_slider4.grid(row=0, column=2, rowspan=3, pady=(10,10), padx=(0,10))

    
    frame3 = tk.Frame(tab1, bg='', bd=0)
    frame3.pack(padx=0, pady=0)  
    label_currentleft = tk.Label(frame3, text=f"current left: {line_position_slider.get()}")
    label_currentleft.grid(row=0, column=0, pady=0, padx=5)  
    label_currenttop = tk.Label(frame3, text=f"current top: {line_position_slider3.get()}")
    label_currenttop.grid(row=0, column=1, pady=0, padx=5)  
    label_currentright = tk.Label(frame3, text=f"current right: {line_position_slider2.get()}")
    label_currentright.grid(row=1, column=0, pady=0, padx=5)  
    label_currentbtm = tk.Label(frame3, text=f"current btm: {line_position_slider4.get()}")
    label_currentbtm.grid(row=1, column=1, pady=0, padx=5)  
    button3 = tk.Button(frame3, text="Reset", command=reset, width=10, height=2, bg='yellow', font=('Helvetica', 8))
    button3.grid(row=2, column=0, columnspan=2, pady=(10,10), padx=(20,20))


    root.protocol("WM_DELETE_WINDOW", on_close)
    threads = []
    
    # start_the_main
    stop_event = threading.Event()
    thread = threading.Thread(target=start_the_main, args=(stop_event,))
    thread.start()
    threads.append((thread, stop_event))
    
    root.mainloop()


