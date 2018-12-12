import numpy as np
from .vector import *

#distance Between Physicalects only, no mixing vectors and Physicalects

GRAVITY = 650

class Target():
	def __init__(self, vec = Vec3()):
		self.loc = vec

	def distance(self, other):
		return self.loc.distance(other.loc)
		
	def to(self, t_loc):
		return t_loc - self.loc

class Physical(Target):
	def __init__(self, vec = Vec3()):
		super(Physical, self).__init__(vec)
		self.vel = Vec3()
		self.rot = Vec3()
		self.ang = Vec3()

		self.matrix = []

	def process(self, physics):
		self.Physical_process(physics)

	def Physical_process(self, physics):
		self.loc = Vec3([physics.location.x,physics.location.y,physics.location.z])
		self.vel = Vec3([physics.velocity.x,physics.velocity.y,physics.velocity.z])
		self.rot = Vec3([physics.rotation.roll,physics.rotation.pitch,physics.rotation.yaw])
		self.ang = Vec3([physics.angular_velocity.x,physics.angular_velocity.y,physics.angular_velocity.z])

	def step(self, n=1):
		new_p = Physical()
		new_p.loc = self.loc + new_p.vel * n
		new_p.vel = self.vel + GRAVITY * n
		return new_p

	def rot_to_mat(self):
		self.matrix = np.matrix([
			self.forward,
			self.left,
			self.up
		])

	@property
	def pitch_vel(self):
		return self.left.dot(self.ang)

	@property
	def roll_vel(self):
		return self.forward.dot(self.ang)

	@property
	def yaw_vel(self):
		return self.up.dot(self.ang)

	@property
	def pitch(self):
		return self.rot.pitch

	@property
	def roll(self):
		return self.rot.roll

	@property
	def yaw(self):
		return self.rot.yaw


	@property
	def x_ang_vel(self):
		return self.ang[0]

	@property
	def y_ang_vel(self):
		return self.ang[1]

	@property
	def z_ang_vel(self):
		return self.ang[2]

	@property
	def x_ang(self):
		return self.left.dot(self.rot)

	@property
	def y_ang(self):
		return self.forward.dot(self.rot)

	@property
	def z_ang(self):
		return self.up.dot(self.rot)


	@property
	def forward(self):
		CR = np.cos(self.rot.roll)
		SR = np.sin(self.rot.roll)

		CP = np.cos(self.rot.pitch)
		SP = np.sin(self.rot.pitch)

		CY = np.cos(self.rot.yaw)
		SY = np.sin(self.rot.yaw)

		# front direction
		return Vec3([
					CP * CY,
					CP * SY,
					SP
				])

	@property
	def left(self):
		CR = np.cos(self.rot.roll)
		SR = np.sin(self.rot.roll)

		CP = np.cos(self.rot.pitch)
		SP = np.sin(self.rot.pitch)

		CY = np.cos(self.rot.yaw)
		SY = np.sin(self.rot.yaw)

		# left direction
		return Vec3([
					CY * SP * SR - CR * SY,
					SY * SP * SR + CR * CY,
					-CP * SR
				])

	@property
	def up(self):
		CR = np.cos(self.rot.roll)
		SR = np.sin(self.rot.roll)

		CP = np.cos(self.rot.pitch)
		SP = np.sin(self.rot.pitch)

		CY = np.cos(self.rot.yaw)
		SY = np.sin(self.rot.yaw)

		# up direction
		return Vec3([
					-CR * CY * SP - SR * SY,
					-CR * SY * SP + SR * CY,
					CP * CR
				])

	def to_local(self, other):
		vec = other if isinstance(other, Vec3) else other.loc
		vec = vec - self.loc
		vec = np.matmul(self.matrix, vec).A.flatten()
		return Vec3(vec)

class Ball(Physical):
	def __init__(self, vec = Vec3()):
		super(Ball, self).__init__(vec)

	def process(self, ball):
		self.Physical_process(ball.physics)
		self.rot_to_mat()

class Car(Physical):
	def __init__(self, index, vec = Vec3()):
		super(Car, self).__init__(vec)
		self.boost = 0

		self.index = index
		self.team = 0

	def process(self, cars):
		car = cars[self.index]
		self.Physical_process(car.physics)
		self.rot_to_mat()
		self.Car_process(car)

	def Car_process(self, car):
		self.boost = car.boost
		self.team = car.team
		self.is_demolished = car.is_demolished
		self.has_wheel_contact = car.has_wheel_contact
		self.is_super_sonic = car.is_super_sonic
		self.is_bot = car.is_bot
		self.jumped = car.jumped
		self.double_jumped = car.double_jumped
		self.name = car.name
		self.team = car.team
		self.boost = car.boost


# 	#retrieve transformation matrix from car info.
# 	def tMat(self):
# 		return Get_TMat(self.Car_Forward(), self.Car_Left(), self.loc)

# def Get_TMat(f, l, t):
# 	#Generate matrix transform
# 	#X Forward, Y = Left, Z = Up

# 	#Y = M . X
# 	#M = Y . X-1
# 	#X = indentity because of f, l, u corresponding to unit vectors

# 	u = f.cross(l)

# 	#the vector t is for translations

