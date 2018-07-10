"""
Define the actions for first aid service that can come under
the category of an ache


NOTE: If possible, define your functions in the bottom
up direction of the action-tree as this will resolve any of
the `NameError` due to non declaration of the action and will
make the code clean


What will service will do is it will ask the user where is
the pain and wherever the pain is and will ask the time the
user is suffering from this pain and then will advice him/her
for any remedy

So the action flow will be:

                                /health
                                /ache
                            head     tooth
                        duration     duration

"""

from ..manager import HealthManager
from actions_framework.actions import Action


# remember to define the callbacks with extra *args and **kwargs other than the expected args as some unexpected
# arguments can also be passed that will cause error if args and kwargs not defined
# Check the Action.invoke_callback() declaration for reference
def tooth_ache_duration_callback(input, session, action, *args, **kwargs):
    if not input.isdigit():
        # if input is wrong, repeat the action
        repeated_action = action.get_repeated_action()
        action.clear_next_actions()
        action.add_actions(repeated_action)
        return "No. of days should be numeric"
    if int(input) > 1:
        return "{} days and you are still looking for a remedy from an automated bot!!! I " \
               "suggest you go see a dentist".format(input)
    else:
        return "Apply some ice and you will be fine :)"


def head_ache_duration_callback(input, session, action, *args, **kwargs):
    if not input.isdigit():
        # if input is wrong, repeat the action
        repeated_action = action.get_repeated_action()
        action.clear_next_actions()
        action.add_actions(repeated_action)
        return "No. of days should be numeric"
    if int(input) > 3:
        return "{} days and you are still looking for a remedy from an automated bot!!! I " \
               "suggest you go see a doctor. I am worried about you.".format(input)
    else:
        return "Probably due to lack of sleep. Go get some rest and you will be fine :)"


def head_ache_callback(session, *args, **kwargs):
    return "For how long are you experiencing this?"


def tooth_ache_callback(session, *args, **kwargs):
    return "For how long are you experiencing this?"


def ache_callback(session, *args, **kwargs):
    return "What part of your body pains?"


tooth_ache_duration_action = Action('duration', 'I', tooth_ache_duration_callback)
head_ache_duration_action = Action('duration', 'I', head_ache_duration_callback)

head_ache_action = Action('head', 'C', head_ache_callback)
head_ache_action.add_actions(head_ache_duration_action)
tooth_ache_action = Action('tooth', 'C', tooth_ache_callback)
tooth_ache_action.add_actions(tooth_ache_duration_action)

ache_action = Action('ache', 'C', ache_callback)
ache_action.add_actions([head_ache_action, tooth_ache_action])

HealthManager.register_action(ache_action)
