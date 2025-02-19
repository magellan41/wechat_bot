import time
import threading

class WxSender(threading.Thread):
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
                now = time.time()
                for key in list(self.msg_dic.keys()):
                    # print('获取消息',self.msg_dic[key])
                    if now - self.msg_dic[key][0] > 5:
                        msg = self.get_msg(key)
                        print(msg)
                        if msg == '':
                            msg = '对不起，我无法理解您的问题'
                        else:
                            msg = self.ai.get_response(key, msg)
                        self.wx.SendMsg(msg, key)
                        del self.msg_dic[key]
            finally:
                self.lock.release()
            time.sleep(1)

    def get_msg(self, who):
        msgs = self.msg_dic[who][1:]
        res = ''
        for msg in msgs:
            if msg.startswith('[语言'):
                continue
            if msg.startswith('[动画'):
                continue
            if msg.startswith('[') and len(msg) < 6:
                continue
            res += msg
            res += '\n\n'

        return res

