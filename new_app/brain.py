from new_app.storage import StorageManager
# from new_app.bot import keyboard_layout
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from new_app.action import StartAction, UnknownAction


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


def strip_command(command):
    """ remove the front `/` from the slash commands """
    if command.startswith('/'):
        return strip_command(command[1:])
    return command


def action_resolver(actions, message):
    # TODO: make use of complex functions to find out if the following message is the correct trigger or not
    """
    *Important*
    The All the actions should be assigned to disjoint set of trigger messages
    :param actions: list of actions which has to be searched for the specified trigger message
    :param message: trigger sent as a message
    :returns: class:Action instance or None
    """
    message = strip_command(message)
    if message == 'start':
        return StartAction
    for action in actions:
        if action.trigger == message:
            return action
    return UnknownAction


def get_keyboard_for_actions(actions):
    _actions = []
    if not isinstance(actions, (list, tuple, set)):
        _actions.append(actions)
    else:
        _actions = actions
    triggers = []
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


from new_app.sessions import SessionManager


# from telegram.update import Update


def respond(update):
    """
    :param update:
    :return: (chat_id, response_message, keyboard)
    """
    # context = ContextManager.resolve(update)
    # message = update.message.text
    # current_action = get_action(context, message)
    #
    # context['last_action'] = current_action.id
    #
    # chat_id = context['chat_id']
    # response = current_action.callback(message)
    # next_actions = current_action.get_next_actions()
    # keyboard = get_keyboard_for_actions(next_actions)
    # return chat_id, response, keyboard
    user = update.effective_user
    session = SessionManager.get_or_create(chat_id=update.message.chat_id, user_id=user.id)
    received_message = update.message.text
    session_data = session.data
    last_action = session_data['action']['last_action']
    current_action = action_resolver(last_action.next_actions, received_message)
    session_data['action']['action'] = current_action

    response = current_action.callback(received_message, session_data) or "No handler was assigned to this action =_="
    next_actions = current_action.get_next_actions()
    chat_id = update.message.chat_id
    keyboard = get_keyboard_for_actions(next_actions)

    # print(current_action)
    # print(next_actions)
    return chat_id, response, keyboard
