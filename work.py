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


@respond_to('work on')
def coming(message):
    with open('channel.id', 'r') as f:
        for line in f:
            for word in line.split():
                ch_id=word
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    t = (message.get_username(), datetime.now().date(),)
    c.execute('SELECT onoff FROM working WHERE user=? and date=? ORDER BY htime DESC, mtime DESC LIMIT 1', t)
    response = c.fetchone()
    if response and ''.join(response) =="on":
        message.reply("you have already registered your entrance today")
    else:
        message.send(message.get_username() + " is working now ---- " + str(datetime.now()), ch_id)
        message.reply("Hello " + message.get_username() + " ! get ready for a good day :) !")
        t = (message.get_username(), 'on', datetime.now().date(), datetime.now().hour, datetime.now().minute)
        c.execute("INSERT INTO working VALUES (?,?,?,?,?)", t)
    conn.commit()
    conn.close()

@respond_to('work off')
def leaving(message):
    with open('channel.id', 'r') as f:
        for line in f:
            for word in line.split():
                ch_id=word

    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    t = (message.get_username(), datetime.now().date(),)
    c.execute('SELECT onoff FROM working WHERE user=? and date=? ORDER BY htime DESC, mtime DESC LIMIT 1', t)
    response = c.fetchone()
    if response and ''.join(response) == "off":
        message.reply("you have already registered your exit today")
    elif not response:
        message.reply("you didn't register your entrance today!")
    else:
        message.send(message.get_username() + " is out of work now ---- " + str(datetime.now()), ch_id)
        message.reply("Thanks for your hard work " + message.get_username() + " ! have a good day :) see you soon !")
        t = (message.get_username(), 'off', datetime.now().date(), datetime.now().hour, datetime.now().minute)
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
        htime=str (row[3])
        mtime=str (row[4])
        if ''.join(row[1]) == "on":
            onoff= "came to office"
        else:
            onoff= "left office"
        message.reply("user " + something +" " + onoff + " at " + htime + " : " + mtime + " in " +date + ".")
    conn.commit()
    conn.close()

@respond_to('user day stat (.*)')
def daystats(message, something):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    t = (something,datetime.now().date(),)
    dayon = 0
    dayoff = 0
    for row in c.execute('SELECT * FROM working WHERE user=? and date=?', t):
        date = ''.join(row[2])
        htime=str (row[3])
        mtime=str (row[4])
        if ''.join(row[1]) == "on":
            dayon = dayon + row[4] + (row[3] * 60)
            onoff= "came to office"
        else:
            dayoff = dayoff + row[4] + (row[3] * 60)
            onoff= "left office"
        message.reply("user " + something + " " + onoff + " at " + htime + " : " + mtime + " in " +date + ".")
    if dayoff < dayon:
        dayoff= dayoff + datetime.now().minute + datetime.now().hour*60
    sumall = dayoff - dayon
    conn.commit()
    conn.close()
    sumhours = sumall / 60
    summinutes = sumall % 60
    message.reply("user " + something + " totally worked " + str (sumhours) + ":" + str(summinutes) + " today.")


@respond_to('user week stat (.*)')
def weekstats(message, something):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    sumall =0
    for i in range (1,8):
        dayon = 0
        dayoff = 0
        t = (something,datetime.now().date() - timedelta(days=i),)
        for row in c.execute('SELECT * FROM working WHERE user=? and date=?', t):
            date = ''.join(row[2])
            htime=str (row[3])
            mtime=str (row[4])
            if ''.join(row[1]) == "on":
                dayon = dayon + row[4] + (row[3] * 60)
                onoff = "came to office"
            else:
                dayoff = dayoff + row[4] + (row[3] * 60)
                onoff = "left office"
            message.reply("user " + something + " " + onoff + " at " + htime + " : " + mtime + " in " +date + ".")
        if dayoff < dayon:
            dayoff = dayoff+1320
        sumall = sumall + (dayoff - dayon)
    conn.commit()
    conn.close()
    sumhours = sumall / 60
    summinutes = sumall % 60
    message.reply("user " + something + " totally worked " + str (sumhours) + ":" + str(summinutes) + " in last 7 days.")

@respond_to('user month stat (.*)')
def monthstats(message, something):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    sumall = 0
    for i in range (1,31    ):
        dayon = 0
        dayoff = 0
        t = (something,datetime.now().date() - timedelta(days=i),)
        for row in c.execute('SELECT * FROM working WHERE user=? and date=?', t):
            date = ''.join(row[2])
            htime=str (row[3])
            mtime=str (row[4])
            if ''.join(row[1]) == "on":
                dayon = dayon + row[4] + (row[3] * 60)
                onoff = "came to office"
            else:
                dayoff = dayoff + row[4] + (row[3] * 60)
                onoff = "left office"
            message.reply("user " + something + " " + onoff + " at " + htime + " : " + mtime + " in " +date + ".")
        if dayoff < dayon:
            dayoff = dayoff + 1320
        sumall = sumall + (dayoff - dayon)
    conn.commit()
    conn.close()
    sumhours = sumall / 60
    summinutes = sumall % 60
    message.reply("user " + something + " totally worked " + str (sumhours) + ":" + str(summinutes) + " in last 30 days.")

@respond_to('my week stat')
def myweekstats(message):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    sumall =0
    for i in range (0,(datetime.today().weekday()+3)%7):
        dayon = 0
        dayoff = 0
        t = (message.get_username(),datetime.now().date() - timedelta(days=i),)
        for row in c.execute('SELECT * FROM working WHERE user=? and date=?', t):
            date = ''.join(row[2])
            htime=str (row[3])
            mtime=str (row[4])
            if ''.join(row[1]) == "on":
                dayon = dayon + row[4] + (row[3] * 60)
                onoff = "came to office"
            else:
                dayoff = dayoff + row[4] + (row[3] * 60)
                onoff = "left office"
            message.reply("user " + message.get_username() + " " + onoff + " at " + htime + " : " + mtime + " in " +date + ".")
        if i == 0: 
            if dayoff < dayon:
                dayoff= dayoff + datetime.now().minute + datetime.now().hour*60
        else:
            if dayoff < dayon:
                dayoff = dayoff+1320

        sumall = sumall + (dayoff - dayon)
    conn.commit()
    conn.close()
    sumhours = sumall / 60
    summinutes = sumall % 60
    message.reply("user " + message.get_username() + " totally worked " + str (sumhours) + ":" + str(summinutes) + " this week.")

coming.__doc__ = "register your enterance to the office"
leaving.__doc__ = "register your enterance to the office"
myweekstats.__doc__ = "shows your work hours from last saturday until this exact time"
daystats.__doc__ = "show any users work hours of today from user's entrance until this exact time or user's exit. example usage: user day stat moosavismd"
weekstats.__doc__ = "show any users work hours of last 7 days. example usage: user week stat moosavismd"
monthstats.__doc__ = "show any users work hours of last 30 days. example usage: user month stat moosavismd"
stats.__doc__ = "show any users work hours of all time (sum of work hours not included). example usage: user stat moosavismd"
