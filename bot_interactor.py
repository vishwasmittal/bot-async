import asyncio
import logging

# from app.schema.telegram.message import MessageSchema
# from database_handler import store_doc
# from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, run_async

# from temp_app.bot_action import Action

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = '617361775:AAHS0S6aUQ_gLFmnfOKv72xQj5EBlhBUfos'


# def keyboard_layout(triggers, row_size=3):
#     """
#     Returns the layout for the keyboard
#
#     :param actions: list of actions that each key represent
#     :param row_size: no. of keys in a single row
#     Layout: list of lists specifying the position of each key (with given action) on the keyboard
#     """
#     layout = []
#     for i in range(0, len(triggers), row_size):
#         layout.append([triggers for triggers in triggers[i:i + row_size]])
#     return layout


class BotApp(object):
    def __init__(self, receiver_callback=None):
        self._updater = Updater(token=TOKEN)
        self.dispatcher = self._updater.dispatcher
        self.bot = self._updater.bot
        self.interactor_callback = receiver_callback

        self.aiojobs_scheduler = None

        # setattr(self._updater.bot, 'actions', None)
        # self.start_action = start_action
        # self.none_action = Action("None", 'C', self.none_handler, self.start_action)
        #
        # def none_handler(self, bot=None, update=None):
        #     return None
        #
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
        #
        # def start_app(self, start_action=None):
        #     if start_action:
        #         self.start_action = start_action
        #     if self.start_action:
        #         self.load_actions(self.start_action)
        #
        #     # print(1, "start_app")
        #     command_handler = MessageHandler(Filters.all, self.parent_handler)
        #     # message_handler = MessageHandler(Filters.text, self.parent_msg_handler)
        #     self.dispatcher.add_handler(command_handler)
        #     # self.dispatcher.add_handler(message_handler)
        #     self._updater.start_polling()

    def add_async_execs(self, scheduler):
        self.aiojobs_scheduler = scheduler

    def add_receiver_callback(self, callback):
        self.interactor_callback = callback

    def send_message(self, chat_id, message, new_keyboard):
        result = self.bot.send_message(chat_id=chat_id,
                                       text=message,
                                       disable_web_page_preview=False,
                                       reply_markup=new_keyboard)
        return result

    def receiver_callback(self, bot, update):
        # spawning the job for this requests to the bot
        asyncio.ensure_future(self.aiojobs_scheduler.spawn(self.interactor_callback(update)))

    def start_app(self):
        command_handler = MessageHandler(Filters.all, self.receiver_callback)
        # message_handler = MessageHandler(Filters.text, self.parent_msg_handler)
        self.dispatcher.add_handler(command_handler)
        # self.dispatcher.add_handler(message_handler)
        self._updater.start_polling()

    def stop_app(self):
        self._updater.stop()


BotApp = BotApp()
