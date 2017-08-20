# -*- coding: utf-8 -*-
import sys
import logging
import os
import sqlite3
from mattermost_bot import bot, settings
import os.path

def main():
    logging.basicConfig(**{
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if settings.DEBUG else logging.INFO,
        'stream': sys.stdout,
    })
    if (os.path.isfile('/usr/local/lib/python2.7/dist-packages/mattermost_bot/plugins/bot.db') ==False):
        fd = os.open('/usr/local/lib/python2.7/dist-packages/mattermost_bot/plugins/bot.db', os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        conn = sqlite3.connect('/usr/local/lib/python2.7/dist-packages/mattermost_bot/plugins/bot.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE working (user,onoff,date,htime,mtime)''')
        conn.commit()
        conn.close()
    try:
        b = bot.Bot()
        b.run()
    except KeyboardInterrupt:
        pass
