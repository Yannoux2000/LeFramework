from .base_exercice import BaseExercice

from LeFramework.common.objs import *
from LeFramework.common.regulators import Timer

from rlbot.utils.structures.game_data_struct import GameTickPacket

class NormalGameExercice(BaseExercice):
	def vars(self):
		self.timer.set_stop()
		
	def reward(self, packet):
		"""
		:return: player's score board only
		"""
		return packet.game_cars[self.index].score_info.score

class TeamScoreExercice(BaseExercice):
	def vars(self):
		self.timer.set_stop()
		
	def reward(self, packet):
		"""
		:return: player's score board only
		"""
		score = 0

		for c in packet.game_cars:
			if c.team == self.team:
				score += c.score_info.score

		return score

class TeamScoreExercice(BaseExercice):
	def vars(self):
		self.timer.set_stop()
		
	def reward(self, packet):
		"""
		:return: player's score board only
		"""
		score = 0
		for c in packet.game_cars:
			if c.team == self.team:
				score += c.score_info.score
			else:
				score -= c.score_info.score

		return score
