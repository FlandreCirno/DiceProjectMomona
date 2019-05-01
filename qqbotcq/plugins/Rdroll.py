#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, os, ast
max_round = 100
max_side = 10000
def onQQMessage(bot, contact, member, content):
    if hasattr(bot, 'Momona_switch'):
        switch = bot.Momona_switch(bot, contact, member, content)
    else:
        switch = True
    if not(len(content) < 3 or bot.isMe(contact, member) or not switch):
        if hasattr(bot, 'Momona_msgParser'):
            content = bot.Momona_msgParser(bot, content)
        output = ''
        if len(content) < 3:
            pass
        elif (content[0] == '.' or content[0] == '。') and content[1:3].lower() == 'rd':
            error = 0
            msg = 0
            if not contact.ctype == 'buddy':
                uin = member.uin
            else:
                uin = contact.uin
            outstr = ''
            try:
                con = content.strip()
                exp = con[3:]
                if not len(exp) > 0:
                    exp = 'd'
                outstr, tempexp = formatexp(exp)
                if len(tempexp) == 0:
                    tempexp = 'd'
                elif tempexp.isdigit():
                    outstr = exp
                    tempexp = 'd'
                if error == 0:
                    exp = tempexp
                    rolldice = bot.dice(bot, contact, member, exp)
                    error = rolldice.error
            except:
                error = -1
            if error == 0:
                if rolldice.longresult == str(rolldice.result):
                    out = rolldice.strexp + '=' + str(rolldice.result)
                else:
                    out = rolldice.strexp + '=' + rolldice.longresult + '=' + str(rolldice.result)
                output = bot.Momona_text['rd_message']
                if len(outstr) == 0 and 'rd_noreason' in bot.Momona_text.keys():
                    output = bot.Momona_text['rd_noreason']
                output = output.replace('{reason}',outstr.strip()).replace('{result}',out)
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
        elif (content[0] == '.' or content[0] == '。') and content[1:4].lower() == 'set':
            error = 0
            if not contact.ctype == 'buddy':
                uin = member.uin
            else:
                uin = contact.uin
            con = content.strip()
            if len(con) == 4:
                error = 1
            else:
                con = con[4:].strip().lower().lstrip('d')
                if len(con) == 0:
                    error = 1
                elif con.isdigit():
                    num = int(con)
                    if num == 0:
                        error = -2
                    elif num > max_side:
                        error = 2
                else:
                    error = -1
            if error == 0:
                bot.defdice[uin] = num
                output = bot.Momona_text['set_success'].replace('{defdice}', str(num))
            elif error == 1:
                if uin in bot.defdice.keys():
                    del bot.defdice[uin]
                output = bot.Momona_text['set_reset']
            elif error == -1:
                output = bot.Momona_text['error_format']
            elif error == -2:
                output = bot.Momona_text['error_d0']
            elif error == 2:
                output = bot.Momona_text['error_toolarge']
        if len(output) > 0:
            bot.SendTo(contact, bot.Momona_msgFormater(bot, contact, member, output))
