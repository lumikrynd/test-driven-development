class TestCase:
	def __init__(self, name):
		self.name = name

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def run(self):
		self.setUp()
		method = getattr(self, self.name)
		method()
		self.tearDown()


class WasRun(TestCase):
	def setUp(self):
		self.log = "setup "

	def testMethod(self):
		self.log += "testMethod "

	def tearDown(self):
		self.log += "tearDown "


class TestCaseTest(TestCase):
	def testTemplateMethod(self):
		test = WasRun("testMethod")
		test.run()
		assert test.log == "setup testMethod tearDown "


TestCaseTest("testTemplateMethod").run()

print("\033[92mGreen\033[0m")