# 	#This matrix convert from local to global
# 	return np.concatenate((f.np(0), l.np(0), u.np(0), t.np(1)), axis=1)

# #using matrix algorithms to find local and global coords
# def to_local(car, vec):
# 	#Inverted from the local to global matrix generated
# 	matM = np.linalg.inv(Car_TMat(car))
# 	outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# 	return outvec

# def to_global(car, vec):

# 	matM = Get_TMat(car)
# 	outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# 	return outvec


	# def reached(self, t_loc, threshold = 500):
	# 	return (self.distance(t_loc) < threshold)

# 	def Forward(self):

# 		facing_x = np.cos(self.rot.) * np.cos(self.yaw)
# 		facing_y = np.cos(self.pitch) * np.sin(self.yaw)
# 		facing_z = np.sin(self.pitch)

# 		#double check normilizations of vectors
# 		return Vector3(facing_x, facing_y, facing_z).normalize()

# 	def Left(self):

# 		left_x = np.cos(self.pitch) * (-np.sin(self.yaw))
# 		left_y = np.cos(self.pitch) * np.cos(self.yaw)
# 		left_z = np.sin(self.pitch)

# 		return Vector3(left_x, left_y, left_z).normalize()

# 	def TMat(self):
# 		return Get_TMat(self.Forward(), self.Left(), self.loc)

# 	def RMat(self):
# 		return Get_TMat(self.Forward(), self.Left(), Vector3())

# 	def localize(self, vec):
# 		#Inverted from the local to global matrix generated
# 		matM = np.linalg.inv(self.TMat())
# 		outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# 		return outvec

# 	def localize_rot(self, vec):

# 		matM = np.linalg.inv(self.RMat())
# 		outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# 		return outvec

# 	def globalize(self, vec):

# 		matM = self.TMat()
# 		outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# 		return outvec

# 	def p_array_to(self, t_loc):
# 		t_local = self.localize(t_loc)

# 		ret = t_local.p_array()
# 		ret[0] = Rad_clip(np.pi - ret[0])
		
# 		return ret

# 	def array_to(self, t_loc):
# 		t_local = self.localize(t_loc)

# 		ret = t_local.array()
# 		ret[0] = Rad_clip(np.pi - ret[0])
		
# 		return ret

# 	def p_array(self):
# 		return self.loc.p_array() + self.dir.p_array() + self.vel.p_array() + self.avl.p_array()

# 	def c_array(self):
# 		return self.loc.c_array() + self.dir.c_array() + self.vel.c_array() + self.avl.c_array()

# 	def array(self):
# 		return self.loc.array() + self.dir.array() + self.vel.array() + self.avl.array()


# def Car_To_Vec(car):
# 	return Vectorize_Loc(car), Car_Forward(car), Vectorize_Vel(car), Vectorize_Avl(car)

# def Rad_clip(val):
# 		# Make sure we go the 'short way'
# 		if abs(val) > np.pi:
# 			val += (2 * np.pi) if val < 0 else (- 2 * np.pi)
# 		return val


# def Car_Forward(car):

# 	pitch = float(car.Rotation.Pitch) * URotationToRadians
# 	yaw = float(car.Rotation.Yaw) * URotationToRadians
# 	roll = float(car.Rotation.Roll) * URotationToRadians

# 	facing_x = np.cos(pitch) *	np.cos(yaw)
# 	facing_y = np.cos(pitch) *	np.sin(yaw)
# 	facing_z = np.sin(pitch)

# 	#double check normilizations of vectors
# 	return Vector3(facing_x, facing_y, facing_z).normalize()

# def Car_Left(car):

# 	pitch = float(car.Rotation.Pitch) * URotationToRadians
# 	yaw = float(car.Rotation.Yaw) * URotationToRadians + np.pi/2
# 	roll = float(car.Rotation.Roll) * URotationToRadians

# 	facing_x = np.cos(pitch) *(-np.sin(yaw))
# 	facing_y = np.cos(pitch) *	np.cos(yaw)
# 	facing_z = np.sin(pitch)

# 	#double check normilizations of vectors
# 	return Vector3(facing_x, facing_y, facing_z).normalize()

# #retrieve transformation matrix from car info.
# def Car_TMat(car):
# 	return Get_TMat(Car_Forward(car), Car_Left(car), Vectorize_Loc(car))

# def Get_TMat(f, l, t):
# 	#Generate matrix transform
# 	#X Forward, Y = Left, Z = Up

# 	#Y = M . X
# 	#M = Y . X-1
# 	#X = indentity because of f, l, u corresponding to unit vectors

# 	u = f.cross(l)

# 	#the vector t is for translations

# 	#This matrix convert from local to global
# 	return np.concatenate((f.np(0), l.np(0), u.np(0), t.np(1)), axis=1)

# # #using matrix algorithms to find local and global coords
# # def to_local(car, vec):
# # 	#Inverted from the local to global matrix generated
# # 	matM = np.linalg.inv(Car_TMat(car))
# # 	outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# # 	return outvec

# # def to_global(car, vec):

# # 	matM = Get_TMat(car)
# # 	outvec = Vectorize_Np(np.dot(matM,vec.np(1)))

# # 	return outvec
