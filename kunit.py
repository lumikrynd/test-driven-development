class TestResult:
	def __init__(self):
		self._runCount = 0
		self._errorCount = 0

	def testStarted(self):
		self._runCount += 1

	def testFailed(self):
		self._errorCount += 1

	def addResult(self, other):
		self._runCount += other._runCount
		self._errorCount += other._errorCount

	def summary(self):
		return "%d run, %d failed" % (self._runCount, self._errorCount)

	def colourSummary(self):
		message = self.summary()
		if (self._errorCount > 0):
			message = "\033[31m%s\033[0m" % message
		else:
			message = "\033[92m%s\033[0m" % message
		return message


class TestCase:
	def __init__(self, name):
		self._name = name

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def run(self):
		result = TestResult()
		result.testStarted()

		try:
			self.setUp()
			method = getattr(self, self._name)
			method()
		except:
			result.testFailed()

		self.tearDown()

		return result

	def getTestNames(self):
		result = set(dir(self)) - set(dir(TestCase))
		result = [s for s in result if s.startswith("test_")]
		return result

	def getTestSuite(self):
		suite = TestSuite()
		return suite


class TestSuite:
	def __init__(self):
		self._tests = []

	def add(self, test):
		self._tests.append(test)

	def run(self):
		result = TestResult()
		for test in self._tests:
			testResult = test.run()
			result.addResult(testResult)

		return result
