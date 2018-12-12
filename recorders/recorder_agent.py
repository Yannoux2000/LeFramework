from rlbot.agents.base_agent import BaseAgent, BOT_CONFIG_AGENT_HEADER, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.parsing.custom_config import ConfigObject, ConfigHeader
from rlbot.utils.class_importer import *

from datetime import datetime

from .Recorder import Recorder
from LeFramework.DAOs import select, Info, Frame

#### DO NOT MODIFY
class RecorderAgent(BaseAgent):
	"""
	This Agent will act just like your agent, only the game states and the agent's actions will be recorded
	"""
	def __init__(self, name, team, index):
		self.recorder = Recorder(name, team, index, "BINDao")

	def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
		"""
		we send our gametickpackets to the host agent, for it to generate
		The function's signature stays unchanged everywhere we only record what is happening
		"""
		outputs = self.agent.get_output(game_tick_packet)
		self.recorder(game_tick_packet, outputs)

		return outputs

	@staticmethod
	def create_agent_configurations(config: ConfigObject):
		"""
		creates the configurations for the recorder to have a well defined config file
		"""
		params = config.get_header(BOT_CONFIG_AGENT_HEADER)
		params.add_value('replay_path', str, default='./tests/replays', description='directory where the replays will be saved.')
		params.add_value('agent_path', str, default='./agents/legacy.py', description='python file containing the agent class, relative to RecorderAgent.py path')
		params.add_value('data_format', str, default='BINDao', description="Dao name for the data format you want \n(BINDao for Binary, JSONDao for Json XMLDao for Xml, ...)")
		params.add_value('max_frames', int, default=-1, description="Number of steps in onefile, -1 means one file for one replay\nthis might be resource intensive")

	def load_config(self, config_header):
		"""
		every variable can be tweaked from the cfg file
		that same cfg file you can use in rlbot
		"""
		#save our path, to only use absolute paths in every commands, script wise.
		#while imposing relative paths from RecorderAgent.py for outsides
		abs_repo_path = os.path.dirname(os.path.realpath(__file__))

		self.recorder.set_params(
				config_header.getint('max_frames'),
				config_header.get('data_format'),
				os.path.join(abs_repo_path, config_header.get('replay_path'))
		)

		#import our host agent thanks to the rlbot framework
		agent_path = config_header.get('agent_path')
		agent_path = os.path.join(abs_repo_path, agent_path)

		if not os.path.isfile(agent_path):
			raise FileNotFoundError("RecorderAgent: Could not find file {}".format(agent_path))
		agent_class = import_agent(agent_path).get_loaded_class()
		#init the agent just like our recorderAgent
		self.agent = agent_class(*self.init)
		self.agent.load_config(config_header)

	def initialize_agent(self):
		self.recorder.start(self.get_field_info())
		self.agent.initialize_agent()

	def save_recordings(self):
		print("Saving replay ...")
		# n_files = len(self.dao.filter(os.listdir(self.replay_path)))
		replay_file = os.path.join(self.replay_path,"{}_{:%Y%m%d_%H%M%S}".format(self.init[0][-2], datetime.now()))
		self.dao.f_write(self.data, replay_file)
		print("Replay Saved!")

	def retire(self):
		self.save_recordings()
		self.agent.retire()

		###########################################
	#the next methods are simply sent to the host agent, and copied if some data can be used
		###########################################

	def _register_field_info(self, field_info_func):
		self.agent._register_field_info(field_info_func)
		super()._register_field_info(field_info_func)

	def _register_ball_prediction(self, ball_prediction_func):
		self.agent._register_ball_prediction(ball_prediction_func)
		super()._register_ball_prediction(ball_prediction_func)

	def _register_quick_chat(self, quick_chat_func):
		self.agent._register_quick_chat(quick_chat_func)
		super()._register_quick_chat(quick_chat_func)

	def handle_quick_chat(self, index, team, quick_chat):
		self.agent.handle_quick_chat(index, team, quick_chat)

	def get_extra_pids(self):
		return self.agent.get_extra_pids()

	def get_helper_process_request(self):
		self.agent.get_helper_process_request()

	def _register_set_game_state(self, game_state_func):
		self.agent.__game_state_func = game_state_func

	def _set_renderer(self, renderer):
		self.agent.renderer = renderer
