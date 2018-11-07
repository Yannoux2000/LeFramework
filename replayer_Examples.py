"""
Welcome to an example / tutorial python script to reading replays
This script contains the only two functions you would ever need to call
Most of the configurations can be made in the function's parameters
"""
from replayer.Base_Replayer import Base_Replayer
from DAOs import select, BINDao

def example_replay(agent_config, replay_dir="./replays", dao=BINDao, n=100):
	"""
	This method replays previously recorded games
	:param agent_config: path to the agent's cfg
	:param replay_dir: path to the directory containings replays
	:param dao: Data accessor object, also used to write, BINDao is my recomandation
	:param n: size of batch
	"""
	#we generate the configurations
	replayer = Base_Replayer(dao)
	"""
	we use the rlbot framework to read from the config file
	therefore, you could train asynchroniously while in game
	"""
	agent_class = replayer.import_agent(agent_config)

	replayer.set_files_list(replay_dir)
	"""
	Here we initialize the agent, after the first iteration
	the files are read only on a call from batch
	"""
	agent = None
	#the batch size could vary at the end of the final file
	for batch in replayer.batch(n=n):
		"""
		the for loop outputs the content of each file once, to train multiple times on the same files, don't forget to call
		replayer.set_files_list(replay_dir)
		"""
		if agent is None:
			agent = replayer.init_agent(agent_class)

		"""
		each batch are lists of n frame objects, a frame object has 3 attributes:
			- f_index 			: index of frame, always in the right order
			- game_tick_packet	: just like in get_output for any agent 
			- controller		: the outputs the agent had for that game_tick_packet
		"""

		####TODO####
		"""
		In this section, it is up to you to decide how to implement what ever you want to do
		this repo was made in mind to help for supervised learning. so everything is ready for you to train here
		"""
	print("Done")

if __name__ == '__main__':
	example_replay("./agents/blank.cfg")

