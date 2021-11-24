from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import RegexHandler, Filters, CommandHandler, MessageHandler



def set_updaters(dispatcher):
    # Старт
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(MessageHandler(Filters.text, analize))
    dispatcher.add_handler(CallbackQueryHandler(callback_parser))


def main():
    updater = Updater(token="780079984:AAFIhcpr_2Av6s2UROl61wsrtEMlvrM_SRc", use_context=True)
    dispatcher = updater.dispatcher
    set_updaters(dispatcher)
    updater.start_polling()


def analize(update, context):
    if update.message.text == "Helloo":
        context.bot.send_message(text="hello", chat_id=update.message.chat_id)


def start(update, context):
    start_1 = InlineKeyboardButton(text="Go1", callback_data="start_1")
    start_2 = InlineKeyboardButton(text="Go2", callback_data="start_2")
    custom_keyboard = [[start_1], [start_2]]
    reply_markup = InlineKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    text = "Вы в главном меню"
    context.bot.send_message(text=text,
                              reply_markup=reply_markup, chat_id=update.message.chat_id)


def callback_parser(update, context):
    query = update.callback_query
    query.edit_message_text(text=f"{query.data}")


if __name__ == '__main__':
    main()

