import telepot

chat_id = '528287360'
token = "5540951687:AAGUKKyw0sJmjc40DctPVn0xfwIsp1mJzEA"

def picture_send():
    bot = telepot.Bot(token)
    picture = open(r'C:\Users\kane6\PycharmProjects\proj_test\my_screenshot.png', 'rb')
    bot.sendPhoto(chat_id, picture)

def status_send(text):
    bot = telepot.Bot(token)
    bot.sendMessage(chat_id, text)


if __name__ == '__main__':
    picture_send()
    status_send()