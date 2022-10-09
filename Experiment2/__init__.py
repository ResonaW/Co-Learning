from dataclasses import replace
from otree.api import *
import pandas as pd
import time
import os
import numpy as np

doc = """Experiment2: 3*2 group, on-demand"""

''' 各组展示方法:
    1A:Human Reward + With Relabeling
    2B:AI Reward + With Relabeling
    3C:Mix Reward + With Relabeling
    4D:Human Reward + Without Relabeling
    5E:AI Reward + Without Relabeling
    6F:Mix Reward + Without Relabeling
'''
def get_group_id(id_in_group):
    # id从1开始
    if (id_in_group - 1) % 6 == 0:
        sort = 'A'
    elif (id_in_group - 2) % 6 == 0:
        sort = 'B'
    elif (id_in_group - 3) % 6 == 0:
        sort = 'C'
    elif (id_in_group - 4) % 6 == 0:
        sort = 'D'
    elif (id_in_group - 5) % 6 == 0:
        sort = 'E'
    elif (id_in_group - 6) % 6 == 0:
        sort = 'F'
    else:
        return None
    return sort

class Bonus():
    '''计算受访者报酬：报酬=5(基础)+1*标对-0.5*标错'''
    def __init__(self, player) -> None:
        c = C()
        self.id_in_group =  player.id_in_group
        self.group_id = get_group_id(player.id_in_group)
        self.flag = False
        self.TRUE_LABELS = player.participant.player_data['label'].iloc[32:].to_list() # 验证集的ground truth标签
        self.manual_csv_name = c.TEST_CSV_PATH+"%d_%s.csv" % (self.id_in_group,self.group_id)
        self.model_csv_name = c.MODEL_CSV_PATH+"%d_%s.csv" % (self.id_in_group,self.group_id)
    '''检查csv文件是否存在 不存在时阻塞'''
    def manual_csv_name_check(self):
        while not os.path.exists(self.manual_csv_name):
            time.sleep(1)
        self.flag = True
    def model_csv_name_check(self):
        while not os.path.exists(self.model_csv_name):
            time.sleep(1)
        self.flag = True
    '''计算收益'''
    def correct_count(self,list_a,list_b):
        n1 = np.array(list_a) - np.array(list_b)
        return n1.tolist().count(0)

    def calculate_bonus(self):
        if self.group_id in "AD":
            manual_df = pd.read_csv(self.manual_csv_name)
            human_correct = self.correct_count(manual_df['label'].to_list(),self.TRUE_LABELS)
            salary = 5+human_correct*2-(32-human_correct)*1
            return human_correct, None, None, salary
        if self.group_id in "BE":
            manual_df = pd.read_csv(self.manual_csv_name)
            model_df = pd.read_csv(self.model_csv_name)
            human_correct = self.correct_count(manual_df['label'].to_list(),self.TRUE_LABELS)
            AI_correct = self.correct_count(model_df['label'].to_list(),self.TRUE_LABELS)
            salary = 5+human_correct*1-(32-human_correct)*0.5+AI_correct*1-(32-AI_correct)*0.5
            return human_correct, AI_correct, None, salary
        if self.group_id in "CF":
            manual_df = pd.read_csv(self.manual_csv_name)
            model_df = pd.read_csv(self.model_csv_name)
            human_correct  = self.correct_count(manual_df['label'].to_list(),self.TRUE_LABELS)
            AI_correct = self.correct_count(model_df['label'].to_list(),self.TRUE_LABELS)
            human_AI_consistency_right = 0
            for i in range(len(manual_df)):
                if manual_df['label'][i]==model_df['label'][i]==self.TRUE_LABELS[i]:
                    human_AI_consistency_right += 1
            salary = 10 + human_correct * 1 - (32 - human_correct) * 0.5 +human_AI_consistency_right*1-(32-human_AI_consistency_right)*0.5
            return human_correct, None, human_AI_consistency_right, salary  

