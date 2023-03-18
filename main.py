## Бот обмена валют ScillBot

import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Приветствую!\n\nЧтобы начать работу, введите команду боту в формате:\n<исходная валюта> \
    <в какую валюту перевести>   <количество валюты>\n\nСписок всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges:
        text = '\n- '.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!\n\nВведите команду в формате:\n<исходная валюта> \
    <в какую валюту перевести>   <количество валюты>')
        
        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )

    else:
        bot.reply_to(message, answer)

bot.polling()
