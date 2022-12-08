import pyautogui

def shot():
    im1 = pyautogui.screenshot(region=(150,250, 700, 900))
    im1.save('my_screenshot.png')

def shot_mail():
    im1 = pyautogui.screenshot(region=(215,400, 140, 45))
    im1.save('shot_mail_new.png')

if __name__ == '__main__':
    shot()