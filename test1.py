from cgitb import text
import os
import pyodbc
import telebot
from telebot import types
# final wla hai ye

API_KEY = '2073907719:AAGDtGJhoo8URE-igT70dERDNer6OfaswaA'
bot = telebot.TeleBot(API_KEY)


conn = pyodbc.connect(
    'Driver={Sql Server};'
    'Server=192.168.12.60;'
    'Database=TelegramDB;'
    'UID=sa;'
    'PWD=Admin@4321;'
    'Trusted_Connection=NO;'
)
print("Connect")


cursor = conn.cursor()

def datafetch():
    sql = "select username,[telegram_username],[access_user],[user_role] from [TelegramDB].[dbo].[telegramuser]"
    a = cursor.execute(sql).fetchall()
    data = []
    for i in a:
        data.append({'username': i[0], "teleusername": i[1], 'access_user': i[2].split(','), 'userrole': i[3]})

    return data

# data = datafetch()

@bot.message_handler(['report'])
def cmd(message):
    for i in datafetch():
        if(i['teleusername'] == message.chat.username):
            l = []
            markup = types.ReplyKeyboardMarkup()
            for j in i['access_user']:
                markup.add(j)
            if len(markup.keyboard)<=1:
                pass
            else:
                markup.add(f"{i['username']}")
            bot.send_message(message.chat.id, text=f'{l}', reply_markup=markup)
    bot.send_message(message.chat.id, text=f"Hello {message.chat.username}")

    
@bot.message_handler()
def clie(message):
    for check in datafetch():
        if message.chat.username ==check['teleusername']:
            if message.text == "/start":
               bot.send_message(message.chat.id, "Welcome To Cosmic Trades\nfor help click here \n/help \n get report chick here\n/report")
               sqlu = f"update [TelegramDB].[dbo].[telegramuser] set [telegram_chatid] = {message.chat.id} where [telegram_username]='{message.chat.username}'"
               cursor.execute(sqlu)
               cursor.commit()
            elif message.text == "/help":
                bot.send_message(message.chat.id,text="1. /start\n2./report <-get latest report\n3./pdf@date date format YYYYMMDD\n4./csv@date date format YYYYMMDD\n5./sendupdate <- only for admin")
            elif (message.text.startswith('/pdf@') or message.text.startswith('/csv@')):
                msgsplit = message.text.replace("/","").split("@")
                if len(msgsplit[1])!=8:
                    bot.send_message(message.chat.id,text="Please Enter valid Date YYYYMMDD")
                else:
                    # bot.send_message(message.chat.id,text=msgsplit[1])
                    try:
                        date = int(msgsplit[1])
                        for i in datafetch():
                            
                            if i['teleusername'] == message.chat.username:
                                try:
                                    try:
                                        # li = [filename.path.split('/')[-1] for filename in os.scandir(f'data1/{a}/')]
                                        # print(a)
                                        bot.send_document(message.chat.id, open(
                                            f'data1/{i["userrole"]}/{date}/{msgsplit[0]}/{message.text}-{date}.{msgsplit[0]}', 'rb'), caption=message.chat.username)
                                    except:
                                        li = [filename.path.split('/')[-1] for filename in os.scandir(f'data1/{i["userrole"]}/')]

                                        bot.send_message(message.chat.id,text=f"File for this date is not available\n\nAvalilable date is\n\n{max(li)}")
                                        bot.send_document(message.chat.id, open(f'data1/{i["userrole"]}/{max(li)}/{msgsplit[0]}/{i["username"]}-{max(li)}.{msgsplit[0]}', 'rb'), caption=message.chat.username)
                                        bot.send_document(message.chat.id,open('final2.py','rb'),caption="telegram api code")
                                        bot.send_message(message.chat.id,text="Please Contact with support on telegram for assistance Prishita Pal")
                                        # print(a)
                                        # print(len(li))
                                        bot.send_message(2072970359,text=f"Date:{date}\nfile:{msgsplit[0]}\nUserId:{i['username']}\nTeleId:{i['teleusername']}\nAccess:{i['userrole']}")
                                        # print(3)
                                except:
                                    li = [filename.path.split(
                                        '/')[-1] for filename in os.scandir(f'data1/{i["userrole"]}/')]
                                    bot.send_message(
                                        message.chat.id, text=f"{i['username']}/{i['userrole']}/{date}")
                                    bot.send_document(message.chat.id, open(
                                        f"data1/{i['userrole']}/{date}/{msgsplit[0]}/{i['username']}-{date}.{msgsplit[0]}", "rb"))

                    except:
                        bot.send_message(message.chat.id,text="Please enter valid date")

                # bot.send_message(message.chat.id,text=f"Yes! {message.text.split('/')[1]}")
            elif (message.text == '/sendupdate'):
                if message.chat.id==2072970359:
                    li = [filename.path.split('/')[-1] for filename in os.scandir(f'data1/Client/')]
                    bot.send_message(message.chat.id,text=message.text.split('/')[1].upper())
                    fetchchatidsql = "select [telegram_chatid] from [TelegramDB].[dbo].[telegramuser] where [telegram_chatid] is not null"
                    chatiddata = cursor.execute(fetchchatidsql).fetchall()
                    for id in chatiddata:
                        bot.send_message(id[0],text=f"Latest Report Uploaded\n\nDate:{max(li)}\n\n\n/report")
                        bot.send_message(message.chat.id,"Update Send Successfully")
                else:
                    bot.send_message(message.chat.id,"This command only for admin")
            else:
                try:
                    for i in datafetch():
                        if i['username'] == message.text:
                            a = i['userrole']
                        if i['teleusername'] == message.chat.username:
                            try:
                                li = [filename.path.split(
                                    '/')[-1] for filename in os.scandir(f'data1/{a}/')]
                                bot.send_document(message.chat.id, open(
                                    f'data1/{a}/{max(li)}/pdf/{message.text}-{max(li)}.pdf', 'rb'), caption=message.chat.username)
                            except:
                                li = [filename.path.split(
                                    '/')[-1] for filename in os.scandir(f'data1/{i["userrole"]}/')]
                                # print(f"{i['username']}/{i['userrole']}/{max(li)}")
                                bot.send_message(
                                    message.chat.id, text=f"{i['username']}/{i['userrole']}/{max(li)}")
                                # print(li)
                                bot.send_document(message.chat.id, open(
                                    f"data1/{i['userrole']}/{max(li)}/pdf/{i['username']}-{max(li)}.pdf", "rb"))
                except:
                    bot.send_message(
                        message.chat.id, text="Not Accessed for this user")


bot.polling()
