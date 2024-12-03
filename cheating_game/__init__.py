from otree.api import *
import random

class Constants(BaseConstants):
    name_in_url = 'cheating_game'
    players_per_group = 2
    num_rounds = 10
    endowment_giver = 10
    endowment_receiver = 0

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
    player_payoff = models.CurrencyField(initial=0)
    player_role = models.StringField()
    round_payoff = models.CurrencyField(initial=0)

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        subsession.group_randomly()
    elif subsession.session.config['changing_partners']:
        subsession.group_randomly()
    assign_roles(subsession)

def assign_roles(subsession):
    for group in subsession.get_groups():
        players = group.get_players()
        if len(players) == 2:
            first_role = random.choice(['giver', 'receiver'])
            players[0].player_role = first_role
            players[1].player_role = 'receiver' if first_role == 'giver' else 'giver'

def set_payoffs(player: Player):
    group = player.group
    if group.giver_choice == False:
        if player.player_role == 'giver':
            player.round_payoff = Constants.endowment_giver
        else:
            player.round_payoff = Constants.endowment_receiver
    else:
        group.caught = random.random() > (group.receiver_effort / 100)
        if group.caught:
            player.round_payoff = 0
        else:
            if player.player_role == 'giver':
                player.round_payoff = 12
            else:
                player.round_payoff = 60 - 0.45 * group.receiver_effort
    
    player.player_payoff = player.player_payoff + player.round_payoff


class Instructions(Page):
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
        return player.player_role == 'giver'

class ReceiverWaitPage(WaitPage):
    pass

class ReceiverDecision(Page):
    form_model = 'group'
    form_fields = ['receiver_effort']
    def is_displayed(player: Player):
        return player.player_role == 'receiver' and player.group.giver_choice

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
            'round_payoff': player.round_payoff,
            'player_role': player.player_role,
            'role': player.player_role
        }

class Results(Page):
    def before_next_page(player: Player, timeout_happened = False):
        set_payoffs(player)

    def vars_for_template(self):
        total_payoff = sum([p.player_payoff for p in self.subsession.get_players()])
        return {
            'total_payoff': total_payoff,
            'rounds': self.subsession.round_number,
        }

page_sequence = [Instructions, WaitForRoleAssignment,
                 RoleAssignment, GiverDecision,
                 ReceiverWaitPage, ReceiverDecision,
                 GiverWaitPage, ResultsRound, Results]