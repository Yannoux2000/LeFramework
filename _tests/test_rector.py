from LeFramework.common.Vector import *
from LeFramework.common.ConstVec import *
from LeFramework.common.Objs import *
from LeFramework.common.Paths import *
from LeFramework.common.Areas import *

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

import unittest

class Test_Vec3(unittest.TestCase):
	def test_init(self):
		a = Vec3([1,2])
		b = Vec3([2,1])

		a = Vec3([1.1,2.2,-3.1,4.0])
		a = Vec3([1.1,2.2])

	def test_equal(self):
		v = Vec3([5,-5,200.5])
		self.assertTrue(v==v)
		self.assertTrue(Vec3([5,0,-0.5])==Vec3([5,0,-0.5]))

	def test_add(self):
		self.assertEqual(Vec3([5,-5,200]) ,Vec3([0,0,-0.5]) + Vec3([5,-5,200.5]))
		self.assertEqual(Vec3([5,-5,200]) ,Vec3([5,-5,200.5]) + Vec3([0,0,-0.5]))
		self.assertEqual(Vec3([51,-25,80.5])	,Vec3([1,-75,30.5]) + 50)

	def test_sub(self):
		self.assertEqual(Vec3([0,5,-11])		,Vec3([5,0,-0.5])		 - Vec3([5,-5,10.5]))
		self.assertEqual(Vec3([0,-5,11])		,Vec3([5,-5,10.5])		 - Vec3([5,0,-0.5]))
		self.assertEqual(Vec3([-45,-55,-39.5])	,Vec3([5,-5,10.5])		 - 50)

	def test_mul(self):
		self.assertEqual(Vec3([0,0,-100.25])	,Vec3([0,0,-0.5])		 * Vec3([5,-5,200.5]))
		self.assertEqual(Vec3([0,0,-100.25])	,Vec3([5,-5,200.5])		 * Vec3([0,0,-0.5]))
		self.assertEqual(Vec3([-25,25,0.5*-5])	,Vec3([5,-5,0.5])		 * -5)

	def test_process(self):
		v = Vec3.process_Vec(type('obj', (object,), {'x': 1,'y': -1.25,'z': 123}))
		self.assertEqual(Vec3([1, -1.25, 123]), v)

		v = Vec3.process_Vec(type('obj', (object,), {'x': 0,'y': 0,'z': 0}))
		self.assertEqual(Vec3([0, 0, 0]), v)

		v = Vec3.process_Rot(type('obj', (object,), {'pitch' : 1, 'yaw' : -1.25, 'roll' : 123}))
		self.assertEqual(Vec3([123, 1, -1.25]), v)

	def test_distance(self):
		self.assertEqual(20	,Vec3([0,0,20]).distance(Vec3([0,20,20])))
		self.assertEqual(0	,Vec3([15,24,32]).distance(Vec3([15,24,32])))
		self.assertEqual(64	,Vec3([15,24,32]).distance(Vec3([15,24,-32])))

	def test_gnd(self):
		self.assertEqual(Vec3([5,-5,0]) ,Vec3([5,-5,0.5]).gnd)
		self.assertEqual(Vec3([5,-5,0]) ,Vec3([5,-5,0]).gnd)
		self.assertEqual(Vec3([5,-5,0]) ,Vec3([5,-5,999]).gnd)

	def test_dot(self):
		self.assertEqual(-100.25				,Vec3([5,-5,200.5]).dot(Vec3([0,0,-0.5])))
		self.assertEqual(25 + 25 + (20**2)		,Vec3([5,-5,20]).dot(Vec3([5,-5,20])))
		self.assertEqual(-75					,Vec3([5,5,5]).dot(Vec3([-5,-5,-5])))
		self.assertEqual(3						,Vec3([2,3,0]).dot(Vec3([3,-1,0])))
		self.assertEqual(-3						,Vec3([2,3,0]).dot(Vec3([-3,1,0])))

	def test_str(self):
		self.assertEqual("(x: +0.00   ,y: +0.00   ,z: +0.00   )"	,str(Vec3()))
		self.assertEqual("(x: +1.25   ,y: +7.26   ,z: -4.16   )"	,str(Vec3([1.25,7.26,-4.156])))

if __name__ == '__main__':
	unittest.main()

# asserter(Vec3([0,0,0])			,Vec3()					, 						"Vec3 init")
# asserter(Vec3([1,2,3])			,Vec3([1,2,3])			, 						"Vec3 init")



# print("ConstVec")

