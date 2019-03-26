#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, os, ast, requests, json
def onQQMessage(bot, contact, member, content):
    if not bot.isMe(contact, member):
        switch = bot.Momona_switch(bot, contact, member, content)
        if len(content) >= 2:
            output = ''
            content = Momona_msgParser(bot, content)
            if len(content) < 2:
                pass
            elif (content[0] == '.' or content[0] == '。') and content[1:5].lower() == 'help' and switch:
                if len(content.strip()) == 5:
                    temp = ''
                    for k,l in bot.helpinfo.items():
                        temp += '.' + k + ' '
                        for p in l[0]:
                            temp += '[' + p + '] '
                        temp += l[1][0] + '\n'
                    output = bot.Momona_text['help']
                    output = output.replace('{helpinfo}', temp)
                elif content[5:].strip().lower() == 'all':
                    temp = ''
                    for k,l in bot.helpinfo.items():
                        temp += '.' + k + ' '
                        for p in l[0]:
                            temp += '[' + p + '] '
                        temp += l[1][0] + '，' + l[1][1] + '\n'
                    output = bot.Momona_text['help_all']
                    output = output.replace('{helpinfo}', temp)
                else:
                    temp = ''
                    con = content[5:].strip().lower()
                    for k,l in bot.helpinfo.items():
                        if con == k:
                            temp = '.' + k + ' '
                            for p in l[0]:
                                temp += '[' + p + '] '
                            temp += l[1][0] + '，' + l[1][1]
                    if len(temp) > 0:
                        output = bot.Momona_text['help_command']
                        output = output.replace('{helpinfo}', temp)
                    else:
                        output = bot.Momona_text['help_nocommand']
                        output = output.replace('{command}', con)
                output = output.replace('{version}', bot.Momona_ver)
            elif (content[0] == '.' or content[0] == '。') and content[1:4].lower() == 'bot':
                switch = None
                id = [bot.qq, bot.qq[-4:]]
                if 'nickname' in bot.config.keys():
                    id.append(bot.config['nickname'])
                if len(content) == 4:
                    output = bot.Momona_text['bot']
                elif content[4:].lower().replace(' ','') in ['off' + x for x in id] + ['off']:
                    switch = False    
                elif content[4:].lower().replace(' ','') in ['on' + x for x in id] + ['on']:
                    switch = True
                if not switch == None:
                    if contact.ctype == 'buddy':
                        bot.Momona_var['switch']['buddy'][contact.uin] = switch
                    else:
                        bot.Momona_var['switch'][contact.uin] = switch
                    if switch:
                        output = bot.Momona_text['bot_on']
                    else:
                        output = bot.Momona_text['bot_off']
                output = output.replace('{version}', bot.Momona_ver)
            elif (content[0] == '!' or content[0] == '！') and content[1:8].lower() == 'dismiss':
                dismiss = False
                if len(content) == 8:
                    dismiss = True
                elif content[8:].lower().strip() == bot.qq:
                    dismiss = True
                elif 'nickname' in bot.config.keys():
                    if content[8:].lower().strip() == bot.config['nickname']:
                        dismiss = True
                if dismiss and contact.ctype != 'buddy':
                    if bot.isManager(contact, member):
                        try:
                            bot.SendTo(contact, Momona_msgFormater(bot, contact, member, bot.Momona_text['dismiss']))
                        except:
                            pass
                        bot.Quit(contact)
                    else:
                        output = bot.Momona_text['dismiss_failed']
            elif (content[0] == '.' or content[0] == '。') and content[1:3].lower() == 'nn' and switch:
                if contact.ctype == 'buddy':
                    uin = contact.uin
                else:
                    uin = member.uin
                if len(content) == 3:
                    output = Momona_msgFormater(bot, contact, member, bot.Momona_text['name_reset'])
                    if uin in bot.Momona_var['name']:
                        del bot.Momona_var['name'][uin]
                else:
                    newname = content[3:]
                    newname = removechar(newname)
                    if newname == '':
                        output = bot.Momona_text['name_empty']
                    else:
                        output = Momona_msgFormater(bot, contact, member, bot.Momona_text['name_set'])
                        bot.Momona_var['name'][uin] = newname
                        output = output.replace('{newname}', newname)
            elif (content[0] == '.' or content[0] == '。') and content[1:8].lower() == 'welcome' and switch and contact.ctype == 'group':
                if bot.isManager(contact, member):
                    if len(content.strip()) == 8:
                        if contact.uin in bot.Momona_var['welcome'].keys():
                            del bot.Momona_var['welcome'][contact.uin]
                        output = bot.Momona_text['welcome_off']
                    else:
                        if contact.uin in bot.Momona_var['welcome'].keys():
                            output = bot.Momona_text['welcome_change']
                        else:
                            output = bot.Momona_text['welcome_on']
                        bot.Momona_var['welcome'][contact.uin] = removechar(content[8:])
                else:
                    output = bot.Momona_text['welcome_error']
            elif content == '--version' or content == '-V':
                bot.SendTo(contact, bot.Momona_ver + ' powered by QQbot and CoolQ\nwraper version ' + bot.version )
            if len(output) > 0:
                bot.SendTo(contact, Momona_msgFormater(bot, contact, member, output))