def init_player_data(player,id_in_group):
    '''将整个pool里的的数据通过random state随机分配给每个用户'''
    player.participant.player_data = pd.DataFrame(columns=player.df.columns)
    for i in range(1,9):
        tmp = player.df[player.df['group']==i].sample(n=8,replace=False,random_state=id_in_group)
        player.participant.player_data = pd.concat([player.participant.player_data,tmp],axis=0,ignore_index=True)
    player.participant.player_data['trail'] = list('12345678'*8)
    player.participant.player_data.sort_values(by=['trail'],inplace=True)
    # 存放用户在prepage中的第一次提交(before relabel)
    player.participant.player_prelabel = pd.DataFrame(columns=["text_id","round", "text", "label", "id", "group", "Human_confidence"])
    # 存放用户的提交的前32条训练数据
    player.participant.player_train = pd.DataFrame(columns=["text_id","round", "text", "label", "id", "group", "AI_confidence", "Human_confidence"])
    # 存放用户的提交的后32条测试数据
    player.participant.player_test = pd.DataFrame(columns=["text_id","round", "text", "label", "id", "group", "Human_confidence"])

emotion_dict = { 1:'快乐', 0:'喜爱', 4:'愤怒', 2:'悲伤', 3:'厌恶', 5:'惊讶', 6:'恐惧'}

# MODELS
class C(BaseConstants):
    NAME_IN_URL = 'exp2'
    # 待修改 后续应该是800人
    PLAYERS_PER_GROUP = 12
    NUM_ROUNDS = 64
    # 训练和验证集csv存放位置
    PRELABEL_CSV_PATH  = './watchdog_trainer/Experiment2_csv/prelabel_csv/'
    TRAIN_CSV_PATH = './watchdog_trainer/Experiment2_csv/train_csv/' 
    TEST_CSV_PATH = './watchdog_trainer/Experiment2_csv/test_csv/' 
    OTHER_CSV_PATH = './watchdog_trainer/Experiment2_csv/other_csv/'
    MODEL_CSV_PATH = './watchdog_trainer/Experiment2_csv/model_csv/'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

