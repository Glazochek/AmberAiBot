import openai
import telebot

from Amber.bot_functions import main

if __name__ == '__main__':
    openai.api_key = "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"
    bot = telebot.TeleBot('6161910493:AAEw80BfdcTgnEP6HJxoxI1ftU5IdtCjntQ')
    main(bot)

