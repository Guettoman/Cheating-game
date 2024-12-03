from otree.api import Currency as c, currency_range
from . import models
from django.http import HttpResponseRedirect
from otree.api import View, SessionConfig
import random
from otree.api import Currency as c, currency_range
from .models import Constants


class Instructions(View):
    pass


class RoleAssignment(View):
    def before_next_page(self):
        if self.player.id_in_group == 1:
            self.player.role = "giver"
        else:
            self.player.role = "receiver"


class GiverDecision(View):
    def is_displayed(self):
        return self.player.role == 'giver'


class ReceiverDecision(View):
    form_model = models.Group
    form_fields = ['receiver_effort']

    def is_displayed(self):
        return self.player.role == 'receiver' and self.group.giver_choice


class ResultsRound(View):
    def vars_for_template(self):
        return {
            'giver_choice': self.group.giver_choice,
            'receiver_effort': self.group.receiver_effort if self.group.giver_choice else None,
            'caught': self.group.caught if self.group.giver_choice else None,
            'round_payoff': self.player.round_payoff,
            'role': self.player.role,
        }


class Results(View):
    def before_next_page(self):
        self.player.set_payoffs()


    def vars_for_template(self):
        total_payoff = sum([p.payoff for p in self.subsession.get_players()])
        return {
            'total_payoff': total_payoff,
            'rounds': self.subsession.round_number,
        }