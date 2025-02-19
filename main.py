import threading
import configparser

from wxauto import WeChat

from ai import AI
from wx_receiver import WxReceiver
from wx_sender import WxSender

#等待时间
wait = 1

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')


listen_friends = [item.strip() for item in config.get('DEFAULT','listen_friends').split(',')]
system_prompt = config.get('DEFAULT','system_prompt')

ai_type = config.get('DEFAULT','ai_type')

api_key = config.get(ai_type,'api_key')
base_url = config.get(ai_type,'base_url')
model = config.get(ai_type,'model')



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
