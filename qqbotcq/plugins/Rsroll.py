#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, os, ast
max_skill = 1000
skillroll_type = 0
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
        elif (content[0] == '.' or content[0] == '。') and content[1:3].lower() in ['rs','rb','rp']:
            error = 0
            if not contact.ctype == 'buddy':
                uin = member.uin
            else:
                uin = contact.uin
            cmd = content[1:3].lower()
            round = 1
            con = content[3:]
            if cmd != 'rs':
                loc = bot.findnum(con)
                if loc[0] == 0:
                    round = max(int(con[loc[0]:loc[1]]), 1)
                    con = con[loc[1]:]
            con = con.strip()
            if len(con) > 0:
                skl = ""
                loc = bot.findnum(con)
                if not loc == [-1,-1]:
                    skl = con[loc[0]:loc[1]]
                    con = con[:loc[0]] + con[loc[1]:]
                if skl.isdigit():
                    skl = int(skl)
                    if skl > max_skill:
                        error = 3
                else:
                    sklname, skl = loadsta(bot, uin, con)
                    if sklname and skl:
                        con = sklname
                    else:
                        error = 1
            else:
                error = 2
            result = random.randint(1, 100)
            digit = result % 10
            if round > 100:
                error = 5
            elif cmd == 'rb':
                rolls = [random.randint(0, 9) for x in range(round)]
                longresult = str(result) + '[奖励骰：'
                for num in rolls:
                    longresult = longresult + str(num) + ', '
                    tempresult = digit + num * 10
                    if tempresult == 0:
                        tempresult = 100
                    if tempresult < result:
                        result = tempresult
                longresult = longresult[:-2] + '] = ' + str(result)
            elif cmd == 'rp':
                rolls = [random.randint(0, 9) for x in range(round)]
                longresult = str(result) + '[惩罚骰：'
                for num in rolls:
                    longresult = longresult + str(num) + ', '
                    tempresult = digit + num * 10
                    if tempresult == 0:
                        tempresult = 100
                    if tempresult > result:
                        result = tempresult
                longresult = longresult[:-2] + '] = ' + str(result)
            else:
                longresult = str(result)
            if error == 0:
                slv = successlevel(result, skl)
                output = bot.Momona_text['rs_results']
                output = output.replace('{skill}', con).replace('{value}', str(skl))
                output = output.replace('{result}', longresult).replace('{successlevel}', bot.Momona_text['rs_successlevels'][slv])
            elif error == 2:
                output = bot.Momona_text['rs_noskill'].replace('{result}', longresult)
            elif error == 1:
                output = bot.Momona_text['rs_skillnotfound'].replace('{skill}', con)
            elif error == 3:
                output = bot.Momona_text['st_skilltoolarge'].replace('{maxskill}', str(max_skill))
            elif error == 5:
                output = bot.Momona_text['rs_toomany']
            else:
                output = bot.Momona_text['error_unknown']
        elif (content[0] == '.' or content[0] == '。') and content[1:3].lower() == 'st':
            error = 0
            if not contact.ctype == 'buddy':
                uin = member.uin
            else:
                uin = contact.uin
            exp = []
            con = content[3:]
            con = rmsym(con)
            if con.isdigit():
                error = 6
            if 'clear' in con.lower():
                if con.lower().find('clear') == 0:
                    exp = ['clear']
                else:
                    exp = [con[0:con.lower().find('clear')],'clear']
                error = 7
            if error == 0 and len(con) == 0:
                error = 6
            if error == 0:
                if bot.findnum(con) == [-1,-1]:
                    error = 5
                    exp = [con]
                else:
                    while bot.findnum(con) != [-1,-1]:
                        loc = bot.findnum(con)
                        if loc[0] != 0:
                            exp.append(con[:loc[0]])
                            exp.append(int(con[loc[0]:loc[1]]))
                        con = con[loc[1]:]
            if error == 0:
                if len(exp) % 2 != 0:
                    exp = exp[:-1]
                for i in range(int(len(exp)/2)):
                    if exp[2*i+1] > max_skill:
                        error = 3
            if error == 0:
                if len(exp) == 2:
                    savesta(bot, uin, exp[0], exp[1])
                    output = bot.Momona_text['st_skill'].replace('{skill}',exp[0]).replace('{value}',str(exp[1]))
                else:
                    for i in range(int(len(exp)/2)):
                        savesta(bot, uin, exp[2*i], exp[2*i+1])
                    output = bot.Momona_text['st_multiple']
            elif error == 3:
                output = bot.Momona_text['st_skilltoolarge'].replace('{maxskill}', str(max_skill))
            elif error == 5:
                sklname, skl = loadsta(bot, uin, exp[0])
                if sklname and skl:
                    output = bot.Momona_text['st_showskill'].replace('{skill}',sklname).replace('{value}',str(skl))
                else:
                    output = bot.Momona_text['st_skillnotfound'].replace('{skill}',exp[0])
            elif error == 6:
                skllist = loadsta(bot, uin)[1]
                if skllist:
                    outstr = ''
                    for k,v in skllist.items():
                        outstr = outstr + k + '：' + str(v) + '\n'
                    outstr = outstr[:-1]
                    output = bot.Momona_text['st_showallskill'].replace('{skill}', outstr)
                else:
                    output = bot.Momona_text['st_noskill']
            elif error == 7:
                if len(exp) == 2:
                    if uin in bot.stlist:
                        if exp[0] in bot.stlist[uin]:
                            del bot.stlist[uin][exp[0]]
                    output = bot.Momona_text['st_clear'].replace('{skill}',exp[0])
                else:
                    if uin in bot.stlist:
                        del bot.stlist[uin]
                    output = bot.Momona_text['st_clearall']
            else:
                output = bot.Momona_text['error_unknown']
        elif (content[0] == '.' or content[0] == '。') and content[1:3].lower() == 'en':
            error = 0
            if not contact.ctype == 'buddy':
                uin = member.uin
            else:
                uin = contact.uin
            if len(content) > 3:
                con = content[3:].split()
                if len(con) > 0:
                    skl = ""
                    loc = bot.findnum(con[0])
                    if not loc == [-1,-1]:
                        skl = con[0][loc[0]:loc[1]]
                        con[0] = con[0][:loc[0]] + con[0][loc[1]:]
                    if skl.isdigit():
                        skl = int(skl)
                        if skl > max_skill:
                            error = 3
                    else:
                        sklname, skl = loadsta(bot, uin, con[0])
                        if sklname and skl:
                            con[0] = sklname
                        else:
                            error = 6
                    if error == 0:
                        outexp = ''
                        if len(con) > 1:
                            outstr, outexp = bot.formatexp(con[1])
                        if len(outexp) == 0:
                            outexp = 'd10'
                        results = bot.dice(bot, contact, member, outexp)
                        if results.error:
                            error = results.error
                else:
                    error = 5
            else:
                error = 5
            result = random.randint(1, 100)
            if error == 0:
                increase = results.result
                if results.longresult == str(results.result):
                    out = results.strexp + '=' + str(results.result)
                else:
                    out = results.strexp + '=' + results.longresult + '=' + str(results.result)
                slv = successlevel(result, skl)
                if result > min(skl, 95):
                    output = bot.Momona_text['en_success'].replace('{skill}', con[0]).replace('{value}', str(skl))
                    output = output.replace('{result}',str(result)).replace('{currentvalue}', str(skl + increase)).replace('{increase}', str(increase))
                    skl += increase
                else:
                    output = bot.Momona_text['en_failed'].replace('{skill}', con[0]).replace('{value}', str(skl))
                    output = output.replace('{result}',str(result)).replace('{currentvalue}', str(skl + increase))
                if len(con[0]) > 0:
                    savesta(bot, uin, con[0], skl)
            elif error == -1:
                output = bot.Momona_text['error_format']
            elif error == -2:
                output = bot.Momona_text['error_d0']
            elif error == 1:
                output = bot.Momona_text['error_toomany']
            elif error == 2:
                output = bot.Momona_text['error_toolarge']
            elif error == 3:
                output = bot.Momona_text['st_skilltoolarge'].replace('{maxskill}', str(max_skill))
            elif error == 5:
                output = bot.Momona_text['en_noskill']
            elif error == 6:
                output = bot.Momona_text['st_skillnotfound'].replace('{skill}',con[0])
            else:
                output = bot.Momona_text['error_unknown']
        if len(output) > 0:
            bot.SendTo(contact, bot.Momona_msgFormater(bot, contact, member, output))