# 10-4：Survey问题改动
class Player(BasePlayer):
    c=C()
    # 训练集dataframe
    df = pd.read_excel("./Experiment1/dataset.xlsx")
    # 用户Attention Check结果dataframe
    player_ac = pd.DataFrame(columns=["round", "result", "id", "group"])
    # 用户Survey结果dataframe
    player_survey = pd.DataFrame(columns=['id','age','gender','education','crt_bat','crt_widget','crt_lake','Q1','Q2','Q3','Q4','attention','Q6',"Q7","Q8"])
    # ----------以下为fields----------
    sen_result = models.IntegerField()  # 用户情感判断结果
    AI_confidence = models.IntegerField() # AI置信度
    Human_confidence = models.IntegerField() # 人类置信度
    AI_demand_flag = models.BooleanField() # 用户是否要显示AI
    data_demand_flag = models.BooleanField() # 用户是否要额外数据
    # ----------SurveyPage问题----------
    age = models.IntegerField(
        label='您的年龄段是?',
        choices=[['1', '18岁以下'], ['2', '18-25岁'], ['3', '26-30岁'], ['4', '31-35岁'], ['5', '35岁以上']],
        widget=widgets.RadioSelect,
    )
    gender = models.StringField(
        choices=[['1', '男性'], ['2', '女性']],
        label='您的性别是?',
        widget=widgets.RadioSelect,
    )
    education = models.StringField(
        choices=[['1', '高中'], ['2', '大专'], ['3', '本科'], ['4', '硕士'], ['5', '博士及以上']],
        label='您的教育程度是?',
        widget=widgets.RadioSelect,
    )
    crt_bat = models.IntegerField(
        label='''
        一个球拍和一个球总共花费22元。
        球拍相比于球要贵20元，
        那么请问买一个球需要多少钱呢?'''
    )
    crt_widget = models.IntegerField(
        label='''
        如果5台机器5分钟生产5个小部件,
        100台机器生产100个小部件需要多少分钟?
        '''
    )
    crt_lake = models.IntegerField(
        label='''
        在一个湖里，有一小片睡莲。
        每一天睡莲的大小都会翻倍.
        如果睡莲一共需要生长48天才能覆盖整片湖泊,
        那么请问睡莲需要花费多少天才能覆盖半个湖面?
        '''
    )
    Q1 = models.IntegerField(
        label='我觉得这项任务需要集中精神：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']],
        widget=widgets.RadioSelect
    )
    Q2 = models.IntegerField(
        label='我觉得成功地完成了我所需要完成的任务：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']],
        widget=widgets.RadioSelect
    )
    Q3 = models.IntegerField(
        label='在标注过程中，我会感到有压力、不安全、气馁、易怒和生气：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']],
        widget=widgets.RadioSelect
    )
    Q4 = models.IntegerField(
        label='我相信AI能够根据评论内容做出正确的分类：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']],
        widget=widgets.RadioSelect
    )
    Q5 = models.IntegerField(
        label='我相信我的标注显着提高了 AI 在文本分类方面的准确性：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']],
        widget=widgets.RadioSelect
    )
    Q6 = models.IntegerField(
        label='我觉得我对人工智能的工作原理有了很好的理解：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']],
        widget=widgets.RadioSelect
    )
    Q7 = models.IntegerField(
        label='我觉得我很好地理解了 AI 将微博分类的理由：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']],
        widget=widgets.RadioSelect
    )
    Q8 = models.IntegerField(
        label='相比于实验前，我觉得我能够更好完成情感标注任务：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']],
        widget=widgets.RadioSelect
    )
    attention = models.IntegerField(
        label='这是一道注意力测试题，旨在检测志愿者在实验过程中是否认真审题、作答。为表明你在本次实验中认真审题、作答，请选择“非常反对”这一选项。',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']],
        widget=widgets.RadioSelect
    )
    phone = models.StringField(label="请您提供手机号后4位，以便我们后续为您发放薪酬")

# PAGES
'''介绍界面'''
# 10-4：介绍页面html改动
class Introduction(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player):
        group_id = get_group_id(player.id_in_group)
        return dict(id=group_id,
                    explaination_path='explaination.png',
                    salary_path='salary.png'
                    )
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        init_player_data(player, player.id_in_group)

# 10-4: 应该无需改动
'''首次标注界面 PreLabel(不展示AI)'''
class PrePage(Page):
    form_model = 'player'
    form_fields = ['sen_result','Human_confidence']
    @staticmethod
    def vars_for_template(player): # 此处做了精简
        r_num = player.round_number
        r_data = player.participant.player_data.iloc[r_num-1]
        return dict(
            id=get_group_id(player.id_in_group),
            ID=r_num, # 轮数
            content_weibo=r_data['text'],
            icon_path='starIcon.png',
            )
    @staticmethod
    def is_displayed(player):
        group_id = get_group_id(player.id_in_group) # ABC组带有Relabeling功能
        return (player.round_number <= 32) and (group_id in 'ABC')
    @staticmethod
    def before_next_page(player, timeout_happened):
        r_num = player.round_number
        r_data = player.participant.player_data.iloc[r_num-1]
        # 将数据写入
        player.participant.player_prelabel.loc[len(player.participant.player_prelabel)] = [
            r_data['id'],
            r_num,
            r_data['text'],
            player.sen_result,
            player.id_in_group,
            get_group_id(player.id_in_group),
            player.Human_confidence
        ]
        if r_num == 32: # 保存用户的数据
            player.participant.player_prelabel.to_csv(player.c.PRELABEL_CSV_PATH + "%d_%s.csv" % (player.id_in_group, get_group_id(player.id_in_group)),index=False)
            player.participant.player_prelabel = None # 释放内存

