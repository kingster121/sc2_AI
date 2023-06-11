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
    async def on_step(self, iteration: int):  # Iterate every step of the game
        # Build pylon
        if self.supply_left < 4:
            if (self.already_pending(UnitTypeId.PYLON) == 0) and (
                self.can_afford(UnitTypeId.PYLON)
            ):
                await self.build(UnitTypeId.PYLON, near=random.choice(self.townhalls))

        # Build workers - look into Unit.surplus_harvester property for distributing workers
        if self.can_afford(UnitTypeId.PROBE):
            for nexus in self.townhalls:
                worker_count = len(self.workers.closer_than(10, nexus))
                if (worker_count < 16) and (nexus.is_idle):
                    nexus.train(UnitTypeId.PROBE)

        # Distribute workers
        await self.distribute_workers()

        # Build Nexus
        if (self.already_pending(UnitTypeId.NEXUS) == 0) and (
            self.can_afford(UnitTypeId.NEXUS)
        ):
            await self.expand_now()

        # Create gateways
        if self.can_afford(UnitTypeId.GATEWAY):
            await self.build(UnitTypeId.GATEWAY, near=random.choice(self.structures(UnitTypeId.PYLON)))

        # Build zealots
        if self.can_afford(UnitTypeId.ZEALOT):
            for gateway in self.structures(UnitTypeId.GATEWAY):
                gateway.train(UnitTypeId.ZEALOT)

        # Send zealots to attack once there is 10 zealots
        if len(self.units(UnitTypeId.ZEALOT)) >= 10:
            for zealot in self.units(UnitTypeId.ZEALOT):
                zealot.attack(self.enemy_start_locations[0])


    def mining_rate(self):
        mineral_rate = self.workers * 55
        return mineral_rate, 0


run_game(
    maps.get("ThunderbirdLE"),
    [Bot(Race.Protoss, MineralBot()), Computer(Race.Protoss, Difficulty.Easy)],
    realtime=False,
)
