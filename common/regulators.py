def clip(v, min_v=-1, max_v=1):
	return max(min_v, min(v, max_v))

ALL_TIMERS = []

def RESET_ALL_TIMERS():
	global ALL_TIMERS
	ALL_TIMERS = []

class Timer():
	def __init__(self, t = 0):
		global ALL_TIMERS
		ALL_TIMERS.append(self)
		self.reset(t)
		self.run = False

	def set_run(self):
		self.run = True

	def set_stop(self):
		self.run = False

	def reset(self, t=0):
		self.t = t
	
	def __call__(self, t):
		return self.t >= t

	def step(self, dt = 1/60):
		if self.run:
			self.t += dt


class PID():
	def __init__(self, p=1, i=0, d=0):
		self.Kp = p
		self.Ki = i
		self.Kd = d
		
		# P is used to set the responds time, while avoiding ocilations (aim for butterworth)
		# I is used to improve precition, deleting any static error, and removing ocilations, but can still provoque more
		# D is used to improve stability, as for avoiding overall ocilations

		self.target = 0
		
		self._error = 0
		self.error_sum = 0

	@property
	def error(self):
		return self._error

	def __str__(self):
		return "Kp{:<4.2f}, Ki{:<4.2f}, Kd{:<4.2f}, {:<6.2f}, {:<10.2f}".format(self.Kp, self.Ki, self.Kd, self.target, self.error_sum)

	def __call__(self, feedback, dt = 1):

		# Calculate error.
		error = self.target - feedback
		self.error_sum = clip(self.error_sum + error, -1e5, 1e5)

		# Add P proportional component.
		alpha = self.Kp * error
		# Add I integral component.
		alpha += (self.Ki / dt) * (self.error_sum)
		# Add D differential component.
		alpha += (self.Kd * dt) * (error - self._error)

		# Maintain memory for next loop.
		self._error = error
		return alpha

class Cascade2PID():
	def __init__(self, pid_regulated = PID(), pid_slave = PID()):
		# as for example x, as a location, can be concider regulated, compared to dx (derivative of x)
		# therefore i called the regulated

		self.regul = pid_regulated
		self.slave = pid_slave

		self.internal_c = 0

	@property
	def error(self):
		return self.regul.error

	@property
	def target(self):
		return self.regul.target

	@target.setter
	def target(self, v):
		self.regul.target = float(v)

	def __call__(self, f, df, dt = 1):
		self.internal_c = self.regul(f, dt) * 1/dt
		self.slave.target = self.internal_c
		self.dc = self.slave(df, dt)
		return self.dc
