import numpy as np
from .Vector import *
from .Objs import *

# class BoostPad(ctypes.Structure):
#     _fields_ = [("location", Vector3),
#                 ("is_full_boost", ctypes.c_bool)]


# class GoalInfo(ctypes.Structure):
#     _fields_ = [("team_num", ctypes.c_ubyte),
#                 ("location", Vector3),
#                 ("direction", Vector3)]


# class FieldInfoPacket(ctypes.Structure):
#     _fields_ = [("boost_pads", BoostPad * MAX_BOOSTS),
#                 ("num_boosts", ctypes.c_int),
#                 ("goals", GoalInfo * MAX_GOALS),
#                 ("num_goals", ctypes.c_int)]

class BoostPad(Target):
	def __init__(self, vec, f_b):
		super(BoostPad, self).__init__(vec)
		self.is_full_boost = f_b

class GoalInfo(Target):
	def __init__(self, vec, direction, team):
		super(BoostPad, self).__init__(vec)
		self.direction = direction
		self.team = team

class MapInfo():
	def __init__(self, index, team):
		self.index = index
		self.team = team

		self.boost_pads = []
		self.goals = []

		self.home = None
		self.goal = None

		self.ready = False

	def process(self, info_packet):
		self.boost_pads = [BoostPad(Vec3.process_Vec(b.location), b.is_full_boost) for b in info_packet.boost_pads]
		self.goals = [GoalInfo(g.location, g.direction, g.team_num) for g in info_packet.goals]

		self.home = [g for g in self.goals if g.team == self.team][0]
		self.goal = [g for g in self.goals if g.team != self.team][0]

		self.ready = True
