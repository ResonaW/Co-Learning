from otree.api import *
from . import *


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield Introduction, dict(test=25)
        if self.round_number <= 100:
            yield MyPage, dict(sen_result="1")
        if self.round_number == 100:
            time.sleep(60)
            yield ResultWaitPage
        if self.round_number > 100:
            yield MyTest, dict(sen_result="1")
        if self.round_number == 50:
            yield MyAC, dict(ac_result="0")
        if self.round_number == 120:
            time.sleep(10)
            yield (
                exit_survey,
                dict(age='1',gender='1',education='1',Q1='1',Q2='1',Q3='1',Q4='1',Q5='1',Q6='1',Q7='1',Q8='1',attention='1',advice='None')
            )



