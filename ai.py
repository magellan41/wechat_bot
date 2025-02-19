from openai import OpenAI

class AI:
    def __init__(self, api_key, base_url, model, system_prompt):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.chat_dict = {}
        self.system_prompt = system_prompt

    def get_response(self, who, message):
        if message == '/clear':
            del self.chat_dict[who]
            return '已清空历史聊天记录'
        try:
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            completion = client.chat.completions.create(
                model=self.model,
                messages=self.get_history_chat(who, message)
            )
            response = completion.choices[0].message.content
            self.chat_dict[who].append({'role': 'assistant', 'content': response})
            return response
        except Exception as e:
            print(f"错误信息：{e}")
            print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

    def get_history_chat(self, who, message):
        if who not in self.chat_dict:
            self.chat_dict[who] = [{'role': 'system', 'content': self.system_prompt}]
        self.chat_dict[who].append({'role': 'user', 'content': message})
        while len(self.chat_dict[who]) > 10 or self.chat_dict[who][1]['role'] == 'assistant':
            self.chat_dict[who].pop(1)
        return self.chat_dict[who]
