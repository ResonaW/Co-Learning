from os import environ

SESSION_CONFIGS = [
    # dict(
    #     name='co_learning',
    #     display_name="co_learning",
    #     app_sequence=['co_learning'],
    #     num_demo_participants=30,
    #     # use_browser_bots=True
    # ),
dict(
        name='Experiment1', # 实验1
        display_name="Experiment1",
        app_sequence=['Experiment1'],
        num_demo_participants=8,
        # use_browser_bots=True # 自动填写fields
    ),
dict(
        name='Experiment2', # 实验1
        display_name="Experiment2",
        app_sequence=['Experiment2'],
        num_demo_participants=12,
        # use_browser_bots=True # 自动填写fields
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="",
)

PARTICIPANT_FIELDS = ['player_data','player_prelabel','player_train','player_test']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

OTREE_PRODUCTION=1

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5908604368973'
INSTALLED_APPS = ['otree']
# DEBUG=False #关闭debug模式
