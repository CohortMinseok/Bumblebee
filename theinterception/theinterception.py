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
import asyncio
import trio
import threading


MOUSE_BUTTON_DELAY = 0.03
KEY_PRESS_DELAY = 0.025

try:
    interception = Interception()
    INTERCEPTION_INSTALLED = True
except Exception:
    INTERCEPTION_INSTALLED = False
print(f'{INTERCEPTION_INSTALLED = }')


async def sleep(dur):
    now = perf_counter()
    end = now + dur
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
    while perf_counter() < end:
        pass


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

async def main():
    time.sleep(1.5)
    while True:
        now = perf_counter()
        # await sleep(10.001)
        for i in range(1):
            for i in range(1):
                # keydown('a')
                await sleep(.002)
                # keyup('a')
                await sleep(.002)
            # keydown('enter')
            # await sleep(.002)
            # keyup('enter')
            # await sleep(.002)
        print(f'{perf_counter()-now:.14f}')
        print(f'timedotsleep 5 ..')
        time.sleep(5)

async def thetriosleep(delay):
    while True:
        now = perf_counter()
        await trio.sleep(delay)
        print(f'trio ..{perf_counter()-now:.14f}')
        time.sleep(1)
        print(f'sleep 1 ..')


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

if __name__ == "__main__":
    print(f'done ..')
    while False:
    # while True:
        # now = perf_counter()
        trio.run(thetriosleep,.001)
        # print(f'end ..{perf_counter()-now:.14f}')
        time.sleep(1)
        print(f'sleep 1 ..')
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    # main()


