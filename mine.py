from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
import qimage2ndarray as q2n
import win32gui
import sys
from PIL import Image
import time
import numpy as np
import pyautogui


def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    hist = sum(1 - (0 if l == r else float(abs(l-r))/max(l,r))for l, r in zip(lh, rh))/len(lh)
    return hist


def calc_similar(li, ri):
    calc_sim = hist_similar(li.histogram(), ri.histogram())
    return calc_sim


base_img = Image.open('base.png')
locs = [
    (275, 527), (275,793), (274, 1060),
    (494, 226), (503, 507), (503, 794), (504, 1080), (503, 1362),
    (733, 387), (751, 662), (755, 932), (733, 1205)
    ]
# hwnd = win32gui.FindWindow(None, 'Tale of Wuxia 1.0.3.2(1.0.3.2)')
hwnd = win32gui.FindWindow(None, 'Tale of Wuxia 1.0.3.2(1.0.3.2)')
print(hwnd)
app = QApplication(sys.argv)
screen = QApplication.primaryScreen()

while True:
    # hwnd = win32gui.FindWindow(None, 'Sublime Text')

    img = screen.grabWindow(hwnd).toImage()
    img = q2n.rgb_view(img)

    sims = []
    for loc in locs:
        x, y = loc
        crop = Image.fromarray(img[x+30:x+105, y+40:y+120], 'RGB')
        sim = calc_similar(base_img, crop)
        sims.append(sim)
    
    if np.max(sims) > 0.58:
        print(np.max(sims), np.min(sims), sims)
        idx = np.argmin(sims)
        x, y = locs[idx]
        pyautogui.moveTo(y + 80, x + 25 + 77)
        pyautogui.click()
        pyautogui.moveTo(100, 100)
        time.sleep(1)
        # print(np.argmin(sims))
        # img = Image.fromarray(img, 'RGB')
        # img.show()
    time.sleep(0.1)
