import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

URotationToRadians = math.pi / float(32768)

class blank(BaseAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)

    def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
        return SimpleControllerState()
