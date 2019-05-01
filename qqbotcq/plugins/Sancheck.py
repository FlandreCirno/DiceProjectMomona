#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
sancheck_type = 0
max_san = 1000
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
        elif (content[0] == '.' or content[0] == '。') and content[1:3].lower() == 'sc':
            error = 0
            if not contact.ctype == 'buddy':
                group = contact.uin
                uin = member.uin
            else:
                group = 'buddy'
                uin = contact.uin
            status = loadsan(bot, uin)
            if status != None:
                if len(content) > 3:
                    exp = content[3:].replace(' ','').split('/')
                    while '' in exp:
                        exp.remove('')
                    if len(exp) == 1:
                        exp.append(exp[0])
                    if len(exp) == 2:
                        outstr, success = bot.formatexp(exp[0])
                        if not len(success) > 0:
                            error = 3
                        outstr, failed = bot.formatexp(exp[1])
                        if not len(failed) > 0:
                            error = 3
                        if error == 0:
                            successdice = bot.dice(bot, contact, member, success)
                            faileddice = bot.dice(bot, contact, member, failed)
                            if successdice.error:
                                error = successdice.error
                            if faileddice.error:
                                error = faileddice.error
                    else:
                        error = 3
                else:
                    error = 3
            else:
                error = 4
            sancheck = random.randint(1, 100)
            if error == 0:
                if sancheck_type == 1:
                    scbase = status[0]
                else:
                    scbase = status[1]
                if sancheck > scbase or sancheck > 95:
                    output = bot.Momona_text['sc_failed']
                    result = faileddice
                else:
                    output = bot.Momona_text['sc_success']
                    result = successdice
                if result.longresult == str(result.result):
                    longresult = result.strexp + '=' + str(result.result)
                else:
                    longresult = result.strexp + '=' + result.longresult + '=' + str(result.result)
                finalsan = min(max(status[1] - result.result, 0), status[2])
                output = output.replace('{sancheck}', str(sancheck)).replace('{result}', longresult)
                output = output.replace('{san}', str(status[1])).replace('{sanmax}', str(status[2]))
                output = output.replace('{finalsan}', str(finalsan)).replace('{pow}', str(status[0]))
                status[1] = finalsan
                savesan(bot, uin, status)
            elif error == -1:
                output = bot.Momona_text['error_format']
            elif error == -2:
                output = bot.Momona_text['error_d0']
            elif error == 1:
                output = bot.Momona_text['error_toomany']
            elif error == 2:
                output = bot.Momona_text['error_toolarge']
            elif error == 3:
                output = bot.Momona_text['sc_sanerror']
            elif error == 4:
                output = bot.Momona_text['sc_sannotfound']
            else:
                output = bot.Momona_text['error_unknown']
        elif (content[0] == '.' or content[0] == '。') and content[1:4].lower() == 'san':
            error = 0
            if not contact.ctype == 'buddy':
                uin = member.uin
            else:
                uin = contact.uin
            status = []
            exp = content[4:].split()
            if len(exp) == 0:
                error = 5
            elif len(exp) == 1:
                exp.append(exp[0])
                if sancheck_type == 1:
                    exp.append(exp[0])
                else:
                    exp.append('99')
            elif len(exp) == 2:
                if sancheck_type == 1:
                    exp.append(exp[0])
                else:
                    exp.append('99')
            if error == 0:
                for i in range(3):
                    if exp[i].isdigit():
                        sts = int(exp[i])
                        if sts > max_san:    
                            error = 3
                        if sts < 1:
                            error = 4
                        else:
                            status.append(int(exp[i]))
                    else:
                        error = -1
                if len(status) >= 3:
                    if status[1] > status[2]:
                        error = 6
            if error == 0:
                savesan(bot, uin, status)
                output = bot.Momona_text['san_set']
                output = output.replace('{san}', str(status[1])).replace('{sanmax}', str(status[2]))
                output = output.replace('{pow}', str(status[0]))
            elif error == -1:
                output = bot.Momona_text['san_error']
            elif error == 3:
                output = bot.Momona_text['st_skilltoolarge'].replace('{maxskill}', str(max_san))
            elif error == 4:
                output = bot.Momona_text['san_0']
            elif error == 5:
                status = loadsan(bot, uin)
                if status != None:
                    output = bot.Momona_text['san_show']
                    output = output.replace('{san}', str(status[1])).replace('{sanmax}', str(status[2]))
                    output = output.replace('{pow}', str(status[0]))
                else:
                    output = bot.Momona_text['san_notset']
            elif error == 6:
                output = bot.Momona_text['san_exceedmax']
            else:
                output = bot.Momona_text['error_unknown']
        if len(output) > 0:
            bot.SendTo(contact, bot.Momona_msgFormater(bot, contact, member, output))
def loadsan(bot, uin):
    name1, san = bot.loadsta(bot, uin, 'san')
    name2, sanmax = bot.loadsta(bot, uin, 'sanmax')
    name3, power = bot.loadsta(bot, uin, '意志')
    if [name1, name2, name3] != ['san', 'sanmax', '意志']:
        if name1 != 'san':
            if name3 != '意志':
                return None
            else:
                san = power
                if name2 != 'sanmax':
                    if sancheck_type == 1:
                        sanmax = power
                    else:
                        sanmax = 99
        else:
            if name3 != '意志':
                power = san
            if name2 != 'sanmax':
                if sancheck_type == 1:
                    sanmax = power
                else:
                    sanmax = 99
    return [power, san, sanmax]
def savesan(bot, uin, san):
    bot.savesta(bot, uin, '意志', san[0])
    bot.savesta(bot, uin, 'san', san[1])
    bot.savesta(bot, uin, 'sanmax', san[2])
def onPlug(bot):
    if not hasattr(bot, 'helpinfo'):
        bot.helpinfo = {}
    bot.helpinfo['san'] = [['意志','当前理智','理智上限'],bot.Momona_text['helpinfo_san']]
    bot.helpinfo['sc'] = [['成功/失败理智扣除'],bot.Momona_text['helpinfo_sc']]
    if 'sanchecktype' in bot.config.keys():
        global sancheck_type = bot.config['sanchecktype']
    if 'maxskill' in bot.config.keys():
        global max_san = bot.config['maxskill']
def onUnplug(bot):
    del bot.sanlist
    del bot.helpinfo['sc']
    del bot.helpinfo['san']
