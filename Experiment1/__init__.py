from otree.api import *
import pandas as pd
import time
import os
import numpy as np
import random

doc = """Co-Learning"""

def get_group_id(id_in_group):
    '''A：手工；B；展示预测；C：展示预测+AI置信度；D：预测+可解释'''
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

# 报酬=5（基础）+1*标对-0.5*标错
class Bonus():
    '''计算受访者报酬'''
    def __init__(self, id_in_group, group_id) -> None:
        self.id_in_group =  id_in_group
        self.group_id = group_id
        self.flag = False
        self.TRUE_LABELS = [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]
        # self.CSV_PATH = '/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/csv/'
        self.CSV_PATH = './Co-Learning/watchdog_trainer/csv/'
        self.manual_csv_name = self.CSV_PATH+"%d_%s_test_manual.csv" % (self.id_in_group,self.group_id)
        self.model_csv_name = self.CSV_PATH+"%d_%s_test_model.csv" % (self.id_in_group,self.group_id)
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
        manual_df = pd.read_csv(self.manual_csv_name)
        human_correct = self.correct_count(manual_df['label'].to_list(),self.TRUE_LABELS)
        salary = 10+human_correct*2-(20-human_correct)*1
        return salary

class C(BaseConstants):
    NAME_IN_URL = 'Experiment1'
    # 待修改 后续应该是600人
    PLAYERS_PER_GROUP = 30
    NUM_ROUNDS = 64
    # file=pd.read_excel("/home/ubuntu/Otree_Project/Co-Learning/co_learning/dataset.xlsx")
    file = pd.read_excel("./co_learning/dataset.xlsx")
    file_spare = pd.read_excel('./co_learning/spare_dataset.xlsx')

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    c=C()
    # 训练集dataframe
    df=c.file
    # 用户情感判断结果dataframe列表
    # player_data = [pd.DataFrame(columns=["ID","text", "round", "label", "id","group","change","AI_confidence","Human_confidence"]) for _ in range(c.PLAYERS_PER_GROUP)]
    player_data = pd.DataFrame(columns=["ID", "text", "round", "label", "id", "group", "change", "AI_confidence", "Human_confidence"])
    # 随机文本展示
    # random_list = [[i for i in range(100)] for _ in range(100)]
    # for i in range(100):
    #     random.shuffle(random_list[i])
    # 用户Attention Check结果dataframe
    player_ac = pd.DataFrame(columns=["round", "result", "id", "group"])
    # 用户情感判断结果及Attention Check结果
    sen_result = models.IntegerField()
    sen_result_pre = models.IntegerField()
    # 用户看过AI预测结果后的更改的结果
    ac_result = models.IntegerField()
    # SurveyPage问题
    age = models.IntegerField(
        label='您的年龄段是?',
        choices=[['1', '18岁以下'], ['2', '18-25岁'], ['3', '26-30岁'], ['4', '31-35岁'], ['5', '35岁以上']],
    )
    gender = models.StringField(
        choices=[['1', '男性'], ['2', '女性']],
        label='您的性别是?',
    )
    education = models.StringField(
        choices=[['1', '高中'], ['2', '大专'], ['3', '本科'], ['4', '硕士'], ['5', '博士及以上']],
        label='您的教育程度是?',
    )
    Q1 = models.IntegerField(
        label='我觉得这项任务需要集中精神：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q2 = models.IntegerField(
        label='我觉得成功地完成了我所需要完成的任务：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q3 = models.IntegerField(
        label='在标注过程中，我会感到有压力、不安全、气馁、易怒和生气：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q4 = models.IntegerField(
        label='我相信AI能够根据评论内容做出正确的分类：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    attention = models.IntegerField(
        label='这是一道注意力测试题，旨在检测志愿者在实验过程中是否认真审题、作答。为表明你在本次实验中认真审题、作答，请选择“非常反对”这一选项。',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q5 = models.IntegerField(
        label='我相信我的标注显着提高了 AI 在文本分类方面的准确性：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q6 = models.IntegerField(
        label='我觉得我对人工智能的工作原理有了很好的理解：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q7 = models.IntegerField(
        label='我觉得我很好地理解了 AI 将评论分类的理由：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q8 = models.IntegerField(
        label='现有以下三种薪酬计算方式：'
              '1、根据你在第二阶段的表现计算薪酬。'
              '2、根据AI在第二阶段的表现计算薪酬。'
              '3、根据你和AI在第二阶段的综合表现计算薪酬。'
              '如果可以选择，你会选择采用哪种计算方式来计算你最后的薪酬？',
        choices=[['1', '第一种'], ['2', '第二种'], ['3', '第三种']]
    )
    advice = models.StringField(label="您是否有其它的建议或意见，或者谈谈您对实验的感受？")
#     添加收集对AI预测结果以及自己判断的信心
    AI_confidence = models.IntegerField()
    AI_confidence_pre = models.IntegerField()
    Human_confidence = models.IntegerField()
    Human_confidence_pre = models.IntegerField()

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
        return dict(id=group_id)

class PrePage(Page):
    form_model = 'player'
    form_fields = ['sen_result_pre','Human_confidence_pre']
    @staticmethod
    def vars_for_template(player):
        r_num = player.round_number
        # r_data = player.df.loc[player.random_list[player.id_in_group-1][r_num-1]].tolist()
        r_data = player.df.loc[player.round_number].tolist()
        group_id = get_group_id(player.id_in_group)
        return dict(
            ID=r_num,
            group_id = group_id,
            content_weibo=r_data[1],
            predict_weibo_sen = r_data[2],
            # 放进AI置信度
            AI_predict_rate = "4",
            # 可解释性导入
            # image_path='lime_imgs/lime_exp{}.png'.format(player.random_list[player.id_in_group-1][r_num-1]),
            image_path='lime_imgs/lime_exp{}.png'.format(player.round_number),
            icon_path='starIcon.png',
            )
    @staticmethod
    def is_displayed(player):
        group_id = get_group_id(player.id_in_group)
        return player.round_number <= 32 and ( group_id == 'D' or group_id == 'E' or group_id == 'A')

'''预测32条文本情感页面'''
class MyPage(Page):
    form_model = 'player'
    form_fields = ['sen_result','AI_confidence','Human_confidence']
    @staticmethod
    def vars_for_template(player):
        r_num = player.round_number
        # r_data = player.df.loc[player.random_list[player.id_in_group-1][r_num-1]].tolist()
        r_data = player.df.loc[player.round_number].tolist()
        group_id = get_group_id(player.id_in_group)
        return dict(
            ID=r_num,
            group_id = group_id,
            content_weibo=r_data[1],
            predict_weibo_sen = r_data[2],
            # 放进AI置信度
            AI_predict_rate = "4",
            # 可解释性导入
            # image_path='lime_imgs/lime_exp{}.png'.format(player.random_list[player.id_in_group-1][r_num-1]),
            image_path='lime_imgs/lime_exp{}.png'.format(player.round_number),
            icon_path='starIcon.png',
            )
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     r_num = player.round_number
    #     ID = player.random_list[player.id_in_group-1][r_num-1]
    #     round_data = player.df.loc[player.random_list[player.id_in_group-1][r_num-1]].tolist()
    #     round_content = round_data[1]
    #     round_result = player.sen_result
    #     group_id = get_group_id(player.id_in_group)
    #     # 是否选择将样本添加训练
    #     train_change = player.change_sample
    #     AI_confidence = player.AI_confidence
    #     Human_confidence = player.Human_confidence
    #     current_df = player.player_data[player.id_in_group-1]
    #     current_df.loc[len(current_df)] = [ID,round_content,r_num,round_result,player.id_in_group,group_id,train_change,AI_confidence,Human_confidence]
    #     if r_num == 100:
    #         current_df = current_df.sort_values(by='ID',ascending=True)
    #         current_df.to_csv("./watchdog_trainer/csv/%d_%s.csv" % (player.id_in_group,group_id),index=False)
    @staticmethod
    def is_displayed(player):
        group_id = get_group_id(player.id_in_group)
        return player.round_number <= 32 and group_id != 'A'

'''Attention Check页面'''
class MyAC(Page):
    form_model = 'player'
    form_fields = ['ac_result']
    @staticmethod
    def vars_for_template(player):
        r_num = player.round_number
        return dict(
            ID=r_num,
            icon_path='starIcon.png'
        )
    @staticmethod
    def before_next_page(player, timeout_happened):
        round_num = player.round_number
        if round_num == 16:
            round_result = player.ac_result
            group_id = get_group_id(player.id_in_group)
            player.player_ac.loc[len(player.player_ac.index)] = [round_num,round_result,player.id_in_group,group_id]
            # player.player_ac.to_csv("/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/attention_check/attention_check.csv", index=False)
            player.player_ac.to_csv("./watchdog_trainer/attention_check/attention_check.csv", index=False)
    def is_displayed(player):
        return player.round_number == 16

'''预测32条文本情感页面'''
class MyTest(Page):
    form_model = 'player'
    form_fields = ['sen_result','Human_confidence']
    @staticmethod
    def vars_for_template(player):
        r_num = player.round_number
        r_data = player.df.loc[r_num-1].tolist()
        return dict(
            ID=r_num-32,
            content_weibo=r_data[1],
            predict_weibo_sen = r_data[2]
        )
    @staticmethod
    def before_next_page(player, timeout_happened):
        r_num = player.round_number
        round_data = player.df.loc[r_num-1].tolist()
        round_content = round_data[1]
        round_result = player.sen_result
        group_id = get_group_id(player.id_in_group)
        current_df = player.player_data[player.id_in_group-1]
        current_df.loc[len(current_df)] = [r_num-1,round_content,r_num,round_result,player.id_in_group,group_id,None,None,None]
        if r_num == 64:
            current_df = current_df.iloc[-20:,:]
            current_df = current_df.sort_values(by='ID',ascending=True)
            # current_df.to_csv("/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/csv/%d_%s_test_manual.csv" % (player.id_in_group, group_id), index=False)
            current_df.to_csv("./watchdog_trainer/csv/%d_%s_test_manual.csv" % (player.id_in_group, group_id), index=False)
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
        if group_id == "A" or group_id == 'B' or group_id == 'C':
            return ['age','gender','education','Q1','Q2','Q3','Q4','attention','Q5','Q6',"Q8",'advice']
        elif group_id == 'D':
            return ['age','gender','education','Q1','Q2','Q3','Q4','attention','Q5','Q6',"Q7","Q8",'advice']
    @staticmethod
    def vars_for_template(player):
        return dict( num=player.round_number )
    @staticmethod
    def is_displayed(player):
        return player.round_number == 64
    # 薪酬部分可能需要改一改
    @staticmethod
    def before_next_page(player, timeout_happened):
        group_id = get_group_id(player.id_in_group)
        bonus = Bonus(id_in_group=player.id_in_group,group_id=group_id)
        # 应该不需要了？
        # if group_id in ['A','D']:
        #     while not bonus.flag:
        #         bonus.manual_csv_name_check()
        # elif group_id in ['B','C','E','F']:
        #     while not bonus.flag:
        #         bonus.model_csv_name_check()

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
        # 清除数据
        player.player_data[player.id_in_group-1] = None
        return dict( reward=reward )

page_sequence = [Introduction,PrePage,MyPage,MyAC,MyTest,ResultWaitPage,ExitSurveyPage,RewardPage]
