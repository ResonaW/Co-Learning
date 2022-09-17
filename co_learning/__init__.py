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
        self.SUFFIX_MODEL = '_test_model'
        self.SUFFIX_MANUAL = '_test_manual'
        self.TRUE_LABELS = [0,0,1,0,1,0,1,0,1,1,1,0,0,0,1,0,1,0,0,1]
        self.CSV_PATH = '/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/csv/'
        
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
    PLAYERS_PER_GROUP = 30
    NUM_ROUNDS = 120
    file=pd.read_excel("/home/ubuntu/Otree_Project/Co-Learning/co_learning/情感分析_20220915.xlsx")

# class Session(BaseSession):
#     pass

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    c=C()
    df=c.file
    test = models.IntegerField(
        label='假设你和AI已经完成了测试阶段的20个标注，你答对了其中的16个，AI答对了其中的14个，你答对的16个标注中有12个是与AI的答案一致的（你和AI都答对了），你标注错误的4个标注中有3个是与AI的答案一致的（你和AI都答错了），那你最后的薪酬是？',
        # choices=[['1', '25'], ['2', '28'], ['3', '24.5']],
    )
    player_data = pd.DataFrame(columns=["content", "round", "result","id","group"])
    player_ac = pd.DataFrame(columns=["round", "result", "id", "group"])
    score = models.IntegerField()
    sen_result = models.IntegerField()
    ac_result = models.IntegerField()
    age = models.IntegerField(
        label='1、您的年龄段是?',
        choices=[['1', '18岁以下'], ['2', '18-25岁'], ['3', '26-30岁'], ['4', '31-35岁'], ['5', '35岁以上']],
    )
    gender = models.StringField(
        choices=[['1', '男性'], ['2', '女性']],
        label='2、您的性别是?',
    )
    education = models.StringField(
        choices=[['1', '高中'], ['2', '大专'], ['3', '本科'], ['4', '硕士'], ['5', '博士及以上']],
        label='3、您的教育程度是?',
    )
    Q1 = models.IntegerField(
        label='4、我觉得这项任务需要集中精神：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q2 = models.IntegerField(
        label='5、我觉得成功地完成了我所需要完成的任务：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q3 = models.IntegerField(
        label='6、在标注过程中，我会感到有压力、不安全、气馁、易怒和生气：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q4 = models.IntegerField(
        label='7、我相信AI能够根据微博内容做出正确的分类：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    attention = models.IntegerField(
        label='8、这是一道注意力测试题，旨在检测志愿者在实验过程中是否认真审题、作答。为表明你在本次实验中认真审题、作答，请选择“非常反对”这一选项。',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q5 = models.IntegerField(
        label='9、我相信我的标注显着提高了 AI 在文本分类方面的准确性：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q6 = models.IntegerField(
        label='10、我觉得我对人工智能的工作原理有了很好的理解：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    Q7 = models.IntegerField(
        label='11、我觉得我很好地理解了 AI 将微博分类的理由：',
        choices=[['1', '非常反对'], ['2', '反对'], ['3', '一般'], ['4', '赞同'], ['5', '非常赞同']]
    )
    advice = models.StringField(label="11、您是否有其它的建议或意见，或者谈谈您对实验的感受？")

# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['sen_result']
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
        round_data = player.df.loc[round_num - 1].tolist()
        round_content = round_data[1]
        round_result = player.sen_result
        id = player.id_in_group
        if id % 3 == 0:
            sort = 'C'
        elif (id - 1) % 3 == 0:
            sort = 'A'
        elif (id - 2) % 3 == 0:
            sort = 'B'
        player.player_data.loc[len(player.player_data.index)] = [round_content,round_num,round_result,player.id_in_group,sort]
        if round_num == 100:
            tmp_df = player.player_data.rename({'content':'标题/微博内容'},axis=1)
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
            ID=r_data[0]-100,
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
        if id % 3 == 0 :
            sort = 'C'
        elif ( id - 1 ) % 3 == 0:
            sort = 'A'
        elif ( id - 2 ) % 3 == 0:
            sort = 'B'
        tmp_list = [round_content,round_num,round_result,player.id_in_group,sort]
        player.player_data.loc[len(player.player_data)] = tmp_list
        if round_num == 120:
            tmp_df = player.player_data.rename({'content':'标题/微博内容'},axis=1)
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
            if id % 3 == 0:
                sort = 'C'
            elif (id - 1) % 3 == 0:
                sort = 'A'
            elif (id - 2) % 3 == 0:
                sort = 'B'
            player.player_ac.loc[len(player.player_ac.index)] = [round_num,round_result,player.id_in_group,sort]
            player.player_ac.to_csv("/home/ubuntu/Otree_Project/Co-Learning/watchdog_trainer/attention_check/attention_check_%d.csv" % player.id_in_group, index=False)
    def is_displayed(player):
        return player.round_number == 50

class exit_survey(Page):
    form_model = 'player'
    form_fields = ['age','gender','education','Q1','Q2','Q3','Q4','Q5','attention','Q6','Q7','advice']
    @staticmethod
    def vars_for_template(player):
        return dict( num=player.round_number )
    @staticmethod
    def is_displayed(player):
        return player.round_number == 120
    @staticmethod
    def before_next_page(player, timeout_happened):
        id = player.id_in_group
        if id % 3 == 0 :
            sort = 'C'
        elif ( id - 1 ) % 3 == 0:
            sort = 'A'
        elif ( id - 2 ) % 3 == 0:
            sort = 'B'
        bonus = Bonus(id_in_group=id,group_id=sort)
        if sort=='A':
            while not bonus.flag:
                bonus.manual_csv_name_check()
        elif sort=='B' or sort=='C':
            while not bonus.flag:
                bonus.model_csv_name_check()
        
class Introduction(Page):
    form_model = 'player'
    def is_displayed(player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player):
        id = player.id_in_group
        if id % 3 == 0 :
            sort = 'C'
        elif ( id - 1 ) % 3 == 0:
            sort = 'A'
        elif ( id - 2 ) % 3 == 0:
            sort = 'B'
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
        if id % 3 == 0 :
            sort = 'C'
        elif ( id - 1 ) % 3 == 0:
            sort = 'A'
        elif ( id - 2 ) % 3 == 0:
            sort = 'B'
        bonus = Bonus(id_in_group=id,group_id=sort)
        reward = bonus.calculate_bonus()
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

class test(Page):
    form_model = 'player'
    form_fields = ['test']
    @staticmethod
    def error_message(player, values):
        id = player.id_in_group
        if id % 3 == 0 :
            print('你的答案是', values)
            if values['test'] != 24.5:
                return '你计算的薪酬有误，再重新想想吧！'
        elif ( id - 1 ) % 3 == 0:
            print('你的答案是', values)
            if values['test'] != 25:
                return '你计算的薪酬有误，再重新想想吧！'
        elif ( id - 2 ) % 3 == 0:
            print('你的答案是', values)
            if values['test'] != 28:
                return '你计算的薪酬有误，再重新想想吧！'
    def is_displayed(player):
        return player.round_number == 1

#随机分组
# def creating_session(subsession):
#     import itertools
#     pressures = itertools.cycle([True, False])
#     for player in subsession.get_players():
#         player.time_pressure = next(pressures)

page_sequence = [Introduction,test,MyPage,ResultWaitPage,MyTest,MyAC,exit_survey,reward]
