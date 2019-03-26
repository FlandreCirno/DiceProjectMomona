#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time, traceback
try:
    from cqhttp_helper import CQHttp
    from qqbotwraper import QQbot
    bot = CQHttp(api_root='http://127.0.0.1:5700/',
                access_token='diceprojectmomona',
                secret='2019143')
    qqbot = QQbot(bot)
    @bot.on_message()
    def handle_msg(context):
        return qqbot.onQQMessage(context)
    @bot.on_event()
    def handle_event(context):
        return qqbot.onEvent(context)
    @bot.on_notice()
    def handle_notice(context):
        return qqbot.onEvent(context)
    @bot.on_request()
    def handle_request(context):
        return qqbot.onRequest(context)
    bot.run(host='127.0.0.1', port=8080)
except Exception as e:
    traceback.print_exc()
finally:
    try:
        qqbot.onExit()
    except Exception as e:
        traceback.print_exc()
    print('Press Enter to continue')
    input()

time.sleep(1)
