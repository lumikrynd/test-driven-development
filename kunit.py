def test(func):
	func.__is_test__ = True
	return func

def is_test(func):
	try:
		return func.__is_test__
	except AttributeError:
		return False

class TestResult:
	def __init__(self):
		self._run_count = 0
		self._error_count = 0

	def test_started(self):
		self._run_count += 1

	def test_failed(self):
		self._error_count += 1

	def add_result(self, other):
		self._run_count += other._run_count
		self._error_count += other._error_count

	def summary(self):
		return "%d run, %d failed" % (self._run_count, self._error_count)

	def colour_summary(self):
		message = self.summary()
		if (self._error_count > 0):
			message = "\033[31m%s\033[0m" % message
		else:
			message = "\033[92m%s\033[0m" % message
		return message


class TestCase:
	def __init__(self):
		self._name = None

	def setup(self):
		pass

	def teardown(self):
		pass

	def set_name(self, name):
		self._name = name

	def run(self):
		result = TestResult()
		result.test_started()

		try:
			self.setup()
			method = getattr(self, self._name)
			method()
		except AttributeError:
			raise
		except:
			result.test_failed()

		self.teardown()
		return result

	def get_test_names(self):
		result = dir(self)
		result = [s for s in result if is_test(getattr(self, s))]
		return result

	def get_test_for(self, name):
		test = self.__class__()
		test.set_name(name)
		return test

	def get_test_suite(self):
		suite = TestSuite()
		for name in self.get_test_names():
			suite.add(self.get_test_for(name))
		return suite


class TestSuite:
	def __init__(self):
		self._tests = []

	def add(self, test):
		self._tests.append(test)

	def run(self):
		result = TestResult()
		for test in self._tests:
			test_result = test.run()
			result.add_result(test_result)

		return result
