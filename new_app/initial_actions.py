from new_app.action import Action, UnknownAction, StartAction
from new_app.storage import StorageManager
from new_app.brain import strip_command

"""
Actions:
    - subscriptions
        - add more
            - confirm
        - unsubscribe
            - confirm
    - trade
        - list of companies
        - quantity
        - comfirm
"""

# def subscriptions_callback(message, session_data):
#     response = "You are subscribed to following notifications:\n"
#     publishers = session_data['subscriptions'].keys()
#     for pub in publishers:
#         response = response + '/' + str(pub) + '\n'
#     return response
#
#
# subscriptions = Action('subscriptions', 'C')
#
#
# def confirm_subscription_add_callback(message, session_data):
#     temp_subs = session_data['action']['data']['temp_subs']
#     for sub in temp_subs:
#         # StorageManager.store['subscriptions'][sub]['subscripbers']
#         pass
#
#
# confirm_add = Action('confirm', 'C')
#
#
# def subscription_item_callback(message, session_data):
#     pub = strip_command(message)
#     if pub in session_data['action']['data']['unsubs_temp']:
#         if 'temp_subs' not in session_data['action']['data']:
#             session_data['action']['data']['temp_subs'] = set()
#         session_data['action']['data']['temp_subs'].add(pub)
#         response = "choose more or click confirm"
#         session_data['action']['data']['unsubs_temp'].remove(pub)
#     else:
#         response = 'Unknown Publisher'
#
#     last_action = session_data['action']['last_action']
#     publishers = session_data['action']['data']['unsubs_temp']
#     for pub in publishers:
#         if pub not in session_data['subscriptions']:
#             last_action.add_actions(Action(str(pub), 'C', subscription_item_callback))
#
#     last_action.add_actions(confirm_add)
#     return response
#
#
# def add_subscriptions_callback(message, session_data):
#     session_data['action']['data']['unsubs_temp'] = set()
#     publishers = StorageManager.store['publishers'].keys()
#     last_action = session_data['action']['last_action']
#     response = "Choose the publishers you want to subscribe to:\n"
#     for pub in publishers:
#         if pub not in session_data['subscriptions']:
#             response = response + '/' + str(pub) + '\n'
#             session_data['action']['data']['unsubs_temp'].add(str(pub))
#             last_action.add_actions(Action(str(pub), 'C', subscription_item_callback))
#
#     return response


subscriptions = Action('subscriptions', 'C')
add_subs = Action('add more', 'C')
confirm_add = Action('confirm', 'C')

unsubscribe = Action('unsubscribe', 'C')
confirm_unsubscribe = Action('confirm', 'C')

trade = Action('trade', 'C')
choose_company = Action('Choose Company', 'M')
quantity = Action('Quantity?', 'M')
confirm_trade = Action('Confrim', 'C')