# 10-4: 需加入功能，On-demand AI EXP 以及On-demand Additional Data，放在一页里或者多添加两页，然后在Player里或者Participant里设置两个变量
# 10-6: 已实现页面内倒计时 接下来实现页面内更换数据
# 10-7: 实现了功能 需要数据
'''预测32条文本情感页面'''
class MyPage(Page):
    form_model = 'player'
    form_fields = ['sen_result','AI_confidence','Human_confidence','AI_demand_flag','data_demand_flag']
    @staticmethod
    def vars_for_template(player):
        r_num = player.round_number
        r_data = player.participant.player_data.iloc[r_num-1] # 随机抽取
        if get_group_id(player.id_in_group) in "ABC":
            previous_choice,previous_confidence = emotion_dict[player.sen_result],player.Human_confidence
        else:
            previous_choice,previous_confidence = None,None
        return dict(
            ID=r_num, # 轮数
            group_id = get_group_id(player.id_in_group),
            content_weibo=r_data['text'],
            predict_weibo_sen = r_data['pred_str'], # 预测类
            image_path='lime_imgs/lime_exp{}.png'.format(r_data['id']), # 可解释性导入
            AI_predict_rate = str(r_data['main_emotion_confidence(1-5)_AI']), # AI置信度
            icon_path='starIcon.png',
            previous_choice = previous_choice,
            previous_confidence = previous_confidence,
            substitute_content = "这是一段替换文本",
            substitute_predict = "替换预测类别",
            substitute_confidence = "5",
            substitute_img = 'lime_imgs/lime_exp{}.png'.format(r_data['id']) # 这里要改的
            )
    @staticmethod
    def before_next_page(player, timeout_happened):
        r_num = player.round_number
        r_data = player.participant.player_data.iloc[r_num-1] # 随机抽取
        # 写入用户的数据
        player.participant.player_train.loc[len(player.participant.player_train)] = [
            r_data['id'],
            r_num,
            r_data['text'],
            player.sen_result,
            player.id_in_group,
            get_group_id(player.id_in_group),
            player.AI_confidence,
            player.Human_confidence
        ]
        if r_num == 32: # 保存用户的数据
            player.participant.player_train.to_csv(player.c.TRAIN_CSV_PATH + "%d_%s.csv" % (player.id_in_group, get_group_id(player.id_in_group)),index=False)
            player.participant.player_train = None
    @staticmethod
    def is_displayed(player):
        return player.round_number <= 32

# 10-4: Additional Data界面 应该和 Mypage是一样的 只是这个页面是否需要AI EXP呢？ 记得把标志复位
'''Additional Data的界面'''
class AdditionalPage(Page):
    pass

# 10-4: 与前面的MyPage保持一致
'''Attention Check页面'''
class MyAC(Page):
    form_model = 'player'
    form_fields = ['sen_result']
    @staticmethod
    def vars_for_template(player):
        r_num = 16
        r_data = player.participant.player_data.iloc[r_num-1]  # 随机抽取
        return dict(
            ID=r_num,  # 轮数
            group_id=get_group_id(player.id_in_group),
            content_weibo=r_data['text'],
            predict_weibo_sen=r_data['pred_str'],  # 预测类
            AI_predict_rate=str(r_data['main_emotion_confidence(1-5)_AI']),  # AI置信度
            image_path='lime_imgs/lime_exp{}.png'.format(r_data['id']),  # 可解释性导入
            icon_path='starIcon.png',
        )
    @staticmethod
    def before_next_page(player, timeout_happened):
        r_num = player.round_number
        if r_num == 16: # 保存数据
            player.player_ac.loc[len(player.player_ac)] = [r_num,player.sen_result,player.id_in_group,get_group_id(player.id_in_group)]
            player.player_ac.to_csv(player.c.OTHER_CSV_PATH + "attention_check.csv", index=False)
    @staticmethod
    def is_displayed(player):
        return player.round_number == 16 or player.round_number == 48 

