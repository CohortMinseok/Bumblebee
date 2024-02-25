# import socket
# import pyautogui
# import signal
# import win32gui
# import win32api
# import win32con
from io import BytesIO
import requests
import json
# import os
import sys
# import uuid
import random
import cv2
import time
from math import log10, floor
from time import perf_counter
import numpy as np
import threading
from pynput import keyboard
# from PIL import ImageGrab
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
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from attack import refreshkeybind, goleftattack, gorightattack, goupattack, godownattack
from runesolver import runechecker, gotorune, enablerune, disablerune

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


async def main(stop_event, left1, right1, top1, btm1, g):
    
    print(f'bot has started ..')

    time.sleep(.01)
    left=left1/2+0
    right=right1/2+0
    top=top1/2-8
    btm=btm1/2-8


    runetimer0=0
    runetimer=0
    checkrune=True
    solverune=False
    now=0
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

            
            now = perf_counter()
            runetimer = now - runetimer0
            if runetimer > 600: # change to 600 when haste
            # if runetimer > 900: # change to 600 when haste
                checkrune = True
            if checkrune:
                solverune = runechecker(g)
            # print(f'{x=} {y=} {statuetimer=} {fountaintimer=}, {runetimer=}, {cctimer=}')
            print(f'{x=} {y=} {runetimer=} {solverune=}')

            if solverune:
                await gotorune(g)
                pass
            else:
                pass
        
        print(f'{x=}, {y=} | {left=}, {top=}, {right=}, {btm=} | {left1=}, {top1=}, {right1=}, {btm1=}')


        #
        #


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'{update.message}')
    # global chat_id
    # print(f'{chat_id =}')
    if update.message.chat.id == 5630992696:
        print(f'Access User ({update.message.chat.id}) in {message_type}: "{text}"')
        pass
    elif update.message.chat.id == 1125332211:
        print(f'Access User ({update.message.chat.id}) in {message_type}: "{text}"')
        pass
    else:
        print(f'Denied User ({update.message.chat.id}) in {message_type}: "{text}"')
        return
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    # if message_type == 'group':
    #     if BOT_USERNAME in text:
    #         new_text: str = text.replace(BOT_USERNAME, '').strip()
    #         response: str = handle_response(new_text)
    #     else:
    #         return
    # else:
    #     response: str = handle_response(text)    
    await update.message.reply_text('Hello! Thanks for chatting with me! I am a banana!')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

async def telegrammain(stop_event):
    print(f'Starting bot ..')
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start_command))
    # app.add_handler(CommandHandler('help', help_command))
    # app.add_handler(CommandHandler('custom', custom_command))
    # app.add_handler(MessageHandler(filters.TEXT, handle_message))
    application.add_error_handler(error)
    print(f'Polling ..')
    application.run_polling(poll_interval=3)
    ##
    ##    
    await application.initialize()
    await application.start()
    # await application.updater.start_{webhook, polling}()
    # Start other asyncio frameworks here
    # Add some logic that keeps the event loop running until you want to shutdown
    # Stop the other asyncio frameworks here
    await application.updater.stop()
    await application.stop()
    await application.shutdown()
    pass


async def start_command_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'{update.message}')
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    await update.message.reply_text('Hello! Thanks for chatting with me! I am a banana2!')


