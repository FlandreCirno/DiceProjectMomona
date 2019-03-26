#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
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
        elif (content[0] == '.' or content[0] == '。') and content[1:5].lower() == 'coc7':
            error = 0
            try:
                con = content.replace(' ','')
                if len(con) > 5:
                    con = con[5:]
                    if con.isdigit():
                        num = int(con)
                        if num > 10:
                            error = 2
                        elif num == 0:
                            num = 1
                    else:
                        num = 1
                else:
                    num = 1
            except:
                error = -1
            if error == 0:
                characteristics = ''
                for i in range(num):
                    temp = ''
                    sta = [Roll3d6(), Roll3d6(), Roll2d66(), Roll3d6(), Roll3d6(), Roll2d66(), Roll3d6(), Roll2d66(), Roll3d6()]
                    sum = 0
                    for nu in sta:
                        sum += nu
                    temp += "力量:" + str(sta[0]) + " 体质:" + str(sta[1]) + " 体型:" + str(sta[2]) + " 敏捷:" + str(sta[3])
                    temp += " 容貌:" + str(sta[4]) + " 智力:" + str(sta[5]) + " 意志:" + str(sta[6]) + " 教育:" + str(sta[7])
                    temp += " 幸运:" + str(sta[8]) + " 总计:" + str(sum)
                    characteristics += temp + '\n'
                characteristics = characteristics[:-1]
                output = bot.Momona_text['coc7'].replace('{result}', characteristics)
            elif error == 2:
                output = bot.Momona_text['coc7_toomany']
            else:
                output = bot.Momona_text['error_unknown']
        if len(output) > 0:
            bot.SendTo(contact, bot.Momona_msgFormater(bot, contact, member, output))
def Roll2d66():
    return (random.randint(1, 6) + random.randint(1, 6) + 6) * 5
def Roll3d6():
    return (random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)) * 5
def onPlug(bot):
    if not hasattr(bot, 'helpinfo'):
        bot.helpinfo = {}
    bot.helpinfo['coc7'] = [['个数'],bot.Momona_text['helpinfo_coc7']]
def onUnplug(bot):
    del bot.helpinfo['coc7']
