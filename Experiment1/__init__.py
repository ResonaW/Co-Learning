from otree.api import *
import pandas as pd
import time
import os
import numpy as np
import random

doc = """Experiment1"""

''' 各组展示方法:
    1A:No AI
    2B:AI
    3C:AI+EXP
    4D:AI+Relabel
    5E:AI+Relabel+EXP
'''
def get_group_id(id_in_group):
    # id从1开始
    if (id_in_group - 1) % 5 == 0:
        sort = 'A'
    elif (id_in_group - 2) % 5 == 0:
        sort = 'B'
    elif (id_in_group - 3) % 5 == 0:
        sort = 'C'
    elif (id_in_group - 4) % 5 == 0:
        sort = 'D'
    elif (id_in_group - 5) % 5 == 0:
        sort = 'E'
    else:
        return None
    return sort

class Bonus():
    '''计算受访者报酬：报酬=5(基础)+1*标对-0.5*标错'''
    def __init__(self, id_in_group, group_id) -> None:
        self.id_in_group =  id_in_group
        self.group_id = group_id
        self.flag = False
        tmp_df = pd.read_excel("./Experiment1/dataset.xlsx")
        self.TRUE_LABELS = tmp_df['label'].iloc[32:].to_list() # 验证集的ground truth标签
        self.CSV_PATH = './watchdog_trainer/test_csv/'
        self.manual_csv_name = self.CSV_PATH+"%d_%s.csv" % (self.id_in_group,self.group_id)
    '''检查csv文件是否存在 不存在时阻塞'''
    def manual_csv_name_check(self):
        while not os.path.exists(self.manual_csv_name):
            time.sleep(1)
        self.flag = True
    '''计算收益'''
    def correct_count(self,list_a,list_b):
        n1 = np.array(list_a) - np.array(list_b)
        return n1.tolist().count(0)
    def calculate_bonus(self):
        manual_df = pd.read_csv(self.manual_csv_name)
        human_correct = self.correct_count(manual_df['label'].to_list(),self.TRUE_LABELS)
        salary = 5+human_correct*1-(32-human_correct)*0.5
        return salary

class C(BaseConstants):
    NAME_IN_URL = 'Experiment1'
    # 待修改 后续应该是600人
    PLAYERS_PER_GROUP = 30
    NUM_ROUNDS = 64
    # 训练和验证集csv存放位置
    PRELABEL_CSV_PATH  = './watchdog_trainer/prelabel_csv/'
    TRAIN_CSV_PATH = './watchdog_trainer/train_csv/' 
    TEST_CSV_PATH = './watchdog_trainer/test_csv/' 
    OTHER_CSV_PATH = './watchdog_trainer/other_csv/'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

