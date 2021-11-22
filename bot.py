import logging
import random
import pyowm
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import RegexHandler, Filters, CommandHandler, MessageHandler
cat = ["https://images.wallpaperscraft.ru/image/krasivyj_kotik_kot_morda_pushistyj_93328_1920x1080.jpg",
       "https://avatars.mds.yandex.net/get-pdb/34158/2f3c181f-f81c-49a1-8677-b852b5fadae4/orig",
       "http://www.like-a.ru/wp-content/uploads/2014/11/slide_332676_3307421_free1-600x682.jpg",
       "https://img4.goodfon.ru/wallpaper/nbig/7/da/kot-koshka-koteika-mordochka-vzgliad-portret-1.jpg",
       "https://hdoboi.kiev.ua/save.php?filename=userfiles/wallpapers_img/baseimg/thumbs/102-koshka-morda-hitrost-vzglyad.jpg",
       "http://wallpapers-image.ru/1680x1050/cats/wallpapers/cats-images-1680x1050-0.jpg"]
kart = ["https://avatars.mds.yandex.net/get-autoru-all/1666312/2d22bc71923cd1cabd3479aa24adffc4/1200x900",
        "https://avatars.mds.yandex.net/get-autoru-all/1344950/060b627f0a79c2d9f3415233f34c40e0/1200x900",
        "https://avatars.mds.yandex.net/get-autoru-all/1590696/3d542b6d599bc980e92d77f75d9667c7/1200x900",
        "https://avatars.mds.yandex.net/get-autoru-all/997630/d65145dd9b420785450959560bdde93c/1200x900",
        "https://avatars.mds.yandex.net/get-verba/787013/2a000001635d904e00dd9f390aab4c94eb59/cattouch",
        "https://avatars.mds.yandex.net/get-autoru-all/1016496/3fa2b2837b418ea598da653d6b20e3b2/1200x900",
        "https://avatars.mds.yandex.net/get-autoru-all/1701372/ab0dad9cffc5de489356393fbd3dbeff/1200x900",
        "https://avatars.mds.yandex.net/get-verba/1030388/2a0000016095f21199aeb28cd2c31ce14fac/cattouch",
        "https://avatars.mds.yandex.net/get-autoru-all/1612728/3f1d325e4b903dea2f1b2a21e90781a8/1200x900",
        "https://avatars.mds.yandex.net/get-verba/787013/2a000001609d165980a32bb7d16cbf73d76c/cattouch"]
url = ["https://auto.ru/cars/new/group/jaguar/xf/20715002/20753482/1085333092-bda8c9f4/",
       "https://auto.ru/cars/used/sale/hispano_suiza/k6/1075903347-6dead/",
       "https://auto.ru/cars/used/sale/ferrari/f12berlinetta/1085261394-fbbefb95/",
       "https://auto.ru/cars/new/group/rimac/c_two/21215745/0/?price_from=60000000&only_official=false&in_stock=ANY_STOCK",
       "https://auto.ru/cars/new/group/mercedes/c_klasse/21297117/21297854/?price_from=950000",
       "https://auto.ru/cars/new/group/ferrari/gtc4lusso/20754843/0/?price_from=30000000&only_official=false&in_stock=ANY_STOCK",
       "https://auto.ru/cars/used/sale/ferrari/laferrari/1071995708-3c46d/",
       "https://auto.ru/cars/new/group/aston_martin/db11/21294152/21525949/?price_from=2100000",
       "https://auto.ru/cars/used/sale/mercedes/sls_amg/1076249459-ffc8719d/?sort=price-desc",
       "https://auto.ru/cars/new/group/rolls_royce/wraith/20462758/0/?price_from=2000000&only_official=false&in_stock=ANY_STOCK"]
pzh = ["https://hdfon.ru/wp-content/uploads/hdfon.ru-449037673.jpg",
       "http://elitefon.ru/images/201504/elitefon.ru_39256.jpg",
       "https://avatars.mds.yandex.net/get-pdb/69339/aee62683-81f8-4684-b914-1742caafbd58/orig",
       "https://storge.pic2.me/c/1360x800/509/584c6ff31963b.jpg",
       "https://pbs.twimg.com/media/DPnZ2AnWkAAzWDx.jpg",
       "https://w-dog.ru/wallpapers/3/4/436036299520318.jpg"]
kosm = [
        "http://wallpapersfan.ru/wp-content/uploads/2018/02/oboi-kosmos-4k-galaktika.jpg",
        "https://img4.goodfon.ru/wallpaper/nbig/5/5c/galaktika-kosmos-zvezdy-1.jpg",
        "https://fotooboi.org.ua/images/product_images/info_images/fotooboi-kosmos-10399.jpg",
        "https://avatars.mds.yandex.net/get-pdb/34158/adde43ed-ed4b-4a3d-8482-03c92e9ceee9/orig",
        "https://www.business-class.su/uploads/news/516ef65e030c0290b64dc35f29b8597c.jpg",
        "https://images.wallpaperscraft.ru/image/kosmos_fon_siniy_tochki_73340_1920x1080.jpg"]
nazv = ["Jaguar XF II",
        "Hispano-Suiza K6",
        "Ferrari F12berlinetta F12tdf",
        "Rimac C Two 2018",
        "Mercedes-Benz C-klasse IV (W205)",
        "Ferrari GTC4Lusso 2016",
        "Ferrari LaFerrari",
        "Aston Martin DB11 I",
        "Mercedes-Benz SLS AMG GT",
        "Rolls-Royce Wraith 2013"]
