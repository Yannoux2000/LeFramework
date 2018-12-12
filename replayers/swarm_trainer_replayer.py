from LeFramework.replayers.Base_Replayer import Base_Replayer
from LeFramework.DAOs import select, BINDao
import multiprocessing

def example_replay(agent_config, replay_dir="./replays", dao=BINDao, n=100):

	replayer = Base_Replayer(dao)
	agent_class = replayer.import_agent(agent_config)

	replayer.set_files_list(replay_dir)
	agent = None
	for batch in replayer.batch(n=n):
		if agent is None:
			agent = replayer.init_agent(agent_class)


	print("Done")