# 这里之后尝试用以下Participants
class Player(BasePlayer):
    c=C()
    # 训练集dataframe
    df = pd.read_excel("./Experiment1/dataset.xlsx")
    # 存放用户在prepage中的第一次提交(before relabel)
    player_prelabel = pd.DataFrame(columns=["round", "text", "label", "id", "group", "Human_confidence"])
    # 存放用户的提交的前32条训练数据
    player_train = pd.DataFrame(columns=["round", "text", "label", "id", "group", "AI_confidence", "Human_confidence"])
    # 存放用户的提交的后32条测试数据
    player_test = pd.DataFrame(columns=["round", "text", "label", "id", "group", "Human_confidence"])
    # 用户Attention Check结果dataframe
    player_ac = pd.DataFrame(columns=["round", "result", "id", "group"])
    # 用户Survey结果dataframe
    player_survey = pd.DataFrame(columns=['id','age','gender','education','crt_bat','crt_widget','crt_lake','Q1','Q2','Q3','Q4','attention','Q5','Q6',"Q7",'advice'])
    # ----------以下为fields----------
    sen_result = models.IntegerField()  # 用户情感判断结果
    AI_confidence = models.IntegerField() # AI置信度
    Human_confidence = models.IntegerField() # 人类置信度
    # SurveyPage问题
    age = models.IntegerField(label='你的年龄是？', min=0, max=125)
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
    attention = models.IntegerField(
        label='这是一道注意力测试题，旨在检测志愿者在实验过程中是否认真审题、作答。为表明你在本次实验中认真审题、作答，请选择“非常反对”这一选项。',
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
    advice = models.StringField(label="您是否有其它的建议或意见，或者谈谈您对实验的感受？")


# PAGES
'''介绍界面'''
class Introduction(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player):
        group_id = get_group_id(player.id_in_group)
        return dict(id=group_id,
                    explaination_path='explaination.png'
                    )

'''首次标注界面（不展示AI）'''
class PrePage(Page):
    form_model = 'player'
    form_fields = ['sen_result','Human_confidence']
    @staticmethod
    def vars_for_template(player): # 此处做了精简
        r_num = player.round_number
        r_data = player.df.iloc[r_num-1]
        return dict(
            ID=r_num, # 轮数
            content_weibo=r_data['text'],
            icon_path='starIcon.png',
            )
    @staticmethod
    def is_displayed(player):
        group_id = get_group_id(player.id_in_group) # 不展示AI，A组直接标注数据，DE组进行第一次Label(Prelabel)
        return player.round_number <= 32 and ( group_id == 'D' or group_id == 'E' or group_id == 'A')
    @staticmethod
    def before_next_page(player, timeout_happened):
        r_num = player.round_number
        r_data = player.df.iloc[r_num-1]
        # 如果为A组，和其他组一样直接将数据保存到train_csv，如果为DE组，则单独创建一个记录保存prelabel结果
        if get_group_id(player.id_in_group) == 'A':
            player.player_train.loc[len(player.player_train)] = [
                r_num,
                r_data['text'],
                player.sen_result,
                player.id_in_group,
                get_group_id(player.id_in_group),
                None,
                player.Human_confidence
            ]
            if r_num == 32: # 保存用户的数据
                current_df_pre = player.player_train[player.player_train['id']==player.id_in_group]
                current_df_pre.to_csv(player.c.TRAIN_CSV_PATH + "%d_%s.csv" % (player.id_in_group, get_group_id(player.id_in_group)),index=False)
                # player.player_train.drop(current_df_pre.index,inplace=True) # 减少存储开销
        else:
            player.player_prelabel.loc[len(player.player_prelabel)] = [
                r_num,
                r_data['text'],
                player.sen_result,
                player.id_in_group,
                get_group_id(player.id_in_group),
                player.Human_confidence
            ]
            if r_num == 32: # 保存用户的数据
                current_df_pre = player.player_prelabel[player.player_prelabel['id']==player.id_in_group]
                current_df_pre.to_csv(player.c.PRELABEL_CSV_PATH + "%d_%s.csv" % (player.id_in_group, get_group_id(player.id_in_group)),index=False)
                # player.player_prelabel.drop(current_df_pre.index,inplace=True) # 减少存储开销

'''预测32条文本情感页面'''
class MyPage(Page):
    form_model = 'player'
    form_fields = ['sen_result','AI_confidence','Human_confidence']
    @staticmethod
    def vars_for_template(player):
        r_num = player.round_number
        r_data = player.df.iloc[r_num-1]
        return dict(
            ID=r_num, # 轮数
            group_id = get_group_id(player.id_in_group),
            content_weibo=r_data['text'],
            predict_weibo_sen = r_data['pred_str'], # 预测类
            AI_predict_rate = str(r_data['main_emotion_confidence(1-5)_AI']), # AI置信度
            image_path='lime_imgs/lime_exp{}.png'.format(r_num-1), # 可解释性导入
            icon_path='starIcon.png',
            )
    @staticmethod
    def before_next_page(player, timeout_happened):
        r_num = player.round_number
        r_data = player.df.iloc[r_num-1]
        # 写入用户的数据
        player.player_train.loc[len(player.player_train)] = [
            r_num,
            r_data['text'],
            player.sen_result,
            player.id_in_group,
            get_group_id(player.id_in_group),
            player.AI_confidence,
            player.Human_confidence
        ]
        if r_num == 32: # 保存用户的数据
            current_df_train = player.player_train[player.player_train['id']==player.id_in_group]
            current_df_train.to_csv(player.c.TRAIN_CSV_PATH + "%d_%s.csv" % (player.id_in_group, get_group_id(player.id_in_group)),index=False)
            # player.player_train.drop(current_df_train.index,inplace=True) # 减少存储开销
    @staticmethod
    def is_displayed(player):
        group_id = get_group_id(player.id_in_group)
        return player.round_number <= 32 and group_id != 'A'

'''Attention Check页面'''
class MyAC(Page):
    form_model = 'player'
    form_fields = ['sen_result']
    @staticmethod
    def vars_for_template(player):
        r_num = player.round_number
        return dict(
            ID=r_num,
            icon_path='starIcon.png'
        )
    @staticmethod
    def before_next_page(player, timeout_happened):
        r_num = player.round_number
        if r_num == 16: # 保存数据
            player.player_ac.loc[len(player.player_ac)] = [r_num,player.sen_result,player.id_in_group,get_group_id(player.id_in_group)]
            player.player_ac.to_csv(player.c.OTHER_CSV_PATH + "attention_check.csv", index=False)
    @staticmethod
    def is_displayed(player):
        return player.round_number == 16

'''预测32条文本情感页面'''
class MyTest(Page):
    form_model = 'player'
    form_fields = ['sen_result','Human_confidence']
    @staticmethod
    def vars_for_template(player):
        r_num = player.round_number
        r_data = player.df.iloc[r_num-1]
        return dict(
            ID=r_num-32,
            content_weibo=r_data['text'],
            icon_path='starIcon.png'
        )
    @staticmethod
    def before_next_page(player, timeout_happened): # 写入和保存至test_csv
        r_num = player.round_number
        r_data = player.df.iloc[r_num-1]
        # 保存数据，字段同上
        player.player_test.loc[len(player.player_test)] = [
            r_num,
            r_data['text'],
            player.sen_result,
            player.id_in_group,
            get_group_id(player.id_in_group),
            player.Human_confidence
        ]
        if r_num == 64:
            current_df_test = player.player_test[player.player_test['id']==player.id_in_group]
            current_df_test.to_csv(player.c.TEST_CSV_PATH + "%d_%s.csv" % (player.id_in_group, get_group_id(player.id_in_group)),index=False)
            player.player_test.drop(current_df_test.index,inplace=True) # 减少存储开销
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
        if group_id in "ABD": # without AI explanation,不展示问题7
            return ['age','gender','education','crt_bat','crt_widget','crt_lake','Q1','Q2','Q3','Q4','attention','Q5','Q6','advice']
        elif group_id in 'CE': # with AI explanation,展示问题7
            return ['age','gender','education','crt_bat','crt_widget','crt_lake','Q1','Q2','Q3','Q4','attention','Q5','Q6',"Q7",'advice']
    @staticmethod
    def vars_for_template(player):
        return dict( num=player.round_number,
                     group_id = get_group_id(player.id_in_group),
                     )
    @staticmethod
    def is_displayed(player):
        return player.round_number == 64
    @staticmethod
    def before_next_page(player, timeout_happened):
        group_id = get_group_id(player.id_in_group)
        if group_id in "ABD":
            player.player_survey.loc[len(player.player_survey)] = [player.id_in_group,player.age,player.gender,player.education,player.crt_bat,player.crt_widget,player.crt_lake,player.Q1,player.Q2,player.Q3,player.Q4,player.attention,player.Q5,player.Q6,None,player.advice]
        elif group_id in 'CE':
            player.player_survey.loc[len(player.player_survey)] = [player.id_in_group,player.age,player.gender,player.education,player.crt_bat,player.crt_widget,player.crt_lake,player.Q1,player.Q2,player.Q3,player.Q4,player.attention,player.Q5,player.Q6,player.Q7,player.advice]
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
        reward = bonus.calculate_bonus()
        return dict( reward=reward )

page_sequence = [Introduction,PrePage,MyPage,MyAC,MyTest,ResultWaitPage,ExitSurveyPage,RewardPage]
