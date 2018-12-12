from .vector import *
from .objs import *
from .paths import *

from random import uniform

#team blue is team 0, blue goal is in (0,-y,0)

class ConstVec():
	#Center
	Center	=			Vec3()

	#Center of a goal. positives Y are for the orange team.
	Pole	=			Vec3([      0	, 5120	,    321.3875])
	#Left pole when facing the goal
	Pole_L	=			Vec3([    893	, 5120	,    0])
	#Right pole when facing the goal
	Pole_R	=			Vec3([   -893	, 5120	,    0])
	#Top pole when facing the goal
	Pole_T	=			Vec3([   -0		, 5120	,    642.775])

	#Left Full Boost pad when facing the goal
	Boost_Corner_L =	Vec3([   3072	, 4096	,    73])
	#Left Full Boost pad when facing the goal
	Boost_Corner_R =	Vec3([  -3072	, 4096	,    73])

	#Left Full Boost pad when facing the goal
	Boost_Center_L =	Vec3([   3584   ,    0  ,    73])
	#Left Full Boost pad when facing the goal
	Boost_Center_R =	Vec3([  -3584   ,    0  ,    73])

	#Wall X
	Wall_L = 			Vec3([   4096   ,    0  ,    0])
	Wall_R = 			Vec3([  -4096   ,    0  ,    0])

	def t_get(name, team=0):
		return Target(ConstVec.get(name, team))


	def get(name, team=0): #team => 1 is orange, 0 is blue
		if name=='Center':
			return ConstVec.Center

		if name=='Goal':
			return ConstVec.Pole * (team*(-2) + 1)
		if name=='Goal_L':
			return ConstVec.Pole_L * (team*(-2) + 1)
		if name=='Goal_R':
			return ConstVec.Pole_R * (team*(-2) + 1)
		if name=='Goal_T':
			return ConstVec.Pole_T * (team*(-2) + 1)

		if name=='Home':
			return ConstVec.Pole * (team*2 - 1)
		if name=='Home_L':
			return ConstVec.Pole_L * (team*2 - 1)
		if name=='Home_R':
			return ConstVec.Pole_R * (team*2 - 1)
		if name=='Home_T':
			return ConstVec.Pole_T * (team*2 - 1)

		if name=='Boost_Goal_L':
			return ConstVec.Boost_Corner_L * (team*(-2) + 1)
		if name=='Boost_Goal_R':
			return ConstVec.Boost_Corner_R * (team*(-2) + 1)

		if name=='Boost_Center_L':
			return ConstVec.Boost_Center_L * (team*(-2) + 1)
		if name=='Boost_Center_R':
			return ConstVec.Boost_Center_R * (team*(-2) + 1)

		if name=='Boost_Home_L':
			return ConstVec.Boost_Corner_L * (team*2 - 1)
		if name=='Boost_Home_R':
			return ConstVec.Boost_Corner_R * (team*2 - 1)

		if name=='Wall_L':
			return ConstVec.Wall_L * (team*(-2) + 1)
		if name=='Wall_R':
			return ConstVec.Wall_R * (team*(-2) + 1)

	def randomVec():
		return Vec3([uniform(-4096, 4096),uniform(-5120, 5120),0])

