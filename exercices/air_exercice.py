from .base_exercice import BaseExercice

from LeFramework.common.objs import *
from LeFramework.common.regulators import Timer

from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.game_state_util import GameState, BallState, CarState, Physics, Vector3, Rotator


class FixedBallExercice(BaseExercice):
	def game_state_update(self, packet):
		ball_state = BallState(physics=Physics(
			location=Vector3(0, 0, 1500),
			velocity=Vector3(0, 0, 0),
			rotation=Rotator(0, 0, 0),
			angular_velocity=Vector3(0, 0, 0)
		))
		car_state = CarState(boost_amount = 100)
		return GameState(ball=ball_state, cars={self.index : car_state})

	def reward(self, packet):
		self.b.process(packet.game_ball)
		self.c.process(packet.game_cars)

		dist = self.c.distance(self.b)

		if dist < 500:
			self.generate()

		return max(10 - (dist/500), -0.1)

class AirRotateExercice(BaseExercice):
	def init_vars(self):
		self.state = None
		self.me = Car(self.index)
		self.ball = Ball(self.index)

	def game_state_reset(self):
		crot = Rotator(
			random.uniform(-np.pi ,np.pi),
			random.uniform(-np.pi ,np.pi),
			random.uniform(-np.pi ,np.pi)
		)

		car_state = CarState(physics=Physics(
			location=Vector3(0, 0, 1000),
			velocity=Vector3(0, 0, 0),
			rotation=None,
			angular_velocity=Vector3(0, 0, 0)
		),boost_amount = 100)

		vel = random.choice([(-1,0),(1,0),(0,-1),(0,1)])

		bloc = Vector3(
			1000 * vel[0] + 200 * vel[1],
			1000 * vel[1] + 200 * vel[0],
			random.choice([500 ,1300])
		)
		
		bvel = Vector3(
			-12 * vel[0] + 3 * vel[1],
			-12 * vel[1] + 3 * vel[0],
			0
		)

		ball_state = BallState(physics=Physics(
			location=bloc,
			velocity=bvel,
			rotation=Rotator(0, 0, 0),
			angular_velocity=Vector3(0, 0, 0)
		))

		self.state = GameState(
			ball=ball_state,
			cars={self.index: car_state})
		return self.state

	def game_state_update(self, packet):
		self.log_info = None
		self.me.process(packet.game_cars)
		self.ball.process(packet.game_ball)

		self.debug_info = self.me.forward.angle3d(self.me.to(self.ball.loc))

		self.state.cars[self.index].physics.rotation = None
		self.state.cars[self.index].physics.angular_velocity = None

		self.state.cars[self.index].physics.location.x = None
		self.state.cars[self.index].physics.location.y = None

		self.state.cars[self.index].physics.velocity.x = None
		self.state.cars[self.index].physics.velocity.y = None

		self.state.ball.physics.location.x += self.state.ball.physics.velocity.x
		self.state.ball.physics.location.y += self.state.ball.physics.velocity.y
		self.state.ball.physics.location.z += self.state.ball.physics.velocity.z
		return self.state
