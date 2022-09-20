from otree.api import *
from . import *


class PlayerBot(Bot):
    def play_round(self):
        group_id = get_group_id(self.player.id_in_group)
        if self.round_number == 1:
            if group_id in ['A','D']:
                yield Introduction, dict(test=25)
            if group_id in ['B','E']:
                yield Introduction, dict(test=28)
            if group_id in ['C','F']:
                yield Introduction, dict(test=24.5)
        if self.round_number <= 100:
            yield MyPage, dict(sen_result="1")
        if self.round_number == 100:
            time.sleep(20)
            yield ResultWaitPage
        if self.round_number > 100:
            yield MyTest, dict(sen_result="1")
        if self.round_number == 50:
            yield MyAC, dict(ac_result="0")
        if self.round_number % 20 == 0 and self.round_number < 100:
            yield RestPage
        if self.round_number == 120:
            time.sleep(10)
            if group_id == "A" or group_id == 'B' or group_id == 'C':
                yield (
                    ExitSurveyPage,
                    dict(age='1',gender='1',education='1',Q1='1',Q2='1',Q3='1',Q4='1',Q5='1',Q6='1',Q8='1',attention='1',advice='None')
                )
            else:
                yield (
                    ExitSurveyPage,
                    dict(age='1',gender='1',education='1',Q1='1',Q2='1',Q3='1',Q4='1',Q5='1',Q6='1',Q7='1',Q8='1',attention='1',advice='None')
                )



