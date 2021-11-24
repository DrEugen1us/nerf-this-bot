from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import RegexHandler, Filters, CommandHandler, MessageHandler, ConversationHandler


def set_updaters(dispatcher):
    # Старт
    start_handler = CommandHandler('start', start)


def main():
    updater = Updater(token="2104502859:AAFiVZVGhIKxySHlXsGs1RgxUN0YsdlPd-4", use_context=True)
    dispatcher = updater.dispatcher
    set_updaters(dispatcher)
    updater.start_polling()


def start(update, context):
    ck = [["Нaшел мусoр"], ["Пoдaть зaявку на рабoту"]]
    reply_markup = ReplyKeyboardMarkup(ck)
    update.message.reply_text(text="Вы в главном меню", reply_markup=reply_markup)


if __name__ == '__main__':
    main()