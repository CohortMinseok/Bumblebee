# import interception
from interception import Interception

from _keycodes import KEYBOARD_MAPPING
# from . import _utils, exceptions
import _utils, exceptions
from strokes import KeyStroke, MouseStroke, Stroke
from _consts import (FilterKeyState, FilterMouseState, KeyState, MouseFlag,
                      MouseRolling, MouseState)
import time
from time import perf_counter
from time import perf_counter_ns
import asyncio
# import trio
import threading
import mymodule
from mymodule import *
import tkinter as tk
from tkinter import messagebox
import random

MOUSE_BUTTON_DELAY = 0.03
KEY_PRESS_DELAY = 0.025

try:
    interception = Interception()
    INTERCEPTION_INSTALLED = True
except Exception:
    INTERCEPTION_INSTALLED = False
print(f'{INTERCEPTION_INSTALLED = }')


async def sleep(time):
    mymodule.timerSleep2(time)


async def sleep2(dur):
    now = perf_counter()
    end = now + dur
    while perf_counter() < end:
        pass

    # if dur > 0.001:
    #     await asyncio.sleep(dur-0.001)
    # await asyncio.sleep(dur)
    # await asyncio.sleep(dur-0.001)
    # while True:
    #     now = perf_counter()
    #     await asyncio.sleep(dur)
    #     print(f'end ..{perf_counter()-now:.14f}')
    #     time.sleep(1)
    #     print(f'sleep 1 ..')
    # now = perf_counter()
    # while now < end:
    #     now = perf_counter()


# interception.capture_keyboard()
# interception.capture_mouse()


# interception.auto_capture_devices(keyboard=True, mouse=True)
# interception.auto_capture_devices(mouse=True)

# interception.move_to(960, 540)
# interception.move_relative(x, y)

# with interception.hold_key("shift"):
#     interception.press("a")

# interception.click(120, 160, button="right", delay=1)


def _get_keycode(key: str) -> int:
    try:
        return KEYBOARD_MAPPING[key]
    except KeyError:
        raise exceptions.UnknownKeyError(key)

key = 'a'
delay = 1


def keydown(key):
    keycode = _get_keycode(key)
    stroke = KeyStroke(keycode, KeyState.KEY_DOWN, 0)
    interception.send_key(stroke)
    # time.sleep(delay or KEY_PRESS_DELAY)
    # await sleep(delay)
    # await sleep(.011)


def keyup(key):
    keycode = _get_keycode(key)
    stroke = KeyStroke(keycode, KeyState.KEY_UP, 0)
    interception.send_key(stroke)
    # time.sleep(delay or KEY_PRESS_DELAY)
    # await sleep(delay)
    # await sleep(.011)

myvariable=False
stop_flag=False
async def main(stop_event):
    global myvariable
    time.sleep(1.5)
    
    now = perf_counter()  
    # test1
    while True:
    # while False:
        #
        for i in range(100):
            keydown(',')
            r = random.randint(31,131)
            r /= 1000
            await sleep(r)
            keyup(',')
            r = random.randint(31,131)
            r /= 1000
            await sleep(r)
            # send2('99')
            # send2('54')
            # send3('99')
            # send3('54')
            # send3('05')
            # ReleaseKey(0x39)
        #
        # hleftclick(x+400,y+450)
        # hleftclick(x+660,y+540)
        # await sleep(.200)
        # await enterp()
        # await sleep(.010)
        # await enterr()
        # await sleep(.110)
        # await enterp()
        # await sleep(.010)
        # await enterr()
        # await sleep(.110)
        # await enterp()
        # await sleep(.010)
        # await enterr()
        # await sleep(1.110)
        #
        # print(f'{g.get_player_location()}')
        # time.sleep(2)
        
        print(f'timedotsleep5 ..')
        time.sleep(.1)
        if perf_counter()-now > 360:
            myvariable = True
        if myvariable:
            print(f'{perf_counter()-now:.10f}')
            while (myvariable):
                now=perf_counter()
                time.sleep(2)
                print('playactions == blocked: (new feature: sleeping(2))')
                print('playactions == released: (new feature: sleeping(2))')
                if stop_event.is_set():
                    global stop_flag
                    stop_flag = True
                    return



def print_numbers(dur):
    now = perf_counter()
    end = now + dur
    while perf_counter() < end:
        # now = perf_counter()
        pass
    # await asyncio.sleep(.0001)
    # for i in range(5):
    #     time.sleep(1)  # Simulate some work
    #     print(f"Thread: {threading.current_thread().name}, Number: {i}")

my_thread = threading.Thread(target=print_numbers, args=(.0001,), name="MyThread")
now = perf_counter()
my_thread.start()
my_thread.join()
print(f'end ..{perf_counter()-now:.14f}')

import ctypes
from ctypes import wintypes
winmm = ctypes.WinDLL('winmm')
winmm.timeBeginPeriod(1)
print(dir(mymodule))
print(mymodule.add(1))
print(mymodule.PySomeClass(5))
m = mymodule.PySomeClass(5)

if __name__ == "__main__":    

    # print(f'done ..')
    # while False:
    # # while True:
    #     # now = perf_counter()
    #     trio.run(thetriosleep,.001)
    #     # print(f'end ..{perf_counter()-now:.14f}')
    #     time.sleep(1)
    #     print(f'sleep 1 ..')
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(main())
    # # main()

    
    
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



