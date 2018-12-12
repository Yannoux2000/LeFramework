
from .base_model import BaseModel
import torch
# from torch import nn
# from torch import optim

class TorchSimpleModel:
	def create_model(self, num_inputs):

		num_outputs = 7

		self.lstm_size = 16
		self.lstm = nn.LSTMCell(num_inputs, self.lstm_size)

		self.critic_linear = nn.Linear(self.lstm_size, 1)
		self.actor_linear = nn.Linear(self.lstm_size, num_outputs)

		self.train()

	def finalize_model(self):
		"""Calc loss here"""
		pass

	def fit(self, x, y, rewards=None, batch_size=1):
		pass

	def forward(self, x):
		hx, cx = self.lstm(x, (hx, cx))
		x = hx
		return self.critic_linear(x), self.actor_linear(x), (hx, cx)

	def save(self, file_path):
		raise NotImplementedError()

	def load(self, file_path):
		raise NotImplementedError()

if __name__ == '__main__':
	BaseModel.load(None, None)