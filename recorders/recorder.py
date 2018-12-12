from LeFramework.daos import select, Info, Frame

from datetime import datetime

class Recorder:
	def __init__(self, name, team, index, max_frames = -1, data_format = "BINDao", replay_path = "./tests/replays"):

		self.init = (name, team, index)
		self.set_params(max_frames, data_format, replay_path)

	def set_params(self, max_frames = -1, data_format = "BINDao", replay_path = "./tests/replays"):
		self.dao = select(data_format)

		self.tick = 0
		self.data = []

		self.max_frames = max_frames
		self.replay_path = replay_path

		self.started = False

	def start(self, info):
		self.data.append(Info(info, self.init))
		self.started = True

	def __call__(self, game_tick_packet, outputs):

		if self.started == False:
			raise Exception("Recorder didn't started, call start before this function")
		self.data.append(Frame(game_tick_packet, outputs, self.tick))
		self.tick += 1

		if self.max_frames != -1 and self.tick%self.max_frames == 0:
			self.save_recordings()

	def save_recordings():
		print("Saving replay ...")
		
		replay_file = os.path.join(self.replay_path,"{}_{:%Y%m%d_%H%M%S}".format(self.init[0][:-3], datetime.now()))
		self.dao.f_write(self.data, replay_file)
		print("Replay Saved!")
