from otree.api import *

class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Round(Page):
    form_model = 'player'
    form_fields = ['give_permission', 'effort']

    def before_next_page(self):
        calculate_payoff(self.player)

class Results(Page):
    def vars_for_template(self):
        return {
            'round_payoff': self.player.round_payoff,
            'total_payoff': sum(p.round_payoff for p in self.player.in_all_rounds())
        }

page_sequence = [Introduction, Round, Results]
