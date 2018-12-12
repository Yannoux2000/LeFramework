import numpy as np
import math

UNIT_X = None
UNIT_Y = None
UNIT_Z = None

def Rad_clip(val):
		# Make sure we go the 'short way'
		if abs(val) > np.pi:
			val += (2 * np.pi) if val < 0 else (- 2 * np.pi)
		return val

class Vec3(np.ndarray):
	def __new__(cls, a = [0,0,0]):
		a = np.concatenate((a, np.zeros(3)))[:3]
		obj = np.asarray(a).view(cls)
		return obj

	def __str__(self):
		return "(x: {0:<+8.2f},y: {1:<+8.2f},z: {2:<+8.2f})".format(*self)

	def __eq__(self, other):
		return np.array_equal(self, other)

	@staticmethod
	def process_Vec(vector):
		return Vec3([vector.x, vector.y, vector.z])

	@staticmethod
	def process_Rot(rot):
		return Vec3([rot.roll, rot.pitch, rot.yaw])

	@property
	def roll(self):
		return self[0]

	@property
	def pitch(self):
		return self[1]

	@property
	def yaw(self):
		return self[2]

	@property
	def norm(self):
		return np.sqrt(self.dot(self))

	@property
	def direction(self):
		return self / self.norm

	@property
	def gnd(self):
		return Vec3(self[:2])

	def cross(self, other):
		return np.cross(self, other)

	def distance(self, other):
		return (self - other).norm

	def homogeneous(self,w=1):
		return [self.vec+[w]]

	def angle_to(self, other):
		return np.arccos(self.dot(other) / (self.norm * other.norm))

	def angle_old(self):
		return np.arctan2(self[1], self[0])

	# calculate angle on plane where v1 and v2 are unit vectors
	def angle(self, v1 = UNIT_X, v2 = UNIT_Y):
		return np.arctan2(self.dot(v2), self.dot(v1))

	def angle_old(self, axes=(1,0)):
		return np.arctan2(self[axes[0]], -self[axes[1]])

	def to_polar(self):
		# The in-game axes are left handed, so use -x
			# ret pitch , yaw
		return Rad_clip(np.arcsin(self[2] / self.norm)), Rad_clip(np.arctan2(self[1], -self[0]))

UNIT_X = Vec3([1,0,0])
UNIT_Y = Vec3([0,1,0])
UNIT_Z = Vec3([0,0,1])
