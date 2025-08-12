from kunit import TestCase
from kunit import TestSuite


class WasRun(TestCase):
	def __init__(self):
		self.log = ""
		super().__init__()

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
	def _createWasRun(self, testName):
		test = WasRun()
		test.setName(testName)
		return test

	def test_TemplateMethod(self):
		test = self._createWasRun("test_Method")
		test.run()
		assert test.log == "setup test_Method tearDown "

	def test_Result(self):
		test = self._createWasRun("test_Method")
		result = test.run()
		assert result.summary() == "1 run, 0 failed"

	def test_FailedResult(self):
		test = self._createWasRun("test_BrokenMethod")
		result = test.run()
		assert result.summary() == "1 run, 1 failed"

	def test_Suite(self):
		suite = TestSuite()
		suite.add(self._createWasRun("test_Method"))
		suite.add(self._createWasRun("test_BrokenMethod"))
		result = suite.run()
		assert result.summary() == "2 run, 1 failed"

	def test_FailedSetup(self):
		test = BrokenSetup()
		test.setName("test_Method")
		result = test.run()
		assert result.summary() == "1 run, 1 failed"

	def test_TearDownRunsOnError(self):
		test = self._createWasRun("test_BrokenMethod")
		test.run()
		assert test.log == "setup tearDown "

	def test_GetTestNames(self):
		result = WasRun().getTestNames()
		assert "test_Method" in result
		assert "test_BrokenMethod" in result
		assert len(result) == 2

	def test_GetTestFor(self):
		name = "test_Method"
		test = WasRun().getTestFor(name)
		result = test.run()
		assert test._name == name
		assert result.summary() == "1 run, 0 failed"

	def test_GetTestSuite(self):
		suite = WasRun().getTestSuite()
		result = suite.run()
		assert result.summary() == "2 run, 1 failed"


def runWithStackTrace(name):
	test = TestCaseTest(name)
	method = getattr(test, name)
	method()


suite = TestCaseTest().getTestSuite()
result = suite.run()
print(result.colourSummary())

# runWithStackTrace("testCase")
