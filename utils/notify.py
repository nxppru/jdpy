#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/16 4:10 下午
# @File    : notify.py
# @Project : jd_scripts
# @Desc    : 通知模块
import requests
import telegram
import os, re
import json
from config import TG_BOT_TOKEN, TG_USER_ID, PUSH_P_TOKEN,  QYWX_AM
from utils.console import println


def wecom_app(title, content):
    try:
        if not QYWX_AM:
            print("QYWX_AM 并未设置！！\n取消推送")
            return
        QYWX_AM_AY = re.split(',', QYWX_AM)
        if 4 < len(QYWX_AM_AY) > 5:
            print("QYWX_AM 设置错误！！\n取消推送")
            return
        corpid = QYWX_AM_AY[0]
        corpsecret = QYWX_AM_AY[1]
        touser = QYWX_AM_AY[2]
        agentid = QYWX_AM_AY[3]
        try:
            media_id = QYWX_AM_AY[4]
        except:
            media_id = ''
        wx = WeCom(corpid, corpsecret, agentid)
        # 如果没有配置 media_id 默认就以 text 方式发送
        if not media_id:
            message = title + '\n\n' + content
            response = wx.send_text(message, touser)
        else:
            response = wx.send_mpnews(title, content, media_id, touser)
        if response == 'ok':
            print('推送成功！')
        else:
            print('推送失败！错误信息如下：\n', response)
    except Exception as e:
        print(e)
        
class WeCom:
    def __init__(self, corpid, corpsecret, agentid):
        self.CORPID = corpid
        self.CORPSECRET = corpsecret
        self.AGENTID = agentid

    def get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_text(self, message, touser="@all"):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
            },
            "safe": "0"
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]

    def send_mpnews(self, title, message, media_id, touser="@all"):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": touser,
            "msgtype": "mpnews",
            "agentid": self.AGENTID,
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": media_id,
                        "author": "Author",
                        "content_source_url": "",
                        "content": message.replace('\n', '<br/>'),
                        "digest": message
                    }
                ]
            }
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]


def push_plus_notify(title, content):
    """
    push+消息通知
    :return:
    """
    try:
        if not PUSH_P_TOKEN:
            println('未配置PUSH+ token, 不推送PUSH+信息!')
            return
        url = 'http://pushplus.hxtrip.com/send'

        headers = {
            'Content-Type': 'application/json',
        }
        content = content.replace('\n', '<br>')
        data = {
            'token': PUSH_P_TOKEN,
            'title': title,
            'content': content,
            'template': 'html'
        }

        response = requests.post(url=url, json=data, headers=headers)
        response_data = response.json()
        if response_data['code'] == 200:
            println('成功推送消息至PUSH+')
        else:
            println('推送PUSH+消息失败, {}'.format(response_data))
    except Exception as e:
        println('推送PUSH+数据失败, {}!'.format(e.args))


def tg_bot_notify(title, message):
    """
    TG消息通知
    :return:
    """
    message = '\n'.join([title, message])
    if TG_BOT_TOKEN and TG_USER_ID:
        try:
            bot = telegram.Bot(TG_BOT_TOKEN)
            bot.send_message(TG_USER_ID, message)
            println('\n成功推送消息到TG!')
        except Exception as e:
            println('\nTG消息通知异常:{}'.format(e.args))
    else:
        println("\n未配置TG_BOT_TOKEN和TG_USER_ID, 不推送TG消息...")


def notify(title, content):
    """
    消息推送
    :param content:
    :param title:
    :param message:
    :return:
    """
    println(title + '\n' + content)
    push_plus_notify(title, content)
    wecom_app(title, content)
    # TG通知
    tg_bot_notify(title, content)

