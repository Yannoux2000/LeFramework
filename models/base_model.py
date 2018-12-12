class BaseModel:
	def __init__(self):
		pass

	def create_model(self, num_inputs):
		pass

	def finalize_model(self):
		"""Calc loss here"""
		pass

	def fit(self, x, y, rewards=None, batch_size=1):
		pass

	def predict(self, arr):
		pass

	def save(self, file_path):
		raise NotImplementedError()

	def load(self, file_path):
		raise NotImplementedError()

if __name__ == '__main__':
	BaseModel.load(None,None)