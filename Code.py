from kunit import TestCase
from kunit import TestSuite


class WasRun(TestCase):
	def __init__(self, name):
		self.log = ""
		super().__init__(name)

	def setUp(self):
		self.log += "setup "

	def tearDown(self):
		self.log += "tearDown "

	def test_Method(self):
		self.log += "test_Method "

	def test_BrokenMethod(self):
		raise Exception


class BrokenSetup(WasRun):
	def setUp(self):
		raise Exception


class TestCaseTest(TestCase):
	def test_TemplateMethod(self):
		test = WasRun("test_Method")
		test.run()
		assert test.log == "setup test_Method tearDown "

	def test_Result(self):
		test = WasRun("test_Method")
		result = test.run()
		assert result.summary() == "1 run, 0 failed"

	def test_FailedResult(self):
		test = WasRun("test_BrokenMethod")
		result = test.run()
		assert result.summary() == "1 run, 1 failed"

	def test_Suite(self):
		suite = TestSuite()
		suite.add(WasRun("test_Method"))
		suite.add(WasRun("test_BrokenMethod"))
		result = suite.run()
		assert result.summary() == "2 run, 1 failed"

	def test_FailedSetup(self):
		test = BrokenSetup("test_Method")
		result = test.run()
		assert result.summary() == "1 run, 1 failed"

	def test_TearDownRunsOnError(self):
		test = WasRun("test_BrokenMethod")
		test.run()
		assert test.log == "setup tearDown "

	def test_GetTestNames(self):
		result = WasRun(None).getTestNames()
		assert "test_Method" in result
		assert "test_BrokenMethod" in result
		assert len(result) == 2

	def test_GetTestSuite(self):
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

runTestCaseTest("test_TemplateMethod")
runTestCaseTest("test_Result")
runTestCaseTest("test_FailedResult")
runTestCaseTest("test_Suite")
runTestCaseTest("test_FailedSetup")
runTestCaseTest("test_TearDownRunsOnError")
runTestCaseTest("test_GetTestNames")
# runTestCaseTest("test_GetTestSuite")

finalResult = suite.run()
print(finalResult.colourSummary())

# runWithStackTrace("testCase")
