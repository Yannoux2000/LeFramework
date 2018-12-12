"""
This script would be used as a mimic for the rlbot framework,
so that, ML agent can be set as training mode, and therefore train in head less mode
"""

import os

from LeFramework.daos import *

from rlbot.parsing.custom_config import *
from rlbot.utils.class_importer import *
from rlbot.agents.base_agent import BaseAgent, PYTHON_FILE_KEY, LOOKS_CONFIG_KEY, BOT_NAME_KEY, BOT_CONFIG_MODULE_HEADER, BOT_CONFIG_AGENT_HEADER

REPLAYER_CONFIG_HEADER = "Replayer Configuration"
CUSTOM_CONFIG_HEADER = "Custom Configuration"

class Base_Replayer:
	def __init__(self, dao = None, reloop = False):
		"""
		:param dao: dao class
		"""
		self.dao = dao
		self.reloop = reloop
		self.infoframe = None

	def init_agent(self, agent_packet):
		if self.infoframe is None:
			raise TypeError("Replay {} has no Info frame".format(self.files_list[0]))

		cls_agent, agent_config = agent_packet

		a = cls_agent(*self.infoframe['init'])

		a.load_config(agent_config.get_header(BOT_CONFIG_AGENT_HEADER))
		
		a._register_field_info(lambda: self.field_info())
		
		a._register_quick_chat(lambda *args: None)
		a._register_set_game_state(lambda *args: None)
		a._register_ball_prediction(lambda *args: None)

		a.initialize_agent()
		return a

	def field_info(self):
		if self.infoframe is None:
			raise TypeError("You must init your agents in the for batch loop\n")
		return self.infoframe['field_info']

	@classmethod
	def create_replayer_configurations(cls):
		config = ConfigObject()
		replayer_config = config.add_header(REPLAYER_CONFIG_HEADER)
		replayer_config.add_value('replay_path', str, default='./tests/replays', description='Directory from where the replays will be loaded.')
		replayer_config.add_value('data_format', str, default='BINDao', description="Dao name for the data format you want \n(BINDao for Binary, JSONDao for Json XMLDao for Xml, ...)")

		cls.create_custom_configurations(config.add_header(CUSTOM_CONFIG_HEADER))
		return config

	@staticmethod
	def create_custom_configurations(config_header: ConfigHeader):
		"""
		used to create configs objects for inheriting classes
		"""
		pass

	def load_base(self, config_header):
		my_path = os.path.dirname(os.path.realpath(__file__))

		config_header.get('replay_path')

	def load_custom(self, config_header):
		"""
		used to load configs objects for inheriting classes
		"""
		pass

	def load_config(self, config_path):
		config = self.create_replayer_configurations()
		config.parse_file(config_path)

		self.load_base(config.get_header(REPLAYER_CONFIG_HEADER))
		self.load_custom(config.get_header(CUSTOM_CONFIG_HEADER))

	def import_agent(self, config_path):
		"""
		does not init the agent class. only returns it using rlbot framework
		:return: the agent class
		"""
		my_path = os.path.dirname(os.path.realpath(__file__))

		#retriving python file path
		base_config = BaseAgent.base_create_agent_configurations()
		base_config.parse_file(config_path)
		agent_python_file = base_config.get(BOT_CONFIG_MODULE_HEADER, PYTHON_FILE_KEY)

		#importing agent class
		python_path = os.path.join(os.path.dirname(config_path), agent_python_file)
		agent_class = import_agent(python_path).get_loaded_class()

		#retriving agent config
		agent_config = agent_class.base_create_agent_configurations()
		agent_config.parse_file(config_path)
		return agent_class, agent_config

	def set_files_list(self, replay_path):
		"""
		define path to replay, accepts file path, or directory, (including subdirectories)
		"""
		files_list = []

		if os.path.isdir(replay_path):
			files_list = [os.path.join(replay_path, f) for f in os.listdir(replay_path)]

		if os.path.isfile(replay_path):
			files_list = [replay_path]

		#Keep only the readable by the dao
		self.files_list = self.dao.filter(files_list)
		#creates a generator that get through all lines of each files
		self.replay = self.file_extractor()

	def file_extractor(self):
		"""
		this generator reads each lines and output the use frames
		also saves fields_info if there are one
		:yield: line wise decoded data
		"""
		for data in (self.dao.f_read(f) for f in self.files_list):
			for frame in data:
				if frame['f_index'] == -1:
					self.infoframe = frame
				else:
					yield frame

	def batch(self, n=1):
		"""
		group up frames
		:param n: number of frames in each batch
		:yield : list of n packets
		"""
		while True:
			batch = [x for _, x in zip(range(n), self.replay)]
			if batch == []: #end condition
				return
			yield batch

	def run(self, agent_packet, callback = (lambda agent, batch: None), epi=1, n=1):
		"""
		helps with multiprocessing stuff to be called and played through
		"""
		agent = None

		for batch in self.batch(n=50):
			if agent is None:
				agent = self.init_agent(agent_packet)

			callback(agent, batch)
