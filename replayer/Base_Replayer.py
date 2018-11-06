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

	def import_agent(self, agent_path):
		"""
		this class does not import the agent class. but you can do so by calling this function
		:return: the agent class
		"""
		return import_agent().get_loaded_class()


	# def load_custom_config(self, config_header):
	# 	"""
	# 	this method is free for you to implement for inheriting classes
	# 	"""
	# 	pass

	# @staticmethod
	# def create_configurations(config: ConfigObject):
	# 	base_header = config.add_header_name(REPLAYER_CONFIG_HEADER)
	# 	base_header.add_value('data_format', str, default='', description="Dao name for the data format you want (BINDao for Binary, JSONDao for Json XMLDao for Xml, ...)")
	# 	base_header.add_value('reloop', bool, default='False', description="should the data be read over and over")
	# 	return config

	# def load_config(self, file_path):
	# 	"""
	# 	Loads a file_path this is called after the constructor but before anything.
	# 	:param file_path: This is the config file's path, for replayer configuration.
	# 	"""
	# 	# config = self.create_configurations(ConfigObject())
	# 	config = ConfigObject()
	# 	#to create a file if it was not created already
	# 	config.parse_file(file_path, max_index=10)

	# 	self.load_custom_config(config.add_header_name(CUSTOM_CONFIG_HEADER))
	# 	base_header = config.get_header(REPLAYER_CONFIG_HEADER)
	# 	self.dao = select(base_header.get('data_format'))
	# 	self.reloop = base_header.getboolean('reloop')

	def set_files_list(self, replay_path):
		"""
		define path to replay, accepts file path, or directory, (including subdirectories)
		"""
		if os.path.isdir(replay_path):
			self.files_list = [os.path.join(replay_path, f) for f in os.listdir(replay_path) if self.dao.is_format(f)]

		if os.path.isfile(replay_path):
			self.files_list = [replay_path] if self.dao.is_format(replay_path) else []

		#creates a generator that get through all lines of each files
		self.replay = self.file_extractor()

	def file_extractor(self):
		"""
		this generator reads each lines and output the use frames
		also saves fields_info if there are one
		:yield: line wise decoded data
		"""
		for data in (self.dao.read(l) for f in self.files_list for l in open(f, self.dao.m_read)):
			if data.f_index == -1:
				self.field_info = data
			else:
				yield data

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
