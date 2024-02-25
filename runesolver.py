import random
from time import perf_counter
import time
import win32gui
from PIL import ImageGrab
import requests
import json
import numpy as np
from configparser import ConfigParser
from attack import npcp, npcr, leftp, leftr, rightp, rightr, jumpp, jumpr, leftjumpjumpattack, \
    rightjumpjumpattack, jumpupjumpattack, ropeconnectpr, downjumpv2, downjump, \
    upp, upr, downp, downr


async def sleep(dur):
    now = perf_counter()
    end = now + dur
    while perf_counter() < end:
        pass







config = ConfigParser()
config.read('config.ini')
ipaddress = config.get('main', 'ipaddress')


def runechecker(g):
    purplebgr = (255, 102, 221)
    purpdist = 0
    lowdist = 0
    highdist = 0
    height = 0
    g_variable = g.get_rune_location()
    x, y = (None, None) if g_variable is None else g_variable
    if x == None:
        return False
    else:
        print(f'x=={x}..means..got..rune..')
        # global allowed
        # allowed = False
        return True


stoprune=False
def disablerune():
    global stoprune
    stoprune=True

def enablerune():
    global stoprune
    stoprune=False

async def gotorune(g):    
    g_variable = g.get_rune_location()
    x, y = (None, None) if g_variable is None else g_variable
    if x == None:
        print(f'x==None..continue..means..no..rune..')
        return
        # purpdist = 0
        # lowdist = 0
        # highdist = 0
        # height = 0        
    else:
        print(f'rune location: {x=} {y=}')
        purpdist = x
        lowdist = x - 2
        highdist = x + 2
        height = y + 1  # LOL

    # global myvariable
    # global changechannel
    global stoprune
    prevhigh = 0
    prevhighcount = 0
    counter = 0
    lastdistance = 0
    lastheight = 0
    pressedleft = False
    pressedright = False
    theI = 0
    # await f5pr()
    # await f5pr()
    # await f5pr()
    # send5('00')
    while (True):
        # if changechannel or myvariable:
        #     print(f'roger ..')
        #     return
        if stoprune:
            return
        while (True):
            print(f'theI {theI}')
            theI += 1
            if theI > 50:
                print(f'theI return .. ')
                return
            r = random.randint(1, 4)
            r /= 1000
            await sleep(r)
            g_variable = g.get_player_location()
            x, y = (None, None) if g_variable is None else g_variable
            if x == None:
                print(f'x==None..continue..means..no..player..something blocking bruh ..f')
                r = random.randint(900, 1100)
                r /= 1000
                await sleep(r)
            else:
                break

        print(f'solving rune?1 ..')
        if (x >= lowdist and x <= highdist):
            # if pressedright:
            #     # ReleaseKey(0xcd)
            #     await send3('79')
            #     pressedright = False
            # if pressedleft:
            #     # ReleaseKey(0xcb)
            #     await send3('80')
            #     pressedleft = False
            print(f'playerx: {x}, playery: {y}, height: {height}, {purpdist =}')
            h1 = 3
            if y >= height-h1 and y <= height+h1:
                # pass
                print('already at rune position')
                # lockit()
                r = random.randint(170, 220)
                r /= 1000
                await sleep(r)
                await npcp()
                # udp_socket.sendto('304'.encode(FORMAT), server_address)
                r = random.randint(1, 31)
                r /= 1000
                await sleep(r)
                await npcr()
                # udp_socket.sendto('404'.encode(FORMAT), server_address)
                r = random.randint(1000, 1700)
                r /= 1000
                await sleep(r)
                await runesolver3()
                # runesolver(d)
                return
                # break
            else:
                if y == prevhigh:
                    prevhighcount += 1
                    if prevhighcount > 6:
                        await leftp()
                        await jumpp()
                        await jumpr()
                        await leftr()
                if abs(y - prevhigh) < 15:
                    yinyang=False
                prevhigh = y
                if y > height:
                    print(y)
                    print(height)
                    # limen2.ropeconnect()
                    # limen2.upjumpshift()
                    # upjump()
                    if abs(y-height) < 15:
                        # await smoljump()
                        await jumpupjumpattack()
                    else:
                        await ropeconnectpr()
                    r = random.randint(1000, 1700)
                    r /= 1000
                    await sleep(r)
                else:
                    print(y)
                    print(height)
                    # if weird:
                    if abs(y-height<15):
                        await downjump()
                    else:
                        await downjumpv2()
                            # if yinyang:
                            #     await yinyangp()
                            #     await yinyangr()
                    # else:
                    #     await downjump()
                    # limen2.downjump()
                    # yinyangp()
                    # yinyangr(111,555)
                    r = random.randint(1000, 1500)
                    r /= 1000
                    await sleep(r)
                r = random.randint(500, 900)
                r /= 1000
                await sleep(r)
        else:
            distance = x - purpdist
            theight = y - height
            print(f'distance: {distance}, {lastdistance}, {purpdist=}, {x=}, ')
            if lastdistance - distance == 0:
                if lastheight - theight == 0:
                    counter += 1
                    # yinyangpr()
                    if counter > 66:
                        await leftp()
                        await jumpp()
                        await jumpr()
                        await leftr()
            else:
                counter = 0
            lastdistance = distance
            lastheight = theight
            # if myvariable:
            #     print('system_paused..')
            #     os.system("pause")
            if distance > 30 or distance < -30:
                if distance > 30:
                    print('hey distance > 30', distance)
                    # jumpjumpleft()
                    # await adjustportalll(distance)
                    await leftjumpjumpattack()
                    # await chainlightningleftshift()
                    # limen2.jumpjumpleft()
                if distance < -30:
                    # jumpjumpright()
                    # await adjustportalll(distance)
                    await rightjumpjumpattack()
                    # await chainlightningrightshift()
                    # limen2.jumpjumpright()
            elif distance > 0:
                # if pressedright:
                #     send3('79')
                #     pressedright = False
                # if not pressedleft:
                #     send2('80') #
                #     pressedleft = True
                distances = int(distance * 100 / 2.0)
                print(f'> 0 {distances}')
                await leftp(distances-50, distances+50)
                await leftr(100, 300)
                print(f'height: {height}')
                if height == 32:
                    time.sleep(.6)
                pass
            elif distance < 0:
                # if pressedleft:
                #     send3('80')
                #     pressedleft = False
                # if not pressedright:
                #     send2('79') #
                #     pressedright = True
                distances = int(abs(distance) * 100 / 2.0)
                print(f'< 0 {distances}')
                await rightp(distances-50, distances+50)
                await rightr(100, 300)
                if height == 32:
                    time.sleep(.6)
                pass
            elif distance == 0:
                pass
                # if pressedright:
                #     send3('79')
                #     pressedright = False
                # if pressedleft:
                #     send3('80')
                #     pressedleft = False
                # if y != height:
                #     if y > height:
                #         # limen2.ropeconnect()
                #         # limen2.upjumpshift()
                #         await upjumpshift()
                #         r = random.randint(1000, 1700)
                #         r /= 1000
                #         await sleep(r)
                #     else:
                #         # limen2.downjump()
                #         await downjump()
                #         await yinyangp()
                #         await yinyangr(111, 555)
                #         r = random.randint(2000, 2500)
                #         r /= 1000
                #         await sleep(r)
                #     r = random.randint(500, 900)
                #     r /= 1000
                #     await sleep(r)


