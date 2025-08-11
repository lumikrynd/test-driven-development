from kunit import TestCase
from kunit import TestSuite


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
		test.run()
		assert test.log == "setup tearDown "

	def testGetTestNames(self):
		result = WasRun(None).getTestNames()
		assert "testMethod" in result
		assert "testBrokenMethod" in result
		assert len(result) == 2

	def testGetTestSuite(self):
		suite = WasRun(None).getTestSuite()
		result = suite.run()
		assert result.summary() == "2 run, 1 failed"


def runTestCaseTest(name):
	suite.add(TestCaseTest(name))


def runWithStackTrace(name):
	test = TestCaseTest(name)
	method = getattr(test, name)
	method()


suite = TestSuite()

runTestCaseTest("testTemplateMethod")
runTestCaseTest("testResult")
runTestCaseTest("testFailedResult")
runTestCaseTest("testSuite")
runTestCaseTest("testFailedSetup")
runTestCaseTest("testTearDownRunsOnError")
runTestCaseTest("testGetTestNames")
# runTestCaseTest("testGetTestSuite")

finalResult = suite.run()
print(finalResult.colourSummary())

# runWithStackTrace("testCase")