def rmsym(str):
    symbols = ',.|:，。：\n '
    for s in symbols:
        str = str.replace(s, '')
    return str
def savesta(bot, uin, name, sta):
    if not uin in bot.stlist:
        bot.stlist[uin] = {}
    bot.stlist[uin][name] = sta
def loadsta(bot, uin, name = None):
    if uin in bot.stlist:
        if name == None:
            return None, bot.stlist[uin]
        elif name in bot.stlist[uin]:
            return name, bot.stlist[uin][name]
        else:
            for k in bot.stlist[uin].keys():
                if k in name or name in k:
                    return k, bot.stlist[uin][k]
    return None, None
def delsta(bot, uin, name):
    sklname, skl = loadsta(bot, uin, name)
    if sklname and skl:
        del bot.stlist[uin][sklname]
        return True
    else:
        return False
def successlevel(result, skill, type = skillroll_type):
    if type == 1:
        fumble = 96
        criticalsuccess = 5
    else:
        if skill >= 50:
            fumble = 100
        else:
            fumble = 96
        criticalsuccess = 1
    if result <= criticalsuccess:
        return 0
    elif result >= fumble:
        return 5
    elif result * 5 <= skill:
        return 1
    elif result * 2 <= skill:
        return 2
    elif result <= skill:
        return 3
    else:
        return 4
