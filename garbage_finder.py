from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import RegexHandler, Filters, CommandHandler, MessageHandler, ConversationHandler
import sqlite3

FIRST = range(1)


def set_updaters(dispatcher):
    # Старт
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(MessageHandler(Filters.regex(r"Нaшел мусoр"), found))
    dispatcher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("Пoдaть зaявку на рабoту"), apply)],
        states={FIRST: [MessageHandler(Filters.text, apply_2)]}, fallbacks=[]
    ))


def main():
    updater = Updater(token="2104502859:AAFiVZVGhIKxySHlXsGs1RgxUN0YsdlPd-4", use_context=True)
    dispatcher = updater.dispatcher
    set_updaters(dispatcher)
    updater.start_polling()


def start(update, context):
    ck = [["Нaшел мусoр"], ["Пoдaть зaявку на рабoту"]]
    reply_markup = ReplyKeyboardMarkup(ck)
    update.message.reply_text(text="Вы в главном меню", reply_markup=reply_markup)


def found(update, context):
    pass


def apply(update, context):
    update.message.reply_text(text=f"Отправьте ваши данные в следующем виде:\n"
                                   f"1. ФИО\n"
                                   f"2. Дата рождения (вам должно быть больше 14 лет)\n"
                                   f"3. Адрес проживания (город, улица, номер дома)\n"
                                   f"4. Удобное время работы (например, с 15:00 по 20:00)\n"
                                   f"После обработки заявки нашей администрацией вы получите ответ.")
    return FIRST


def apply_2(update, context):
    txt = update.message.text
    id = update.message.from_user.id
    name = txt[txt.find("1.") + 3:txt.find("2.")]
    birth_date = txt[txt.find("2.") + 3:txt.find("3.")]
    address = txt[txt.find("3.") + 3:txt.find("4.")]
    hours = txt[txt.find("4.") + 3:]
    data = list(map(no_space, [id, name, birth_date, address, hours]))
    conn = sqlite3.connect("base.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO applications VALUES (?, ?, ?, ?, ?)", tuple(data))
    conn.commit()
    conn.close()
    update.message.reply_text(text="Спасибо за вашу заявку!")
    start(update, context)
    return ConversationHandler.END


def no_space(x):
    x = str(x)
    if x[0] == " " or x[0] == "\n":
        x = x[1:]
    if x[-1] == " " or x[-1] == "\n":
        x = x[:-1]
    return x


if __name__ == '__main__':
    main()