async def runesolver3():
    print('solving rune2 ..')
    hwnd = win32gui.FindWindow(None, "MapleStory")
    position = win32gui.GetWindowRect(hwnd)
    x, y, w, h = position
    runepos = (x+121, y+143, x+697, y+371)
    screenshot = ImageGrab.grab(runepos)
    # screenshot.show()
    # time.sleep(5)
    img = np.array(screenshot)
    sendjson = {
        'image': img.tolist()
    }
    # link = 'http://'+POINT17+':8001/'
    link = 'http://'+ipaddress+':8001/'
    # link = 'http://'+'192.168.0.17'+':8001/'
    # link = 'http://'+'127.0.0.1'+':8001/'
    link = link + 'predict'
    r = requests.post(url=link, json=sendjson)
    json_data = json.loads(r.text)
    print(json_data['prediction'])
    sms = json_data['prediction']
    # print(f"{sms}")
    for i in range(len(sms)):
        print(sms[i:i+1])
        # PressKey(captchadict[sms[i:i+1]])
        if sms[i:i+1] == 'u':
            print('up')
            await upp(1,11)
            await upr(31,131)
        if sms[i:i+1] == 'd':
            print('down')
            await downp(1,11)
            await downr(31,131)
        if sms[i:i+1] == 'l':
            print('left')
            await leftp(1,11)
            await leftr(31,131)
        if sms[i:i+1] == 'r':
            print('right')
            await rightp(1,11)
            await rightr(31,131)
        time.sleep(0.001)
