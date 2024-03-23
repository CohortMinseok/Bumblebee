# import socket
# import pyautogui
# import signal
# import win32gui
# import win32api
# import win32con
# from io import BytesIO
# import requests
# import json
# import os
# import sys
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
# from tkinter import ttk
# from tkinter import *
# import gdi_capture
# from PIL import Image, ImageTk
# from configparser import ConfigParser
# from typing import Final
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from attack import refreshkeybind, goleftattack, gorightattack, goupattack, godownattack
# from runesolver import runechecker, gotorune, enablerune, disablerune, gotopoloportal

# from theinterception.interception import Interception
# from theinterception._keycodes import KEYBOARD_MAPPING
# import theinterception._utils as _utils
# import theinterception.exceptions as exceptions
# from theinterception.strokes import KeyStroke, MouseStroke, Stroke
# from theinterception._consts import (FilterKeyState, FilterMouseState, KeyState, MouseFlag,
#                       MouseRolling, MouseState)

from contextlib import contextmanager
import functools

def requires_driver(func):
    """Wraps any function that requires the interception driver to be installed
    such that, if it is not installed, a `DriverNotFoundError` is raised"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not INTERCEPTION_INSTALLED:
            raise exceptions.DriverNotFoundError
        return func(*args, **kwargs)

    return wrapper

from theinterception import Interception
from theinterception import KEYBOARD_MAPPING
from theinterception import _utils
from theinterception import exceptions
from theinterception import KeyStroke, MouseStroke, Stroke
from theinterception import (FilterKeyState, FilterMouseState, KeyState, MouseFlag,
                      MouseRolling, MouseState)
from theinterception.types import MouseButton

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
# auto_capture_devices2()


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

# extract from theinterception inputs.py
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

def _get_button_states(button: str, *, down: bool) -> int:
    try:
        states = MouseState.from_string(button)
        return states[not down]  # first state is down, second state is up
    except KeyError:
        raise exceptions.UnknownButtonError(button)

# button :class:`Literal["left", "right", "middle", "mouse4", "mouse5"] | str`:
def mousedown(button):    
    button_state = _get_button_states(button, down=True)
    stroke = MouseStroke(button_state, MouseFlag.MOUSE_MOVE_ABSOLUTE, 0, 0, 0, 0)
    interception.send_mouse(stroke)

def mouseup(button):    
    button_state = _get_button_states(button, down=False)
    stroke = MouseStroke(button_state, MouseFlag.MOUSE_MOVE_ABSOLUTE, 0, 0, 0, 0)
    interception.send_mouse(stroke)
    
from typing import Literal, Optional
MOUSE_BUTTON_DELAY = 0.03
def mouse_down(button: MouseButton, delay: Optional[float] = None) -> None:
    """Holds a mouse button down, will not be released automatically.

    If you want to hold a mouse button while performing an action, please use
    `hold_mouse`, which offers a context manager.
    """
    button_state = _get_button_states(button, down=True)
    stroke = MouseStroke(button_state, MouseFlag.MOUSE_MOVE_ABSOLUTE, 0, 0, 0, 0)
    interception.send_mouse(stroke)
    time.sleep(delay or MOUSE_BUTTON_DELAY)

def mouse_up(button: MouseButton, delay: Optional[float] = None) -> None:
    """Releases a mouse button."""
    button_state = _get_button_states(button, down=False)
    stroke = MouseStroke(button_state, MouseFlag.MOUSE_MOVE_ABSOLUTE, 0, 0, 0, 0)
    interception.send_mouse(stroke)
    time.sleep(delay or MOUSE_BUTTON_DELAY)

def move_to(x: int | tuple[int, int], y: Optional[int] = None) -> None:
    """Moves to a given absolute (x, y) location on the screen.

    The paramters can be passed as a tuple-like `(x, y)` coordinate or
    seperately as `x` and `y` coordinates, it will be parsed accordingly.

    Due to conversion to the coordinate system the interception driver
    uses, an offset of 1 pixel in either x or y axis may occur or not.

    ### Examples:
    ```py
    # passing x and y seperately, typical when manually calling the function
    interception.move_to(800, 1200)

    # passing a tuple-like coordinate, typical for dynamic operations.
    # simply avoids having to unpack the arguments.
    target_location = (1200, 300)
    interception.move_to(target_location)
    ```
    """
    x, y = _utils.normalize(x, y)
    x, y = _utils.to_interception_coordinate(x, y)

    stroke = MouseStroke(0, MouseFlag.MOUSE_MOVE_ABSOLUTE, 0, x, y, 0)
    interception.send_mouse(stroke)

def move_relative(x: int = 0, y: int = 0) -> None:
    """Moves relatively from the current cursor position by the given amounts.

    Due to conversion to the coordinate system the interception driver
    uses, an offset of 1 pixel in either x or y axis may occur or not.

    ### Example:
    ```py
    interception.mouse_position()
    >>> 300, 400

    # move the mouse by 100 pixels on the x-axis and 0 in y-axis
    interception.move_relative(100, 0)
    interception.mouse_position()
    >>> 400, 400
    """
    stroke = MouseStroke(0, MouseFlag.MOUSE_MOVE_RELATIVE, 0, x, y, 0)
    interception.send_mouse(stroke)

def click(
    x: Optional[int | tuple[int, int]] = None,
    y: Optional[int] = None,
    button: MouseButton | str = "left",
    clicks: int = 1,
    interval: int | float = 0.1,
    delay: int | float = 0.3,
) -> None:
    """Presses a mouse button at a specific location (if given).

    Parameters
    ----------
    button :class:`Literal["left", "right", "middle", "mouse4", "mouse5"] | str`:
        The button to click once moved to the location (if passed), default "left".

    clicks :class:`int`:
        The amount of mouse clicks to perform with the given button, default 1.

    interval :class:`int | float`:
        The interval between multiple clicks, only applies if clicks > 1, default 0.1.

    delay :class:`int | float`:
        The delay between moving and clicking, default 0.3.
    """
    if x is not None:
        move_to(x, y)
        time.sleep(delay)

    for _ in range(clicks):
        mouse_down(button)
        mouse_up(button)

        if clicks > 1:
            time.sleep(interval)

# decided against using functools.partial for left_click and right_click
# because it makes it less clear that the method attribute is a function
# and might be misunderstood. It also still allows changing the button
# argument afterall - just adds the correct default.
def left_click(clicks: int = 1, interval: int | float = 0.1) -> None:
    """Thin wrapper for the `click` function with the left mouse button."""
    click(button="left", clicks=clicks, interval=interval)

def right_click(clicks: int = 1, interval: int | float = 0.1) -> None:
    """Thin wrapper for the `click` function with the right mouse button."""
    click(button="right", clicks=clicks, interval=interval)

def mouse_position() -> tuple[int, int]:
    """Returns the current position of the cursor as `(x, y)` coordinate.

    This does nothing special like other conventional mouse position functions.
    """
    return _utils.get_cursor_pos()

@requires_driver
@contextmanager
def hold_mouse(button: MouseButton):
    """Holds a mouse button down while performing another action.

    ### Example:
    ```py
    with interception.hold_mouse("left"):
        interception.move_to(300, 300)
    """
    mouse_down(button=button)
    try:
        yield
    finally:
        mouse_up(button=button)

async def movetoandleftclick(x,y):
    # move_to(x,y)
    await custommoveto(x,y)
    time.sleep(.3)
    left_click()

async def custommoveto(targetx,targety):    
    print(f'moving mouse .. {targetx=}, {targety=} ')
    # while True:
    for i in range(1500):
        x,y = mouse_position()
        print(f'custom mouse test {i=} {x=},{y=}')
        # print(f'{x=},{y=}')
        if x >= targetx-3 and x <= targetx+3:
            if y>= targety-3 and y <= targety+3:
                break
        if targetx-x < 0:
            r = random.randint(1,5)
            move_relative(-r,0)
            r/=1000
            await sleep(r)
            # time.sleep(r)
        else:
            r = random.randint(1,5)
            move_relative(r,0)
            r/=1000
            await sleep(r)
            # time.sleep(r)
        if targety-y < 0:
            r = random.randint(1,5)
            move_relative(0,-r)
            r/=1000
            await sleep(r)
            # time.sleep(r)
        else:
            r = random.randint(1,5)
            move_relative(0,r)
            r/=1000
            await sleep(r)
            # time.sleep(r)
        # print(f'moved. ')
        # time.sleep(.5)
    print(f'moved finished. ')

    
async def initiate_move():
    for i in range(10):
        r = random.randint(1,5)
        move_relative(r,r)
        r/=1000
        await sleep(r)
    for i in range(10):
        r = random.randint(1,5)
        move_relative(-r,r)
        r/=1000
        await sleep(r)
    for i in range(10):
        r = random.randint(1,5)
        move_relative(-r,-r)
        r/=1000
        await sleep(r)
    for i in range(10):
        r = random.randint(1,5)
        move_relative(r,-r)
        r/=1000
        await sleep(r)