import logging
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, InlineQueryHandler

from bot_action import Action

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = '617361775:AAHS0S6aUQ_gLFmnfOKv72xQj5EBlhBUfos'

universal_keyboard = ReplyKeyboardMarkup([
    ["/start", "https://google.com", "/unsubscribe"],
    ["/abort", "/blah", "action 6"],
    # ["action 7", "action 8", "action 9"],
    # ["action 10", ],
])


def keyboard_layout(triggers, row_size=3):
    """
    Returns the layout for the keyboard

    :param actions: list of actions that each key represent
    :param row_size: no. of keys in a single row
    Layout: list of lists specifying the position of each key (with given action) on the keyboard
    """
    layout = []
    for i in range(0, len(triggers), row_size):
        layout.append([triggers for triggers in triggers[i:i + row_size]])
    return layout


class BotApp(object):
    def __init__(self, start_action=None):
        self._updater = Updater(token=TOKEN)
        self.dispatcher = self._updater.dispatcher
        setattr(self._updater.bot, 'actions', None)
        self.start_action = start_action

    # def on_start(self, bot, update):
    #     bot.send_message(chat_id=update.message.chat_id,
    #                      text="Bot at your serviced... ☜(⌒▽⌒)☞",
    #                      reply_markup=universal_keyboard)

    # def on_unsubscribe(self, bot, update):
    #     bot.send_message(chat_id=update.message.chat_id,
    #                      text='You have been unsubscribed from this service. Good luck on you future endeavours. '
    #                           '\nIn case you change your mind, Feel free to /start again. ʘ‿ʘ',
    #                      reply_markup=universal_keyboard)
    #
    # def on_abort(self, bot, update):
    #     bot.send_message(chat_id=update.message.chat_id,
    #                      text='Thanks for wasting my time!!! ( ಠ ʖ̯ ಠ)', )
    #
    # def on_message(self, bot, update):
    #     bot.send_message(chat_id=update.message.chat_id, text="You want to say something? (ง'̀-'́)ง")
    #
    # def on_unknown(self, bot, update):
    #     bot.send_message(chat_id=update.message.chat_id,
    #                      text="Sorry, I didn't understand that command. ¯\_(ツ)_/¯")

    def none_handler(self, bot, update):
        return None

    def action_resolver(self, message, bot=None):
        if not bot:
            bot = self._updater.bot
        # Assuming that each action is unique in the
        # current action group which is a fair assumption
        for action in bot.actions:
            if action.kind == "C":
                message = message[1:]
            if action.trigger == message:
                return action
        return None

    def parent_command_handler(self, bot, update):
        curr_action = self.action_resolver(update.message.text)
        # if not isinstance(curr_action, Action):
        #     # TODO: make this generic and use on_unknown handler
        #     return bot.send_message(chat_id=update.message.chat_id,
        #                             text="Sorry, I didn't understand that command. ¯\_(ツ)_/¯",
        #                             reply_markup=universal_keyboard)

        handler = curr_action.handler or self.none_handler
        bot_response = handler() or "Anything good"
        new_keyboad = self.load_actions(curr_action.next_actions)

        return bot.send_message(chat_id=update.message.chat_id,
                                text=bot_response,
                                reply_markup=new_keyboad)

    def parent_msg_handler(self, bot, update):
        pass

    def load_actions(self, actions):
        _actions = []
        if not isinstance(actions, (list, tuple)):
            _actions.append(actions)
        else:
            _actions = actions
        triggers = []
        self._updater.bot.actions = _actions
        for action in _actions:
            # TODO: change the name from handler to callback in Action
            kind = action.kind
            trigger = action.trigger if kind == "M" else '/{}'.format(action.trigger)
            # callback = action.handler or self.none_handler
            # handler = CommandHandler if kind == 'C' else MessageHandler
            # handler(trigger, callback)
            triggers.append(trigger)
        return ReplyKeyboardMarkup(keyboard_layout(triggers))

    def start_app(self, start_action=None):
        # print("starting app")
        #
        # start = CommandHandler('start', self.on_start)
        # unsubscribe = CommandHandler('unsubscribe', self.on_unsubscribe)
        # abort = CommandHandler('abort', self.on_abort)
        # unknown = MessageHandler(Filters.command, self.on_unknown)
        # message = MessageHandler(Filters.text, self.on_message)
        #
        # self.dispatcher.add_handler(start)
        # self.dispatcher.add_handler(unsubscribe)
        # self.dispatcher.add_handler(abort)
        # self.dispatcher.add_handler(unknown)
        # self.dispatcher.add_handler(message)
        #
        # self._updater.start_polling()
        # print("bot starting")

        # import time
        # print("sleeping")
        # time.sleep(10)
        # self.dispatcher.handlers[0] = []
        # print(self.dispatcher.handlers)
        # print("woke up")
        if start_action:
            self.start_action = start_action
        if self.start_action:
            self.load_actions(self.start_action)

        command_handler = MessageHandler(Filters.command, self.parent_command_handler)
        self.dispatcher.add_handler(command_handler)
        self._updater.start_polling()


