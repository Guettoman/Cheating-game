from otree.api import *

class Constants(BaseConstants):
    name_in_url = 'cheating_game'
    players_per_group = 2
    num_rounds = 5  # Количество раундов
    payoff_no_cheat = 10
    payoff_cheat_success = 12
    payoff_cheat_fail = 0
    base_score = 60
    min_score = 15

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    effort = models.FloatField(min=0, max=100)
    give_permission = models.BooleanField()
    round_payoff = models.CurrencyField()

def creating_session(subsession):
    if subsession.round_number == 1:
        subsession.group_randomly()
