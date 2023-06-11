# Objective: Explore expansion and increasing mining rate
# Understand when to build Nexus and workers.
# Move workers from one base to another to maximise mining efficiency

from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId

import random


class MineralBot(BotAI):
    async def on_step(self):
        if self.supply_left < 4:
            # build pylons.
            if self.already_pending(UnitTypeId.PYLON) == 0:
                if self.can_afford(UnitTypeId.PYLON):
                    await self.build(
                        UnitTypeId.PYLON, near=random.choice(self.townhalls)
                    )
                    found_something = True


run_game(
    maps.get("ThunderbirdLE"),
    [Bot(Race.Protoss, MineralBot()), Computer(Race.Protoss, Difficulty.Easy)],
    realtime=False,
)
