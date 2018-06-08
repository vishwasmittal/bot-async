from library_bot_sample import universal_keyboard


def on_start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Bot at your serviced... ☜(⌒▽⌒)☞",
                     reply_markup=universal_keyboard)


def on_unsubscribe(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='You have been unsubscribed from this service. Good luck on you future endeavours. '
                          '\nIn case you change your mind, Feel free to /start again. ʘ‿ʘ',
                     reply_markup=universal_keyboard)


def on_abort(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Thanks for wasting my time!!! ( ಠ ʖ̯ ಠ)', )


def on_message(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="You want to say something? (ง'̀-'́)ง")


def on_unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Sorry, I didn't understand that command. ¯\_(ツ)_/¯")


def on_trade(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="If you want to trade, go to market. Why bother me? ¯\_(ツ)_/¯")


def on_news(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="If you want to get news, go get a newspaper. Why bother me? ¯\_(ツ)_/¯")
