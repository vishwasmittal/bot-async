import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters

from bot_action import Action
from database_handler import store_doc
from app.schema.telegram.message import MessageSchema
from .brain import respond

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = '617361775:AAHS0S6aUQ_gLFmnfOKv72xQj5EBlhBUfos'


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
        # setattr(self._updater.bot, 'actions', None)
        self.bot = self._updater.bot
        # self.start_action = start_action
        # self.none_action = Action("None", 'C', self.none_handler, self.start_action)

    # def none_handler(self, bot=None, update=None):
    #     return None

    # def action_resolver(self, message, bot=None, kind='C'):
    #     if not bot:
    #         bot = self._updater.bot
    #     # Assuming that each action is unique in the
    #     # current action group which is a fair assumption
    #     for action in bot.actions:
    #         if action.can_be_triggered(message, kind):
    #             # print("5, action_can_triggeted: {}".format(action))
    #             return action
    #     return self.none_action
    #
    # def parent_handler(self, bot, update):
    #     # print(2, "parent_handler")
    #     if update.message.text.startswith('/'):
    #         trigger = update.message.text[1:]  # commands have preceding /
    #         kind = 'C'
    #     else:
    #         trigger = update.message.text
    #         kind = 'M'
    #     curr_action = self.action_resolver(message=trigger, kind=kind)
    #     # print(3, curr_action)
    #     handler = curr_action.handler
    #     bot_response = handler(trigger) or "I am not going to dignify that with a response. =_="
    #     # print(4, "bot_response: {}".format(bot_response))
    #     new_keyboard = self.load_actions(curr_action.next_actions)
    #     result = bot.send_message(chat_id=update.message.chat_id,
    #                               text=bot_response,
    #                               reply_markup=new_keyboard)
    #     msg_doc = [MessageSchema().dump(update.message), MessageSchema().dump(result)]
    #     store_doc(msg_doc)
    #
    # def load_actions(self, actions):
    #     _actions = []
    #     if not isinstance(actions, (list, tuple)):
    #         _actions.append(actions)
    #     else:
    #         _actions = actions
    #     triggers = []
    #     if len(_actions) == 0:
    #         _actions = [self.start_action]
    #     self._updater.bot.actions = _actions
    #     # print(6, "_actions: {}".format(_actions))
    #     for action in _actions:
    #         # TODO: change the name from handler to callback in Action
    #         kind = action.kind
    #         if kind == 'C':
    #             trigger = '/' + action.trigger
    #             triggers.append(trigger)
    #     if len(triggers) > 0:
    #         keyboard = ReplyKeyboardMarkup(keyboard_layout(triggers))
    #         return keyboard
    #     return None

    def send_message(self, chat_id, message, keyboard=None):
        """ Send message to the bot """
        return self.bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)

    def message_handler(self, bot, update):
        chat_id, message, keyboard = respond(update)

    def start_app(self):
        # if start_action:
        #     self.start_action = start_action
        # if self.start_action:
        #     self.load_actions(self.start_action)

        # command_handler = MessageHandler(Filters.all, self.parent_handler)
        command_handler = MessageHandler(Filters.all, self.message_handler)
        # message_handler = MessageHandler(Filters.text, self.parent_msg_handler)
        self.dispatcher.add_handler(command_handler)
        # self.dispatcher.add_handler(message_handler)
        self._updater.start_polling()


BotApp = BotApp()


# if __name__ == "__main__":
#     from action_handlers import *
#
#     start = Action(trigger='start', kind='C', handler=on_start)
#     unsubscribe = Action(trigger='unsubscribe', kind='C', handler=on_unsubscribe)
#     abort = Action(trigger='abort', kind='C', handler=on_abort)
#     unknown = Action(trigger=Filters.command, kind='M', handler=on_unknown)
#     message = Action(trigger=Filters.text, kind='M', handler=on_message)
#     news = Action(trigger='news', kind='C', handler=on_news)
#     trade = Action(trigger='trade', kind='C', handler=on_trade)
#
#     news_source = Action(trigger="news_source", kind='M', handler=get_news)
#
#     start.add_actions([news, trade, unsubscribe, abort])
#     news.add_actions([news_source, abort, unsubscribe])
#     trade.add_actions([abort, unsubscribe])
#
#     # import json
#     # print(json.dumps(start.export_action(), indent=4))
#
#     bot_app = BotApp(start_action=start)
#     bot_app.start_app()





# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, InlineQueryHandler
# import telegram
# import logging
#
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#
#
# TOKEN = '617361775:AAHS0S6aUQ_gLFmnfOKv72xQj5EBlhBUfos'
# #
# # updater = Updater(token=token)
# #
# # dispatcher = updater.dispatcher
# #
# # from telegram import KeyboardButton, ReplyKeyboardMarkup
# #
#
#
# universal_keyboard = ReplyKeyboardMarkup([
#     ["/start", "/news", "/trade"],
#     # ["action 4", "action 5", "action 6"],
#     # ["action 7", "action 8", "action 9"],
#     # ["action 10", ],
# ])
#
#
# class BotApp(object):
#     def __init__(self):
#         self._updater = Updater(token=TOKEN)
#
#     def onStart(self, bot, update):
#         bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!", reply_markup=universal_keyboard)
#
#     def onCaps(self, bot, update, args):
#         text_caps = ' '.join(args).upper()
#         bot.send_message(chat_id=update.message.chat_id, text=text_caps)
#
#     def onEcho(self, bot, update):
#         # bot.send_message(chat_id=update.message.chat_id, text=update.message.text, parse_mode=telegram.ParseMode.MARKDOWN)
#         bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
#
#     def onScript(self, bot, update):
#         location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
#         contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
#         custom_keyboard = [[location_keyboard, contact_keyboard]]
#         reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
#         bot.send_message(chat_id=update.message.chat_id,
#                          text="Would you mind sharing your location and contact with me?", reply_markup=reply_markup)
#
#     def onFirst(self):
#         logging.info("Callback Hit")
#
#     def build_menu(self, buttons,
#                    n_cols,
#                    header_buttons=None,
#                    footer_buttons=None):
#         menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
#         if header_buttons:
#             menu.insert(0, header_buttons)
#         if footer_buttons:
#             menu.append(footer_buttons)
#         return menu
#
#     def onKeyboard(self, bot, update):
#         # button_list = [
#         #     telegram.InlineKeyboardButton("col1", callback_data=self.onFirst),
#         #     telegram.InlineKeyboardButton("col2", callback_data=self.onFirst),
#         #     telegram.InlineKeyboardButton("row 2", callback_data=self.onFirst)
#         # ]
#
#         # reply_markup = telegram.InlineKeyboardMarkup([self.build_menu(button_list, n_cols=2)])
#         # buttons = telegram.InlineKeyboardButton
#         keyboard = [[telegram.InlineKeyboardButton("Option 1", callback_data='1'),
#                      telegram.InlineKeyboardButton("Option 2", callback_data='2')],
#                     [telegram.InlineKeyboardButton("Option 3", callback_data='3')]]
#
#         reply_markup = telegram.InlineKeyboardMarkup(keyboard)
#
#         bot.send_message(chat_id=update.message.chat_id, text="A two-column menu", reply_markup=reply_markup)
#
#     def onInlineCaps(self, bot, update):
#         query = update.inline_query.query
#         if not query:
#             return
#         results = list()
#         logging.info(query)
#         results.append(
#             telegram.InlineQueryResultArticle(
#                 id='adani',
#                 title='Adani',
#                 input_message_content=telegram.InputTextMessageContent("Adani")
#             )
#         )
#         results.append(
#             telegram.InlineQueryResultArticle(
#                 id='pnb',
#                 title='PNB',
#                 input_message_content=telegram.InputTextMessageContent("PNB")
#             )
#         )
#         results.append(
#             telegram.InlineQueryResultArticle(
#                 id='reliance',
#                 title='Reliance Industries Limited',
#                 input_message_content=telegram.InputTextMessageContent("/script RELIANCE"),
#                 # This will be enterend into the chat bot
#                 thumb_url="https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png",
#                 description="Symbol Name: RELIANCE LTP: 433"
#             )
#         )
#         bot.answer_inline_query(update.inline_query.id, results)
#
#     def onUnknown(self, bot, update):
#         bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
#
#     def onButton(self, bot, update):
#         query = update.callback_query
#         bot.edit_message_text(text="Selected option: {}".format(query.data),
#                               chat_id=query.message.chat_id,
#                               message_id=query.message.message_id)
#
#     def startBot(self):
#         dispatcher = self._updater.dispatcher
#
#         # Register commands here
#         # Command Handler Type
#         start_handler = CommandHandler('start', self.onStart)
#         caps_handler = CommandHandler('caps', self.onCaps, pass_args=True)
#         script_handler = CommandHandler('script', self.onScript)
#         keyboard_handler = CommandHandler('keyboard', self.onKeyboard)
#         # Message handler Type
#         echo_handler = MessageHandler(Filters.text, self.onEcho)
#         # Create a new inline query handler
#         inline_caps_handler = InlineQueryHandler(self.onInlineCaps)
#
#         # New Type of callback handler
#         button_handler = CallbackQueryHandler(self.onButton)
#
#         # Unknown Handler
#         unknown_handler = MessageHandler(Filters.command, self.onUnknown)
#
#         # Work on dispatcher
#         dispatcher.add_handler(start_handler)
#         dispatcher.add_handler(caps_handler)
#         dispatcher.add_handler(echo_handler)
#         dispatcher.add_handler(inline_caps_handler)
#         dispatcher.add_handler(script_handler)
#         dispatcher.add_handler(keyboard_handler)
#         dispatcher.add_handler(button_handler)
#         dispatcher.add_handler(unknown_handler)
#
#         self._updater.start_polling()
#
# # def start(bot, update):
# #     bot.send_message(chat_id=update.message.chat_id, text="yo ho ho...", reply_markup=universal_keyboard)
# #
# #
# # def echo_caps(bot, update):
# #     bot.send_message(chat_id=update.message.chat_id, text=update.message.text.upper(), reply_markup=universal_keyboard)
# #
# # # CommandHandler, MessageHandler, Filters
# #
# #
# # command_handler = CommandHandler('start', start)
# # message_handler = MessageHandler(Filters.all, echo_caps)
# #
# #
# # dispatcher.add_handler(command_handler)
# # dispatcher.add_handler(message_handler)
# #
# # updater.start_polling()
