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

# import mymodule
# from mymodule import *
import tkinter as tk
from tkinter import messagebox







async def main(stop_event):
    
    while True:
        time.sleep(1)
        print(f'running loop ..')
        if stop_event.is_set():
            return




if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())

    
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

    def themyvariable():
        # messagebox.showinfo("Hello", "Hello, GUI!")
        global myvariable
        print(f'{myvariable}')
        myvariable = not myvariable
        print(f'{myvariable}')

    def between_main(stop_event):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main(stop_event))
        loop.close()

    root = tk.Tk()
    root.title("Simple GUI")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 300
    window_height = 200
    window_x = screen_width - window_width
    window_y = 0
    root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
    button = tk.Button(root, text="Start", command=on_button_click, width=10, height=2, bg='lightblue')
    button.pack(pady=(10,5))
    button = tk.Button(root, text="F11", command=themyvariable, width=30, height=8, bg='lightblue')
    button.pack(pady=(10,20))
    # label = tk.Label(root, text="Click the button to start a task.")
    # label.pack(pady=20)
    root.protocol("WM_DELETE_WINDOW", on_close)
    threads = []
    root.mainloop()
