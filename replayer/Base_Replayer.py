"""
This script would be used as a mimic for the rlbot framework,
so that, ML agent can be set as training mode, and therefore train in head less mode
"""

import os
from DAOs import *
from rlbot.parsing.custom_config import *
from rlbot.utils.class_importer import *

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

	def init_agent(self, cls_agent):

		if self.infoframe is None:
			raise Error("Replay without an info frame")

		a = cls_agent(*self.infoframe.init)
		#TODO
		a.load_config(config.get_header(BOT_CONFIG_AGENT_HEADER))
		
		a._register_field_info(lambda: self.field_info())
		
		a._register_quick_chat(lambda *args: None)
		a._register_set_game_state(lambda *args: None)
		a._register_ball_prediction(lambda *args: None)

		a.initialize_agent()
		return a

	def field_info(self):
		if self.infoframe is None:
			raise TypeError("You must init your agents in the for batch loop\n")
		return self.infoframe.field_info

	def import_agent(self, agent_path):
		"""
		does not init the agent class. only returns it using rlbot framework
		:return: the agent class
		"""
		return import_agent(agent_path).get_loaded_class()


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
				if frame.f_index == -1:
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
