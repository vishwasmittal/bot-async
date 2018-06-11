from library_bot_sample import universal_keyboard


def on_start(bot=None, update=None):
    # bot.send_message(chat_id=update.message.chat_id,
    #                  text="Bot at your serviced... ☜(⌒▽⌒)☞",
    #                  reply_markup=universal_keyboard)
    return "Bot at your serviced... ☜(⌒▽⌒)☞"


def on_unsubscribe(bot=None, update=None):
    # bot.send_message(chat_id=update.message.chat_id,
    #                  text='You have been unsubscribed from this service. Good luck on you future endeavours. '
    #                       '\nIn case you change your mind, Feel free to /start again. ʘ‿ʘ',
    #                  reply_markup=universal_keyboard)
    return 'You have been unsubscribed from this service. Good luck on you future endeavours. ' \
           '\nIn case you change your mind, Feel free to /start again. ʘ‿ʘ'


def on_abort(bot=None, update=None):
    # bot.send_message(chat_id=update.message.chat_id,
    #                  text='Thanks for wasting my time!!! ( ಠ ʖ̯ ಠ)', )
    return 'Thanks for wasting my time!!! ( ಠ ʖ̯ ಠ)'


def on_message(bot=None, update=None):
    # bot.send_message(chat_id=update.message.chat_id, text="You want to say something? (ง'̀-'́)ง")
    return "You want to say something? (ง'̀-'́)ง"


def on_unknown(bot=None, update=None):
    # bot.send_message(chat_id=update.message.chat_id,
    #                  text="Sorry, I didn't understand that command. ¯\_(ツ)_/¯")
    return "Sorry, I didn't understand that command. ¯\_(ツ)_/¯"


def on_trade(bot=None, update=None):
    # bot.send_message(chat_id=update.message.chat_id,
    #                  text="If you want to trade, go to market. Why bother me? ¯\_(ツ)_/¯")
    return "If you want to trade, go to market. Why bother me? ¯\_(ツ)_/¯"


def on_news(bot=None, update=None):
    # bot.send_message(chat_id=update.message.chat_id,
    #                  text="If you want to get news, go get a newspaper. Why bother me? ¯\_(ツ)_/¯")
    return "If you want to get news, go get a newspaper. Why bother me? ¯\_(ツ)_/¯"
