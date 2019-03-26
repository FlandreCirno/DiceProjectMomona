#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, os, ast, requests

def onQQMessage(bot, contact, member, content):
    if hasattr(bot, 'Momona_switch'):
        switch = bot.Momona_switch(bot, contact, member, content)
    else:
        switch = True
    if not(len(content) < 6 or bot.isMe(contact, member) or not switch):
        output = ''
        if hasattr(bot, 'Momona_msgParser'):
            content = bot.Momona_msgParser(bot, content)
        if len(content) < 6:
            pass
        elif (content[0] == '.' or content[0] == '。') and content[1:6].lower() == 'rules':
            error = 0
            rulename = content[6:].strip()
            if len(rulename) > 0:
                try:
                    rule = getrule(bot, rulename)
                    if not rule:
                        error = 1
                except Exception as e:
                    error = -2
                    errormsg = str(e)
            else:
                error = 2
            if error == 0:
                output = bot.Momona_text['rules'].replace('{rule}', rule).replace('{rulename}', rulename)
            elif error == 1:
                output = bot.Momona_text['rules_notfound'].replace('{rulename}', rulename)
            elif error == 2:
                output = bot.Momona_text['rules_empty']
            elif error == -2:
                output = bot.Momona_text['rules_error'].replace('{error}', errormsg)
            else:
                output = bot.Momona_text['error_unknown']
        if len(output) > 0:
            bot.SendTo(contact, bot.Momona_msgFormater(bot, contact, member, output))


def getrule(bot, rulename, ruletype = 'Rules-COC7'):
    result = requests.post("http://api.kokona.tech:5555/rules", data={'Type': ruletype, 'Name': rulename, 'QQ': bot.qq, 'v': '20190114'})
    if result.status_code != 200:
        raise Exception('Network Error! Status code: ' + str(result.status_code))
    return result.text


def onPlug(bot):
    if not hasattr(bot, 'helpinfo'):
        bot.helpinfo = {}
    bot.helpinfo['rules'] = [['关键词'],bot.Momona_text['helpinfo_rules']]


def onUnplug(bot):
    del bot.helpinfo['rules']