def onPlug(bot):
    if not hasattr(bot, 'helpinfo'):
        bot.helpinfo = {}
    bot.helpinfo['rs'] = [['技能'],bot.Momona_text['helpinfo_rs']]
    bot.helpinfo['rb'] = [['次数', '技能'],bot.Momona_text['helpinfo_rb']]
    bot.helpinfo['rp'] = [['次数', '技能'],bot.Momona_text['helpinfo_rp']]
    bot.helpinfo['st'] = [['技能名称/clear', '数值/clear'],bot.Momona_text['helpinfo_st']]
    bot.helpinfo['en'] = [['技能', '成长数值'],bot.Momona_text['helpinfo_en']]
    bot.loadsta = loadsta
    bot.savesta = savesta
    loadData(bot)
    if not hasattr(bot, 'stlist'):
        bot.WARN('属性表已重置')
        bot.stlist = {}
    if 'skillrolltype' in bot.config.keys():
        global skillroll_type = bot.config['skillrolltype']
    if 'maxskill' in bot.config.keys():
        global max_skill = bot.config['maxskill']
def onUnplug(bot):
    saveData(bot)
    del bot.helpinfo['rs']
    del bot.helpinfo['rb']
    del bot.helpinfo['rp']
    del bot.helpinfo['st']
    del bot.helpinfo['en']
    del bot.stlist
    del bot.loadsta
    del bot.savesta
def onInterval(bot):
    if hasattr(bot, 'stlist'):
        if len(bot.stlist) > 0:
            saveData(bot)
def onExit(bot, code, reason, error):
    if hasattr(bot, 'stlist'):
        if len(bot.stlist) > 0:
            saveData(bot)
def saveData(bot):
    filepath = bot.config['datapath'] + r'\stlist.txt'
    f = open(filepath, 'w', encoding='utf-8')
    f.write(str(bot.stlist))
    f.close()
def loadData(bot):
    filepath = bot.config['datapath'] + r'\stlist.txt'
    if os.path.isfile(filepath):
        f = open(filepath, 'r+', encoding='utf-8')
        s = f.read()
        bot.stlist = ast.literal_eval(s.strip('\ufeff'))
        f.close()
        bot.INFO('属性表读取成功')
    else:
        bot.WARN('文件%s未找到' % filepath)
