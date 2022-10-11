from otree.api import *
from . import *
import random


class PlayerBot(Bot):
    def play_round(self):
        group_id = get_group_id(self.player.id_in_group)
        if self.round_number == 1:
            yield Introduction, dict(phone=str(random.randint(0,1000)))
            # time.sleep(10)
        if self.round_number <= 32 and ( group_id in 'ADEG'):
            yield PrePage, dict(sen_result=str(random.randint(0,6)), Human_confidence="5",pagetime=10)
        if self.round_number <= 32 and group_id != 'A':
            yield MyPage, dict(sen_result=str(random.randint(0,6)),AI_confidence="1",Human_confidence="5",pagetime=10)
            # time.sleep(3)
        if self.round_number == 16 or self.round_number == 48:
            yield MyAC, dict(sen_result="1")
            time.sleep(5)
        if self.round_number > 32:
            yield MyTest, dict(sen_result=str(random.randint(0,6)), Human_confidence="5",pagetime=10)
        if self.round_number == 32:
            yield ResultWaitPage
            # time.sleep(30)
        if self.round_number == 64:
            if group_id == "A":
                yield (
                    ExitSurveyPage,
                    dict(age='1',gender='1',education='1',Q1='1',Q2='1',Q3='1',Q13='1',Q8='1',attention='1',crt_bat=100,crt_widget=100,crt_lake=100)
                )
            elif group_id in "BD":
                yield (
                    ExitSurveyPage,
                    dict(age='1',gender='1',education='1',Q1='1',Q2='1',Q3='1',Q4='1',Q6='1',Q8='1',attention='1',crt_bat=100,crt_widget=100,crt_lake=100,Q13='1',Q9='1',Q10='1',Q11='1',Q12='1')
                )
            else:
                yield (
                    ExitSurveyPage,
                    dict(age='1',gender='1',education='1',Q1='1',Q2='1',Q3='1',Q4='1',Q7='1',Q8='1',attention='1',crt_bat=100,crt_widget=100,crt_lake=100,Q13='1',Q9='1',Q10='1',Q11='1',Q12='1')
                )
            time.sleep(20)



