import numpy as np

from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

from LeFramework.common.Objs import *
from LeFramework.common.Regulators import Timer

class BaseExercice():
	DEFAULT = -1
	def __init__(self, index, team, complexity=-1):
		self.index = index
		self.team = team
		self.complexity = complexity
		self.finished = False

		self.debug_info = None
		self.timer = Timer()
		self.timer.set_run()
		self.t_limit = 5

		self.init_vars()

		self.reward = None

	def __call__(self, packet: GameTickPacket):
		gs = self.game_state_update(packet)
		r = self.reward(packet)
		if self.timer(self.t_limit):
			# print(self.debug_info)
			gs = self.reset()
			self.timer.reset()
		return gs

	@property
	def side(self):
		return (self.team * 2) - 1

	def reset(self):
		self.finished = False
		return self.game_state_reset()

	def init_vars(self): pass
	def game_state_reset(self): self.log_info = None; return GameState()
	def game_state_update(self, packet): self.log_info = None; return GameState()
