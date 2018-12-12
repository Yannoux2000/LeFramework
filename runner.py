from rlbot.setup_manager import SetupManager
import os


"""custom runner to load the configs i would want"""


def custom_main(config_location = "./rlbot.cfg"):
	print("starting")
	manager = SetupManager()
	manager.startup()
	manager.load_config(config_location = os.path.realpath(config_location))
	manager.launch_bot_processes()
	manager.run()
