from .context_manager import ContextManager
from .bot import BotApp


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
    for action in actions:
        if action.trigger == message:
            return action
    return None


def get_action(context, message):
    last_action = ContextManager.actions[context['last_action']]
    next_actions = last_action.get_next_actions()
    current_action = action_resolver(next_actions, message)
    return current_action


def respond(update):
    context = ContextManager.resolve(update)
    message = update.message.text
    current_action = get_action(context, message)
    # TODO: handle the case of None instead of an Action instance
    context['last_action'] = current_action.id
    response = current_action.callback(message)
    return BotApp.sendMessage(context.chat_id, response)