# print(ConstVec.get('Center', 0))
# print(ConstVec.get('Goal', 0))
# print(ConstVec.get('Goal', 1))
# print(ConstVec.get('Goal_L', 0))
# print(ConstVec.get('Goal_L', 1))
# print(ConstVec.get('Goal_R', 0))
# print(ConstVec.get('Goal_R', 1))
# print(ConstVec.get('Goal_T', 0))
# print(ConstVec.get('Goal_T', 1))
# print(ConstVec.get('Home', 0))
# print(ConstVec.get('Home', 1))
# print(ConstVec.get('Home_L', 0))
# print(ConstVec.get('Home_L', 1))
# print(ConstVec.get('Home_R', 0))
# print(ConstVec.get('Home_R', 1))
# print(ConstVec.get('Home_T', 0))
# print(ConstVec.get('Home_T', 1))
# print(ConstVec.get('Boost_Goal_L', 0))
# print(ConstVec.get('Boost_Goal_L', 1))
# print(ConstVec.get('Boost_Goal_R', 0))
# print(ConstVec.get('Boost_Goal_R', 1))
# print(ConstVec.get('Boost_Center_L', 0))
# print(ConstVec.get('Boost_Center_L', 1))
# print(ConstVec.get('Boost_Center_R', 0))
# print(ConstVec.get('Boost_Center_R', 1))

# asserter(Vec3(),Target().loc,"Target init")
# asserter(Vec3(),Target(Vec3()).loc,"Target init")

# bma = BallMetaArea()

# print(ConstVec.get('Goal_L', 1))
# print(ConstVec.get('Goal_R', 1))

# ball = Ball(Vec3([0,0,0]))

# a = - ball.to(ConstVec.get('Goal_L', 1))
# b = - ball.to(ConstVec.get('Goal_R', 1))

# ball.rot = Vec3()
# ball.rot_to_mat()
# bma.update(ball, 1)

# asserter(False	,bma.inShotZone(Vec3([-893,-5119,-321.39]))	, "Area")
# asserter(False	,bma.inShotZone(Vec3([-893,-5119, 321.39]))	, "Area")
# asserter(True	,bma.inShotZone(Vec3([-893,-5121,-321.39]))	, "Area")
# asserter(True	,bma.inShotZone(Vec3([-893,-5121, 321.39]))	, "Area")
# asserter(True	,bma.inShotZone(Vec3([-892,-5120,-321.39]))	, "Area")
# asserter(True	,bma.inShotZone(Vec3([-892,-5120, 321.39]))	, "Area")
# asserter(False	,bma.inShotZone(Vec3([-894,-5120,-321.39]))	, "Area")
# asserter(False	,bma.inShotZone(Vec3([-894,-5120, 321.39]))	, "Area")

# asserter(False	,bma.inShotZone(Vec3([893,-5119,-321.39]))	, "Area")
# asserter(False	,bma.inShotZone(Vec3([893,-5119, 321.39]))	, "Area")
# asserter(True	,bma.inShotZone(Vec3([893,-5121,-321.39]))	, "Area")
# asserter(True	,bma.inShotZone(Vec3([893,-5121, 321.39]))	, "Area")
# asserter(True	,bma.inShotZone(Vec3([892,-5120,-321.39]))	, "Area")
# asserter(True	,bma.inShotZone(Vec3([892,-5120, 321.39]))	, "Area")
# asserter(False	,bma.inShotZone(Vec3([894,-5120,-321.39]))	, "Area")
# asserter(False	,bma.inShotZone(Vec3([894,-5120, 321.39]))	, "Area")

# for e in range(20):
# 	ball = Ball(ConstVec.randomVec())
# 	team = 0

# 	a = - ball.to(ConstVec.get('Goal_L', team))
# 	b = - ball.to(ConstVec.get('Goal_R', team))

# 	ball.rot = Vec3()
# 	ball.rot_to_mat()
# 	bma.update(ball, team)

# 	asserter(False	,bma.inShotZone(Vec3([a[0],a[1]+1,a[2]]))	, "Area")
# 	asserter(True	,bma.inShotZone(Vec3([a[0],a[1]-1,a[2]]))	, "Area")
# 	asserter(True	,bma.inShotZone(Vec3([a[0]+1,a[1],a[2]]))	, "Area")
# 	asserter(False	,bma.inShotZone(Vec3([a[0]-1,a[1],a[2]]))	, "Area")

# 	asserter(False	,bma.inShotZone(Vec3([b[0],b[1]+1,b[2]]))	, "Area")
# 	asserter(True	,bma.inShotZone(Vec3([b[0],b[1]-1,b[2]]))	, "Area")
# 	asserter(True	,bma.inShotZone(Vec3([b[0]-1,b[1],b[2]]))	, "Area")
# 	asserter(False	,bma.inShotZone(Vec3([b[0]+1,b[1],b[2]]))	, "Area")
