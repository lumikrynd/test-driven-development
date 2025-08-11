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

	def getTestNames(self):
		result = set(dir(self)) - set(dir(TestCase))
		result = [s for s in result if s.startswith("test")]
		return result

	def getTestSuite(self):
		suite = TestSuite()
		return suite


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
