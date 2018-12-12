"""
Welcome to an example / tutorial python script to reading replays
This script contains the only two functions you would ever need to call
Most of the configurations can be made in the function's parameters


MAY NOT BE UP TO DATE

"""
from replayers.base_replayer import Base_Replayer
from daos import select, BINDao

# example_replay("./agents/legacy.cfg", "./tests/replays", select("BINDao"), n=200)
def example_replay(agent_config, replay_dir="./replays", dao=BINDao, n=100):

	replayer = Base_Replayer(dao)
	agent_class = replayer.import_agent(agent_config)

	replayer.set_files_list(replay_dir)
	agent = None
	for batch in replayer.batch(n=n):
		if agent is None:
			agent = replayer.init_agent(agent_class)

			for b in batch[::-1]:
				print(b['f_index']) 
				print(b['game_tick_packet'])
				print()
				print(b['controller'])
				print(agent.get_output(b['game_tick_packet']))

	print("Done")
# example_train
def example_train(agent, batch):
	for b in batch:
		print(agent.get_output(b).__dict__)



if __name__ == '__main__':

	rplr = Base_Replayer(BINDao)
	rplr.set_files_list("./tests/replays")
	agt_packet = rplr.import_agent("./agents/blank.cfg")

