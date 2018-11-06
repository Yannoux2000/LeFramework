from rlbot.agents.base_agent import BaseAgent, BOT_CONFIG_AGENT_HEADER, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.parsing.custom_config import ConfigObject, ConfigHeader
from rlbot.utils.class_importer import *

#select here what type of file you want to use.
#Make sure the DAOs.py file is accessible from this file
from DAOs import select

"""
Steps before executing :
	-	Setting this agent as the one being used by rlbot
	-	Defining your agent class as the one being imported as recorded Agent
	-	Defining path in the config file for your bot
"""

#### DO NOT MODIFY
#theses classes are used to keep a structure in the saved objects
class Frame:
	def __init__(self, game_tick_packet, controller, f_index):
		self.f_index = f_index
		self.game_tick_packet = game_tick_packet
		self.controller = controller

class Info:
	def __init__(self, field_info, init):
		self.f_index = -1
		self.field_info = field_info
		self.init = init

class RecorderAgent(BaseAgent):
	"""This Agent will act just like your agent, only the gametickpackets and outputs will be recorded"""

	dao = select('JSONDao')

	def __init__(self, name, team, index):
		# save these args for the embeded agent to init
		self.init = (name, team, index)
		self.agent = None
		self.tick = 0

		super().__init__(name, team, index)

	@staticmethod
	def create_agent_configurations(config: ConfigObject):
		params = config.get_header(BOT_CONFIG_AGENT_HEADER)
		params.add_value('replay_path', str, default='./replays', description='directory where the replays will be saved.')
		params.add_value('agent_path', str, default='../agents/legacy.py', description='python file containing the agent class')
		params.add_value('data_format', str, default='JSONDao', description="Dao name for the data format you want (BINDao for Binary, JSONDao for Json XMLDao for Xml, ...)")

	def load_config(self, config_header):
		dao_name = config_header.get('data_format')
		self.dao = select(dao_name)

		replay_path = config_header.get('replay_path')
		if not os.path.exists(replay_path):
			os.makedirs(replay_path)

		self.replay_file = "{0}/{1}.{2}".format(replay_path, len(os.listdir(replay_path)), self.dao.ext())

		agent_path = config_header.get('agent_path')
		agent_class = import_agent(agent_path).get_loaded_class()
		#init the agent just like our recorderAgent
		self.agent = agent_class(*self.init)

		self.agent.load_config(config_header)

	def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
		outputs = self.agent.get_output(game_tick_packet)

		data = Frame(game_tick_packet,outputs,self.tick)
		self.tick += 1
		self.file.write(self.dao.write(data))
		return outputs

	def initialize_agent(self):
		self.file = open(self.replay_file,"a")
		
		data = Info(self.get_field_info(),self.init)
		self.file.write(self.dao.write(data))

		self.agent.initialize_agent()

	def handle_quick_chat(self, index, team, quick_chat):
		self.agent.handle_quick_chat(index, team, quick_chat)

	def get_extra_pids(self):
		self.agent.get_extra_pids()

	def retire(self):
		self.agent.retire()
		self.file.close()