if __name__ == "__main__":
    from action_handlers import *

    start = Action(trigger='start', kind='C', handler=on_start)
    unsubscribe = Action(trigger='unsubscribe', kind='C', handler=on_unsubscribe)
    abort = Action(trigger='abort', kind='C', handler=on_abort)
    unknown = Action(trigger=Filters.command, kind='M', handler=on_unknown)
    message = Action(trigger=Filters.text, kind='M', handler=on_message)
    news = Action(trigger='news', kind='C', handler=on_news)
    trade = Action(trigger='trade', kind='C', handler=on_trade)

    start.add_actions([news, trade, unsubscribe])
    news.add_actions([abort, unsubscribe])
    trade.add_actions([abort, unsubscribe])

    # import json
    # print(json.dumps(start.export_action(), indent=4))

    bot_app = BotApp(start_action=start)
    bot_app.start_app()












# def onScript(self, bot, update):
#     location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
#     contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
#     custom_keyboard = [[location_keyboard, contact_keyboard]]
#     reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
#     bot.send_message(chat_id=update.message.chat_id,
#                      text="Would you mind sharing your location and contact with me?", reply_markup=reply_markup)

# def build_menu(self, buttons,
#                n_cols,
#                header_buttons=None,
#                footer_buttons=None):
#     menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
#     if header_buttons:
#         menu.insert(0, header_buttons)
#     if footer_buttons:
#         menu.append(footer_buttons)
#     return menu

# def onKeyboard(self, bot, update):
#     # button_list = [
#     #     telegram.InlineKeyboardButton("col1", callback_data=self.onFirst),
#     #     telegram.InlineKeyboardButton("col2", callback_data=self.onFirst),
#     #     telegram.InlineKeyboardButton("row 2", callback_data=self.onFirst)
#     # ]
#
#     # reply_markup = telegram.InlineKeyboardMarkup([self.build_menu(button_list, n_cols=2)])
#     # buttons = telegram.InlineKeyboardButton
#     keyboard = [[telegram.InlineKeyboardButton("Option 1", callback_data='1'),
#                  telegram.InlineKeyboardButton("Option 2", callback_data='2')],
#                 [telegram.InlineKeyboardButton("Option 3", callback_data='3')]]
#
#     reply_markup = telegram.InlineKeyboardMarkup(keyboard)
#
#     bot.send_message(chat_id=update.message.chat_id, text="A two-column menu", reply_markup=reply_markup)

# def onInlineCaps(self, bot, update):
#     query = update.inline_query.query
#     if not query:
#         return
#     results = list()
#     logging.info(query)
#     results.append(
#         telegram.InlineQueryResultArticle(
#             id='adani',
#             title='Adani',
#             input_message_content=telegram.InputTextMessageContent("Adani")
#         )
#     )
#     results.append(
#         telegram.InlineQueryResultArticle(
#             id='pnb',
#             title='PNB',
#             input_message_content=telegram.InputTextMessageContent("PNB")
#         )
#     )
#     results.append(
#         telegram.InlineQueryResultArticle(
#             id='reliance',
#             title='Reliance Industries Limited',
#             input_message_content=telegram.InputTextMessageContent("/script RELIANCE"),
#             # This will be enterend into the chat bot
#             thumb_url="https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png",
#             description="Symbol Name: RELIANCE LTP: 433"
#         )
#     )
#     bot.answer_inline_query(update.inline_query.id, results)
# def onButton(self, bot, update):
#     query = update.callback_query
#     bot.edit_message_text(text="Selected option: {}".format(query.data),
#                           chat_id=query.message.chat_id,
#                           message_id=query.message.message_id)

# def startBot(self):
#     dispatcher = self._updater.dispatcher
#
#     # Register commands here
#     # Command Handler Type
#     start_handler = CommandHandler('start', self.onStart)
#     caps_handler = CommandHandler('caps', self.onCaps, pass_args=True)
#     script_handler = CommandHandler('script', self.onScript)
#     keyboard_handler = CommandHandler('keyboard', self.onKeyboard)
#     # Message handler Type
#     echo_handler = MessageHandler(Filters.text, self.onEcho)
#     # Create a new inline query handler
#     inline_caps_handler = InlineQueryHandler(self.onInlineCaps)
#
#     # New Type of callback handler
#     button_handler = CallbackQueryHandler(self.onButton)
#
#     # Unknown Handler
#     unknown_handler = MessageHandler(Filters.command, self.onUnknown)
#
#     # Work on dispatcher
#     dispatcher.add_handler(start_handler)
#     dispatcher.add_handler(caps_handler)
#     dispatcher.add_handler(echo_handler)
#     dispatcher.add_handler(inline_caps_handler)
#     dispatcher.add_handler(script_handler)
#     dispatcher.add_handler(keyboard_handler)
#     dispatcher.add_handler(button_handler)
#     dispatcher.add_handler(unknown_handler)
#
#     self._updater.start_polling()

# def start(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text="yo ho ho...", reply_markup=universal_keyboard)
#
#
# def echo_caps(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text=update.message.text.upper(), reply_markup=universal_keyboard)
#
# # CommandHandler, MessageHandler, Filters
#
#
# command_handler = CommandHandler('start', start)
# message_handler = MessageHandler(Filters.all, echo_caps)
#
#
# dispatcher.add_handler(command_handler)
# dispatcher.add_handler(message_handler)
#
# updater.start_polling()
