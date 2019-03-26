#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random, os, ast
def onQQMessage(bot, contact, member, content):
    if len(content) < 5 or not bot.isAdmin(contact, member):
        pass
    elif content[:5] == '.eval':
        con = content[5:].strip()
        result = str(eval(con))
        bot.SendTo(contact, result)
    elif content[:5] == '.exec':
        exec(content[5:].strip())
