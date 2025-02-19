import time
import threading

class WxReceiver(threading.Thread):
    def __init__(self, wx, ai, msg_dic, lock):
        threading.Thread.__init__(self)
        self.wx = wx
        self.ai = ai
        self.msg_dic = msg_dic
        self.lock = lock

    def run(self):
        while True:
            self.lock.acquire()
            try:
                msgs = self.wx.GetListenMessage()
                for chat in msgs:
                    who = chat.who  # 获取聊天窗口名（人或群名）
                    one_msgs = msgs.get(chat)  # 获取消息内容
                    for msg in one_msgs:
                        msg_type = msg.type  # 获取消息类型
                        if msg_type == 'friend':
                            content = msg.content  # 获取消息内容，字符串类型的消息内容
                            if content == '/clear':
                                if who in self.msg_dic:
                                    del self.msg_dic[who]
                                self.wx.SendMsg(self.ai.get_response(content), who)
                            if who not in self.msg_dic:
                                self.msg_dic[who] = [time.time()]
                            # 重置时间
                            self.msg_dic[who][0] = time.time()
                            self.msg_dic[who].append(content)
                            # print('接受消息存储',self.msg_dic[who])
            finally:
                self.lock.release()
            time.sleep(1)