class PATHS:
	def CIRCLE():
		return [ConstVec.t_get("Goal"),
			  ConstVec.t_get("Boost_Goal_R"),
			  ConstVec.t_get("Boost_Center_R"),
			  ConstVec.t_get("Boost_Home_L"),
			  ConstVec.t_get("Home"),
			  ConstVec.t_get("Boost_Home_R"),
			  ConstVec.t_get("Boost_Center_L"),
			  ConstVec.t_get("Boost_Goal_L")]

	def MID():
		return [Node(BOOSTPAD.b0),
				Node(BOOSTPAD.b7),
				Node(BOOSTPAD.b13),
				Node(BOOSTPAD.b20),
				Node(BOOSTPAD.b26),
				Node(BOOSTPAD.b33)]

	# R2 = [5 ,10 ,16 ,22 ,27]
	# R1 = [1 ,12 ,19 ,31]
	# Rw = [3 , 8 ,15 ,24 ,29]
	# def RS():
	# 	return [Node(BOOSTPAD.b0),
	# 			Node([ -940.0, -3308.0, 70.0]),
	# 			Node([-1788.0, -2300.0, 70.0]),
	# 			Node([-2048.0, -1036.0, 70.0]),
	# 			Node([-2048.0,  1036.0, 70.0]),
	# 			Node([-1788.0,  2300.0, 70.0]),
	# 			Node([ -940.0,  3308.0, 70.0]),
	# 			Node([    0.0,  4240.0, 70.0])]

	# Lw = [4 , 9 ,18 ,25 ,30]
	# L1 = [2 ,14 ,21 ,32]
	# L2 = [6 ,11 ,17 ,23 ,28]
	def LS(team = 0):
		b_t = team == 1
		return PATHS.SideCurve(True)
	def RS(team = 0):
		return PATHS.SideCurve()
		#from blue toward orange on Right side
	def SideCurve(flip_x=False, flip_y=False):
		return [BOOSTPAD.get( 'b0' , flip_x, flip_y),
				BOOSTPAD.get( 'b6' , flip_x, flip_y),
				BOOSTPAD.get( 'b11', flip_x, flip_y),
				BOOSTPAD.get( 'b14', flip_x, flip_y),
				BOOSTPAD.get( 'b21', flip_x, flip_y),
				BOOSTPAD.get( 'b23', flip_x, flip_y),
				BOOSTPAD.get( 'b28', flip_x, flip_y),
				BOOSTPAD.get( 'b33', flip_x, flip_y)]

	# Mid= [0 , 7 ,13 ,20 ,26 ,33]

	# fsL = [11,13,20]
	# fsR = [10,13,20]
	# fsM = [ 7,13,20]



