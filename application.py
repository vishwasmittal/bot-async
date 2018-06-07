"""
Sample Script for a telegram bot
"""
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

from telegram.ext import Updater, Filters
import telegram
# Add a new query handler
from telegram.ext import CommandHandler, MessageHandler, InlineQueryHandler, CallbackQueryHandler

# from telegram import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup

G_BOT_TOKEN = '599651855:AAEN4po3PUajQOA2je5m0754xkIPhtzyFEM'


class BotApp(object):
    def __init__(self):
        self._updater = Updater(token=G_BOT_TOKEN)

    def onStart(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

    def onCaps(self, bot, update, args):
        text_caps = ' '.join(args).upper()
        bot.send_message(chat_id=update.message.chat_id, text=text_caps)

    def onEcho(self, bot, update):
        # bot.send_message(chat_id=update.message.chat_id, text=update.message.text, parse_mode=telegram.ParseMode.MARKDOWN)
        bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

    def onScript(self, bot, update):
        location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
        contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
        custom_keyboard = [[location_keyboard, contact_keyboard]]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Would you mind sharing your location and contact with me?", reply_markup=reply_markup)

    def onFirst(self):
        logging.info("Callback Hit")

    def build_menu(self, buttons,
                   n_cols,
                   header_buttons=None,
                   footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    def onKeyboard(self, bot, update):
        # button_list = [
        #     telegram.InlineKeyboardButton("col1", callback_data=self.onFirst),
        #     telegram.InlineKeyboardButton("col2", callback_data=self.onFirst),
        #     telegram.InlineKeyboardButton("row 2", callback_data=self.onFirst)
        # ]

        # reply_markup = telegram.InlineKeyboardMarkup([self.build_menu(button_list, n_cols=2)])
        # buttons = telegram.InlineKeyboardButton
        keyboard = [[telegram.InlineKeyboardButton("Option 1", callback_data='1'),
                     telegram.InlineKeyboardButton("Option 2", callback_data='2')],
                    [telegram.InlineKeyboardButton("Option 3", callback_data='3')]]

        reply_markup = telegram.InlineKeyboardMarkup(keyboard)

        bot.send_message(chat_id=update.message.chat_id, text="A two-column menu", reply_markup=reply_markup)

    def onInlineCaps(self, bot, update):
        query = update.inline_query.query
        if not query:
            return
        results = list()
        logging.info(query)
        results.append(
            telegram.InlineQueryResultArticle(
                id='adani',
                title='Adani',
                input_message_content=telegram.InputTextMessageContent("Adani")
            )
        )
        results.append(
            telegram.InlineQueryResultArticle(
                id='pnb',
                title='PNB',
                input_message_content=telegram.InputTextMessageContent("PNB")
            )
        )
        results.append(
            telegram.InlineQueryResultArticle(
                id='reliance',
                title='Reliance Industries Limited',
                input_message_content=telegram.InputTextMessageContent("/script RELIANCE"),
                # This will be enterend into the chat bot
                thumb_url="https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png",
                description="Symbol Name: RELIANCE LTP: 433"
            )
        )
        bot.answer_inline_query(update.inline_query.id, results)

    def onUnknown(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    def onButton(self, bot, update):
        query = update.callback_query
        bot.edit_message_text(text="Selected option: {}".format(query.data),
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)

    def startBot(self):
        dispatcher = self._updater.dispatcher

        # Register commands here
        # Command Handler Type
        start_handler = CommandHandler('start', self.onStart)
        caps_handler = CommandHandler('caps', self.onCaps, pass_args=True)
        script_handler = CommandHandler('script', self.onScript)
        keyboard_handler = CommandHandler('keyboard', self.onKeyboard)
        # Message handler Type
        echo_handler = MessageHandler(Filters.text, self.onEcho)
        # Create a new inline query handler
        inline_caps_handler = InlineQueryHandler(self.onInlineCaps)

        # New Type of callback handler
        button_handler = CallbackQueryHandler(self.onButton)

        # Unknown Handler
        unknown_handler = MessageHandler(Filters.command, self.onUnknown)

        # Work on dispatcher        
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(caps_handler)
        dispatcher.add_handler(echo_handler)
        dispatcher.add_handler(inline_caps_handler)
        dispatcher.add_handler(script_handler)
        dispatcher.add_handler(keyboard_handler)
        dispatcher.add_handler(button_handler)
        dispatcher.add_handler(unknown_handler)

        self._updater.start_polling()


def main():
    a = BotApp()
    a.startBot()


if __name__ == '__main__':
    main()
