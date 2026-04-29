
import re
from datetime import datetime

# ===== 1. Message 类 =====
# TODO: 完成消息类的实现
# 作用：表示一条聊天消息
class Message:
    def __init__(self, sender, content):
        # TODO: 初始化消息
        self.sender = sender
        self.content = content
        self.timestamp = datetime.now()
        

    def __str__(self):
        # TODO: 返回格式化字符串，格式如 "[14:22:01] 你: 你好"
        return f"[{self.timestamp.strftime('%H:%M:%S')}] {self.sender}: {self.content}"
        


# ===== 2. ChatHistory 类 =====
# TODO: 完成聊天记录类的实现
# 作用：管理所有聊天消息，支持添加、查看最近消息、限制总数量
class ChatHistory:
    def __init__(self, max_size=20):
        # TODO: 初始化聊天记录
        # - self._messages: 存储消息的列表
        self._messages=[]
        # - self._max_size: 最大消息数量
        self._max_size=max_size
        

    def add(self, msg):
        # TODO: 添加消息到记录中
        # 1. 将消息追加到列表-append方法，列表的内置添加方法
        self._messages.append(msg)
        # 2. 如果超过 max_size，删除最早的一条（索引为0）
        if len(self._messages)>self._max_size:
            self._messages.pop(0)
        

    def recent(self, n=5):
        # TODO: 返回最近 n 条消息
        return  self._messages[-n:]
        

    def __len__(self):
        # TODO: 返回当前消息总数
        return len(self._messages)

    def __str__(self):
        # TODO: 将所有消息拼接成一个字符串
        # 1. 如果没有消息，返回 "暂无消息"
        # 2. 否则，将每条消息用 \n 连接
        if not self._messages:
            return "暂无消息"
        #生成器
        return "\n".join(str(msg) for msg in self._messages)
    
        


# ===== 3. Skill 父类 =====
# TODO: 完成技能基类
# 作用：所有技能的父类，定义统一接口
class Skill:
    def __init__(self, name):
        # TODO: 初始化技能，记录技能名称
        self._name=name
        

    def can_handle(self, user_input):
        # TODO: 判断是否能处理用户输入
        # 默认返回 False，由子类重写
        return False


    def handle(self, user_input):
        # TODO: 处理用户输入并返回回复
        # 默认返回提示信息，由子类重写
        return "暂时无法理解"
        


# ===== 4. Calculator 子类 =====
# TODO: 完成计算器技能
# 作用：处理数学计算，如 "1+2"、"3*4" 等
class Calculator(Skill):
    def __init__(self):
        # TODO: 调用父类初始化，名称设为 "计算器"
        super().__init__("计算器")
    

    def can_handle(self, user_input):
        # TODO: 判断是否包含运算符 + - * /
        return bool(re.search(r'[+\-*/]',user_input))

    def handle(self, user_input):
        # TODO: 执行计算
        # 步骤：
        # 1. 定义允许的字符集合（数字、+-*/(). 和空格）
        # 2. 检查每个字符是否合法，不合法返回"表达式格式有误"
        # 3. 使用 eval() 计算结果
        # 4. 捕获异常，如果出错返回"表达式格式有误"
        # 5. 返回格式化的结果，如 "1+2 = 3"
        allowed=set('0123456789+-*/(). ')
        if not all(c in allowed for c in user_input):
            return "表达式格式有误"
        
        try:
            result=eval(user_input)
            return  f"{user_input}={result}"
        except ZeroDivisionError:
            return "有误：除数不能为0"
        except Exception:
            return "表达式格式有误"



# ===== 5. Translator 子类 =====
# TODO: 完成翻译器技能
# 作用：翻译英文单词，如 "apple" -> "苹果"
class Translator(Skill):
    def __init__(self):
        # TODO: 调用父类初始化，名称设为 "翻译器"
        super().__init__("翻译器")
    

    # TODO: 添加单词字典
    word_dic = {
        "apple": "苹果",
        "assistant": "助理",
        "calculator": "计算器",
        "me":"我",
    }

    def can_handle(self, user_input):
        # TODO: 判断是否需要翻译
        # 提示：检查是否包含"翻译"、"什么意思"、"是什么"等关键词
        # 或者检查是否包含英文字母
        return re.search(r"翻译|什么意思|是什么|怎么说",user_input)
        

    def handle(self, user_input):
        # TODO: 执行翻译
        # 步骤：
        # 1. 从用户输入中提取英文单词
        # 2. 在字典中查找翻译
        # 3. 如果找到，返回 "单词 的意思是：翻译"
        # 4. 如果没找到，返回"这个词暂时不认识"
        # 提示：使用 re.findall(r'[a-zA-Z]+', user_input) 提取英文
        words=re.findall(r'[a-zA-Z]+',user_input)
        results=[]
        for word in words:
            trans=self.word_dic.get(word.lower())
            if trans:
                results.append(f"{word}的意思是：{trans}")
            
        if results:
            return "\n".join(results)
        return "这个单词我暂时还没学会,再换一个吧"
                



