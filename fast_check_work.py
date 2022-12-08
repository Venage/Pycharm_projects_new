from test.clik import enterance,exit
from test.screen_shot import shot,shot_mail
from test.telegram import picture_send,status_send
from test.my_pictures import dif_pictures
from time import sleep

if __name__ == '__main__':
    enterance()
    sleep(10)
    shot()
    shot_mail()
    sleep(2)
    exit()
    sleep(2)
    picture_send()
    sleep(1)
    status_send(dif_pictures())

