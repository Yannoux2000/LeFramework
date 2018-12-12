from .base_exercice import BaseExercice

from LeFramework.common.Objs import Car, Ball
from LeFramework.common.Regulators import Timer

from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator

import random

class RandomPlaceExercice(BaseExercice):

	def generate(self):
		self.x = random.uniform(-1000, 1000)
		self.y = random.uniform(-1000, 1000)

	def init_vars(self):
		self.b = Ball()
		self.c = Car(self.index)
		self.generate()

	def game_state_update(self, packet):
		ball_state = BallState(physics=Physics(
			location=Vector3(self.x, self.y, 500),
			velocity=Vector3(0, 0, 0),
			rotation=Rotator(0, 0, 0),
			angular_velocity=Vector3(0, 0, 0)
		))

		return GameState(ball=ball_state)

	def reward(self, packet):
		self.b.process(packet.game_ball)
		self.c.process(packet.game_cars)

		dist = self.c.distance(self.b)

		if dist < 500:
			self.generate()
			return 10

		return max(3 - (dist/1000)**2, -0.1)
