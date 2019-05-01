#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, os, ast, datetime
def onQQMessage(bot, contact, member, content):
    if hasattr(bot, 'Momona_switch'):
        switch = bot.Momona_switch(bot, contact, member, content)
    else:
        switch = True
    if not(len(content) < 5 or bot.isMe(contact, member) or not switch):
        output = ''
        if hasattr(bot, 'Momona_msgParser'):
            content = bot.Momona_msgParser(bot, content)
        if len(content) < 5:
            pass
        elif (content[0] == '.' or content[0] == '。') and content[1:5].lower() == 'jrrp':
            if contact.ctype == 'buddy':
                uin = contact.uin
            else:
                uin = member.uin
            date = datetime.date.today()
            if not (bot.jrrplist['date'][0] == date.month and bot.jrrplist['date'][1] == date.day):
                bot.jrrplist = {'date':[date.month, date.day]}
            rp = getrp(bot, uin)
            output = bot.Momona_text['jrrp'].replace('{result}',str(rp))
        elif (content[0] == '.' or content[0] == '。') and content[1:5].lower() == 'xrxc':
            nm = bot.Momona_name(bot, contact, member, content)
            output = bot.Momona_text['xrxc'].replace('{result}',str([random.randint(0,9) for x in range(4)]))
        if len(output) > 0:
            bot.SendTo(contact, bot.Momona_msgFormater(bot, contact, member, output))
def getrp(bot, uin):
    if uin in bot.jrrplist:
        rp = bot.jrrplist[uin]
    else:
        rp = random.randint(1, 100)
        bot.jrrplist[uin] = rp
    return rp
def onPlug(bot):
    date = datetime.date.today()
    if not hasattr(bot, 'helpinfo'):
        bot.helpinfo = {}
    loadData(bot)
    if not hasattr(bot, 'jrrplist'):
        bot.jrrplist = {'date':[date.month, date.day]}
    bot.helpinfo['jrrp'] = [[],bot.Momona_text['helpinfo_jrrp']]
    bot.helpinfo['xrxc'] = [[],bot.Momona_text['helpinfo_xrxc']]
def onUnplug(bot):
    saveData(bot)
    del bot.sanlist
    del bot.helpinfo['jrrp']
    del bot.helpinfo['xrxc']
def onInterval(bot):
    if hasattr(bot, 'jrrplist'):
        if len(bot.jrrplist) > 0:
            saveData(bot)
def onExit(bot, code, reason, error):
    if hasattr(bot, 'jrrplist'):
        if len(bot.jrrplist) > 0:
            saveData(bot)
def saveData(bot):
    filepath = bot.config['datapath'] + r'\jrrplist.txt'
    f = open(filepath, 'w', encoding='utf-8')
    f.write(str(bot.jrrplist))
    f.close()
def loadData(bot):
    filepath = bot.config['datapath'] + r'\jrrplist.txt'
    if os.path.isfile(filepath):
        f = open(filepath, 'r+', encoding='utf-8')
        s = f.read()
        bot.jrrplist = ast.literal_eval(s.strip('\ufeff'))
        f.close()
    else:
        bot.WARN('文件%s未找到' % filepath)