class BOOSTPAD:
	b0 =  [    0.0, -4240.0, 70.0]
	b1 =  [-1792.0, -4184.0, 70.0]
	b2 =  [ 1792.0, -4184.0, 70.0]
	b3 =  [-3072.0, -4096.0, 73.0]
	b4 =  [ 3072.0, -4096.0, 73.0]
	b5 =  [- 940.0, -3308.0, 70.0]
	b6 =  [  940.0, -3308.0, 70.0]
	b7 =  [    0.0, -2816.0, 70.0]
	b8 =  [-3584.0, -2484.0, 70.0]
	b9 =  [ 3584.0, -2484.0, 70.0]
	b10 = [-1788.0, -2300.0, 70.0]
	b11 = [ 1788.0, -2300.0, 70.0]
	b12 = [-2048.0, -1036.0, 70.0]
	b13 = [    0.0, -1024.0, 70.0]
	b14 = [ 2048.0, -1036.0, 70.0]
	b15 = [-3584.0,     0.0, 73.0]
	b16 = [-1024.0,     0.0, 70.0]
	b17 = [ 1024.0,     0.0, 70.0]
	b18 = [ 3584.0,     0.0, 73.0]
	b19 = [-2048.0,  1036.0, 70.0]
	b20 = [    0.0,  1024.0, 70.0]
	b21 = [ 2048.0,  1036.0, 70.0]
	b22 = [-1788.0,  2300.0, 70.0]
	b23 = [ 1788.0,  2300.0, 70.0]
	b24 = [-3584.0,  2484.0, 70.0]
	b25 = [ 3584.0,  2484.0, 70.0]
	b26 = [    0.0,  2816.0, 70.0]
	b27 = [- 940.0,  3310.0, 70.0]
	b28 = [  940.0,  3308.0, 70.0]
	b29 = [-3072.0,  4096.0, 73.0]
	b30 = [ 3072.0,  4096.0, 73.0]
	b31 = [-1792.0,  4184.0, 70.0]
	b32 = [ 1792.0,  4184.0, 70.0]
	b33 = [    0.0,  4240.0, 70.0]

	def all():
		return [Node(BOOSTPAD.b0),  Node(BOOSTPAD.b1),
				Node(BOOSTPAD.b2),  Node(BOOSTPAD.b3),
				Node(BOOSTPAD.b4),  Node(BOOSTPAD.b5),
				Node(BOOSTPAD.b6),  Node(BOOSTPAD.b7),
				Node(BOOSTPAD.b8),  Node(BOOSTPAD.b9),
				Node(BOOSTPAD.b10), Node(BOOSTPAD.b11),
				Node(BOOSTPAD.b12), Node(BOOSTPAD.b13),
				Node(BOOSTPAD.b14), Node(BOOSTPAD.b15),
				Node(BOOSTPAD.b16), Node(BOOSTPAD.b17),
				Node(BOOSTPAD.b18), Node(BOOSTPAD.b19),
				Node(BOOSTPAD.b20), Node(BOOSTPAD.b21),
				Node(BOOSTPAD.b22), Node(BOOSTPAD.b23),
				Node(BOOSTPAD.b24), Node(BOOSTPAD.b25),
				Node(BOOSTPAD.b26), Node(BOOSTPAD.b27),
				Node(BOOSTPAD.b28), Node(BOOSTPAD.b29),
				Node(BOOSTPAD.b30), Node(BOOSTPAD.b31),
				Node(BOOSTPAD.b32), Node(BOOSTPAD.b33)]

	def get(name, flip_x=False, flip_y=False):

		if name=='b0':
			vec = BOOSTPAD.b0
		if name=='b1':
			vec = BOOSTPAD.b1
		if name=='b2':
			vec = BOOSTPAD.b2
		if name=='b3':
			vec = BOOSTPAD.b3
		if name=='b4':
			vec = BOOSTPAD.b4
		if name=='b5':
			vec = BOOSTPAD.b5
		if name=='b6':
			vec = BOOSTPAD.b6
		if name=='b7':
			vec = BOOSTPAD.b7
		if name=='b8':
			vec = BOOSTPAD.b8
		if name=='b9':
			vec = BOOSTPAD.b9
		if name=='b10':
			vec = BOOSTPAD.b10
		if name=='b11':
			vec = BOOSTPAD.b11
		if name=='b12':
			vec = BOOSTPAD.b12
		if name=='b13':
			vec = BOOSTPAD.b13
		if name=='b14':
			vec = BOOSTPAD.b14
		if name=='b15':
			vec = BOOSTPAD.b15
		if name=='b16':
			vec = BOOSTPAD.b16
		if name=='b17':
			vec = BOOSTPAD.b17
		if name=='b18':
			vec = BOOSTPAD.b18
		if name=='b19':
			vec = BOOSTPAD.b19
		if name=='b20':
			vec = BOOSTPAD.b20
		if name=='b21':
			vec = BOOSTPAD.b21
		if name=='b22':
			vec = BOOSTPAD.b22
		if name=='b23':
			vec = BOOSTPAD.b23
		if name=='b24':
			vec = BOOSTPAD.b24
		if name=='b25':
			vec = BOOSTPAD.b25
		if name=='b26':
			vec = BOOSTPAD.b26
		if name=='b27':
			vec = BOOSTPAD.b27
		if name=='b28':
			vec = BOOSTPAD.b28
		if name=='b29':
			vec = BOOSTPAD.b29
		if name=='b30':
			vec = BOOSTPAD.b30
		if name=='b31':
			vec = BOOSTPAD.b31
		if name=='b32':
			vec = BOOSTPAD.b32
		if name=='b33':
			vec = BOOSTPAD.b33

		if flip_x:
			vec = [-vec[0], vec[1], vec[2]]
		if flip_y:
			vec = [vec[0],-vec[1], vec[2]]

		return Node(vec)
