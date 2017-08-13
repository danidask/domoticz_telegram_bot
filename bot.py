#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
import requests
import json
import logging

# Get credentials
try:
    jfile = open('credentials.json', 'r')
    cred = json.load(jfile)
    jfile.close()
except json.decoder.JSONDecodeError:
    print("Wrong format in 'credentials.json'. See 'credentials_example.json'")
    quit(1)
except FileNotFoundError:
    print("'credentials.json' not found. Rename 'credentials_example.json' to 'credentials.json' "
          "and fill it with your credentials")
    quit(1)

# Enable logging
logFormatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter,
                    level=logging.DEBUG, filename='telegram.log')
log = logging.getLogger(__name__)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter(logFormatter))
log.addHandler(consoleHandler)


if cred['user'] != '':
    dzurl = "http://{}:{}@{}:{}/json.htm?".format(cred['user'], cred['password'], cred['ip'], cred['port'])
else:
    dzurl = "http://{}:{}/json.htm?".format(cred['ip'], cred['port'])

# Check if reachable
try:
    r = requests.get(dzurl)
except requests.exceptions.ConnectionError:
    log.critical("Can not reach domoticz server. Check connection and credentials in 'credentials.json'")
    quit(1)
log.info("Connected to domoticz server. ip {} port {}".format(cred['ip'], cred['port']))

# r = requests.get(dzurl + 'type=devices&rid=32')  # Potus fertilidad
# print(r.status_code)
# print(r.text)
# j = r.json()
# print(j['status'])  # 'OK'
# print(j['result'][0]['Data'])  # 'Off' 'On'

def getvaloridx(idx):
    requrl = dzurl + 'type=devices&rid=' + str(idx)
    r = requests.get(requrl)
    if r.status_code != 200:
        log.warning('error {} al intentar conectarse a {}'.format(r.status_code, requrl))
        return None
    j = r.json()
    if j['status'] != 'OK':
        log.warning('El sensor idx{} respondio con status: {}'.format(idx, j['status']))
        return None
    try:
        ret = j['result'][0]['Data']
    except KeyError:
        log.warning("El sensor idx{} no devuelve 'result'".format(idx, j['status']))
        ret = None
    return ret


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def temperatura(bot, update):
    temp = getvaloridx(30)  # potus temp
    if not temp:
        respuesta = 'No he podido hacer la consulta. Intentalo mas tarde o revisa si hay algo mal.'
    else:
        respuesta = 'Temperatura en casa: {}'.format(temp)
    update.message.reply_text(respuesta)


def plantas(bot, update):
    hum = getvaloridx(29)  # potus humedad
    fert = getvaloridx(32)  # potus fertilidad
    if not hum or not fert:
        respuesta = 'No he podido hacer la consulta. Intentalo mas tarde o revisa si hay algo mal.'
    else:
        respuesta = '''Potus:
        Humedad: {} (20-50)
        Fertilizante: {} (350-2000)'''.format(hum, fert)
    update.message.reply_text(respuesta)


def echo(bot, update):
    update.message.reply_text("No entiendo " + update.message.text)
    log.info("Frase '{}' no contemplada".format(update.message.text))


def error(bot, update, error):
    try:
        raise error
    except Unauthorized:
        log.critical("TOKEN incorrect. See and check 'credentials.json' file.")
        quit(1)
    log.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(cred["token"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("temperatura", temperatura))
    dp.add_handler(CommandHandler("plantas", plantas))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    #telegram.error.Unauthorized
    log.info("Bot connected. Listening...")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
