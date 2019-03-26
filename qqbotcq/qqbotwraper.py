#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, sys, os, threading, ast, json
from html.parser import HTMLParser
import util
sys.path.append(sys.path[0] + r"\plugins")
mlist = ['Momona', 'Rdroll', 'Rhroll', 'Rcroll', 'Rsroll', 'Coc7', 'Rules', 'Jrrp', 'Sancheck', 'Insane', 'Console']
qqbotwraper_ver = '1.2.2'
class QQbot(object):
    def __init__(self, bot):
        self.bot = bot
        self.util = util
        if os.path.isfile(r'config.cfg'):
            with open(r'config.cfg', 'r+', encoding='utf-8') as cfgfile:
                self.config = json.load(cfgfile)
        else:
            self.config = {'mlist':mlist, 'admin':[], 'datapath':(r'data'), 'loglevel':'INFO'}
            with open(r'config.cfg', 'w', encoding='utf-8') as cfgfile:
                json.dump(self.config, cfgfile, sort_keys = True, indent = 4, separators = (',', ': '))
        self.logger = self.util.logger(filepath = r'logs', loglevel = self.config['loglevel'])
        self.DEBUG = self.logger.DEBUG
        self.INFO = self.logger.INFO
        self.WARN = self.logger.WARN
        self.ERROR = self.logger.ERROR
        self.version = qqbotwraper_ver
        self.qq = str(self.bot.get_login_info()['user_id'])
        self.parser = HTMLParser()
        self.INFO('加载插件中，插件列表：' + str(self.config['mlist']))
        self.modlist = {}
        for mod in self.config['mlist']:
            self.modlist[mod] = __import__(mod)
        self.INFO('插件加载完毕')
        self.evlist = {'onInterval':[],'onPlug':[],'onQQMessage':[],'onExit':[],'onUnplug':[],'onEvent':[],'onRequest':[]}
        #self.UpdateBuddy()
        for mod in self.config['mlist']:
            for k in self.evlist.keys():
                if hasattr(self.modlist[mod], k):
                    self.evlist[k].append(mod)
        self.INFO('加载联系人缓存中')
        if os.path.isfile(self.config['datapath'] + r'\contact.txt'):
            f = open(self.config['datapath'] + r'\contact.txt', 'r+', encoding='utf-8')
            self.contact = eval(f.read())
            f.close()
        else:
            self.INFO('未找到缓存文件，获取联系人中')
            self.contact = {'buddy':{}, 'group':{}, 'discuss':{}}
            self.UpdateGroup()
        self.INFO('联系人加载完毕')
        self.onPlug()
        self.interval = threading.Thread(target = self.sub_thread)
        self.interval.daemon = True
        self.interval.start()
    def sub_thread(self):
        while True:
            time.sleep(300)
            self.onInterval()
            f = open(self.config['datapath'] + r'\contact.txt', 'w', encoding='utf-8')
            f.write(str(self.contact))
            f.close()
    def onExit(self):
        self.INFO('Exiting...')
        for mod in self.evlist['onExit']:
            self.modlist[mod].onExit(self, None, None, None)
    def onPlug(self):
        for mod in self.evlist['onPlug']:
            self.modlist[mod].onPlug(self)
    def onInterval(self):
        for mod in self.evlist['onInterval']:
            self.modlist[mod].onInterval(self)
    def onQQMessage(self, context):
        self.DEBUG('收到信息，内容：'+str(context))
        msg = self.parser.unescape(context['message'])
        if context['message_type'] == 'private':
            uin = str(context['user_id'])
            qcon = self.util.findcontact(self, uin)
            self.onQQMessage_helper(qcon, self.util.qcontact(), msg)
        elif context['message_type'] == 'group':
            uin = str(context['group_id'])
            memuin = str(context['user_id'])
            qcon = self.util.findcontact(self, uin, None, 'group')
            memqcon = self.util.findcontact(self, memuin, uin, 'group-member')
            self.onQQMessage_helper(qcon, memqcon, msg)
        elif context['message_type'] == 'discuss':
            uin = str(context['discuss_id'])
            memuin = str(context['user_id'])
            qcon = self.util.findcontact(self, uin, None, 'discuss')
            memqcon = self.util.findcontact(self, memuin, uin, 'discuss-member')
            self.onQQMessage_helper(qcon, memqcon, msg)
    def onQQMessage_helper(self, contact, member, content):
        for mod in self.evlist['onQQMessage']:
            result = self.modlist[mod].onQQMessage(self, contact, member, content)
            if result:
                return result
    def onEvent(self, context):
        self.DEBUG('收到事件，内容：'+str(context))
        if 'event' in context.keys():
            context['notice_type'] = context['event']
        if not 'sub_type' in context.keys():
            context['sub_type'] = None
        if context['notice_type'] == 'group_increase':
            self.util.UpdatePerson(self, context['user_id'], context['group_id'], 'group-member')
            self.util.findcontact(self, context['user_id'], context['group_id'], 'group-member').role = 'member'
        elif context['notice_type'] == 'group_admin':
            if context['sub_type'] == 'set':
                self.util.findcontact(self, context['user_id'], context['group_id'], 'group-member').role = 'admin'
            elif context['sub_type'] == 'unset':
                self.util.findcontact(self, context['user_id'], context['group_id'], 'group-member').role = 'member'
        if context['notice_type'] == 'friend_add':
            contact = self.util.findcontact(self, str(context['user_id']), None, 'buddy')
            operator = contact
            target = self.util.findcontact(self, self.qq, None, 'buddy')
        else:
            contact = self.util.findcontact(self, str(context['group_id']), None, 'group')
            target = self.util.findcontact(self, str(context['user_id']), str(context['group_id']), 'group-member')
        if 'operator_id' in context.keys():
            operator = self.util.findcontact(self, str(context['operator_id']), str(context['group_id']), 'group-member')
        if context['notice_type'] == 'group_admin':
            operator = self.util.qcontact(None, None, None)
        elif context['notice_type'] == 'group_upload':
            operator = target
            target = context['file']
        for mod in self.evlist['onEvent']:
            result = self.modlist[mod].onEvent(self, contact, operator, target, context['notice_type'], context['sub_type'])
            if result:
                return result
    def onRequest(self, context):
        pass
    def isMe(self, contact, member):
        return (contact.ctype == 'buddy' and contact.uin == self.qq) or \
               (contact.ctype != 'buddy' and member.uin == self.qq)
    def isAdmin(self, contact, member):
        return (contact.ctype == 'buddy' and contact.uin in self.config['admin']) or \
               (contact.ctype != 'buddy' and member.uin in self.config['admin'])
    def isManager(self, contact, member):
        if contact.ctype == 'group':
            return member.role != 'member'
        elif contact.ctype == 'discuss':
            return True
        return False
    def SendTo(self, contact, message, resendOn1202 = False):
        try:
            if contact.ctype == 'group':
                self.bot.send_group_msg(group_id = int(contact.uin), message = message)
                self.INFO('成功发送信息到群'+contact.uin+'，内容：'+message)
            elif contact.ctype == 'discuss':
                self.bot.send_discuss_msg(discuss_id = int(contact.uin), message = message)
                self.INFO('成功发送信息到讨论组'+contact.uin+'，内容：'+message)
            else:
                self.bot.send_private_msg(user_id = int(contact.uin), message = message)
                self.INFO('成功发送信息到'+contact.uin+'，内容：'+message)
            return True
        except Exception as e:
            self.ERROR('发送信息'+message+'到'+str(contact)+'失败，错误信息：'+str(e))
            raise
    def List(self, contact):
        if isinstance(contact, str):
            if contact.lower() == 'buddy':
                return self.contact['buddy']
            elif contact.lower() == 'group':
                rlist = []
                for group in self.contact['group']:
                    rlist.append(group['qcontact'])
                return rlist
        elif isinstance(contact, self.util.qcontact):
            if contact.ctype == 'group':
                for group in self.contact['group']:
                    if group['uin'] == contact.uin:
                        return group['member']
                return None
            else:
                return None
        else:
            return None
    def Stop(self):
        pass
    def Update(self, contact):
        pass
    def UpdateGroup(self, group = None):
        self.util.UpdateGroup(self, group)
    def Quit(self, contact):
        if contact.ctype == 'group':
            self.bot.set_group_leave(group_id = int(contact.uin))
            self.INFO("已退出群" + str(contact))
        elif contact.ctype == 'discuss':
            self.bot.set_discuss_leave(discuss_id = int(contact.uin))
            self.INFO("已退出讨论组" + str(contact))
    def UpdateBuddy(self): #无效
        buddy = self.bot.get_friend_list()
        for fgp in buddy:
            for friend in fgp:
                if 'remark' in friend.keys():
                    friname = friend['remark']
                else:
                    firname = friend['nickname']
                friendqcon = self.util.qcontact('buddy', friname, str(friend[user_id]))
                self.contact['buddy'].append(friendqcon)
