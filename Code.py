class TestCase:
	def __init__(self, name):
		self.name = name

	def setUp(self):
		pass

	def run(self):
		method = getattr(self, self.name)
		self.setUp()
		method()


class WasRun(TestCase):
	wasRun = False
	wasSetUp = False

	def setUp(self):
		self.wasSetUp = True

	def testMethod(self):
		self.wasRun = True


class TestCaseTest(TestCase):
	def setUp(self):
		self.test = WasRun("testMethod")

	def testRunning(self):
		assert not self.test.wasRun
		self.test.run()
		assert self.test.wasRun

	def testSetup(self):
		self.test.run()
		assert self.test.wasSetUp


TestCaseTest("testRunning").run()
TestCaseTest("testSetup").run()

print("\033[92mGreen\033[0m")
