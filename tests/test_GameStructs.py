"""
Theses classes mimic the ins and outs of any agent, it is not needed to
Used for tests on Linux, hey what did you expect ?
this file could become more important than just for tests in the future.
trust me, random signals are the best signals to understand systems
"""
import random as r

class Vector3:
	def __init__(self, x = 0, y = 0, z = 0):
		self.update(x,y,z)

	def update(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z

class Rotator:
	def __init__(self, pitch = 0, yaw = 0, roll = 0):
		self.update(pitch, yaw, roll)

	def update(self, pitch = 0, yaw = 0, roll = 0):
		self.pitch = pitch
		self.yaw = yaw
		self.roll = roll

class Physics:
	def __init__(self, location = Vector3(), rotation = Rotator(), velocity = Vector3(), angular_velocity = Vector3()):
		self.update(location, rotation, velocity, angular_velocity)

	def update(self, location = Vector3(), rotation = Rotator(), velocity = Vector3(), angular_velocity = Vector3()):
		self.location = location
		self.rotation = rotation
		self.velocity = velocity
		self.angular_velocity = angular_velocity

	@staticmethod
	def random():
		return Physics(Vector3(r.random(),r.random(),r.random()),
						Rotator(r.random(),r.random(),r.random()),
						Vector3(r.random(),r.random(),r.random()),
						Vector3(r.random(),r.random(),r.random()))

class Touch:
	def __init__(self, name = "", time = 0, hit_location = Vector3(), hit_normal = Vector3()):
		self.update(name, time, hit_location, hit_normal)

	def update(self, name = "", time = 0, hit_location = Vector3(), hit_normal = Vector3()):
		self.player_name = name
		self.time_seconds = time
		self.hit_location = hit_location
		self.hit_normal = hit_normal

class ScoreInfo:
	def __init__(self, score = 0, goals = 0, own_goals = 0, assists = 0, saves = 0, shots = 0, demolitions = 0):
		self.update(score, goals, own_goals, assists, saves, shots, demolitions)

	def update(self, score = 0, goals = 0, own_goals = 0, assists = 0, saves = 0, shots = 0, demolitions = 0):
		self.score = score
		self.goals = goals
		self.own_goals = own_goals
		self.assists = assists
		self.saves = saves
		self.shots = shots
		self.demolitions = demolitions

class PlayerInfo:
	def __init__(self, physics = Physics(), score_info = ScoreInfo(), is_demolished = False, has_wheel_contact = False,
				is_super_sonic = False, is_bot = False, jumped = False, double_jumped = False, name = "", team = 0, boost = 0):
		self.update(physics, score_info, is_demolished, has_wheel_contact,
				is_super_sonic, is_bot, jumped, double_jumped, name, team, boost)

	def update(self, physics = Physics(), score_info = ScoreInfo(), is_demolished = False, has_wheel_contact = False,
				is_super_sonic = False, is_bot = False, jumped = False, double_jumped = False, name = "", team = 0, boost = 0):
		self.physics = Physics()
		self.score_info = ScoreInfo()
		self.is_demolished = is_demolished
		self.has_wheel_contact = has_wheel_contact
		self.is_super_sonic = is_super_sonic
		self.is_bot = is_bot
		self.jumped = jumped
		self.double_jumped = double_jumped
		self.name = name
		self.team = team
		self.boost = boost

	@staticmethod
	def random():
		return PlayerInfo(physics=Physics.random(), team=r.randint(0,1), boost=r.randint(0,100))

class DropShotInfo:
	def __init__(self, absorbed_force = 0, damage_index = 0, force_accum_recent = 0):
		self.update(absorbed_force, damage_index, force_accum_recent)

	def update(self, absorbed_force = 0, damage_index = 0, force_accum_recent = 0):
		self.absorbed_force = absorbed_force
		self.damage_index = damage_index
		self.force_accum_recent = force_accum_recent

class BallInfo:
	def __init__(self, physics = Physics(), latest_touch = Touch(), drop_shot_info = DropShotInfo()):
		self.update(physics, latest_touch, drop_shot_info)

	def update(self, physics = Physics(), latest_touch = Touch(), drop_shot_info = DropShotInfo()):
		self.physics = physics
		self.latest_touch = latest_touch
		self.drop_shot_info = drop_shot_info

	@staticmethod
	def random():
		return BallInfo(physics=Physics.random())

class BoostPadState:
	def __init__(self, is_active = False, timer = 0):
		self.update(is_active, timer)

	def update(self, is_active = False, timer = 0):
		self.is_active = is_active
		self.timer = timer

class TileInfo:
	def __init__(self, tile_state = 0):
		self.update(tile_state)

	def update(self, tile_state = 0):
		self.tile_state = tile_state

class GameInfo:
	def __init__(self, seconds_elapsed = 0, game_time_remaining = 0, is_overtime = False, is_unlimited_time = False,
				is_round_active = False, is_kickoff_pause = False, is_match_ended = False):
		self.update(seconds_elapsed, game_time_remaining, is_overtime, is_unlimited_time,
				is_round_active, is_kickoff_pause, is_match_ended)

	def update(self, seconds_elapsed = 0, game_time_remaining = 0, is_overtime = False, is_unlimited_time = False,
				is_round_active = False, is_kickoff_pause = False, is_match_ended = False):
		self.seconds_elapsed = seconds_elapsed
		self.game_time_remaining = game_time_remaining
		self.is_overtime = is_overtime
		self.is_unlimited_time = is_unlimited_time
		self.is_round_active = is_round_active
		self.is_kickoff_pause = is_kickoff_pause
		self.is_match_ended = is_match_ended

	@staticmethod
	def random():
		return GameInfo(r.random(),r.random())


class BoostPad:
	def __init__(self, location = Vector3(), is_full_boost = False):
		self.update(location, is_full_boost)

	def update(self, location = Vector3(), is_full_boost = False):
		self.location = location
		self.is_full_boost = is_full_boost

class GoalInfo:
	def __init__(self, team_num = 0, location = Vector3(), direction = Vector3()):
		self.update(team_num, location, direction)

	def update(self, team_num = 0, location = Vector3(), direction = Vector3()):
		self.team_num = team_num
		self.location = location
		self.direction = direction

class FieldInfoPacket:
	def __init__(self):
		self.update(boost_pads, goals)

	def update(self, boost_pads = [], goals = []):
		self.boost_pads = boost_pads
		self.num_boosts = len(boost_pads)
		self.goals = goals
		self.num_goals = len(goals)

class GameTickPacket:
	def __init__(self, game_cars = [], game_boosts = [], game_ball = BallInfo(), game_info = GameInfo(), dropshot_tiles = []):
		self.update(game_cars, game_boosts, game_ball, game_info, dropshot_tiles)

	def update(self, game_cars = [], game_boosts = [], game_ball = BallInfo(), game_info = GameInfo(), dropshot_tiles = []):
		self.game_cars = game_cars
		self.num_cars = len(game_cars)
		self.game_boosts = game_boosts
		self.num_boost = len(game_boosts)
		self.game_ball = game_ball
		self.game_info = game_info
		self.dropshot_tiles = dropshot_tiles
		self.num_tiles = len(dropshot_tiles)

	@staticmethod
	def random():
		cars = []
		for i in range(10):
			cars.append(PlayerInfo.random())
		return GameTickPacket(cars, [], BallInfo.random())

class SimpleControllerState:
	def __init__(self, steer = 0, throttle = 0, pitch = 0, yaw = 0, roll = 0, jump = False, boost = False, handbrake = False):
		self.update(steer, throttle, pitch, yaw, roll, jump, boost, handbrake)

	def update(self, steer = 0, throttle = 0, pitch = 0, yaw = 0, roll = 0, jump = False, boost = False, handbrake = False):
		self.steer = steer
		self.throttle = throttle
		self.pitch = pitch
		self.yaw = yaw
		self.roll = roll
		self.jump = jump
		self.boost = boost
		self.handbrake = handbrake
