import gdi_capture
import numpy as np
import cv2

# These are colors taken from the mini-map in BGRA format.
PLAYER_BGRA = (68, 221, 255, 255)
RUNE_BGRA = (255, 102, 221, 255)
ENEMY_BGRA = (0, 0, 255, 255)
GUILD_BGRA = (255, 102, 102, 255)
BUDDY_BGRA = (225, 221, 17, 255)

EB3BGR = (0, 34, 204, 255)
EBBGR = (238, 255, 255, 255)
LDBGR = (136, 51, 170, 255)
RDBGR = (0, 0, 255, 255)
GDBGR = (221, 170, 170, 255)
WDBGR = (255, 255, 255, 255)
DCBGR = (187, 221, 238, 255)
OKBGR = (17,187,170, 255) # broid die #normalpc
# OKBGR = (17,187,153, 255) # broid die 
# OKBGR = (0,187,170, 255) # died_ok [0 187 170] [0 204 153]
ORBGR = (1,136,245, 255) # orange_mushroom [1 136 245] [] #normalpc
LOBGR = (17,170,136, 255) # 
POBGR = (17,85,238, 255) # 
PO2BGR = (0,0,255, 255) # 


class Game:
    def __init__(self, region):
        self.hwnd = gdi_capture.find_window_from_executable_name("MapleStory.exe")
        # These values should represent pixel locations on the screen of the mini-map.
        self.top, self.left, self.bottom, self.right = region[0], region[1], region[2], region[3]
        # self.left, self.top, self.bottom, self.right = region[0], region[1], region[2], region[3]

    def get_rune_image(self):
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            if img is None:
                print("MapleStory.exe was not found.")
                return None
            return img.copy()

    def locate(self, *color):
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            locations = []
            if img is None:
                print("MapleStory.exe was not found.")
            else:
                # Crop the image to show only the mini-map.
                img_cropped = img[self.left:self.right, self.top:self.bottom]
                # img_cropped = img[self.top:self.bottom, self.left:self.right]
                height, width = img_cropped.shape[0], img_cropped.shape[1]
                # Reshape the image from 3-d to 2-d by row-major order.
                img_reshaped = np.reshape(img_cropped, ((width * height), 4), order="C")
                # cv2.imshow('img_reshaped', img_reshaped)
                # cv2.imshow('img_cropped', img_cropped)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                for c in color:
                    sum_x, sum_y, count = 0, 0, 0
                    # Find all index(s) of np.ndarray matching a specified BGRA tuple.
                    matches = np.where(np.all((img_reshaped == c), axis=1))[0]
                    for idx in matches:
                        # Calculate the original (x, y) position of each matching index.
                        sum_x += idx % width
                        sum_y += idx // width
                        count += 1
                    if count > 0:
                        x_pos = sum_x / count
                        y_pos = sum_y / count
                        locations.append((x_pos, y_pos))
            return locations

    def get_player_location(self):
        location = self.locate(PLAYER_BGRA)
        return location[0] if len(location) > 0 else None

    def get_rune_location(self):
        location = self.locate(RUNE_BGRA)
        return location[0] if len(location) > 0 else None

    def get_other_location(self):
        location = self.locate(ENEMY_BGRA, GUILD_BGRA, BUDDY_BGRA)
        return len(location) > 0

    def get_screenshot(self):
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            if img is None:
                print("MapleStory.exe was not found.")
                return None
            return img.copy()
    
    def get_screenshot_bytes(self):
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            if img is None:
                print("MapleStory.exe was not found.")
                return None
            print(f'{img.size=} {img.shape}')
            return img.copy().tobytes()

    def checker(self, *color, x=0,y=0,w=800,h=600):
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            locations = []
            if img is None:
                print("MapleStory.exe was not found.")
            else:
                # print(f'{img}')
                # print(f'{img.ndim}')
                # print(f'{img.shape[0]}')
                # print(f'{img.shape[1]}')
                # print(f'{img.shape[2]}')
                img_cropped = img[y:h, x:w]
                # img_cropped = img[0:600, 0:800]
                # print(f'{img_cropped.shape[0]}')
                # print(f'{img_cropped.shape[1]}')
                # print(f'{img_cropped.ndim}')
                # img_cropped = img[self.left:self.right, self.top:self.bottom]
                # print(f'{img_cropped[60:61][60:61]}')
                height, width = img_cropped.shape[0], img_cropped.shape[1]
                # Reshape the image from 3-d to 2-d by row-major order.
                img_reshaped = np.reshape(img_cropped, ((width * height), 4), order="C")
                for c in color:
                    sum_x, sum_y, count = 0, 0, 0
                    # Find all index(s) of np.ndarray matching a specified BGRA tuple.
                    matches = np.where(np.all((img_reshaped == c), axis=1))[0]
                    # print(f'{matches=}')
                    for idx in matches:
                        # Calculate the original (x, y) position of each matching index.
                        sum_x += idx % width
                        sum_y += idx // width
                        count += 1
                        # print(f'{sum_x=} {sum_y=} {count=}')
                        # print(f'{idx % width=} {idx // width=} {idx % height=} {idx // height=} {width=} {count=}')
                        # print(f'{idx % width=} {idx // width=} {width=} {count=}')
                    if count > 0:
                        x_pos = sum_x / count
                        y_pos = sum_y / count
                        locations.append((x_pos, y_pos))
            # print(f'{locations=}')
            return locations

    def died_checker(self):        
        location = self.checker(OKBGR, x=300,y=300,w=400,h=400)
        # location = self.checker(OKBGR, x=360,y=360,w=361,h=361)
        # location = self.checker(PLAYER_BGRA)
        return location[0] if len(location) > 0 else None

    def polo_checker(self):
        location = self.locate(POBGR)
        # location = self.checker(PLAYER_BGRA)
        return location[0] if len(location) > 0 else None

    def polo2_checker(self): # Polo or Frito
        location = self.checkertest(PO2BGR,x=200,y=253,w=201,h=254)
        # location = self.checker(PLAYER_BGRA)
        return location[0] if len(location) > 0 else None

    def polo3_checker(self): # Flamewolf portal
        location = self.checkertest(PO2BGR,x=172,y=233,w=173,h=234)
        # location = self.checker(PLAYER_BGRA)
        return location[0] if len(location) > 0 else None

    def polo4_checker(self): # Especia portal
        location = self.checkertest(PO2BGR,x=199,y=244,w=200,h=245)
        # location = self.checker(PLAYER_BGRA)
        return location[0] if len(location) > 0 else None

    def hunting_map_checker(self): # Hidden Street Bounty Hunt
        location = self.checkertest(WDBGR,x=85,y=9,w=86,h=10)
        # location = self.checker(PLAYER_BGRA)
        return location[0] if len(location) > 0 else None
    
    def hunting_map2_checker(self): # Hidden Street Guarding The Castle Wall
        location = self.checkertest(WDBGR,x=87,y=9,w=88,h=10)
        # location = self.checker(PLAYER_BGRA)
        return location[0] if len(location) > 0 else None


        
    def checkertest(self, *color, x,y,w,h):
        with gdi_capture.CaptureWindow(self.hwnd) as img:
            locations = []
            if img is None:
                print("MapleStory.exe was not found.")
            else:
                # print(f'{img}')
                # print(f'{img.ndim}')
                # print(f'{img.shape[0]}')
                # print(f'{img.shape[1]}')
                # print(f'{img.shape[2]}')
                img_cropped = img[y:h, x:w]
                # img_cropped = img[0:600, 0:800]
                # print(f'{img_cropped.shape[0]}')
                # print(f'{img_cropped.shape[1]}')
                # print(f'{img_cropped.ndim}')
                # img_cropped = img[self.left:self.right, self.top:self.bottom]
                height, width = img_cropped.shape[0], img_cropped.shape[1]
                # Reshape the image from 3-d to 2-d by row-major order.
                img_reshaped = np.reshape(img_cropped, ((width * height), 4), order="C")
                for c in color:
                    sum_x, sum_y, count = 0, 0, 0
                    # Find all index(s) of np.ndarray matching a specified BGRA tuple.
                    matches = np.where(np.all((img_reshaped == c), axis=1))[0]
                    # print(f'{matches=}')
                    for idx in matches:
                        # Calculate the original (x, y) position of each matching index.
                        sum_x += idx % width
                        sum_y += idx // width
                        count += 1
                        # print(f'{sum_x=} {sum_y=} {count=}')
                        # print(f'{idx % width=} {idx // width=} {idx % height=} {idx // height=} {width=} {count=}')
                        print(f'{idx % width=} {idx // width=} {width=} {count=}')
                    if count > 0:
                        x_pos = sum_x / count
                        y_pos = sum_y / count
                        locations.append((x_pos, y_pos))
            # print(f'{locations=}')
            return locations