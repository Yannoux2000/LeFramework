class BaseReward(object):
	def __init__(self):
		pass

	def __call__(self, packet):
		raise NotImplementedError()

from LeFramework.common.objs import Car, Ball
from LeFramework.common.regulators import Timer

class DistanceReward(BaseReward):
	def __init__(self, distance = 500):
		super().__init__()

		self.b = Ball()
		self.c = Car(self.index)

		self.t_dist = distance

	def __call__(self, packet):
		self.b.process(packet.game_ball)
		self.c.process(packet.game_cars)

		dist = self.c.distance(self.b)

		if dist < self.t_dist:
			self.generate()
			return 10

		return max(((self.t_dist - dist)/1000)**2, -0.1)
