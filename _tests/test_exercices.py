from LeFramework.exercices.base_exercice import BaseExercice
from LeFramework._tests.test_game_structs import GameTickPacket, SimpleControllerState, FieldInfoPacket

from rlbot.utils.game_state_util import GameState

import unittest

##############################################

   ####### #######  #####  #######  #####
      #    #       #          #    #
      #    ###      #####     #     #####
      #    #             #    #          #
      #    #######  #####     #     #####

##############################################

class Test_BaseExercice(unittest.TestCase):
	def test_init(self):
		b = BaseExercice(0,0)
		b = BaseExercice(1,0)
		b = BaseExercice(2,1)
		b = BaseExercice(3,1)

	def test_reset(self):
		b = BaseExercice(0,0)
		b.reset()

	def test_side(self):
		b = BaseExercice(0,0)
		if b.team:
			self.assertEqual(b.side, 1)
		else:
			self.assertEqual(b.side, -1)

	def test_call(self):
		b = BaseExercice(0,0)
		c = b(GameTickPacket.random())
		self.assertIsInstance(c, GameState)

	def test_update(self):
		b = BaseExercice(0,0)
		c = b.game_state_update(GameTickPacket.random())
		self.assertIsInstance(c, GameState)

	def test_reset(self):
		b = BaseExercice(0,0)
		c = b.game_state_reset()
		self.assertIsInstance(c, GameState)


class Test_BaseReward(unittest.TestCase):
	def test_reward(self):
		b = DistanceReward(0,0)
		r = b.reward(GameTickPacket.random())
		self.assertIs(type(r), int)
if __name__ == '__main__':
	unittest.main()