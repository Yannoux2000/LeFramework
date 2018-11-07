from rlbot.agents.base_agent import BaseAgent, BOT_CONFIG_AGENT_HEADER, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.parsing.custom_config import ConfigObject, ConfigHeader
from rlbot.utils.class_importer import *
from DAOs import select


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
	"""
	This Agent will act just like your agent, only the observations and actions will be recorded
	"""
	def __init__(self, name, team, index):

		self.init = (name, team, index)
		self.tick = 0
		self.data = []
		self.dao = select("BINDao")

	def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
		"""
		we send our gametickpackets to the host agent, for it to generate
		The function's signature stays unchanged everywhere we only record what is happening
		"""
		outputs = self.agent.get_output(game_tick_packet)

		self.data.append(Frame(game_tick_packet,outputs,self.tick))
		self.tick += 1

		if self.max_frames != -1 and self.tick%self.max_frames:
			self.save_recordings()

		return outputs

	@staticmethod
	def create_agent_configurations(config: ConfigObject):
		"""
		creates the configurations for the recorder to have a well defined config file
		"""
		params = config.get_header(BOT_CONFIG_AGENT_HEADER)
		params.add_value('replay_path', str, default='./tests/replays', description='directory where the replays will be saved.')
		params.add_value('agent_path', str, default='./agents/legacy.py', description='python file containing the agent class')
		params.add_value('data_format', str, default='BINDao', description="Dao name for the data format you want \n(BINDao for Binary, JSONDao for Json XMLDao for Xml, ...)")
		params.add_value('max_frames', int, default=-1, description="Number of steps in onefile, -1 means one file for one replay\nthis might be resource intensive")

	def load_config(self, config_header):
		"""
		every variable can be tweaked from the cfg file
		that same cfg file you can use in rlbot
		"""
		dao_name = config_header.get('data_format')
		self.dao = select(dao_name)

		replay_dir = config_header.get('replay_path')
		n_files = len(self.dao.filter(os.listdir(replay_dir)))
		self.replay_path = os.path.join(replay_dir,"{:08d}".format(n_files))

		self.max_frames = config_header.getint('max_frames')

		#import our host agent thanks to the rlbot framework
		agent_path = config_header.get('agent_path')
		agent_class = import_agent(agent_path).get_loaded_class()
		#init the agent just like our recorderAgent
		self.agent = agent_class(*self.init)
		self.agent.load_config(config_header)

	def initialize_agent(self):
		self.data.append(Info(self.get_field_info(),self.init))
		self.agent.initialize_agent()

	def save_recordings(self):
		self.dao.f_write(self.data, self.replay_path)

	def retire(self):
		self.agent.retire()
		self.save_recordings()

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
		self.agent.get_extra_pids()

	def get_helper_process_request(self):
		self.agent.get_helper_process_request()

	def _register_set_game_state(self, game_state_func):
		self.agent.__game_state_func = game_state_func

	def _set_renderer(self, renderer):
		self.agent.renderer = renderer
