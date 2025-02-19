import threading
import configparser
import time

from wxauto import WeChat

from ai import AI
from wx_receiver import WxReceiver
from wx_sender import WxSender

#等待时间
wait = 1
# 监听的好友列表

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


api_key = config.get('DEFAULT','api_key')
base_url = config.get('DEFAULT','base_url')
model = config.get('DEFAULT','model')
listen_friends = [item.strip() for item in config.get('DEFAULT','listen_friends').split(',')]
system_prompt = config.get('DEFAULT','system_prompt')



ai = AI(api_key, base_url, model, system_prompt)
wx = WeChat()
for listen_friend in listen_friends:
    wx.AddListenChat(listen_friend)

msg_dic = {}
lock = threading.Lock()


wx_receiver_obj = WxReceiver(wx, ai, msg_dic, lock)
wx_sender_obj = WxSender(wx, ai,msg_dic, lock)

wx_receiver_obj.start()
wx_sender_obj.start()

wx_receiver_obj.join()
wx_sender_obj.join()
