from rlbot.agents.base_agent import BaseAgent, SimpleControllerState

#select here what type of file you want to use.
#Make sure the DAOs.py file is accessible from this file
from DAOs import BINDao as DAO
"""import your agent here"""
from <your_agent_here> import <your_agent_here> as recordedAgent

"""
Steps before executing :
	-	Setting this agent as the one being used by rlbot
	-	Defining your agent class as the one being imported as recorded Agent
	-	Defining path in the config file for your bot
	-	Selecting the DAO class used for your 
"""


#this class is used to keep a structure in the saved objects
class Tick:
	def __init__(self, game_tick_packet, controller, index):
		self.index = index
		self.game_tick_packet = game_tick_packet
		self.controller = controller

class RLRecorderAgent(recordedAgent):
	"""This Agent will act just like your agent, only the gametickpackets and outputs will be recorded"""

	def __init__(self, name, team, index):
		super().__init__(name, team, index)
		self.tick = 0

	def load_config(self, config_header):
		self.path = config_header.get('path')

		if not os.path.exists(self.path):
			os.makedirs('/'.join(self.path.split('/')[:-1]))# create dirs removing file name from path avoid creating dir called as file
			os.mknod(self.path)

		super().load_config(config_header)

	def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
		outputs = super().get_output(game_tick_packet)

		data = Tick(game_tick_packet,outputs,self.tick)
		self.tick += 1

		file = open(self.path,"a")
		file.write(data.toJSON())
		file.close()

		return outputs
