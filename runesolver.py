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
from initinterception import movetoandleftclick


hwnd = None
stoprune=False

def disablerune():
    global stoprune
    stoprune=True

def enablerune():
    global stoprune
    stoprune=False

async def sleep(dur):
    now = perf_counter()
    end = now + dur
    while perf_counter() < end:
        pass




class RuneSolver:
    
    def __init__(self):
        config = ConfigParser()
        config.read('config.ini')
        self.ipaddress = config.get('main', 'ipaddress')
        self.maplehwnd=None
        self.stoprune=False
        

    def set_maplehwnd(self, maplehwnd):
        self.maplehwnd = maplehwnd
        print(f'{self.maplehwnd}')


    def disablerune(self):
        self.stoprune=True

    def enablerune(self):
        self.stoprune=False


    def runechecker(self, g):
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

    async def gotopoloportal(self, g):    
        g_variable = g.get_polo_locations()
        x, y = (None, None) if g_variable is None else g_variable
        if x == None:
            print(f'x==None..continue..means..no..rune..')
            return  
        else:
            print(f'polo location: {x=} {y=}')
            purpdist = x+0
            lowdist = purpdist - 2
            highdist = purpdist + 2
            height = y + 1  # 

        # global stoprune
        prevhigh = 0
        prevhighcount = 0
        counter = 0
        lastdistance = 0
        lastheight = 0
        theI = 0
        while (True):
            if self.stoprune:
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

            print(f'going to polo portal?1 ..')
            if (x >= lowdist and x <= highdist):
                print(f'playerx: {x}, playery: {y}, height: {height}, {purpdist =}')
                # newly added
                if x >= purpdist-0.5 and x <=purpdist+0.5:
                    h1 = 4
                    if y >= height-h1 and y <= height+h1:
                        print('already at polo position')
                        # lockit()
                        r = random.randint(770, 920)
                        r /= 1000
                        await sleep(r)
                        print(f'pressing up ..')
                        # await npcp()
                        await upp()
                        r = random.randint(3, 11)
                        r /= 1000
                        await sleep(r)
                        # await npcr()
                        await upr()
                        print(f'done pressing up ..')
                        r = random.randint(300, 700)
                        r /= 1000
                        await sleep(r)
                        # await runesolver3()
                        result = await self.checkportaltype(g)
                        return result
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
                            if abs(y-height) < 15:
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
                            r = random.randint(1000, 1500)
                            r /= 1000
                            await sleep(r)
                        r = random.randint(500, 900)
                        r /= 1000
                        await sleep(r)
                else:
                    if x<purpdist:
                        await rightp()
                        await rightr()
                    elif x>purpdist:
                        await leftp()
                        await leftr()
            else:
                distance = x - purpdist
                theight = y - height
                print(f'distance: {distance}, {lastdistance}, {purpdist=}, {x=}, ')
                if lastdistance - distance == 0:
                    if lastheight - theight == 0:
                        counter += 1
                        if counter > 66:
                            await leftp()
                            await jumpp()
                            await jumpr()
                            await leftr()
                else:
                    counter = 0
                lastdistance = distance
                lastheight = theight
                if distance > 30 or distance < -30:
                    if distance > 30:
                        print('hey distance > 30', distance)
                        await leftjumpjumpattack()
                    if distance < -30:
                        await rightjumpjumpattack()
                elif distance > 0:
                    distances = int(distance * 100 / 2.0)
                    print(f'> 0 {distances}')
                    await leftp(distances-50, distances+50)
                    await leftr(100, 300)
                    print(f'height: {height}')
                    if height == 32:
                        time.sleep(.6)
                    pass
                elif distance < 0:
                    distances = int(abs(distance) * 100 / 2.0)
                    print(f'< 0 {distances}')
                    await rightp(distances-50, distances+50)
                    await rightr(100, 300)
                    if height == 32:
                        time.sleep(.6)
                    pass
                elif distance == 0:
                    pass

    async def gotorune(self, g):    
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
        # global stoprune
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
            if self.stoprune:
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
                    r = random.randint(770, 920)
                    r /= 1000
                    await sleep(r)
                    print(f'pressing npc ..')
                    await npcp(3,11)
                    # r = random.randint(3, 11)
                    # r /= 1000
                    # await sleep(r)
                    await npcr()
                    print(f'done pressing npc ..')
                    r = random.randint(1000, 1700)
                    r /= 1000
                    await sleep(r)
                    await self.runesolver3()
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
                        if abs(y-height<15):
                            await downjump()
                        else:
                            await downjumpv2()
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
                    if distance < -30:
                        # jumpjumpright()
                        # await adjustportalll(distance)
                        await rightjumpjumpattack()
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

    async def checkportaltype(self, g):
        # hwnd = win32gui.FindWindow(None, "MapleStory")
        position = win32gui.GetWindowRect(self.maplehwnd)
        x, y, w, h = position
        # check white dot
        whitedotcheckerlocations = g.white_dot_checker()
        if whitedotcheckerlocations is None:
            print(f'nowhiteportalyet')
            for i in range(3):
                await upp()
                await sleep(.05)
                await upr()
                await sleep(.1)
                whitedotcheckerlocations = g.white_dot_checker()
                if whitedotcheckerlocations is not None:
                    break
            if whitedotcheckerlocations is None:
                print(f'nowhiteportalintheend')
                return 'w'
        print(f'gotwhiteportalintheend')
        await movetoandleftclick(x+392,y+326)
        await sleep(.15)
        polo2checkerlocations = g.polo2_checker() # check if dialogue is polo portal or frito portal
        if polo2checkerlocations is not None: # if is polo portal
            print(f'{polo2checkerlocations=}')
            # press npc button once
            await npcp(1,11)
            await npcr()
            await sleep(.3)
            await movetoandleftclick(x+392,y+326)
            await sleep(.2)
            print(f'yes is polo portal, click dialogue')
            polo3checkerlocations = g.polo3_checker() # check if polo is flamewolf or hunting ground
            if polo3checkerlocations is not None:
                print(f'{polo3checkerlocations=}')
                # if is flamewolf, skip, end chat
                return 'f'
            else:
                # press enter or npc button, enter polo portal
                # check what type of hunting ground it is
                await npcp(1,11)
                await npcr()
                await sleep(.4)
                # await movetoandleftclick(x+392,y+326)
                await sleep(2.0)
                for i in range(50): # for testing
                    huntingmapcheckerlocations = g.hunting_map_checker() # check if is hidden street bounty hunt
                    if huntingmapcheckerlocations is not None:
                        print(f'{huntingmapcheckerlocations=}')
                        return 'b'
                    print(f'not b')
                    huntingmap2checkerlocations = g.hunting_map2_checker() # check if is hidden street guarding the castle wall
                    if huntingmap2checkerlocations is not None:
                        print(f'{huntingmap2checkerlocations=}')
                        return 'g'
                    print(f'not g')
                    huntingmap3checkerlocations = g.hunting_map3_checker() # check if is hidden street stormwing
                    if huntingmap3checkerlocations is not None:
                        print(f'{huntingmap3checkerlocations=}')
                        return 'd'
                    print(f'not d')
        else:
            print(f'no is not polo portal')
            polo4checkerlocations = g.polo4_checker() # check if portal is especia portal
            if polo4checkerlocations is not None: #
                print(f'yes is especia portal')
                print(f'{polo4checkerlocations=}')
                # press enter blah and go into especia map
                # spam npc until solve
                for i in range(2):
                    await npcp(1,11)
                    await npcr()
                    await sleep(.3)
                    await movetoandleftclick(x+392,y+326)
                    await sleep(.3)
                return 'e'
            else:
                print(f'no is not especia portal, means its frito, end chat. ')
                return 'r'


    async def runesolver3(self):
        now=perf_counter()
        print('solving rune2 ..')
        # hwnd = win32gui.FindWindow(None, "MapleStory")
        position = win32gui.GetWindowRect(self.maplehwnd)
        x, y, w, h = position
        runepos = (x+121, y+143, x+697, y+371)
        screenshot = ImageGrab.grab(runepos)
        # screenshot.show()
        # time.sleep(5)
        img = np.array(screenshot)
        sendjson = {
            'image': img.tolist()
        }
        link = 'http://'+self.ipaddress+':8001/'
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
        print(f'{perf_counter()-now=}')
