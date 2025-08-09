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
	def __init__(self, name):
		self.wasRun = False
		self.wasSetUp = False
		TestCase.__init__(self, name)

	def testMethod(self):
		self.wasRun = True

	def setUp(self):
		self.wasSetUp = True


class TestCaseTest(TestCase):
	def testRunning(self):
		test = WasRun("testMethod")
		assert not test.wasRun
		test.run()
		assert test.wasRun

	def testSetup(self):
		test = WasRun("testMethod")
		test.run()
		assert test.wasSetUp


TestCaseTest("testRunning").run()
TestCaseTest("testSetup").run()
