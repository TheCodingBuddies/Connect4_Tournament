from Bots.bot_ai import BotAI
from Bots.fill_ai import FillAI
from Bots.random_ai import RandomAI
from Bots.user_ai import UserAI

ai_bots = {
    "random": RandomAI,
    "fill": FillAI,
    "user": UserAI
}


def AiFactory(bot_selection="random") -> BotAI:
    return ai_bots[bot_selection]()