class dicelist():
    def __init__(self, bot, contact, member, exp):
        self.strexp = ''
        if contact.ctype == 'buddy':
            uin = contact.uin
        else:
            uin = member.uin
        if uin in bot.defdice.keys():
            self.defdice = bot.defdice[uin]
        else:
            self.defdice = 100
        self.exp = [exp]
        signs = ['+','-']
        for sign in signs:
            newexp = []
            for ex in self.exp:
                tempexp = ex.split(sign)
                for i in range(len(tempexp)-1):
                    tempexp.insert(i*2+1, sign)
                newexp = newexp + tempexp
            self.exp = newexp
        i = 2
        while i < len(self.exp):
            if len(self.exp[i]) == 0:
                self.exp = self.exp[:i-1] + self.exp[i+1:]
            else:
                i += 2
        if len(self.exp[0]) == 0:
            self.dicelist = [dice(exp = self.exp[2], sign = self.exp[1], defdice = self.defdice)]
            self.strexp = self.strexp + self.exp[1]
            self.exp = self.exp[2:]
        else:
            self.dicelist = [dice(exp = self.exp[0], defdice = self.defdice)]
        self.error = self.dicelist[0].error
        self.strexp = self.strexp + self.dicelist[0].exp
        for i in range(len(self.exp)//2):
            tempdice = dice(exp = self.exp[2*i+2], sign = self.exp[2*i+1], defdice = self.defdice)
            self.strexp = self.strexp + tempdice.sign + tempdice.exp
            self.dicelist.append(tempdice)
            if tempdice.error != 0:
                self.error = tempdice.error
        if not self.error:
            self.roll()
    def roll(self):
        self.result = 0
        self.longresult = ''
        for tempdice in self.dicelist:
            tempdice.roll()
            result = 0
            if result != None:
                self.longresult = self.longresult + tempdice.sign
                if isinstance(tempdice.result, list):
                    self.longresult = self.longresult + '('
                    for num in tempdice.result:
                        self.longresult = self.longresult + str(num) + '+'
                        result = result + num
                    self.longresult = self.longresult[:-1] + ')'
                else:
                    self.longresult = self.longresult + str(tempdice.result)
                    result = tempdice.result
                if tempdice.sign == '-':
                    self.result = self.result - result
                else:
                    self.result = self.result + result

class dice():
    def __init__(self, exp, sign = '', defdice = 100):
        self.error = 0
        self.sign = sign
        self.exp = exp
        exp = exp.lower()
        if 'd' in exp:
            count = exp[:exp.find('d')]
            if len(count) == 0:
                count = '1'
            num = exp[exp.find('d')+1:]
            if len(num) == 0:
                num = str(defdice)
                self.exp += num
            if count.isdigit() and num.isdigit():
                self.count = int(count)
                self.num = int(num)
                if self.num == 0:
                    self.error = -2
                elif self.count > max_round:
                    self.error = 1
                elif self.num > max_side:
                    self.error = 2
        else:
            self.roll = lambda: None
            if len(exp) == 0:
                self.result = None
                self.sign = ''
            else:
                self.result = int(exp)
    def roll(self):
        self.result = []
        for i in range(self.count):
            self.result.append(random.randint(1, self.num))
        if len(self.result) == 1:
            self.result = self.result[0]
        
        
def formatexp(exp):
    outexp = ''
    outstr = ''
    exp, items = extract(exp)
    exp = [exp]
    signs = ['+','-']
    for sign in signs:
        newexp = []
        for ex in exp:
            tempexp = ex.split(sign)
            for i in range(len(tempexp)-1):
                tempexp.insert(i*2+1, sign)
            newexp = newexp + tempexp
        exp = newexp
    for i in range(len(exp)//2 + 1):
        if i != 0 and len(exp[2*i]) != 0:
            outexp = outexp + exp[2*i - 1]
        if len(exp[2*i]) == 0:
            pass
        elif exp[2*i].isdigit():
            outexp = outexp + exp[2*i]
        elif exp[2*i].lower() == 'd' or exp[2*i].lower().strip() == 'd':
            outexp = outexp + exp[2*i].strip()
        else:
            foundexp = False
            if 'd' in exp[2*i].lower():
                index = exp[2*i].lower().find('d')
                i1 = index - 1
                i2 = index + 2
                if exp[2*i][i1:index].isdigit():
                    while exp[2*i][i1:index].isdigit():
                        i1 += -1
                        if i1 < 0:
                            break
                    i1 += 1
                else:
                    i1 = index
                if exp[2*i][index + 1:i2].isdigit():
                    while exp[2*i][index + 1:i2].isdigit():
                        i2 += 1
                        if i2 > len(exp[2*i]):
                            break
                    i2 += -1
                else:
                    i2 = index + 1
                if i1 != index or i2 != index + 1:
                    outstr += exp[2*i][0:i1] + exp[2*i][i2:len(exp[2*i])]
                    outexp = outexp + exp[2*i][i1:i2]
                    foundexp = True
            if not foundexp:
                loc = findnum(exp[2*i])
                if not loc == [-1,-1]:
                    outstr += exp[2*i][0:loc[0]] + exp[2*i][loc[1]:len(exp[2*i])]
                    outexp = outexp + exp[2*i][loc[0]:loc[1]]
                else:
                    outstr += exp[2*i]
    outstr = putback(outstr, items)
    return outstr, outexp
    
def extract(str):
    i1 = str.find('{')
    output = []
    while i1 != -1:
        i2 = str.find('}', i1)
        if i2 == -1:
            break
        output.append(str[i1:i2+1])
        str = str[:i1+1] + str[i2:]
        i1 = str.find('{', i1+1)
    return str, output

def putback(str, items):
    i = str.find('{}')
    for item in items:
        str = str[:i] + str[i:].replace('{}', item, 1)
        i = i + len(item)
        i = str.find('{}', i)
    return str
        
def findnum(str):
    index = 0
    for i in range(len(str)):
        if str[i].isdigit():
            index = i
            break
    i = index + 1
    while i <= len(str):
        if str[index:i].isdigit():
            i += 1
        else:
            i += -1
            break
    if index == i or index >= len(str):
        return [-1,-1]
    else:
        return [index,min(i,len(str))]
    
def onPlug(bot):
    if not hasattr(bot, 'helpinfo'):
        bot.helpinfo = {}
    bot.helpinfo['rd'] = [['表达式'],bot.Momona_text['helpinfo_rd']]
    bot.helpinfo['set'] = [['默认骰'],bot.Momona_text['helpinfo_set']]
    loadData(bot)
    if not hasattr(bot, 'defdice'):
        bot.defdice = {}
    bot.dice = dicelist
    bot.formatexp = formatexp
    bot.findnum = findnum
    if 'maxround' in bot.config.keys():
        global max_round = bot.config['maxround']
    if 'maxside' in bot.config.keys():
        global max_side = bot.config['maxside']
def onUnplug(bot):
    saveData(bot)
    del bot.dice
    del bot.defdice
    del bot.helpinfo['rd']
    del bot.helpinfo['set']
    del bot.formatexp
    del bot.findnum
def onInterval(bot):
    saveData(bot)
def saveData(bot):
    filepath = bot.config['datapath'] + r'\defdice.txt'
    f = open(filepath, 'w', encoding='utf-8')
    f.write(str(bot.defdice))
    f.close()
def loadData(bot):
    filepath = bot.config['datapath'] + r'\defdice.txt'
    if os.path.isfile(filepath):
        f = open(filepath, 'r+', encoding='utf-8')
        s = f.read()
        bot.defdice = ast.literal_eval(s.strip('\ufeff'))
        f.close()
    else:
        bot.WARN('文件%s未找到' % filepath)