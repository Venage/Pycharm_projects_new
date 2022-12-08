import pyautogui
import keyboard
from time import sleep
import pyautogui as pag

def enterance():
    pyautogui.leftClick(x=170, y=1050, interval=0.0, duration=0.0)
    sleep(2)
    keyboard.press("enter")
    sleep(3)
    pag.typewrite(['tab', 'enter'],0.1)
    pag.typewrite(['tab','tab', 'enter'],0.1)
    pag.typewrite(['tab','tab','tab','tab', 'enter'],0.1)

    sleep(3)
    pyautogui.leftClick(x=220, y=1050)
    sleep(1)
    keyboard.press("enter")

def exit():
    pyautogui.leftClick(x=1205, y=9, interval=0.0, duration=1)
    sleep(1)
    pyautogui.leftClick(x=170, y=1050, interval=0.0, duration=0.0)
    sleep(2)
    keyboard.press("enter")
    sleep(1)
    pyautogui.leftClick(x=170, y=1050, interval=0.0, duration=0.0)

if __name__ == '__main__':
    enterance()




