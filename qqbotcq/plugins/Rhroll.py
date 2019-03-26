#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, os, ast
def onQQMessage(bot, contact, member, content):
    if hasattr(bot, 'Momona_switch'):
        switch = bot.Momona_switch(bot, contact, member, content)
    else:
        switch = True
    if not(len(content) < 3 or bot.isMe(contact, member) or not switch):
        output = ''
        if hasattr(bot, 'Momona_msgParser'):
            content = bot.Momona_msgParser(bot, content)
        if len(content) < 3:
            pass
        elif (content[0] == '.' or content[0] == '。') and content[1:3].lower() == 'rh' and not contact.ctype == 'buddy':
            rhcontact = member
            outstr = ''
            error = 0
            try:
                con = content.strip()
                if len(con) > 3:
                    exp = con[3:]
                    if not len(exp) > 0:
                        exp = 'd'
                    outstr, tempexp = bot.formatexp(exp)
                    if len(tempexp) == 0:
                        tempexp = 'd'
                    elif tempexp.isdigit():
                        outstr = exp
                        tempexp = 'd'
                    if error == 0:
                        exp = tempexp
                        rolldice = bot.dice(bot, contact, member, exp)
                        error = rolldice.error
                else:
                    exp = 'd'
                    rolldice = bot.dice(bot, contact, member, exp)
            except:
                error = -1
            if error == 0:
                if rolldice.longresult == str(rolldice.result):
                    out = rolldice.strexp + '=' + str(rolldice.result)
                else:
                    out = rolldice.strexp + '=' + rolldice.longresult + '=' + str(rolldice.result)
                bot.SendTo(contact, bot.Momona_msgFormater(bot, contact, member, bot.Momona_text['rh_message']))
                result = bot.Momona_text['rh_results'].replace('{reason}', outstr.strip())
                result = result.replace('{groupname}', contact.name).replace('{result}', out)
                result = bot.Momona_msgFormater(bot, contact, member, result)
                bot.SendTo(rhcontact, result)
                if contact.uin in bot.rhlist:
                    for k,rhmember in bot.rhlist[contact.uin].items():
                        if k != member.uin:
                            bot.SendTo(rhmember, result)
            elif error == -1:
                output = bot.Momona_text['error_format']
            elif error == -2:
                output = bot.Momona_text['error_d0']
            elif error == 1:
                output = bot.Momona_text['error_toomany']
            elif error == 2:
                output = bot.Momona_text['error_toolarge']
            else:
                output = bot.Momona_text['error_unknown']
        elif (content[0] == '.' or content[0] == '。') and content[1:3].lower() == 'ob' and not contact.ctype == 'buddy':
            if not contact.uin in bot.rhlist:
                bot.rhlist[contact.uin] = {}
            if 'list' in content[3:].strip().lower():
                if contact.uin in bot.rhlist:
                    if len(bot.rhlist[contact.uin]) > 0:
                        outstr = ''
                        for k,rhmember in bot.rhlist[contact.uin].items():
                            outstr = outstr + rhmember.name + "(" + k + ")\n"
                        output = bot.Momona_text['ob_list']
                        output = output.replace('{oblist}', outstr[:-1])
                        
                    else:
                        output = bot.Momona_text['ob_listempty']
                else:
                    output = bot.Momona_text['ob_listempty']
            else:
                if not member.uin in bot.rhlist[contact.uin]:
                    bot.rhlist[contact.uin][member.uin] = member
                    output = bot.Momona_text['ob_on']
                else:
                    del bot.rhlist[contact.uin][member.uin]
                    output = bot.Momona_text['ob_off']
            if len(output) > 0:
                bot.SendTo(contact, bot.Momona_msgFormater(bot, contact, member, output))
def onPlug(bot):
    if not hasattr(bot, 'helpinfo'):
        bot.helpinfo = {}
    bot.rhlist = {}
    bot.helpinfo['rh'] = [['表达式'],bot.Momona_text['helpinfo_rh']]
    bot.helpinfo['ob'] = [['list'],bot.Momona_text['helpinfo_ob']]
def onUnplug(bot):
    del bot.helpinfo['rh']
    del bot.helpinfo['ob']
