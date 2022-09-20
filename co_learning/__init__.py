from otree.api import *
import pandas as pd
import time
import os
import numpy as np

doc = """
Your app description
"""

class Bonus():
    
    def __init__(self, id_in_group, group_id) -> None:
        self.id_in_group =  id_in_group
        self.group_id = group_id
        self.flag = False
        # self.SUFFIX_MODEL = '_test_model'
        # self.SUFFIX_MANUAL = '_test_manual'
        # 真实标签待修改
        self.TRUE_LABELS = [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]
        self.CSV_PATH = '/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/csv/'
        # 可以进一步修改

    def manual_csv_name_check(self):
        manual_csv_name = self.CSV_PATH+"%d_%s_test_manual.csv" % (self.id_in_group,self.group_id)
        while not os.path.exists(manual_csv_name):
            time.sleep(1)
        self.flag = True

    def model_csv_name_check(self):
        model_csv_name = self.CSV_PATH+"%d_%s_test_model.csv" % (self.id_in_group,self.group_id)
        while not os.path.exists(model_csv_name):
            time.sleep(1)
        self.flag = True
    
    def correct_count(self,list_a,list_b):
        n1 = np.array(list_a) - np.array(list_b)
        return n1.tolist().count(0)

    def calculate_bonus(self):
        manual_csv_name = self.CSV_PATH+"%d_%s_test_manual.csv" % (self.id_in_group,self.group_id)
        model_csv_name = self.CSV_PATH+"%d_%s_test_model.csv" % (self.id_in_group,self.group_id)
        if self.group_id == 'B':
            manual_df = pd.read_csv(manual_csv_name)
            human_correct = self.correct_count(manual_df['label'].to_list(),self.TRUE_LABELS)
            salary = 10+human_correct*2-(20-human_correct)*1
            return salary

        if self.group_id == 'A':
            manual_df = pd.read_csv(manual_csv_name)
            model_df = pd.read_csv(model_csv_name)
            human_correct = self.correct_count(manual_df['label'].to_list(),self.TRUE_LABELS)
            AI_correct = self.correct_count(model_df['label'].to_list(),self.TRUE_LABELS)
            salary = 10+human_correct*1-(20-human_correct)*0.5+AI_correct*1-(20-AI_correct)*0.5
            return salary

        if self.group_id == 'C':
            manual_df = pd.read_csv(manual_csv_name)
            model_df = pd.read_csv(model_csv_name)
            human_correct = self.correct_count(manual_df['label'].to_list(),self.TRUE_LABELS)
            human_AI_consistency_right = self.correct_count(model_df['label'].to_list(),manual_df['label'].to_list())
            salary = 10 + human_correct * 1 - (20 - human_correct) * 0.5 +human_AI_consistency_right*1-(20-human_AI_consistency_right)*0.5
            return salary

class C(BaseConstants):
    NAME_IN_URL = 'co_learning'
    # 待修改
    PLAYERS_PER_GROUP = 30
    NUM_ROUNDS = 120
    file=pd.read_excel("/home/ubuntu/Otree_Project/Co-Learning/co_learning/情感分析_20220915.xlsx")

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    c=C()
    df=c.file
    test = models.FloatField(
        label='在下面的输入框中给出你的答案，只有正确计算出薪酬才能开始接下来的标注任务',
    )
    player_data = [pd.DataFrame(columns=["content", "round", "result","id","group"]) for x in range(c.PLAYERS_PER_GROUP)]
    player_ac = pd.DataFrame(columns=["round", "result", "id", "group"])
    score = models.IntegerField()
    sen_result = models.IntegerField()
    ac_result = models.IntegerField()
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

# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['sen_result']
    @staticmethod
    def vars_for_template(player):
        r_num = player.round_number
        r_data_0 = player.df.loc[r_num-1]
        r_data = r_data_0.tolist()
        id = player.id_in_group
        if id % 6 == 0:
            sort = 'F'
        elif (id - 1) % 6 == 0 or id == 1:
            sort = 'A'
        elif (id - 2) % 6 == 0 or id == 2:
            sort = 'B'
        elif (id - 3) % 6 == 0 or id == 3:
            sort = 'C'
        elif (id - 4) % 6 == 0 or id == 4:
            sort = 'D'
        elif (id - 5) % 6 == 0 or id == 5:
            sort = 'E'
        return dict(
            ID=r_num,
            group_id = sort,
            content_weibo=r_data[1],
            predict_weibo_sen = r_data[2],
            # 把图片读进网页,路径待修改
            image_path='lime_imgs/lime_exp{}.png'.format(int(r_num)-1),
            label=sort
            )
    @staticmethod
    def before_next_page(player, timeout_happened):
        round_num = player.round_number
        round_data = player.df.loc[round_num - 1].tolist()
        round_content = round_data[1]
        round_result = player.sen_result
        id = player.id_in_group
        if id % 6 == 0:
            sort = 'F'
        elif (id - 1) % 6 == 0 or id == 1:
            sort = 'A'
        elif (id - 2) % 6 == 0 or id == 2:
            sort = 'B'
        elif (id - 3) % 6 == 0 or id == 3:
            sort = 'C'
        elif (id - 4) % 6 == 0 or id == 4:
            sort = 'D'
        elif (id - 5) % 6 == 0 or id == 5:
            sort = 'E'
        current_df = player.player_data[player.id_in_group-1]
        current_df.loc[len(current_df)] = [round_content,round_num,round_result,player.id_in_group,sort]
        if round_num == 100:
            tmp_df = current_df.rename({'content':'标题/微博内容'},axis=1)
            tmp_df['label'] = tmp_df['result'].apply(lambda x:1 if str(x)=='111' else 0)
            tmp_df.to_csv("/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/csv/%d_%s.csv" % (player.id_in_group,sort),index=False)
    def is_displayed(player):
        return player.round_number <= 100

class MyTest(Page):
    form_model = 'player'
    form_fields = ['sen_result']
    @staticmethod
    def vars_for_template(player):
        r_num = player.round_number
        r_data_0 = player.df.loc[r_num-1]
        r_data = r_data_0.tolist()
        return dict(
            ID=r_num-100,
            content_weibo=r_data[1],
            predict_weibo_sen = r_data[2]
        )
    @staticmethod
    def before_next_page(player, timeout_happened):
        round_num = player.round_number
        round_data = player.df.loc[round_num - 1].tolist()
        round_content = round_data[1]
        round_result = player.sen_result
        id = player.id_in_group
        if id % 6 == 0:
            sort = 'F'
        elif (id - 1) % 6 == 0 or id == 1:
            sort = 'A'
        elif (id - 2) % 6 == 0 or id == 2:
            sort = 'B'
        elif (id - 3) % 6 == 0 or id == 3:
            sort = 'C'
        elif (id - 4) % 6 == 0 or id == 4:
            sort = 'D'
        elif (id - 5) % 6 == 0 or id == 5:
            sort = 'E'
        current_df = player.player_data[player.id_in_group-1]
        current_df.loc[len(current_df)] = [round_content,round_num,round_result,player.id_in_group,sort]
        if round_num == 120:
            tmp_df = current_df.rename({'content':'标题/微博内容'},axis=1)
            tmp_df['label'] = tmp_df['result'].apply(lambda x:1 if str(x)=='111' else 0)
            tmp_df = tmp_df.iloc[-20:,:]
            tmp_df.to_csv("/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/csv/%d_%s_test_manual.csv" % (player.id_in_group,sort), index=False)
    def is_displayed(player):
        return player.round_number > 100

class MyAC(Page):
    form_model = 'player'
    form_fields = ['ac_result']
    @staticmethod
    def vars_for_template(player):
        r_num = player.round_number
        r_data_0 = player.df.loc[r_num-1]
        r_data = r_data_0.tolist()
        return dict(
            ID=r_data[0],
            content_weibo=r_data[1],
            predict_weibo_sen = r_data[2]
        )
    @staticmethod
    def before_next_page(player, timeout_happened):
        round_num = player.round_number
        id = player.id_in_group
        if round_num == 50:
            round_result = player.ac_result
            if id % 6 == 0:
                sort = 'F'
            elif (id - 1) % 6 == 0 or id == 1:
                sort = 'A'
            elif (id - 2) % 6 == 0 or id == 2:
                sort = 'B'
            elif (id - 3) % 6 == 0 or id == 3:
                sort = 'C'
            elif (id - 4) % 6 == 0 or id == 4:
                sort = 'D'
            elif (id - 5) % 6 == 0 or id == 5:
                sort = 'E'
            player.player_ac.loc[len(player.player_ac.index)] = [round_num,round_result,player.id_in_group,sort]
            player.player_ac.to_csv("/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/attention_check/attention_check.csv", index=False)
    def is_displayed(player):
        return player.round_number == 50