def onPlug(bot):
    if not hasattr(bot, 'helpinfo'):
        bot.helpinfo = {}
    loadData(bot)
    bot.helpinfo['bot'] = [['on/off', 'QQ号'], bot.Momona_text['helpinfo_bot']]
    bot.helpinfo['nn'] = [['名称'], bot.Momona_text['helpinfo_nn']]
    bot.helpinfo['welcome'] = [['欢迎语'], bot.Momona_text['helpinfo_welcome']]
    if not hasattr(bot, 'Momona_var'):
        bot.Momona_var = {'switch':{'buddy':{}},'name':{},'blacklist':{},'welcome':{}}
    bot.Momona_name = Momona_name
    bot.Momona_switch = Momona_switch
    bot.Momona_msgParser = Momona_msgParser
    bot.Momona_msgFormater = Momona_msgFormater
    bot.Momona_ver = 'DiceProjectMomona ver. 1.4.3'
    bot.AddBlackList = AddBlackList
    bot.isBlacklisted = isBlacklisted
def onUnplug(bot):
    saveData(bot)
    del bot.helpinfo['bot']
    del bot.helpinfo['nn']
    del bot.helpinfo['welcome']
    del bot.Momona_name
    del bot.Momona_switch
    del bot.Momona_var
    del bot.Momona_text
    del bot.Momona_ver
    del bot.Momona_msgParser
    del bot.Momona_msgFormater
    del bot.AddBlackList
    del bot.isBlacklisted
def onEvent(bot, contact, operator, target, type, sub_type):
    if type == 'group_decrease':
        onGroupQuit(bot, contact, operator, target, sub_type)
    elif type == 'group_increase':
        onGroupAdd(bot, contact, operator, target, sub_type)
def onGroupQuit(bot, contact, operator, target, type):
    pass
def onGroupAdd(bot, contact, operator, target, type):
    if bot.isMe(contact, target) and 'join' in bot.Momona_text.keys():
        if len(bot.Momona_text['join']) > 0:
            bot.SendTo(contact, Momona_msgFormater(bot, contact, operator, bot.Momona_text['join']))
    else:
        if contact.uin in bot.Momona_var['welcome'].keys():
            bot.SendTo(contact, Momona_msgFormater(bot, contact, target, bot.Momona_var['welcome'][contact.uin]))
def Momona_name(bot, contact, member, content):
    if contact.ctype == 'buddy':
        if contact.uin in bot.Momona_var['name']:
            return bot.Momona_var['name'][contact.uin]
        else:
            return removechar(contact.name)
    else:
        if member.uin in bot.Momona_var['name']:
            return bot.Momona_var['name'][member.uin]
        else:
            return removechar(member.name)
