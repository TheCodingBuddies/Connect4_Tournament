from Bots.bot_ai import BotAI
from Bots.fill_ai import FillAI
from Bots.random_ai import RandomAI

ai_bots = {
    "random": RandomAI,
    "fill": FillAI,
}


def AiFactory(bot_selection="random") -> BotAI:
    return ai_bots[bot_selection]()
