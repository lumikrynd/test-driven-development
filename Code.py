class TestResult:
	def __init__(self):
		self.runCount = 0
		self.errorCount = 0

	def testStarted(self):
		self.runCount += 1

	def testFailed(self):
		self.errorCount += 1

	def addResult(self, other):
		self.runCount += other.runCount
		self.errorCount += other.errorCount

	def summary(self):
		return "%d run, %d failed" % (self.runCount, self.errorCount)


class TestCase:
	def __init__(self, name):
		self.name = name

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def run(self):
		result = TestResult()
		result.testStarted()

		try:
			self.setUp()
			method = getattr(self, self.name)
			method()
		except:
			result.testFailed()

		self.tearDown()

		return result


class TestSuite:
	def __init__(self):
		self.tests = []

	def add(self, test):
		self.tests.append(test)

	def run(self):
		result = TestResult()
		for test in self.tests:
			testResult = test.run()
			result.addResult(testResult)

		return result


class WasRun(TestCase):
	def __init__(self, name):
		self.log = ""
		super().__init__(name)

	def setUp(self):
		self.log += "setup "

	def testMethod(self):
		self.log += "testMethod "

	def tearDown(self):
		self.log += "tearDown "

	def testBrokenMethod(self):
		raise Exception


class BrokenSetup(WasRun):
	def setUp(self):
		raise Exception


class TestCaseTest(TestCase):
	def testTemplateMethod(self):
		test = WasRun("testMethod")
		test.run()
		assert test.log == "setup testMethod tearDown "

	def testResult(self):
		test = WasRun("testMethod")
		result = test.run()
		assert result.summary() == "1 run, 0 failed"

	def testFailedResult(self):
		test = WasRun("testBrokenMethod")
		result = test.run()
		assert result.summary() == "1 run, 1 failed"

	def testSuite(self):
		suite = TestSuite()
		suite.add(WasRun("testMethod"))
		suite.add(WasRun("testBrokenMethod"))
		result = suite.run()
		assert result.summary() == "2 run, 1 failed"

	def testFailedSetup(self):
		test = BrokenSetup("testMethod")
		result = test.run()
		assert result.summary() == "1 run, 1 failed"

	def testTearDownRunsOnError(self):
		test = WasRun("testBrokenMethod")
		result = test.run()
		assert test.log == "setup tearDown "

	def testGetTestSuite(self):
		suite = WasRun(None).getTestSuite()
		result = suite.run()
		assert result.summary() == "2 run, 1 failed"
		pass

def runTestcaseTest(name):
	suite.add(TestCaseTest(name))


def runWithStackTrace(name):
	test = TestCaseTest(name)
	method = getattr(test, name)
	method()


suite = TestSuite()

runTestcaseTest("testTemplateMethod")
runTestcaseTest("testResult")
runTestcaseTest("testFailedResult")
runTestcaseTest("testSuite")
runTestcaseTest("testFailedSetup")
runTestcaseTest("testTearDownRunsOnError")
# runTestcaseTest("testGetTestSuite")

finalResult = suite.run()
print(finalResult.summary())

# runWithStackTrace("testCase")

assert finalResult.errorCount == 0

print("\033[92mGreen\033[0m")
