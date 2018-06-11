import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters

from bot_action import Action

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = '617361775:AAHS0S6aUQ_gLFmnfOKv72xQj5EBlhBUfos'

# universal_keyboard = ReplyKeyboardMarkup([
#     ["/start", "https://google.com", "/unsubscribe"],
#     ["/abort", "/blah", "action 6"],
#     # ["action 7", "action 8", "action 9"],
#     # ["action 10", ],
# ])


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
        self.none_action = Action("None", 'C', self.none_handler, self.start_action)

    def none_handler(self, bot=None, update=None):
        return None

    def action_resolver(self, message, bot=None, kind='C'):
        if not bot:
            bot = self._updater.bot
        # Assuming that each action is unique in the
        # current action group which is a fair assumption
        for action in bot.actions:
            if action.can_be_triggered(message, kind):
                # print("5, action_can_triggeted: {}".format(action))
                return action
        return self.none_action

    def parent_handler(self, bot, update):
        # print(2, "parent_handler")
        if update.message.text.startswith('/'):
            trigger = update.message.text[1:]  # commands have preceding /
            kind = 'C'
        else:
            trigger = update.message.text
            kind = 'M'
        curr_action = self.action_resolver(message=trigger, kind=kind)
        # print(3, curr_action)
        handler = curr_action.handler
        bot_response = handler(trigger) or "I am not going to dignify that with a response. =_="
        # print(4, "bot_response: {}".format(bot_response))
        new_keyboard = self.load_actions(curr_action.next_actions)
        print(bot.send_message(chat_id=update.message.chat_id,
                               text=bot_response,
                               reply_markup=new_keyboard))

    def load_actions(self, actions):
        _actions = []
        if not isinstance(actions, (list, tuple)):
            _actions.append(actions)
        else:
            _actions = actions
        triggers = []
        if len(_actions) == 0:
            _actions = [self.start_action]
        self._updater.bot.actions = _actions
        # print(6, "_actions: {}".format(_actions))
        for action in _actions:
            # TODO: change the name from handler to callback in Action
            kind = action.kind
            if kind == 'C':
                trigger = '/' + action.trigger
                triggers.append(trigger)
        if len(triggers) > 0:
            keyboard = ReplyKeyboardMarkup(keyboard_layout(triggers))
            return keyboard
        return None

    def start_app(self, start_action=None):
        if start_action:
            self.start_action = start_action
        if self.start_action:
            self.load_actions(self.start_action)

        # print(1, "start_app")
        command_handler = MessageHandler(Filters.all, self.parent_handler)
        # message_handler = MessageHandler(Filters.text, self.parent_msg_handler)
        self.dispatcher.add_handler(command_handler)
        # self.dispatcher.add_handler(message_handler)
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

    news_source = Action(trigger="news_source", kind='M', handler=get_news)

    start.add_actions([news, trade, unsubscribe, abort])
    news.add_actions([news_source, abort, unsubscribe])
    trade.add_actions([abort, unsubscribe])

    # import json
    # print(json.dumps(start.export_action(), indent=4))

    bot_app = BotApp(start_action=start)
    bot_app.start_app()
