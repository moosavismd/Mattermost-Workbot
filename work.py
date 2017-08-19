#!/usr/bin/python

# -*- coding: utf-8 -*-
import re
import sys
import sqlite3
from mattermost_bot.cli import main
from mattermost_bot.bot import respond_to, listen_to
from time import gmtime, strftime
from datetime import datetime
from datetime import timedelta

@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply('I can understand hi or HI!')


@respond_to('I love you')
def love(message):
    message.reply('I love you too!')


@respond_to('work on')
def coming(message):
    message.send(message.get_username()+ " is working now ---- " + str (datetime.now()),'khio3dze8tdzujqmwhey1qacmy')
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    t = (message.get_username(),'on',datetime.now().date(),datetime.now().hour,datetime.now().minute)
    c.execute("INSERT INTO working VALUES (?,?,?,?,?)",t)
    conn.commit()
    conn.close()


@respond_to('work off')
def leaving(message):
    message.send(message.get_username()+ " is out of work now ---- " + str (datetime.now()),'khio3dze8tdzujqmwhey1qacmy')
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    t = (message.get_username(),'off',datetime.now().date(),datetime.now().hour,datetime.now().minute)
    c.execute("INSERT INTO working VALUES (?,?,?,?,?)",t)
    conn.commit()
    conn.close()



@respond_to('user stat (.*)')
def stats(message, something):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    t = (something,)
    for row in c.execute('SELECT * FROM working WHERE user=?', t):
        date = ''.join(row[2])
        if ''.join(row[1]) == "on":
           onoff= "came to office"
        else:
           onoff= "left office"
        htime=str (row[3])
        mtime=str (row[4])
        message.reply("user " + something +" " + onoff + " at " + htime + " : " + mtime + " in " +date + ".")
    conn.commit()
    conn.close()

@respond_to('user day stat (.*)')
def daystats(message, something):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    t = (something,datetime.now().date(),)
    for row in c.execute('SELECT * FROM working WHERE user=? and date=?', t):
        date = ''.join(row[2])
        if ''.join(row[1]) == "on":
           onoff= "came to office"
        else:
           onoff= "left office"
        htime=str (row[3])
        mtime=str (row[4])
        message.reply("user " + something + " " + onoff + " at " + htime + " : " + mtime + " in " +date + ".")
    conn.commit()
    conn.close()


@respond_to('user week stat (.*)')
def weekstats(message, something):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    for i in range (0,7):
      t = (something,datetime.now().date() - timedelta(days=i),)
      for row in c.execute('SELECT * FROM working WHERE user=? and date=?', t):
          date = ''.join(row[2])
          if ''.join(row[1]) == "on":
             onoff= "came to office"
          else:
             onoff= "left office"
          htime=str (row[3])
          mtime=str (row[4])
          message.reply("user " + something + " " + onoff + " at " + htime + " : " + mtime + " in " +date + ".")
    conn.commit()
    conn.close()

@respond_to('user month stat (.*)')
def monthstats(message, something):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    for i in range (0,30):
      t = (something,datetime.now().date() - timedelta(days=i),)
      for row in c.execute('SELECT * FROM working WHERE user=? and date=?', t):
          date = ''.join(row[2])
          if ''.join(row[1]) == "on":
             onoff= "came to office"
          else:
             onoff= "left office"
          htime=str (row[3])
          mtime=str (row[4])
          message.reply("user " + something + " " + onoff + " at " + htime + " : " + mtime + " in " +date + ".")
    conn.commit()
    conn.close()
