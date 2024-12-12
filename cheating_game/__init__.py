from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL= 'cheating_game'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2
    endowment_giver = 10
    endowment_receiver = 0
    GIVER_ROLE = 'giver'
    RECEIVER_ROLE = 'receiver'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    giver_choice = models.BooleanField(
        choices=[[True, "Разрешить списывание"], [False, "Не разрешать списывание"]],
        widget=widgets.RadioSelect
    )
    receiver_effort = models.FloatField(
        min=0, max=100,
        label="Усилия по списывание (от 0 до 100)",
        blank=True
    )
    caught = models.BooleanField()

class Player(BasePlayer):
    name = models.StringField(label="Ваше имя")

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        subsession.group_randomly()
    elif subsession.session.config['changing_partners']:
        subsession.group_randomly()

def set_payoffs(player: Player):
    group = player.group
    if group.giver_choice == False:
        if player.role == 'giver':
            player.payoff = C.endowment_giver
        else:
            player.payoff = C.endowment_receiver
    else:
        group.caught = random.random() > (group.receiver_effort / 100)
        if group.caught:
            player.payoff = 0
        else:
            if player.role == 'giver':
                player.payoff = 12
            else:
                player.payoff = 60 - 0.45 * group.receiver_effort

    
class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class Login(Page):
    form_model = 'player'
    form_fields = ['name']

    def is_displayed(self):
        return self.round_number == 1
    
    
class WaitForRoleAssignment(WaitPage):
    pass

class RoleAssignment(Page):
    pass

class GiverDecision(Page):
    form_model = 'group'
    form_fields = ['giver_choice']
    
    def is_displayed(player: Player):
        return player.role == 'giver'

class ReceiverWaitPage(WaitPage):
    pass

class ReceiverDecision(Page):
    form_model = 'group'
    form_fields = ['receiver_effort']
    def is_displayed(player: Player):
        return player.role == 'receiver' and player.group.giver_choice

class GiverWaitPage(WaitPage):
    pass

class ResultsRound(Page):
    def vars_for_template(player: Player):
        set_payoffs(player)
        group = player.group
        return {
            'giver_choice': group.giver_choice,
            'receiver_effort': group.receiver_effort if group.giver_choice else None,
            'caught': group.caught if group.giver_choice else None,
            'round_payoff': player.payoff,
            'role': player.role
        }

class Results(Page):
    def vars_for_template(player: Player):
        total_payoff = player.total_payoff
        return {
            'player_total_payoff': total_payoff,
            'rounds': player.subsession.round_number,
        }

class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

    def vars_for_template(self):
        players = self.subsession.get_players()
        return {
            'players': players
        }


page_sequence = [Instructions, Login, WaitForRoleAssignment,
                 RoleAssignment, GiverDecision,
                 ReceiverWaitPage, ReceiverDecision,
                 GiverWaitPage, ResultsRound]

