from telegram.ext import Updater, CommandHandler
import logging
import requests
from bs4 import BeautifulSoup

token = "Telegram BOT Token"
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="'Che Notizie vuoi? (/P)ost ,(/A)nsa, (/S)ole 24 ore, (/V)aligia Blu'")

url_post = 'https://www.ilpost.it/bits/'
url_ansa = 'https://www.ansa.it/'
url_sole24ore = 'https://www.ilsole24ore.com/sez/italia'
url_vblu = 'https://www.valigiablu.it/'

def post_fun(update,context):
    response = requests.get(url_post)
    soup = BeautifulSoup(response.text, 'html.parser')
    news = soup.find(id='main')
    list_of_news = news.find_all(class_='entry-content')
    for n in list_of_news:
        test = n.find(class_='entry-title').get_text()
        link = n.find(class_='entry-title').find('a')['href']
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{test}  {link}")

def ansa_fun(update, context):
    response = requests.get(url_ansa)
    soup = BeautifulSoup(response.text, 'html.parser')
    news = soup.find(class_='span3 breaking-news')
    list_of_news = news.find_all('li')
    for n in list_of_news:
        test = n.find('a').text
        link = n.find('a')['href']
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{test}  https://www.ansa.it{link}")

def sole_fun(update,context):
    response = requests.get(url_sole24ore)
    soup = BeautifulSoup(response.text, 'html.parser')
    news = soup.find(class_='list-lined list-lined--sep')
    list_of_news = news.find_all(class_='list-lined-item')
    for n in list_of_news:
        test = n.find(class_='aprev-title').text
        link1 = n.find(class_='d-block')['href']
        link = f'https://www.ilsole24ore.com{link1}'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{test}  {link}")

def valig_fun(update,context):
    response = requests.get(url_vblu)
    soup = BeautifulSoup(response.text, 'html.parser')
    news = soup.find(class_='entry-content')
    list_of_news = news.find_all(class_='blog-post-text-zone col-12 col-lg-6')
    for n in list_of_news:
        test = n.find('h2').find('a').text
        link = n.find('h2').find('a')['href']
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"{test}  {link}")


start_handler = CommandHandler('start', start)
post = CommandHandler('P', post_fun)
ansa = CommandHandler('A', ansa_fun)
sole = CommandHandler('S', sole_fun)
valig = CommandHandler('V', valig_fun)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(post)
dispatcher.add_handler(ansa)
dispatcher.add_handler(sole)
dispatcher.add_handler(valig)

updater.start_polling()
