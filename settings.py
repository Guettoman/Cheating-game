SECRET_KEY = "bluh376blun"

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [
    dict(
        name='cheating_game',
        display_name="Игра в списывание",
        num_demo_participants=2,
        app_sequence=['cheating_game'],
        changing_partners=False,  # True - партнёры меняются, False - партнёры постоянные
        num_rounds=10,  # Укажите желаемое количество раундов
    ),
]

LANGUAGE_CODE = 'en'
USE_POINTS = True
INSTALLED_APPS = ['otree']