# ===== 6. WeatherSkill 子类 =====
# TODO: 完成天气查询技能
# 作用：查询城市天气，如 "北京天气" -> "晴，18℃"
class WeatherSkill(Skill):
    def __init__(self):
        # TODO: 调用父类初始化，名称设为 "天气查询"
        super().__init__("天气查询")
    

    # TODO: 添加天气字典
    weather_dic = {
        "北京": "晴，18℃",
        "上海": "多云，23℃",
        "四川": "小雨，22℃",
    }

    def can_handle(self, user_input):
        # TODO: 判断是否查询天气
        # 提示：检查是否包含"天气"或"温度"
        return re.search(r"天气|温度",user_input)
        

    def handle(self, user_input):
        # TODO: 执行天气查询
        # 步骤：
        # 1. 从用户输入中提取城市名
        # 2. 在字典中查找天气
        # 3. 如果找到，返回 "城市天气：天气信息"
        # 4. 如果没找到，返回"这个城市的天气目前我还不知道哦"
        # 提示：使用 for city in weather_dic: if city in user_input:
        for city in self.weather_dic:
            if city in user_input:
                return f"{city}的天气：{self.weather_dic[city]}"
        
        return "这个城市的天气我目前还不知道哦,再换一个吧"
        

# ===== 7. Assistant 主类 =====
# TODO: 完成助手主类
# 作用：管理所有技能，处理用户对话
class Assistant:
    def __init__(self, name):
        # TODO: 初始化助手
        # - self.name: 助手名称
        self._name=name
        # - self.history: 聊天记录（ChatHistory 实例）
        self._history=ChatHistory()
        # - self.skills: 技能列表
        self._skills=[]
        
    @property
    def name(self):
        return self._name

    def add_skill(self, skill):
        # TODO: 添加技能到列表
        self._skills.append(skill)
        

    def chat(self, user_input):
        # TODO: 处理用户输入并返回回复
        # 步骤：
        # 1. 创建用户 Message 对象并添加到 history
        # 2. 遍历 skills，找到第一个 can_handle 返回 True 的技能
        # 3. 如果找到，调用技能 handle 得到回复
        # 4. 如果没找到，使用默认回复（如："我不理解，请换个说法"）
        # 5. 创建机器人 Message 对象并添加到 history
        # 6. 返回回复字符串
        user_msg=Message("你",user_input)
        self._history.add(user_msg)
        response=None
        for skill in self._skills:
            if skill.can_handle(user_input):
                response=skill.handle(user_input)
                break

        if response is None:
            response=f"我不理解，试试看其他的吧"

        robot_msg=Message(self._name,response)
        self._history.add(robot_msg)

        return response        
    

    def show_history(self):
        """返回格式化的历史记录"""
        return str(self._history)
    
    def message_count(self):
        return len(self._history)


# ===== 8. main 入口 =====
# TODO: 完成主程序
if __name__ == "__main__":
    # TODO: 1. 创建 Assistant 实例
    bot=Assistant("XiaoMiao")
    
    # TODO: 2. 创建并注册技能（Calculator, Translator, WeatherSkill）
    bot.add_skill(Calculator())
    bot.add_skill(Translator())
    bot.add_skill(WeatherSkill())
    # TODO: 3. 打印欢迎信息
    print(f"欢迎使用{bot.name},试着问我一些问题吧，但是不要太难哦")
    # TODO: 4. 进入对话循环
    while True:
        user_input = input("你: ").strip()
        
        if user_input == "quit":
            # 打印再见消息和对话数量
            print(f"{bot.name}:再见朋友，我们这次一共进行了{bot.message_count()}条对话，期待下次再会")
            break
        
        if user_input == "history":
            # 打印聊天记录
            print(bot.show_history())
            continue
        
        reply = bot.chat(user_input)
        print(f"{bot.name}: {reply}\n")
    