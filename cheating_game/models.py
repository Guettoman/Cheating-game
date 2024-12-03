from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer
)
import random

doc = """
This is a cheating game.
"""


class Constants(BaseConstants):
    name_in_url = 'cheating_game'
    players_per_group = 2
    num_rounds = 1 # Изменено:  число раундов задается в settings.py
    endowment_giver = 10
    endowment_receiver = 0
    changing_partners = False # Переменная для настройки режима партнёров


class Subsession(BaseSubsession):
    def creating_session(self):
        self.session.vars['changing_partners'] = self.session.config['changing_partners']
        if not self.round_number == 1:
            self.group_randomly()

class Group(BaseGroup):
    giver_choice = models.BooleanField(
        choices=[
            [True, "Разрешить списывание"],
            [False, "Не разрешать списывание"]
        ],
        widget=widgets.RadioSelect
    )
    receiver_effort = models.FloatField(
        min=0, max=100,
        widget=widgets.SliderInput(attrs={"step": 0.1}),
        label="Усилия по списыванию (от 0 до 100)",
        blank=True
    )
    caught = models.BooleanField()


class Player(BasePlayer):
    payoff = models.CurrencyField()
    role = models.StringField()
    round_payoff = models.CurrencyField()


    def set_payoffs(self):
        group = self.group

        if group.giver_choice == False:
            if self.role == 'giver':
                self.round_payoff = Constants.endowment_giver
            else:
                self.round_payoff = Constants.endowment_receiver
        else:
            group.caught = random.random() < (group.receiver_effort / 100)

            if group.caught:
                self.round_payoff = 0
            else:
                if self.role == 'giver':
                    self.round_payoff = 12
                else:
                    self.round_payoff = 60 - 0.45 * group.receiver_effort
        self.payoff += self.round_payoff
