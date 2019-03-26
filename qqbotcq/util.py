#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, datetime
class qcontact(object):
    def __init__(self, ctype = None, name = None, uin = None, fromdict = None):
        if fromdict:
            self.ctype = fromdict['ctype']
            self.name = fromdict['name']
            self.uin = fromdict['uin']
            self.role = fromdict['role']
            self.createtime = fromdict['time']
        else:
            self.ctype = ctype
            self.name = name
            self.uin = uin
            self.role = 'undef'
            self.createtime = time.time()
    def __repr__(self):
        return "util.qcontact(fromdict = " + repr({'ctype': self.ctype, 'name': self.name, 'uin': self.uin, 'role': self.role, 'time': self.createtime}) + ")"

class logger():
    def __init__(self, filepath, loglevel):
        self.filepath = filepath + '\\' + time.ctime()[4:].replace(' ','_').replace(':','') + '.log'
        with open(self.filepath, 'w', encoding='utf-8') as logfile:
            logfile.write('Log file created.')
        if loglevel.upper() == 'ERROR':
            self.loglevel = 1
        elif loglevel.upper() == 'WARN':
            self.loglevel = 2
        elif loglevel.upper() == 'INFO':
            self.loglevel = 3
        elif loglevel.upper() == 'DEBUG':
            self.loglevel = 4
        else:
            self.loglevel = 4
        self.INFO('Logger initiate complete.')
    def ERROR(self, message):
        if self.loglevel > 0:
            message = '[ERROR]'+ self.gettime() + message
            print(message)
            self.writelog('\n' + message)
    def WARN(self, message):
        if self.loglevel > 1:
            message = '[WARN] '+ self.gettime() + message
            print(message)
            self.writelog('\n' + message)
    def INFO(self, message):
        if self.loglevel > 2:
            message = '[INFO] '+ self.gettime() + message
            print(message)
            self.writelog('\n' + message)
    def DEBUG(self, message):
        if self.loglevel > 3:
            message = '[DEBUG]'+ self.gettime() + message
            print(message)
            self.writelog('\n' + message)
    def gettime(self):
        return '[' + str(datetime.datetime.now())[:-7] + ']'
    def writelog(self, message):
        with open(self.filepath, 'a', encoding='utf-8') as logfile:
            logfile.write(message)

def findcontact(bot, uin, guin = None, type = 'buddy'):
    if type == 'group':
        if not uin in bot.contact['group'].keys():
            UpdateGroup(bot, uin)
        if not uin in bot.contact['group'].keys():
            bot.contact['group'][uin] = {'qcontact':qcontact('group', '群'+uin, uin), 'member':{}}
        if isOld(bot.contact['group'][uin]['qcontact']):
            UpdateGroup(bot, uin)
        return bot.contact['group'][uin]['qcontact']
    elif type == 'discuss':
        if not uin in bot.contact['discuss'].keys():
            bot.contact['discuss'][uin] = {'qcontact':qcontact('discuss', '讨论组' + uin, uin), 'member':{}}
        return bot.contact['discuss'][uin]['qcontact']
    elif type == 'buddy':
        if uin in bot.contact['buddy'].keys():
            if isOld(bot.contact['buddy'][uin]):
                UpdatePerson(bot, uin, guin, type)
        else:
            UpdatePerson(bot, uin, guin, type)
        return bot.contact['buddy'][uin]
    elif type == 'group-member':
        try:
            if uin in bot.contact['group'][guin]['member'].keys():
                if isOld(bot.contact['group'][guin]['member'][uin]):
                    UpdateGroupMember(bot, guin)
            else:
                UpdateGroupMember(bot, guin)
            if not uin in bot.contact['group'][guin]['member'].keys():
                UpdatePerson(bot, uin, guin, type)
        except:
            UpdatePerson(bot, uin, guin, type)
        return bot.contact['group'][guin]['member'][uin]
    elif type == 'discuss-member':
        if uin in bot.contact['discuss'][guin]['member'].keys():
            if isOld(bot.contact['discuss'][guin]['member'][uin]):
                UpdatePerson(bot, uin, guin, type)
        else:
            UpdatePerson(bot, uin, guin, type)
        return bot.contact['discuss'][guin]['member'][uin]
def isOld(contact):
    if contact.ctype == 'group':
        return time.time() - contact.createtime > 7200
    elif contact.ctype == 'group-member':
        return time.time() - contact.createtime > 1800
    else:
        return time.time() - contact.createtime > 300

def UpdateGroup(bot, group = None):
    grouplist = bot.bot.get_group_list()
    for g in grouplist:
        uin = str(g['group_id'])
        name = g['group_name']
        qcon = qcontact('group', name, uin)
        if uin in bot.contact['group'].keys():
            bot.contact['group'][uin]['qcontact'] = qcon
        else:
            bot.contact['group'][uin] = {'qcontact':qcon, 'member':{}}
        if uin == group or not group:
            UpdateGroupMember(bot, uin)

def UpdateGroupMember(bot, group):
    memberlist = bot.bot.get_group_member_list(group_id = int(group))
    for mem in memberlist:
        if len(mem['card']) > 0:
            memname = mem['card']
        else:
            memname = mem['nickname']
        memqcon = qcontact('group-member', memname, str(mem['user_id']))
        memqcon.role = mem['role']
        bot.contact['group'][group]['member'][str(mem['user_id'])] = memqcon

def UpdatePerson(bot, uin, guin = None, type = 'buddy'):
    if type == 'buddy':
        try:
            name = bot.bot.get_stranger_info(user_id = int(uin))['nickname']
        except:
            name = ''
        bot.contact['buddy'][uin] = qcontact('buddy', name, uin)
    elif type == 'group-member':
        try:
            name = bot.bot.get_stranger_info(user_id = int(uin))['nickname']
        except:
            name = ''
        if not guin in bot.contact['group'].keys():
            bot.contact['group'][guin] = {'qcontact':qcontact('group', '', guin), 'member':{}}
        bot.contact['group'][guin]['member'][uin] = qcontact('group-member', name, uin)
    elif type == 'discuss-member':
        try:
            name = bot.bot.get_stranger_info(user_id = int(uin))['nickname']
        except:
            name = ''
        bot.contact['discuss'][guin]['member'][uin] = qcontact('discuss-member', name, uin)
        