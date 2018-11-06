"""
This file is only used for debuging and testing
"""
import os

from DAOs import *
from recorder.RecorderAgent import *
from replayer.Base_Replayer import *
from tests.test_GameStructs import *

import random
import unittest
from itertools import islice

#############################################

   ####### #######  #####  #######  #####
      #    #       #          #    #
      #    ###      #####     #     #####
      #    #             #    #          #
      #    #######  #####     #     #####

#############################################

# TEST_CONFIG_REPLAYER = os.path.realpath("./replayer/Base_Replayer.cfg")
TEST_REPLAY_DIRECTORY = os.path.realpath("./tests/replays")

# print(TEST_CONFIG_REPLAYER)

class Test_Replayer:#(unittest.TestCase):
	def generate_replay(file_name, dao_class, length=600):

		file_path = "{0}/{1}.{2}".format(TEST_REPLAY_DIRECTORY, file_name, dao_class.ext())
		if not os.path.exists(file_path):
			os.mknod(file_path)

		file = open(file_path, dao_class.m_write)
		for f_index in range(length):
			gtp = GameTickPacket.random()
			ctrlr = SimpleControllerState()
			dao_class.write(Frame(gtp, ctrlr, f_index))
			file.write()
		file.close()

	def test_batch(self):
		dao = BINDao
		Test_Replayer.generate_replay("test_batch", dao)

		replayer = Base_Replayer(dao)
		replayer.set_files_list(TEST_REPLAY_DIRECTORY)

		for batch in replayer.batch(n=50):
			self.assertNotEqual(batch, [])

		replayer.set_files_list("{}/{}.{}".format(TEST_REPLAY_DIRECTORY,"test_batch", dao.ext()))

		for batch in replayer.batch(n=700):
			self.assertNotEqual(batch, [])

class Test_DAO(unittest.TestCase):
	def data_integrity(self, dao_class):
		real_gtp = GameTickPacket()
		real_controller = SimpleControllerState()

		data = dao_class.write([Frame(real_gtp, real_controller, 0)])
		read = dao_class.read(data)[0]

		self.assertEqual(real_controller.boost, read.controller.boost)
		self.assertEqual(real_controller.steer, read.controller.steer)
		self.assertEqual(real_controller.yaw, read.controller.yaw)
		self.assertEqual(real_controller.pitch, read.controller.pitch)
		self.assertEqual(real_controller.roll, read.controller.roll)
		self.assertEqual(real_controller.roll, read.controller.roll)
		self.assertEqual(0, read.f_index)

	def test_file_name(self):
		self.assertTrue(JSONDao.is_format(JSONDao._f_name("./replays/salut")))
		self.assertTrue(BINDao.is_format(BINDao._f_name("./replays/salut")))
		self.assertTrue(XMLDao.is_format(XMLDao._f_name("./replays/salut")))

	def test_data_integrity(self):
		self.data_integrity(JSONDao)
		self.data_integrity(BINDao)
		self.data_integrity(XMLDao)

	def test_select(self):
		#JSONDao
		self.assertIs(select("JSONDao"), JSONDao)
		self.assertIs(select("json"), JSONDao)
		with self.assertRaises(NameError) as context:
			select("doajson")
		self.assertTrue(context.exception)

		#XMLDao
		self.assertIs(select("xmlDao"), XMLDao)
		self.assertIs(select("xml"), XMLDao)
		with self.assertRaises(NameError) as context:
			select("doaxml")
		self.assertTrue(context.exception)

		#BINDao
		self.assertIs(select("binDao"), BINDao)
		self.assertIs(select("bin"), BINDao)
		with self.assertRaises(NameError) as context:
			select("doabin")
		self.assertTrue(context.exception)

class Test_Recorder(unittest.TestCase):
	def test(self):
		pass

if __name__ == '__main__':
	unittest.main()
