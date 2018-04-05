from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
import logging
import telegram
bot=telegram.Bot(token='455133823:AAGWek6_eef7hwv1jtVKkfaOYSUTRv5P8fw')
base='https://google.co.in/search?q='
flag=-1
mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}

#print(bot.get_me())
updater=Updater(bot=bot)
dispatcher=updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
def yolo(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text="Welcome to the world of Treasure,My mate")
def start(bot, update):
     bot.send_message(chat_id=update.message.chat_id, text="Hey Dude! What's up?")

def echo(bot, update):
    #bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    base='https://google.co.in/search?q='
    flag=-1
    mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
    search=update.message.text
    search=search.strip()
    search=search.replace(" ","+")
    url=base+search+'+song+lyrics'
    res=requests.get(url,headers=mozhdr)
    soup=BeautifulSoup(res.content,'html.parser')
    results=soup.find_all("h3",class_="r")
    urls=[]
    for each in results:
        result=each.find("a",href=True)
        res_url=result['href'].strip('/url?q=')
        res_url=res_url.split('&',1)[0]
        urls.append(res_url)
        #res=res_url.split('https://',1)[1]
        if('azlyrics' in res_url):
            #global flag
            flag=flag+1
            break
        elif('paadalvarigal' in res_url):
            flag=flag+2
            break
    if(flag==0):
        lyrics=requests.get(res_url,headers=mozhdr)
        ly=BeautifulSoup(lyrics.content,'html.parser')
        found=ly.find_all("b",limit=2)
        for each in found:
            bot.send_message(chat_id=update.message.chat_id,text=each.text)
        txt=ly.find("div",class_='col-xs-12 col-lg-8 text-center')
        try:
            bot.send_chat_action(chat_id=update.message.chat_id,action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=update.message.chat_id,text=txt.contents[16].text)

        except:
            bot.send_chat_action(chat_id=update.message.chat_id,action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=update.message.chat_id,text=txt.contents[19].text)
    elif(flag==1):
        lyrics=requests.get(res_url,headers=mozhdr)
        ly=BeautifulSoup(lyrics.content,'html.parser')
        txt=ly.find("div",class_='mh-content left')
        txt=txt.find_all("p")
        in1=0
        for each in txt:
            if(in1==0):
                bot.send_message(chat_id=update.message.chat_id,text=each.text)
                in1=1
            else:
                content=each.contents
                if(each.contents[0]!='Last Modified: '):
                    for li in content[::2]:
                        bot.send_message(chat_id=update.message.chat_id,text=li)
                        bot.send_chat_action(chat_id=update.message.chat_id,action=telegram.ChatAction.TYPING)
                else:
                    bot.send_message(chat_id=update.message.chat_id,text=each.text)
    else:
        bot.send_message(chat_id=update.message.chat_id,text="Oops! Lyrics not found. Try again using different keywords")
        bot.send_chat_action(chat_id=update.message.chat_id,action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=update.message.chat_id,text="Here are other alternatives:")
        text=''
        for each_url in urls:
             bot.send_message(chat_id=update.message.chat_id,text='<a href=\"'+each_url+'\">link</a>.',parse_mode=telegram.ParseMode.HTML)
                        #text=text+'<a href='+each_url+'></a>'+' '
        #bot.send_message(chat_id=update.message.chat_id,text=text,parse_mode=telegram.ParseMode.HTML)

def lyrics(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="Enter song name you want to search for")


yolo_handler = CommandHandler('yolo', yolo)
dispatcher.add_handler(yolo_handler)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
lyric_handler=CommandHandler('lyrics',lyrics)
updater.start_polling()