def removechar(name):
    return name.lstrip(' .。!！\n\r')
def keyreplace(bot, message, keys):
    if isinstance(keys, str):
        message = message.replace('{' + keys + '}', bot.Momona_text[keys])
    else:
        for key in keys:
            message = message = message.replace('{' + key + '}', bot.Momona_text[key])
    return message
def Momona_switch(bot, contact, member, content):
    if contact.ctype == 'buddy':
        if contact.uin in bot.Momona_var['switch']['buddy']:
            return bot.Momona_var['switch']['buddy'][contact.uin] and not isBlacklisted(bot, contact, member)
        return True
    else:
        if contact.uin in bot.Momona_var['switch']:
            return bot.Momona_var['switch'][contact.uin] and not isBlacklisted(bot, contact, member)
        return True
def Momona_msgParser(bot, content):
    content = content.lstrip('\n ')
    atme = '[CQ:at,qq=' + bot.qq + ']'
    if content.find(atme) == 0:
        content = content.replace(atme, '', 1)
        content = content.lstrip('\n ')
    if content[:1] in '.。!！':
        i1 = content.find('[CQ:')
        while i1 != -1:
            i2 = content.find(']', i1)
            if i2 == -1:
                break
            content = content.replace('[CQ:', '{CQ:', 1)
            content = content[:i2] + '}' + content[i2+1:]
            i1 = content.find('[CQ:')
    return content
def Momona_msgFormater(bot, contact, member, content):
    if contact.ctype == 'buddy':
        person = contact
    else:
        person = member
    content = content.replace('{@}', '[CQ:at,qq=' + person.uin + ']')
    content = content.replace('{fullname}', '{prefix}{name}{postfix}')
    content = content.replace('{name}', Momona_name(bot, contact, member, content))
    content = content.replace('{nick}', removechar(person.name))
    content = keyreplace(bot, content, ['prefix', 'postfix'])
    i1 = content.find('{CQ:')
    while i1 != -1:
        i2 = content.find('}', i1)
        if i2 == -1:
            break
        content = content.replace('{CQ:', '[CQ:', 1)
        content = content[:i2] + ']' + content[i2+1:]
        i1 = content.find('{CQ:')
    return content
def AddBlackList(bot, uin):
    uin = str(uin)
    if uin in bot.Momona_var['blacklist'].keys():
        bot.Momona_var['blacklist'] = bot.Momona_var['blacklist'][uin] + 1
    else:
        bot.Momona_var['blacklist'][uin] = 1
    return bot.Momona_var['blacklist'][uin]
def isBlacklisted(bot, contact, member):
    if contact.ctype == 'buddy':
        uin = contact.uin
    else:
        uin = member.uin
    if uin in bot.Momona_var['blacklist'].keys():
        return bot.Momona_var['blacklist'][uin] >= 2
    else:
        return False
def onInterval(bot):
    saveData(bot)
def onExit(bot, code, reason, error):
    saveData(bot)
def saveData(bot):
    filepath = bot.config['datapath'] + r'\Momona.txt'
    f = open(filepath, 'w', encoding='utf-8')
    f.write(str(bot.Momona_var))
    f.close()
def loadData(bot):
    filepath = bot.config['datapath'] + r'\Momona.txt'
    if os.path.isfile(filepath):
        f = open(filepath, 'r+', encoding='utf-8')
        s = f.read()
        bot.Momona_var = ast.literal_eval(s.strip('\ufeff'))
        f.close()
        bot.INFO('全局信息读取成功')
    else:
        bot.WARN('文件%s未找到' % filepath)
    if 'textfile' in bot.config.keys():
        f = open(bot.config['textfile'], 'r+', encoding='utf-8')
    else:
        f = open(r'Text.txt', 'r+', encoding='utf-8')
    bot.Momona_text = json.load(f)
    f.close()