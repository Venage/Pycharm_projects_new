from PIL import Image
from PIL import ImageChops
#from pyti import pyt_proj

pyt_test = 'C:/Users/kane6/PycharmProjects/proj_test/test/'
pyt_proj = 'C:/Users/kane6/PycharmProjects/proj_test/'

def dif_pictures():
    name1 = "shot_mail_test.png"
    name2 = "shot_mail_new.png"

    pyt1 = "".join([pyt_proj, name1])
    pyt2 = "".join([pyt_proj, name2])

    image_one = Image.open(pyt1)
    image_two = Image.open(pyt2)
    diff = ImageChops.difference(image_one, image_two)
    if diff.getbbox():
        status = "РАБОТА!"
    else:
        status = "Работы то нет =)"
    return(status)

if __name__ == '__main__':
    print(dif_pictures())
