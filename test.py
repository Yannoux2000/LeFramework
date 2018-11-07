"""
This file is only used for debuging and testing
"""
import os

from DAOs import *
from recorder.RecorderAgent import *
from replayer.Base_Replayer import *
from tests.test_GameStructs import GameTickPacket, SimpleControllerState, FieldInfoPacket

from rlbot.agents.base_agent import BaseAgent, BOT_CONFIG_AGENT_HEADER

import unittest

#############################################

   ####### #######  #####  #######  #####
      #    #       #          #    #
      #    ###      #####     #     #####
      #    #             #    #          #
      #    #######  #####     #     #####

#############################################

TEST_CONFIG_RECORDER = os.path.realpath("./recorder/RecorderAgent.cfg")
TEST_REPLAY_DIRECTORY = os.path.realpath("./tests/replays")
TEST_AGENT_PATH = os.path.realpath("./agents/legacy.cfg")

class Test_Replayer(unittest.TestCase):
	def generate_replay(file_path, dao_class, length=600):
		data = [Info(FieldInfoPacket, ("SwaggLord6969",0,0))]
		for i in range(length):
			data.append(Frame(GameTickPacket.random(), SimpleControllerState(), i))
		dao_class.f_write(data, file_path)

	def test_batch(self):
		file_path1 = "{0}/{1}".format(TEST_REPLAY_DIRECTORY, "test_batch1")
		file_path2 = "{0}/{1}".format(TEST_REPLAY_DIRECTORY, "test_batch2")
		file_path3 = "{0}/{1}".format(TEST_REPLAY_DIRECTORY, "test_batch3")
		dao = BINDao

		Test_Replayer.generate_replay(file_path1, dao)
		Test_Replayer.generate_replay(file_path2, dao)
		Test_Replayer.generate_replay(file_path3, dao)

		replayer = Base_Replayer(dao)
		replayer.set_files_list(TEST_REPLAY_DIRECTORY)

		for batch in replayer.batch(n=50):
			self.assertNotEqual(batch, [])

		replayer.set_files_list(TEST_REPLAY_DIRECTORY)

		for batch in replayer.batch(n=700):
			self.assertNotEqual(batch, [])

		replayer.set_files_list(TEST_REPLAY_DIRECTORY)

		for batch in replayer.batch():
			self.assertNotEqual(batch, [])

	def test_replay(self):
		file_path = "{0}/{1}".format(TEST_REPLAY_DIRECTORY, "test_batch")
		dao = BINDao

		replayer = Base_Replayer(dao)
		replayer.set_files_list(TEST_REPLAY_DIRECTORY)
		cls_agent = replayer.import_agent(TEST_AGENT_PATH)

		inited = False
		for batch in replayer.batch():
			if inited == False:
				agent = replayer.init_agent(cls_agent)

			for b in batch:
				# print(agent.get_output(b.game_tick_packet))
				pass


class Test_DAO(unittest.TestCase):
	def data_integrity(self, dao_class):
		real_gtp = GameTickPacket.random()
		real_controller = SimpleControllerState()

		file_path = "./tests/replays/flat"

		data = dao_class.f_write([Frame(real_gtp, real_controller, 0)], file_path)
		read = dao_class.f_read(file_path)[0]

		self.assertEqual(real_controller.boost, read.controller.boost)
		self.assertEqual(real_controller.steer, read.controller.steer)
		self.assertEqual(real_controller.yaw, read.controller.yaw)
		self.assertEqual(real_controller.pitch, read.controller.pitch)
		self.assertEqual(real_controller.roll, read.controller.roll)

		self.assertEqual(real_gtp.game_cars[0].physics.location.x, read.game_tick_packet.game_cars[0].physics.location.x)
		self.assertEqual(real_gtp.game_cars[1].physics.location.x, read.game_tick_packet.game_cars[1].physics.location.x)
		self.assertEqual(real_gtp.game_cars[2].physics.location.x, read.game_tick_packet.game_cars[2].physics.location.x)
		self.assertEqual(0, read.f_index)

	def test_file_name(self):
		self.assertTrue(JSONDao.is_format(JSONDao._f_name("./replays/salut")))
		self.assertTrue(BINDao.is_format(BINDao._f_name("./replays/salut")))
		self.assertTrue(XMLDao.is_format(XMLDao._f_name("./replays/salut")))
		
		self.assertTrue(JSONDao.is_format(JSONDao._f_name("./replays/salut.json")))
		self.assertTrue(BINDao.is_format(BINDao._f_name("./replays/salut.bin")))
		self.assertTrue(XMLDao.is_format(XMLDao._f_name("./replays/salut.xml")))

		self.assertFalse(JSONDao.is_format("./replays/salut.not"))
		self.assertFalse(BINDao.is_format("./replays/salut.not"))
		self.assertFalse(XMLDao.is_format("./replays/salut.not"))

	def test_data_integrity(self):
		self.data_integrity(JSONDao)
		self.data_integrity(BINDao)
		# self.data_integrity(XMLDao)

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
	def create_config_file():
		config = RecorderAgent.base_create_agent_configurations()

		if not os.path.isfile(TEST_CONFIG_RECORDER):
			os.mknod(TEST_CONFIG_RECORDER)
			with open(TEST_CONFIG_RECORDER, "w") as f:
				f.write(str(config))

		config.parse_file(TEST_CONFIG_RECORDER)
		return config

	def load_agent(config):
		rec = RecorderAgent("SwaggLord6969", 0, 0)
		rec.load_config(config.get_header(BOT_CONFIG_AGENT_HEADER))

		rec._register_field_info(FieldInfoPacket.make)
		# print(hasattr(rec.__field_info_func))

		# Once all engine setup is done, do the agent-specific initialization, if any:
		rec.initialize_agent()
		return rec

	def test_emulate_rlbot(self):
		cfg = Test_Recorder.create_config_file()
		agent = Test_Recorder.load_agent(cfg)

		for n in range(30):
			c = agent.get_output(GameTickPacket.random())

		agent.retire()

		self.assertTrue(os.path.isfile(agent.dao._f_name(agent.replay_path)))

class IntergrationTests(unittest.TestCase):
	def test_record_replayer(self):
		replay_path = "{0}/{1}".format(TEST_REPLAY_DIRECTORY, "test_batch")
		dao = BINDao

		replayer = Base_Replayer(dao)
		replayer.set_files_list(replay_path)
		agent_packet = replayer.import_agent("./recorder/RecorderAgent.cfg")
		agent = None

		for batch in replayer.batch(n=50):
			if agent is None:
				agent = replayer.init_agent(agent_packet)

			#### you decide your code here
			for b in batch:
				agent.get_output(batch)

			#### 


if __name__ == '__main__':
	unittest.main()
