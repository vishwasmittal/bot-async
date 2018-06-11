from library_bot_sample import universal_keyboard


def on_start(message):
    return "Bot at your serviced... ☜(⌒▽⌒)☞"


def on_unsubscribe(message):
    return 'You have been unsubscribed from this service. Good luck on you future endeavours. ' \
           '\nIn case you change your mind, Feel free to /start again. ʘ‿ʘ'


def on_abort(message):
    return 'Thanks for wasting my time!!! ( ಠ ʖ̯ ಠ)'


def on_message(message):
    return "You want to say something? (ง'̀-'́)ง"


def on_unknown(message):
    return "Sorry, I didn't understand that command. ¯\_(ツ)_/¯"


def on_trade(message):
    return "If you want to trade, go to market. Why bother me? ¯\_(ツ)_/¯"


def on_news(message):
    # return "If you want to get news, go get a newspaper. Why bother me? ¯\_(ツ)_/¯"
    return "Enter a new source"


def get_news(source):
    return "Contacting the chairman of {} to get a paper for you +_+".format(source)