'''预测32条文本情感页面'''
class MyTest(Page):
    form_model = 'player'
    form_fields = ['sen_result','Human_confidence']
    @staticmethod
    def vars_for_template(player):
        r_num = player.round_number
        r_data = player.participant.player_data.iloc[r_num-1] # 随机抽取
        return dict(
            ID=r_num-32,
            content_weibo=r_data['text'],
            icon_path='starIcon.png'
        )
    @staticmethod
    def before_next_page(player, timeout_happened): # 写入和保存至test_csv
        r_num = player.round_number
        r_data = player.participant.player_data.iloc[r_num-1] # 随机抽取
        # 保存数据，字段同上
        player.participant.player_test.loc[len(player.participant.player_test)] = [
            r_data['id'],
            r_num,
            r_data['text'],
            player.sen_result,
            player.id_in_group,
            get_group_id(player.id_in_group),
            player.Human_confidence
        ]
        if r_num == 64:
            player.participant.player_test.to_csv(player.c.TEST_CSV_PATH + "%d_%s.csv" % (player.id_in_group, get_group_id(player.id_in_group)),index=False)
            player.participant.player_test = None
    @staticmethod
    def is_displayed(player):
        return player.round_number > 32

'''32条标注后提示界面'''
class ResultWaitPage(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 32

'''Survey页面'''
class ExitSurveyPage(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        group_id = get_group_id(player.id_in_group)
        if group_id in "A": # without AI, 不展示问题467
            return ['age','gender','education','crt_bat','crt_widget','crt_lake','Q1','Q2','Q3','attention','Q8','phone']
        elif group_id in "BD": # without AI explanation, 不展示问题7
            return ['age','gender','education','crt_bat','crt_widget','crt_lake','Q1','Q2','Q3','Q4','attention','Q6','Q8','phone']
        else: # with AI explanation,不展示问题6
            return ['age','gender','education','crt_bat','crt_widget','crt_lake','Q1','Q2','Q3','Q4','attention',"Q7",'Q8','phone']
    @staticmethod
    def vars_for_template(player):
        return dict( num=player.round_number,
                     group_id = get_group_id(player.id_in_group),
                     icon_path='starIcon.png',
                     )
    @staticmethod
    def is_displayed(player):
        return player.round_number == 64 # 写成1时用于测试
    @staticmethod
    def before_next_page(player, timeout_happened):
        group_id = get_group_id(player.id_in_group)
        if group_id == "A":
            player.player_survey.loc[len(player.player_survey)] = [player.id_in_group,player.age,player.gender,player.education,player.crt_bat,player.crt_widget,player.crt_lake,player.Q1,player.Q2,player.Q3,None,player.attention,None,None,player.Q8]
        elif group_id in 'BD':
            player.player_survey.loc[len(player.player_survey)] = [player.id_in_group,player.age,player.gender,player.education,player.crt_bat,player.crt_widget,player.crt_lake,player.Q1,player.Q2,player.Q3,player.Q4,player.attention,player.Q6,None,player.Q8]
        else:
            player.player_survey.loc[len(player.player_survey)] = [player.id_in_group,player.age,player.gender,player.education,player.crt_bat,player.crt_widget,player.crt_lake,player.Q1,player.Q2,player.Q3,player.Q4,player.attention,None,player.Q7,player.Q8]
        player.player_survey.to_csv(player.c.OTHER_CSV_PATH + "survey.csv", index=False)
        bonus = Bonus(id_in_group=player.id_in_group,group_id=group_id)
        bonus.manual_csv_name_check() 
        time.sleep(1) # 阻塞一秒，防止用户提交的csv没有完全写入

'''展示报酬界面'''
class RewardPage(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 64
    @staticmethod
    def vars_for_template(player):
        group_id = get_group_id(player.id_in_group)
        bonus = Bonus(id_in_group=player.id_in_group,group_id=group_id)
        correct, reward = bonus.calculate_bonus()
        return dict(reward=reward, correct=correct, wrong=32-correct, QR_code='QR_code.jpg')

page_sequence = [Introduction,PrePage,MyPage,MyAC,MyTest,ResultWaitPage,ExitSurveyPage,RewardPage]