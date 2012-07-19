import sys
class ProgressMeter:
	def __init__(self,job_size,update_time=1):
		self.job_size=float(job_size)
		self.steps_done=float(0)
		self.update_time = update_time

	def step (self):
		self.steps_done +=1
		self.__show(self.steps_done)

	def update (self, step):
		self.steps_done = step
		if (self.steps_done % self.update_time == 0):
			self.__show(self.steps_done)

	def __show (self,complete):
		sys.stdout.write("Working: {:.2%} done\r".format(complete/self.job_size))
		sys.stdout.flush()

	def done(self):
		clear = chr(27) + '[2K' + chr(27) +'[G'
		sys.stdout.write(clear + "Job complete!\n")
		sys.stdout.flush()