class TkinterBot:
    
    def __init__(self):

        self.config = ConfigParser()
        self.config.read('settings.ini')
        self.minimapX = int(self.config.get('main', 'minimapX'))
        self.minimapY = int(self.config.get('main', 'minimapY'))
        self.initial_line_position = float(self.config.get('main', 'initial_line_position'))
        self.initial_line_position2 = float(self.config.get('main', 'initial_line_position2'))
        self.initial_line_position3 = float(self.config.get('main', 'initial_line_position3'))
        self.initial_line_position4 = float(self.config.get('main', 'initial_line_position4'))
        self.ipaddress = self.config.get('main', 'ipaddress')
        self.g = Game((8, 63, self.minimapX, self.minimapY)) #   

        self.TOKEN = self.config.get('telegram', 'TOKEN')
        self.chat_id = self.config.get('telegram', 'chat_id')

        self.att = self.config.get('keybind', 'attack')
        self.jump = self.config.get('keybind', 'jump')
        self.teleport = self.config.get('keybind', 'teleport')
        self.ropeconnect = self.config.get('keybind', 'ropeconnect')
        self.npc = self.config.get('keybind', 'npc')

        self.application = None

        self.threads = []
        self.stop_event = threading.Event()
        self.pause = False
        self.telegram_keep_alive = True
        
        self.loop1 = asyncio.new_event_loop()
        self.loop2 = asyncio.new_event_loop()
        self.loop3 = asyncio.new_event_loop()
        self.thread1 = threading.Thread(target=self.run_thread1)
        self.thread2 = threading.Thread(target=self.run_thread2)
        self.thread3 = threading.Thread(target=self.run_thread3)

    def init_tkinter(self):        
        self.root = tk.Tk()
        self.root.title("Bumblebee")
        photo=PhotoImage(file='icon.ico')
        self.root.iconphoto(False,photo)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 600
        window_height = 800
        window_x = screen_width - window_width
        window_y = 0
        self.root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        # # background_image = tk.PhotoImage(file="bumblebee.gif")
        # background_image = Image.open("bumblebee.gif")
        # background_image = background_image.resize((window_width, window_height),  Image.Resampling.LANCZOS)
        # background_photo = ImageTk.PhotoImage(background_image)
        # background_label = tk.Label(root, image=background_photo)
        # background_label.place(relwidth=1, relheight=1)
        # background_label.image = background_photo
        print(f'setup_tab')
        self.setup_tab()
        print(f'setup_tab1')
        self.setup_tab1()
        print(f'setup_tab4')
        self.setup_tab4()
        # print(f'setup_tab5')
        # self.setup_tab5()
        print(f'setup_tab6')
        self.setup_tab6()
        print(f'setup_tabs_done')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # self.threads = []
        # self.stop_event = threading.Event()
        # self.thread = threading.Thread(target=self.start_the_main, args=(self.stop_event,))
        # self.thread.start()
        # self.threads.append((self.thread, self.stop_event))
        # self.thread2 = threading.Thread(target=self.start_the_main2, args=(self.stop_event,))
        # self.thread2.start()
        # self.threads.append((self.thread, self.stop_event), (self.thread2, self.stop_event))
        self.root.mainloop()
        

    async def async_function(self, thread_name, iterations):        
        self.application = Application.builder().token(self.TOKEN).build()
        # self.application.add_handler(CommandHandler('start', self.start_command))
        self.application.add_handler(CommandHandler('status', self.status_command))
        # app.add_handler(CommandHandler('help', help_command))
        # app.add_handler(CommandHandler('custom', custom_command))
        # app.add_handler(MessageHandler(filters.TEXT, handle_message))
        self.application.add_error_handler(self.error)
        async with self.application:
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            # self.root.mainloop() # press close and this line over
            # await asyncio.sleep(30)
            while self.telegram_keep_alive:
            # for i in range(iterations):
                print(f"{thread_name} - Iteration i")
                await asyncio.sleep(1)  # Simulating asynchronous work
            print(f'finished telegram_run1')
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            print(f'finished telegram_run2')
            
    async def async_function2(self, thread_name, iterations):
        self.init_tkinter()
        # for i in range(iterations):
        #     print(f"{thread_name} - Iteration {i}")
        #     await asyncio.sleep(1)  # Simulating asynchronous work

    def run_thread1(self):
        asyncio.set_event_loop(self.loop1)
        self.loop1.run_until_complete(self.async_function("Thread 1", 5))

    def run_thread2(self):
        asyncio.set_event_loop(self.loop2)
        self.loop2.run_until_complete(self.async_function2("Thread 2", 5))

    def run_thread3(self):
        asyncio.set_event_loop(self.loop3)
        self.loop3.run_until_complete(self.async_function3("Thread 3", 5))

    def start_threads(self):
        # Start both threads
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()

    def wait_for_threads(self):
        # Wait for both threads to finish
        self.thread1.join()
        self.thread2.join()
        self.thread3.join()

    async def async_function3(self, thread_name, iterations):
        print(f'bot has started ..')
        time.sleep(3.01)        
        left1=self.line_position_slider.get()
        right1=self.line_position_slider2.get()
        top1=self.line_position_slider3.get()
        btm1=self.line_position_slider4.get()
        left=self.line_position_slider.get()/2+0
        right=self.line_position_slider2.get()/2+0
        top=self.line_position_slider3.get()/2-8
        btm=self.line_position_slider4.get()/2-8
        runetimer0=0
        runetimer=0
        checkrune=True
        solverune=False
        now=0
        xynotfound=0        
        self.pause = True
        while True:
            if self.pause:
                print(f'script is paused .. click resume to resume. ')
                while self.pause:
                    # do nothing
                    time.sleep(1)
                    if self.stop_event.is_set():
                        return
                print(f'script resumed ..')
            #
            time.sleep(.411) # when testing ..
            # time.sleep(.011) # when real botting ..
            g_variable = self.g.get_player_location()
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
                
                now = perf_counter()
                runetimer = now - runetimer0
                if runetimer > 600: # change to 600 when haste
                # if runetimer > 900: # change to 600 when haste
                    checkrune = True
                if checkrune:
                    solverune = runechecker(self.g)
                # print(f'{x=} {y=} {statuetimer=} {fountaintimer=}, {runetimer=}, {cctimer=}')
                print(f'{x=} {y=} {runetimer=} {solverune=}')

                if solverune:
                    await gotorune(self.g)
                    pass
                else:
                    pass
            
            print(f'{x=}, {y=} | {left=}, {top=}, {right=}, {btm=} | {left1=}, {top1=}, {right1=}, {btm1=}')


    async def telegram_run(self):
        
        self.application = Application.builder().token(self.TOKEN).build()
        # self.application.add_handler(CommandHandler('start', start_command_class))
        self.application.add_handler(CommandHandler('start', self.start_command))
        # app.add_handler(CommandHandler('help', help_command))
        # app.add_handler(CommandHandler('custom', custom_command))
        # app.add_handler(MessageHandler(filters.TEXT, handle_message))
        self.application.add_error_handler(self.error)

        async with self.application:
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            # self.root.mainloop() # press close and this line over
            await asyncio.sleep(30)
            print(f'finished telegram_run1')
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            print(f'finished telegram_run2')
        
    def tkinter_run(self):
        self.root.mainloop()
    

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type
        text: str = update.message.text
        print(f'{update.message=}')
        print(f'{self.chat_id=}')
        print(f'{type(self.chat_id)=}')
        print(f'{type(update.message.chat.id)=}')
        if str(update.message.chat.id) == self.chat_id:
            print(f'Access User ({update.message.chat.id}) in {message_type}: "{text}"')
            pass
        else:
            print(f'Denied User ({update.message.chat.id}) in {message_type}: "{text}"')
            return
        print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')        
        print(f'telegramstatus')
        now = perf_counter()
        photo0 = self.g.get_screenshot()
        success, photo0_encoded = cv2.imencode('.png', photo0)
        photo0_bytes = photo0_encoded.tobytes()
        files = {'photo': photo0_bytes}
        payload = {
            'chat_id': self.chat_id,
            'caption': 'dummy photo'
        }
        # response = requests.post('https://api.telegram.org/bot'+self.TOKEN+'/sendPhoto', data=payload, files=files)
        # if response.status_code == 200:
        #     print(f'{perf_counter()-now =}')
        #     print(f"success {response.json().get('description')}")
        #     print(f"success {response.json()}")
        # else:
        #     print(f"Request failed with status code_: {response.status_code}")
        #     print(f"{response.json().get('description')}")
        # await update.message.reply_text('Hello! Thanks for chatting with me! I am a banana!')
        await update.message.reply_photo(photo0_bytes)
        print(f'{perf_counter()-now =}')

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type
        text: str = update.message.text
        print(f'{update.message}')
        # global chat_id
        # print(f'{chat_id =}')
        if update.message.chat.id == 5630992696:
            print(f'Access User ({update.message.chat.id}) in {message_type}: "{text}"')
            pass
        elif update.message.chat.id == 1125332211:
            print(f'Access User ({update.message.chat.id}) in {message_type}: "{text}"')
            pass
        else:
            print(f'Denied User ({update.message.chat.id}) in {message_type}: "{text}"')
            return
        print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
        # if message_type == 'group':
        #     if BOT_USERNAME in text:
        #         new_text: str = text.replace(BOT_USERNAME, '').strip()
        #         response: str = handle_response(new_text)
        #     else:
        #         return
        # else:
        #     response: str = handle_response(text)    
        await update.message.reply_text('Hello! Thanks for chatting with me! I am a banana!')

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f'Update {update} caused error {context.error}')


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

    def setup_tab(self):
        self.notebook = ttk.Notebook(self.root)
        # Create tabs (frames) to be added to the Notebook
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)
        self.tab5 = ttk.Frame(self.notebook)
        self.tab6 = ttk.Frame(self.notebook)
        # Add tabs to the Notebook
        self.notebook.add(self.tab1, text="Tab 1")
        self.notebook.add(self.tab2, text="Tab 2")
        self.notebook.add(self.tab3, text="Tab 3")
        self.notebook.add(self.tab4, text="Tab 4")
        self.notebook.add(self.tab5, text="Tab 5")
        self.notebook.add(self.tab6, text="Tab 6")
        # Bind the tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        # Pack the Notebook widget
        self.notebook.pack(expand=1, fill="both")
        # Add content to each tab
        label1 = tk.Label(self.tab1, text="Rectangular Rotation Method")
        label1.pack(padx=10, pady=10)
        label2 = tk.Label(self.tab2, text="Script Recording Method (Coming Soon .. )")
        label2.pack(padx=10, pady=10)
        label3 = tk.Label(self.tab3, text="Custom Map Rotation Design Method (Coming Soon ..)")
        label3.pack(padx=10, pady=10)
        label4 = tk.Label(self.tab4, text="Telegram Setup")
        label4.pack(padx=10, pady=10)
        label5 = tk.Label(self.tab5, text="Autoclicker (Monster Life)")
        label5.pack(padx=10, pady=10)
        label6 = tk.Label(self.tab6, text="Settings")
        label6.pack(padx=10, pady=10)

    def setup_tab1(self):
        self.button = tk.Button(self.tab1, text="Resume", command=self.resumebutton, width=20, height=5, bg='tomato', font=('Helvetica', 16))
        self.button.pack(pady=(10,20))
        frame = tk.Frame(self.tab1, bg='', bd=0)
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
        self.entry1 = Spinbox(frame, from_=100, to=400, font=("Helvetica", 16), width=5, increment=10)
        self.entry1.delete(0,tk.END)
        self.entry1.insert(0,self.minimapX)
        self.entry1.grid(row=0,column=0, padx=(0,0), pady=(0,0))
        self.entry2 = Spinbox(frame, from_=100, to=300, font=("Helvetica", 16), width=5, increment=10)
        self.entry2.delete(0,tk.END)
        self.entry2.insert(0,self.minimapY)
        self.entry2.grid(row=0,column=1, padx=(0,0), pady=(0,0))
        self.button2 = tk.Button(frame, text="adjust minimap", command=self.button_adjustminimap)
        self.button2.grid(row=0, column=2, padx=(1,0), pady=(0,1))
        image_path = "minimap.png"  # Replace with the actual path to your image
        img = PhotoImage(file=image_path)


        self.frame2 = tk.Frame(self.tab1, bg='orange', bd=0)
        self.frame2.pack(padx=0, pady=0)
        self.canvas = tk.Canvas(self.frame2, width=self.minimapX-8, height=self.minimapY-63, bg='#fabb29')
        self.canvas.grid(row=0, column=0, rowspan=1, padx=10, pady=(10,0))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        
        hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
        top, left, bottom, right = 8, 63, self.minimapX, self.minimapY
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
            self.canvas.delete("all")
            self.canvas.config(width=width,height=height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
            self.canvas.image = tk_image 

        self.canvas_width=width
        self.canvas_height=height
        # canvas_width=minimapX-8
        # canvas_height=minimapY-63

        self.vertical_line = self.canvas.create_line(self.initial_line_position, 0, self.initial_line_position, self.minimapY-63, fill="red", width=2)    
        # slider_label = tk.Label(frame, text="left threshold:", bg='#ffbb29')
        # slider_label.grid(row=3, column=1, pady=5, padx=5)
        self.line_position_slider = tk.Scale(self.frame2, from_=2, to=self.canvas_width, orient=tk.HORIZONTAL, length=self.canvas_width, resolution=1, command=self.update_line_position)
        self.line_position_slider.set(self.initial_line_position)
        self.line_position_slider.grid(row=1, column=0, pady=1, padx=1)
        
        self.vertical_line2 = self.canvas.create_line(self.initial_line_position2, 0, self.initial_line_position2, self.minimapY-63, fill="yellow", width=2)    
        # slider_label2 = tk.Label(frame, text="right threshold:", bg='#ffbb29')
        # slider_label2.grid(row=4, column=1, pady=5, padx=5)
        self.line_position_slider2 = tk.Scale(self.frame2, from_=2, to=self.canvas_width, orient=tk.HORIZONTAL, length=self.canvas_width, resolution=1, command=self.update_line_position2)
        self.line_position_slider2.set(self.initial_line_position2)
        self.line_position_slider2.grid(row=2, column=0, pady=(0,10), padx=1)

        self.vertical_line3 = self.canvas.create_line(2, self.initial_line_position, self.canvas_height, self.initial_line_position, fill="lime", width=2)
        self.line_position_slider3 = tk.Scale(self.frame2, from_=2, to=self.canvas_height, orient=tk.VERTICAL, length=self.canvas_height*2, resolution=1, command=self.update_line_position3)
        self.line_position_slider3.set(self.initial_line_position3)
        self.line_position_slider3.grid(row=0, column=1, rowspan=3, pady=(10,10), padx=(0,10))

        self.vertical_line4 = self.canvas.create_line(2, self.initial_line_position, self.canvas_height, self.initial_line_position, fill="lightblue", width=2)
        self.line_position_slider4 = tk.Scale(self.frame2, from_=2, to=self.canvas_height, orient=tk.VERTICAL, length=self.canvas_height*2, resolution=1, command=self.update_line_position4)
        self.line_position_slider4.set(self.initial_line_position4)
        self.line_position_slider4.grid(row=0, column=2, rowspan=3, pady=(10,10), padx=(0,10))

        
        self.frame3 = tk.Frame(self.tab1, bg='', bd=0)
        self.frame3.pack(padx=0, pady=0)  
        self.label_currentleft = tk.Label(self.frame3, text=f"current left: {self.line_position_slider.get()}")
        self.label_currentleft.grid(row=0, column=0, pady=0, padx=5)  
        self.label_currenttop = tk.Label(self.frame3, text=f"current top: {self.line_position_slider3.get()}")
        self.label_currenttop.grid(row=0, column=1, pady=0, padx=5)  
        self.label_currentright = tk.Label(self.frame3, text=f"current right: {self.line_position_slider2.get()}")
        self.label_currentright.grid(row=1, column=0, pady=0, padx=5)  
        self.label_currentbtm = tk.Label(self.frame3, text=f"current btm: {self.line_position_slider4.get()}")
        self.label_currentbtm.grid(row=1, column=1, pady=0, padx=5)  
        self.button3 = tk.Button(self.frame3, text="Reset", command=self.reset, width=10, height=2, bg='yellow', font=('Helvetica', 8))
        self.button3.grid(row=2, column=0, columnspan=2, pady=(10,10), padx=(20,20))


    def resumebutton(self):
        self.pause = not self.pause
        print(f'resumebutton pressed .. {self.pause}')
        if self.pause:
            self.button.config(text='Resume', bg='tomato')
            disablerune()
        else:
            self.button.config(text='Pause', bg='lime')
            enablerune()

    def button_adjustminimap(self):
        # global minimapX    
        # global minimapY
        # global vertical_line
        # global vertical_line2
        # global vertical_line3
        # global vertical_line4
        # global initial_line_position
        # global canvas_width
        # global canvas_height
        minimapX = int(self.entry1.get())
        minimapY = int(self.entry2.get())
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
            self.canvas.delete("all")
            self.canvas.config(width=width,height=height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)        
            self.canvas.image = tk_image
            
            self.canvas_width=width
            self.canvas_height=height
            # canvas_width=minimapX-8
            # canvas_height=minimapY-63
            initial_line_position = self.canvas_width / 2

            self.vertical_line = self.canvas.create_line(initial_line_position, 2, initial_line_position, self.canvas_height, fill="red", width=2)
            self.line_position_slider.config(to=self.canvas_width, length=self.canvas_width)
            self.update_line_position(self.line_position_slider.get())
            
            self.vertical_line2 = self.canvas.create_line(initial_line_position, 2, initial_line_position, self.canvas_height, fill="yellow", width=2)
            self.line_position_slider2.config(to=self.canvas_width, length=self.canvas_width)
            self.update_line_position2(self.line_position_slider2.get())
            
            self.vertical_line3 = self.canvas.create_line(2, initial_line_position, self.canvas_height, initial_line_position, fill="lime", width=2)
            self.line_position_slider3.config(to=self.canvas_height, length=self.canvas_height*2)
            self.update_line_position3(self.line_position_slider3.get())

            self.vertical_line4 = self.canvas.create_line(2, initial_line_position, self.canvas_height, initial_line_position, fill="lightblue", width=2)
            self.line_position_slider4.config(to=self.canvas_height, length=self.canvas_height*2)
            self.update_line_position4(self.line_position_slider4.get())
        
        # g = Game((8, 63, minimapX, minimapY)) # 
        
        # background_image = Image.open("bumblebee.gif")
        # background_image = background_image.resize((window_width, window_height),  Image.Resampling.LANCZOS)
        # background_photo = ImageTk.PhotoImage(background_image)
        # background_label = tk.Label(root, image=background_photo)
        # background_label.place(relwidth=1, relheight=1)
        # background_label.image = background_photo
        # root.configure(bg='orange')
        # frame2.config(bg='', bd=0)


    def update_line_position(self, value):
        self.canvas.coords(self.vertical_line, float(value), 0, float(value), self.canvas_height)
    
    def update_line_position2(self, value):
        self.canvas.coords(self.vertical_line2, float(value), 0, float(value), self.canvas_height)

    def update_line_position3(self, value):
        self.canvas.coords(self.vertical_line3, 0, float(value), self.canvas_width, float(value))
    
    def update_line_position4(self, value):
        self.canvas.coords(self.vertical_line4, 0, float(value), self.canvas_width, float(value))

    def reset(self):
        global pause
        pause=True
        # self.pause=True
        for _, stop_event in self.threads:
            stop_event.set()
        for thread, _ in self.threads:
            thread.join()
        stop_event = threading.Event()
        thread = threading.Thread(target=self.start_the_main, args=(stop_event,))
        thread.start()
        self.threads.append((thread, stop_event))
        self.label_currentleft.config(text=f"current left: {self.line_position_slider.get()}")
        self.label_currentright.config(text=f"current right: {self.line_position_slider2.get()}")
        self.label_currenttop.config(text=f"current top: {self.line_position_slider3.get()}")
        self.label_currentbtm.config(text=f"current btm: {self.line_position_slider4.get()}")
            
    def on_tab_change(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        print("Selected Tab:", selected_tab)

    def setup_tab4(self):
        # frametelegram = tk.Frame(tab4, bg='#a1b2c3', bd=0)
        self.frametelegram = tk.Frame(self.tab4, bg='#f1f2f3', bd=0)
        self.frametelegram.pack(padx=0, pady=0)
        self.labeltoken = tk.Label(self.frametelegram, anchor='w', justify='left', text="Token: ")
        self.labeltoken.grid(row=0, column=0, padx=1, pady=1, sticky='w')
        self.entrytoken = tk.Entry(self.frametelegram, width=50)
        self.entrytoken.insert(0, self.TOKEN)
        self.entrytoken.grid(row=0, column=1, padx=1, pady=1)
        self.labelchatid = tk.Label(self.frametelegram, anchor='w', justify='left', text="Chat ID: ")
        self.labelchatid.grid(row=1, column=0, padx=1, pady=1)
        self.labelchatid2 = tk.Label(self.frametelegram, anchor='w', justify='left', text=self.chat_id)
        self.labelchatid2.grid(row=1, column=1, padx=1, pady=1, sticky='w')
        message = ""
        buttondisabled=False
        if self.TOKEN != '0' and self.chat_id != '0':
            # message += f"Your bot token is: {TOKEN} \n Your telegram chat_id is {chat_id} \n Account is binded with this program. If you can't receive bot message, "
            message += f"Account is binded with this program. \nIf you can't receive bot message, \n"
            buttondisabled=True
        else:
            if self.TOKEN == '0':
                message += f"Bot TOKEN not found. \n"
            if self.chat_id == '0':
                message += f'Telegram account not binded. \n'
        message += "kindly rebind your account. \n1. Create your telegram bot at BotFather. \n2. Paste your telegram bot token here. \n3. Search your telegram bot name on telegram. \
            \n4. Type something in that telegram bot. \n5. Press bind button below. "
        self.labelmessage = tk.Label(self.frametelegram, anchor='w', justify='left', text=message)
        self.labelmessage.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
        self.labelmessage2 = tk.Label(self.frametelegram, anchor='w', justify='left', text="")
        self.labelmessage2.grid(row=3, column=0, columnspan=2, padx=1, pady=1)
        # framebutton = tk.Frame(frametelegram, bg='#e47ac3', bd=0)
        self.framebutton = tk.Frame(self.frametelegram, bg='#f1f2f3', bd=0)
        self.framebutton.grid(row=4, column=0, columnspan=2, pady=1)
        self.buttonbind = tk.Button(self.framebutton, text="bind", command=self.get_token, anchor='w')
        self.buttonbind.grid(row=0, column=0, pady=1, padx=1)
        self.buttonrebind = tk.Button(self.framebutton, text="rebind", command=self.rebind)
        self.buttonrebind.grid(row=0, column=1, pady=1, padx=1)
        if buttondisabled:
            self.buttonbind.config(state=tk.DISABLED)
        else:
            self.buttonrebind.config(state=tk.DISABLED)

        # stucked alert
        # white text alert
        # red dot alert
        # framecommands = tk.Frame(tab4, bg='#91a2b3', bd=0)
        self.framecommands = tk.Frame(self.tab4, bg='#f1f2f3', bd=0)
        self.framecommands.pack(padx=0, pady=(20,20))
        self.labelcommands = tk.Label(self.framecommands, text='below you can test each telegram bot command')
        self.labelcommands.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.buttonpause = tk.Button(self.framecommands, text="Pause", height=2, bg='#a1f2f3', command=self.telegrampause, state=tk.DISABLED)
        self.buttonpause.grid(row=1, column=0, pady=2, padx=2, sticky='nsew')
        self.buttontown = tk.Button(self.framecommands, text="Town", height=2, bg='#91f2f3', command=self.telegramtown, state=tk.DISABLED)
        self.buttontown.grid(row=1, column=1, pady=2, padx=2, sticky='nsew')
        self.buttonmessage = tk.Button(self.framecommands, text="Message", height=2, bg='#81f2f3', command=self.telegrammessage, state=tk.DISABLED)
        self.buttonmessage.grid(row=2, column=0, pady=2, padx=2, sticky='nsew')
        self.buttonstatus = tk.Button(self.framecommands, text="Status", height=2, bg='#71f2f3', command=self.telegramstatus)
        self.buttonstatus.grid(row=2, column=1, pady=2, padx=2, sticky='nsew')
        self.buttonstop = tk.Button(self.framecommands, text="Stop", height=2, bg='#61f2f3', command=self.telegramstop, state=tk.DISABLED)
        self.buttonstop.grid(row=3, column=0, pady=2, padx=2, sticky='nsew')
        self.buttonresume = tk.Button(self.framecommands, text="Resume", height=2, bg='#51f2f3', command=self.telegramresume, state=tk.DISABLED)
        self.buttonresume.grid(row=3, column=1, pady=2, padx=2, sticky='nsew')
        self.buttonenable = tk.Button(self.framecommands, text="Enable", height=2, bg='#41f2f3', command=self.telegramenable, state=tk.DISABLED)
        self.buttonenable.grid(row=4, column=0, pady=2, padx=2, sticky='nsew')
        self.buttondisable = tk.Button(self.framecommands, text="Disable", height=2, bg='#31f2f3', command=self.telegramdisable, state=tk.DISABLED)
        self.buttondisable.grid(row=4, column=1, pady=2, padx=2, sticky='nsew')
        self.buttoncc = tk.Button(self.framecommands, text="CC", height=2, bg='#21f2f3', command=self.telegramcc, state=tk.DISABLED)
        self.buttoncc.grid(row=5, column=0, pady=2, padx=2, sticky='nsew')
        self.buttonshutdown = tk.Button(self.framecommands, text="Shut Down", height=2, bg='#11f2f3', command=self.telegramshutdown, state=tk.DISABLED)
        self.buttonshutdown.grid(row=5, column=1, pady=2, padx=2, sticky='nsew')


    def setup_tab5(self):
        pass

    def setup_tab6(self):        
        self.framesettings = tk.Frame(self.tab6, bg='#f1f2f3', bd=0)
        self.framesettings.pack(padx=0, pady=0)
        self.labelipaddress = tk.Label(self.framesettings, anchor='w', justify='left', text="runesolver ip address: ")
        self.labelipaddress.grid(row=0, column=0, padx=1, pady=1, sticky='w')
        self.entryipaddress = tk.Entry(self.framesettings)
        self.entryipaddress.insert(0, self.ipaddress)
        self.entryipaddress.grid(row=0, column=1, padx=1, pady=1)
        self.labelatt = tk.Label(self.framesettings, anchor='w', justify='left', text="main att key: ")
        self.labelatt.grid(row=1, column=0, padx=1, pady=1, sticky='w')
        self.entryatt = tk.Entry(self.framesettings)
        self.entryatt.insert(0, self.att)
        self.entryatt.grid(row=1, column=1, padx=1, pady=1)
        self.labeljump = tk.Label(self.framesettings, anchor='w', justify='left', text="jump key: ")
        self.labeljump.grid(row=2, column=0, padx=1, pady=1, sticky='w')
        self.entryjump = tk.Entry(self.framesettings)
        self.entryjump.insert(0, self.jump)
        self.entryjump.grid(row=2, column=1, padx=1, pady=1)
        self.labelteleport = tk.Label(self.framesettings, anchor='w', justify='left', text="teleport key: ")
        self.labelteleport.grid(row=3, column=0, padx=1, pady=1, sticky='w')
        self.entryteleport = tk.Entry(self.framesettings)
        self.entryteleport.insert(0, self.teleport)
        self.entryteleport.grid(row=3, column=1, padx=1, pady=1)
        self.labelropeconnect = tk.Label(self.framesettings, anchor='w', justify='left', text="ropeconnect key: ")
        self.labelropeconnect.grid(row=4, column=0, padx=1, pady=1, sticky='w')
        self.entryropeconnect = tk.Entry(self.framesettings)
        self.entryropeconnect.insert(0, self.ropeconnect)
        self.entryropeconnect.grid(row=4, column=1, padx=1, pady=1)
        self.labelnpc = tk.Label(self.framesettings, anchor='w', justify='left', text="npc key: ")
        self.labelnpc.grid(row=5, column=0, padx=1, pady=1, sticky='w')
        self.entrynpc = tk.Entry(self.framesettings)
        self.entrynpc.insert(0, self.npc)
        self.entrynpc.grid(row=5, column=1, padx=1, pady=1)

        self.framesettings2 = tk.Frame(self.tab6, bg='#f1f2f3', bd=0)
        self.framesettings2.pack(padx=0, pady=(20,20))
        self.buttonsave = tk.Button(self.framesettings2, text="Save", command=self.settingssave, state=tk.NORMAL)
        self.buttonsave.grid(row=0, column=0, pady=2, padx=2, sticky='nsew')

    def settingssave(self):
        self.config.set('main', 'ipaddress', str(self.entryipaddress.get()))
        self.config.set('keybind', 'attack', str(self.entryatt.get()))
        self.config.set('keybind', 'jump', str(self.entryjump.get()))
        self.config.set('keybind', 'teleport', str(self.entryteleport.get()))
        self.config.set('keybind', 'ropeconnect', str(self.entryropeconnect.get()))
        self.config.set('keybind', 'npc', str(self.entrynpc.get()))
        with open('settings.ini', 'w') as f:
            self.config.write(f)
        refreshkeybind()

    def rebind(self):
        self.entrytoken.delete(0,tk.END)
        self.labelchatid2.config(text='')
        self.labelmessage.config(text='telegram bot resetted. \nkindly rebind your telegram bot. \n1. Create your telegram bot at BotFather. \n2. Paste your telegram bot token here. \n3. Search your telegram bot name on telegram. \
        \n4. Type something in that telegram bot. \n5. Press bind button below. ')
        self.buttonbind.config(state=tk.NORMAL)
        self.buttonrebind.config(state=tk.DISABLED)
    
    def get_token(self):
        token = self.entrytoken.get()
        print("Token:", token)
        if token == '0':
            return
        response = requests.get('https://api.telegram.org/bot'+token+'/getUpdates')
        if response.status_code == 200:
            # Parse and print the JSON content
            json_data = response.json()
            print(f'{json_data=}')
            # formated = json.dumps(json_data, indent=2)
            # print("Returned JSON:")
            # print(formated)
            if json_data['result']:
                chat_id = json_data['result'][0]['message']['chat']['id']
                print(f'{chat_id = }')
                # 6871179594:AAH6ZiIEPyfmGQhgGp1bsCy3PvhA42rtyfk
                img = self.g.get_screenshot()
                print(f'{type(img)}')
                payload = {
                    'chat_id': chat_id,
                    'photo': 'https://picsum.photos/200/300',
                    'caption': 'dummy photo'
                }
                response = requests.post('https://api.telegram.org/bot'+token+'/sendPhoto', data=payload)
                if response.status_code == 200:
                    msg = 'telegram bot binded with account successfully. \nnow you can use various functions available to your bot. \nstay safe. enjoy.'
                    self.labelchatid2.config(text=chat_id)
                    self.labelmessage.config(text=msg)
                    self.labelmessage2.config(text='')
                    self.buttonbind.config(state=tk.DISABLED)
                    self.buttonrebind.config(state=tk.NORMAL)
                else:
                    print(f"Request failed with status code_: {response.status_code}")
            else:
                msg = "type something or press /start in the telegram bot to start binding. "
                self.labelmessage2.config(text=msg)
                # labelmessage.grid(row=2, column=0, columnspan=2, padx=1, pady=1)
                print(f'type something or press /start in the telegram bot to start binding. ')
        else:
            print(f"Request failed with status code: {response.status_code}")


    def telegrampause(self):
        print(f'telegrampause')
        pass

    def telegramtown(self):
        print(f'telegramtown')
        pass

    def telegrammessage(self):
        print(f'telegrammessage')
        pass

    def telegramstatus(self):
        print(f'telegramstatus')        
        now = perf_counter()
        photo0 = self.g.get_screenshot()        
        # photo = g.get_screenshot_bytes()        
        # photo3 = Image.open('minimap.PNG')
        # photo2 = ''
        # with open('minimap.png', 'rb') as f:
        #     photo2 = f.read()
        # photo4 = cv2.imread('minimap.png')
        # success, photo4_encoded = cv2.imencode('.png', photo4)
        # photo4_bytes = photo4_encoded.tobytes()
        success, photo0_encoded = cv2.imencode('.png', photo0)
        photo0_bytes = photo0_encoded.tobytes()
        # print(f'{type(photo)=} {sys.getsizeof(photo)}')
        # print(f'{type(photo2)=}')
        # print(f'{type(photo3)=}')
        # print(f'{type(photo0)=}')
        # print(f'{photo0=}')
        # print(f'{type(photo4)=}')
        # print(f'{photo4=}')
        # print(f'{type(photo4_encoded)=}')
        # print(f'{type(photo4_bytes)=}')
        # print(f'telegrampause')
        # print(f'{photo=}')
        # print(f'{photo2=}')
        # photo_encode = photo.encode('utf-8')
        # photo2_encode = photo2.encode('utf-8')
        # binary_data = b'\x48\x65\x6C\x6C\x6F\x2C\x20\x57\x6F\x72\x6C\x64\x21'
        # with open('photo.bin', 'wb') as file:
        #     file.write(binary_data)
        # with open('photo2.txt', 'wb') as file:
        #     file.write(binary_data)
        # image2 = Image.open(BytesIO(photo2))
        # image2.show()
        # image = Image.open(BytesIO(photo))
        # image.show()
        # image0 = Image.fromarray(photo0)
        # image0.show()
        files = {'photo': photo0_bytes}
        payload = {
            'chat_id': self.chat_id,
            # 'photo': 'https://picsum.photos/200/300',
            'caption': 'dummy photo'
        }
        response = requests.post('https://api.telegram.org/bot'+self.TOKEN+'/sendPhoto', data=payload, files=files)
        # response = requests.post('https://api.telegram.org/bot'+TOKEN+'/sendPhoto', params=payload, files=files)
        if response.status_code == 200:
            print(f'{perf_counter()-now =}')
            print(f"success {response.json().get('description')}")
            print(f"success {response.json()}")
        else:
            print(f"Request failed with status code_: {response.status_code}")
            print(f"{response.json().get('description')}")
        pass

    def telegramstop(self):
        print(f'telegramstop')
        pass

    def telegramresume(self):
        print(f'telegramresume')
        pass

    def telegramenable(self):
        print(f'telegramenable')
        pass

    def telegramdisable(self):
        print(f'telegramdisable')
        pass

    def telegramcc(self):
        print(f'telegramcc')
        pass

    def telegramshutdown(self):
        print(f'telegramshutdown')
        pass




    
    def on_close(self):
        print("Closing the window")
        #
        self.pause=True
        # Add your code here to run before closing the window
        # config.add_section('main')
        self.config.set('main', 'key1', 'value1')
        self.config.set('main', 'key2', 'value2')
        self.config.set('main', 'key3', 'value3')
        self.config.set('main', 'minimapX', str(self.minimapX))
        self.config.set('main', 'minimapY', str(self.minimapY))
        self.config.set('main', 'initial_line_position', str(self.line_position_slider.get()))
        self.config.set('main', 'initial_line_position2', str(self.line_position_slider2.get()))
        self.config.set('main', 'initial_line_position3', str(self.line_position_slider3.get()))
        self.config.set('main', 'initial_line_position4', str(self.line_position_slider4.get()))
        with open('config.ini', 'w') as f:
            self.config.write(f)
        self.stop_event.set()
        # for _, stop_event in self.threads:
        #     stop_event.set()
        # for thread, _ in self.threads:
        #     thread.join()
        self.root.destroy()
        self.telegram_keep_alive = False



    # def on_button_click():
    #     stop_event = threading.Event()
    #     thread = threading.Thread(target=start_the_main, args=(stop_event,))
    #     thread.start()
    #     threads.append((thread, stop_event))


    # async def start_telegram():
    #     application = Application.builder().token(TOKEN).build()
    #     application.add_handler(CommandHandler('start', start_command))
    #     # app.add_handler(CommandHandler('help', help_command))
    #     # app.add_handler(CommandHandler('custom', custom_command))
    #     # app.add_handler(MessageHandler(filters.TEXT, handle_message))
    #     application.add_error_handler(error)
    #     async with application:
    #         await application.initialize() # inits bot, update, persistence
    #         await application.start()
    #         await application.updater.start_polling()
    

    # def start_the_main(stop_event):
    #     g = Game((8, 63, minimapX, minimapY)) # 
    #     loop = asyncio.new_event_loop()
    #     # loop = asyncio.get_event_loop()
    #     asyncio.set_event_loop(loop)
    #     # loop.create_task(start_telegram())
    #     # loop.run_until_complete(start_telegram())
    #     # loop.run_until_complete(main(

    #     loop.create_task(main(
    #         stop_event, 
    #         float(line_position_slider.get()), 
    #         float(line_position_slider2.get()), 
    #         float(line_position_slider3.get()), 
    #         float(line_position_slider4.get()), 
    #         g
    #     ))
    #     loop.run_forever()
    #     # await application.updater.stop()
    #     # await application.stop()
    #     # await application.shutdown()
    #     loop.close()

    # def entry_focus_in(event):
    #     if entry1.get()=="Enter x...":
    #         entry1.delete(0,'end')
    #         entry1.config(fg='Black')

    # def entry_focus_out(event):
    #     if entry1.get()=="":
    #         entry1.insert(0,'Enter x...')
    #         entry1.config(fg='gray')

    # def entry2_focus_in(event):
    #     if entry2.get()=="Enter y...":
    #         entry2.delete(0,'end')
    #         entry2.config(fg='Black')

    # def entry2_focus_out(event):
    #     if entry2.get()=="":
    #         entry2.insert(0,'Enter y...')
    #         entry2.config(fg='gray')





    

    # def start_the_main2(stop_event):
    #     # loop = asyncio.new_event_loop()
    #     loop = asyncio.get_event_loop()
    #     asyncio.set_event_loop(loop)
    #     loop.run_until_complete(telegrammain(
    #         stop_event,
    #     ))
    #     loop.create_task(telegrammain(stop_event))
    #     # loop.close()



async def main2():
    # mytkinter = TkinterBot()
    # await mytkinter.telegram_run()
    # asyncio.run(mytkinter.telegram_run())
    # mytkinter.tkinter_run()

    # TOKEN = '6871179594:AAH6ZiIEPyfmGQhgGp1bsCy3PvhA42rtyfk'
    # application = Application.builder().token(TOKEN).build()
    # application.add_handler(CommandHandler('start', start_command))
    # # app.add_handler(CommandHandler('help', help_command))
    # # app.add_handler(CommandHandler('custom', custom_command))
    # # app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # application.add_error_handler(error)    

    # Run application and other_application() within the same event loop
    # async with application:
    #     await application.initialize() # inits bot, update, persistence
    #     await application.start()
    #     await application.updater.start_polling()
    #     await asyncio.sleep(60)

    print('done!')


if __name__ == "__main__":    
    # loop = asyncio.get_event_loop()
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(main2())
    
    mytkinter = TkinterBot()
    # await mytkinter.telegram_run()
    # asyncio.run(mytkinter.telegram_run())    
    mytkinter.start_threads()
    mytkinter.wait_for_threads()
    # asyncio.run(main2())
    pass
