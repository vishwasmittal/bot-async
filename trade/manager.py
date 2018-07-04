from managers.actions import StartAction
from managers.service_manager import BaseServiceManager
from actions_framework.actions import Action

AbortAction = Action('abort', 'C', Action.abort_callback)
AbortAction.add_actions(StartAction)
companies = [
    {
        'name': 'Reliance',
        'script': 'reliance_script'
    },
    {
        'name': 'Adani',
        'script': 'adani_script'
    },
    {
        'name': 'PNB',
        'script': 'pnb_script'
    },
    {
        'name': 'Axis bank',
        'script': 'axis_script'
    },
    {
        'name': 'infosys',
        'script': 'infosys_script'
    },
]


class TradeManager(BaseServiceManager):
    def __init__(self, name):
        super(TradeManager, self).__init__(name)
        """
        self.main_action defines the parent action for this service
        self.users['subscribed'] defines users who are subscribed to this service
        self.users['unsubscribed'] defines those who have unsubscribed
        self.send_message(to, message, next_actions) sends message to others

        """
        self.define_actions()

    def define_actions(self):
        for company in companies:
            company_action = Action(company['name'], 'M', self.company_callback)
            quantity_action = Action('quantity', 'I', self.call_trade_script, script_name=company['script'])
            company_action.add_actions(quantity_action)
            quantity_action.add_actions(StartAction)
            self.main_action.add_actions(company_action)

        self.main_action.add_actions(AbortAction)

    def company_callback(self, *args, **kargs):
        return "enter quantity"

    def call_trade_script(self, session, script_name, input, *args, **kwargs):
        return "called the script: {}\ninput: {}".format(script_name, input)

    async def incoming_action_callback(self, session, action):
        # message = action.callback(session=session)
        message = action.invoke_callback(session=session)
        await self.send_message(session.get('chat_id'), message, action.next_action_list())


TradeManager = TradeManager(name='trade')