facts=["Среднее облако весит порядка 500 тонн, столько же весят 80 слонов.",
       "Флот США содержит больше авианосцев, чем все флоты мира вместе взятые.",
       "В Канаде озер больше, чем в любой другой стране.",
       "Марокко — единственная в мире страна, где козы из-за нехватки травы взбираются на деревья и пасутся там целыми стадами, лакомясь плодами аргании, дерева из орехов которого изготавливают душистое масло.",
       "Жевательная резинка за десять минут уничтожает почти столько же бактерий, сколько и процедура чистки зубной нитью.",
       "Енот-полоскун так назван потому, что перед тем, как что-либо съесть, зверёк моет пищу. Если же поблизости нет воды, а есть хочется, то енот ограничивается тем, что делает несколько «моющих» движений.",
       "Мало кто знает историю возникновения помпона на шапке. Однако, он был придуман не просто так, а для того, чтобы защищать головы французским матросам. Все дело в том, что раньше при строении кораблей мало кого беспокоил комфорт, и потолки в помещениях корабля были очень низкие. И вот именно помпон предохранял голову матроса от случайного удара головой о потолок. Прошло еще немало времени с тех пор, да и потолки сейчас делают гораздо выше, однако до наших дней шапочки французских моряков украшают красные помпоны.",
       "В среднем в день мышцы фокусировки глаза двигаются около 100 000 раз. Это очень много. Для примера, чтобы совершить столько же движений мышцами ног нужно пройти пешком примерно 80 километров. "]

REQUEST_KWARGS={'proxy_url': 'http://142.93.34.45:3128/%27%7D'}
def create_log():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)


def set_updaters(dispatcher):
    # Старт
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    pict = RegexHandler('Картинки', pic)
    dispatcher.add_handler(pict)
    pez = RegexHandler('Пейзажи', pezh)
    dispatcher.add_handler(pez)
    kos = RegexHandler('Космос', kosmos)
    dispatcher.add_handler(kos)
    kot = RegexHandler('Котики', kotik)
    dispatcher.add_handler(kot)
    menu = RegexHandler("Назад в меню", start)
    dispatcher.add_handler(menu)
    car = RegexHandler("Машины", mash)
    dispatcher.add_handler(car)
    gen1 = RegexHandler('Генератор паролей', gen)
    dispatcher.add_handler(gen1)
    donate = RegexHandler('Донат в VK Coin', donat)
    dispatcher.add_handler(donate)
    pogoda = RegexHandler('Погода', w)
    dispatcher.add_handler(pogoda)
    fac = RegexHandler('Интересные факты', fact)
    dispatcher.add_handler(fac)

    location_handler = MessageHandler(Filters.location, weather)
    dispatcher.add_handler(location_handler)
    gener2 = MessageHandler(Filters.text, gen2)
    dispatcher.add_handler(gener2)



def main():
    create_log()
    updater = Updater(token= "780079984:AAFIhcpr_2Av6s2UROl61wsrtEMlvrM_SRc", request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher
    set_updaters(dispatcher)
    updater.start_polling()
def weather(bot, update):

    owm = pyowm.OWM('319480d9f647c5f3f5d8745cf1a575cb')
    observation = owm.weather_around_coords(update.message.location["latitude"],update.message.location["longitude"])
    print(observation)
    w = observation[0].get_weather()
    w.get_temperature('celsius')
    temp = w.get_temperature('celsius')
    text = f"Температура в данное время : {temp['temp']} ℃ "
    update.message.reply_text(text=text)


def start(bot, update):
    custom_keyboard = [["Картинки", "Машины"], ["Генератор паролей"],["Погода", "Интересные факты"], ["Донат в VK Coin"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    text = "Вы в главном меню"
    update.message.reply_text(text=text,
                              reply_markup=reply_markup)


def pic(bot, update):
    c = [["Пейзажи", "Космос", "Котики"],["Назад в меню"]]
    rm = ReplyKeyboardMarkup(c, resize_keyboard=True)
    update.message.reply_text(text="Выберите вариант", reply_markup=rm)


def pezh(bot, update):
    user_id = update.message.from_user.id
    bot.send_photo(user_id, pzh[random.randint(0,5)])


def kosmos(bot, update):
    user_id = update.message.from_user.id
    bot.send_photo(user_id, kosm[random.randint(0, 5)])


def kotik(bot, update):
    user_id = update.message.from_user.id
    bot.send_photo(user_id, cat[random.randint(0, 5)])


def mash(bot,update):
    o = random.randint(0,9)
    user_id = update.message.from_user.id
    bot.send_photo(user_id, kart[o])
    b1 = [[InlineKeyboardButton(text="Подробнее здесь)", url=url[o])]]
    kb = InlineKeyboardMarkup(b1)
    update.message.reply_text(text=nazv[o], reply_markup=kb)


def gen(bot, update):
    update.message.reply_text(text = "Введите количество символов в пароле")


def gen2(bot, update):
    kol = update.message.text
    if kol.isdigit() and int(kol) <= 200:
        pas = ''
        for x in range(int(kol)):
            pas = pas + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
        update.message.reply_text(text=pas)
    else:
        update.message.reply_text("Проверьте введенный текст и повторите попытку)")


def donat(bot, update):
    bot.send_photo(update.message.from_user.id,"https://pp.userapi.com/c855420/v855420054/1b59a/RYfRsE1vbU0.jpg")
    update.message.reply_text(text="Если хотите поддержать проект, пожертвуйте 💵VK Coin'ов💵 на этот вк vk.com/eugenekek.В будущем вас ждут новые фичи🔑, недоступные стандартным пользователям)")

def w(bot, update):
    update.message.reply_text("Чтобы узнать текущую температуру, отправьте свою геолокацию боту")
def fact(bot,update):
    rand = random.randint(0, 7)

    update.message.reply_text(facts[rand])
if __name__ == '__main__':
    main()

