class RunningAverage:
	def __init__(self, buffer_size=256, initial_value=1):
		self.buffer_size = buffer_size
		self.buffer = [initial_value] * buffer_size  # Fixed-size buffer initialized with 1s
		self.index = 0  # Current index in the buffer
		self.total = initial_value * buffer_size  # Initial total sum of the buffer

	def add_value(self, value):
		# Subtract the oldest value from the total and add the new value
		self.total -= self.buffer[self.index]
		self.total += value
		# Replace the oldest value with the new value in the buffer
		self.buffer[self.index] = value
		# Move to the next index, wrapping around if necessary
		self.index = (self.index + 1) % self.buffer_size

	def get_average(self):
		# Compute and return the running average
		return self.total / self.buffer_size
