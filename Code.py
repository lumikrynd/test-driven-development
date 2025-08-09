class WasRun:
	def __init__(self, name):
		self.wasRun = False

	def testMethod(self):
		self.wasRun = True


test = WasRun("testMethod")
print(test.wasRun)
test.testMethod()
print(test.wasRun)