class exit_survey(Page):
    form_model = 'player'
    form_fields = ['age','gender','education','Q1','Q2','Q3','Q4','attention','Q5','Q6','advice']
    @staticmethod
    def get_form_fields(player):
        id = player.id_in_group
        if id % 6 == 0:
            sort = 'F'
        elif (id - 1) % 6 == 0 or id == 1:
            sort = 'A'
        elif (id - 2) % 6 == 0 or id == 2:
            sort = 'B'
        elif (id - 3) % 6 == 0 or id == 3:
            sort = 'C'
        elif (id - 4) % 6 == 0 or id == 4:
            sort = 'D'
        elif (id - 5) % 6 == 0 or id == 5:
            sort = 'E'
        if sort == "A" or sort == 'B' or sort == 'C':
            return ['age','gender','education','Q1','Q2','Q3','Q4','attention','Q5','Q6',"Q8",'advice']
        elif sort == "C" or sort == 'D' or sort == 'E':
            return ['age','gender','education','Q1','Q2','Q3','Q4','attention','Q5','Q6',"Q7","Q8",'advice']
    @staticmethod
    def vars_for_template(player):
        return dict( num=player.round_number )
    @staticmethod
    def is_displayed(player):
        return player.round_number == 120
    @staticmethod
    def before_next_page(player, timeout_happened):
        id = player.id_in_group
        if id % 6 == 0:
            sort = 'F'
        elif (id - 1) % 6 == 0 or id == 1:
            sort = 'A'
        elif (id - 2) % 6 == 0 or id == 2:
            sort = 'B'
        elif (id - 3) % 6 == 0 or id == 3:
            sort = 'C'
        elif (id - 4) % 6 == 0 or id == 4:
            sort = 'D'
        elif (id - 5) % 6 == 0 or id == 5:
            sort = 'E'
        bonus = Bonus(id_in_group=id,group_id=sort)
        if sort=='A':
            while not bonus.flag:
                bonus.manual_csv_name_check()
        elif sort=='B' or sort=='C':
            while not bonus.flag:
                bonus.model_csv_name_check()
        
class Introduction(Page):
    form_fields = ['test']
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def error_message(player, values):
        id = player.id_in_group
        if id % 6 == 0 or (id - 3) % 6 == 0 or id == 3:
            print('你的答案是', values)
            if values['test'] != 24.5:
                return '你计算的薪酬有误，再重新想想吧！'
        elif (id - 1) % 6 == 0 or id == 1 or (id - 4) % 6 == 0 or id == 4:
            print('你的答案是', values)
            if values['test'] != 25:
                return '你计算的薪酬有误，再重新想想吧！'
        elif (id - 2) % 6 == 0 or id == 5 or (id - 5) % 6 == 0 or id == 2:
            print('你的答案是', values)
            if values['test'] != 28:
                return '你计算的薪酬有误，再重新想想吧！'
    @staticmethod
    def vars_for_template(player):
        id = player.id_in_group
        if id % 6 == 0:
            sort = 'F'
        elif (id - 1) % 6 == 0 or id == 1:
            sort = 'A'
        elif (id - 2) % 6 == 0 or id == 2:
            sort = 'B'
        elif (id - 3) % 6 == 0 or id == 3:
            sort = 'C'
        elif (id - 4) % 6 == 0 or id == 4:
            sort = 'D'
        elif (id - 5) % 6 == 0 or id == 5:
            sort = 'E'
        return dict(id=sort)

class ResultWaitPage(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 100

class reward(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 120
    @staticmethod
    def vars_for_template(player):
        id = player.id_in_group
        if id % 6 == 0:
            sort = 'F'
        elif (id - 1) % 6 == 0 or id == 1:
            sort = 'A'
        elif (id - 2) % 6 == 0 or id == 2:
            sort = 'B'
        elif (id - 3) % 6 == 0 or id == 3:
            sort = 'C'
        elif (id - 4) % 6 == 0 or id == 4:
            sort = 'D'
        elif (id - 5) % 6 == 0 or id == 5:
            sort = 'E'
        bonus = Bonus(id_in_group=id,group_id=sort)
        reward = bonus.calculate_bonus()
        # 清除数据
        player.player_data[player.id_in_group-1] = None
        return dict( reward=reward )

#新加进来的部分！！0916
class xiuxi(Page):
    form_model = 'player'
    def is_displayed(player):
        return player.round_number % 20 == 0 and player.round_number < 100
    @staticmethod
    def vars_for_template(player):
        return dict(
            round = player.round_number,
        )


page_sequence = [Introduction,MyPage,ResultWaitPage,MyTest,MyAC,exit_survey,reward]
