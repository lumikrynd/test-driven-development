def test(func):
	func.__is_test__ = True
	return func

def is_test(func):
	try:
		return func.__is_test__
	except AttributeError:
		return False

INDENT = "    "

class TestResult:
	def __init__(self):
		self._run_count = 0
		self._errors = []

	def test_started(self):
		self._run_count += 1

	def test_failed(self, name, err):
		self._errors.append((name, err))

	def add_result(self, other):
		self._run_count += other._run_count
		self._errors.extend(other._errors)

	def _error_count(self):
		return len(self._errors)

	def failed_tests(self):
		temp = map(lambda x: x[0], self._errors)
		return list(temp)

	def summary(self):
		error_count = self._error_count()
		return "%d run, %d failed" % (self._run_count, error_count)

	def _errors_summary(self):
		indented = map(lambda x: INDENT + x, self.failed_tests())
		error_names = '\n'.join(indented)
		error_names = "Failed tests:\n" + error_names
		return error_names

	def _format_error(err_info):
		result = "Test: " + err_info[0]

		err = err_info[1]
		result += "\n" + INDENT + type(err).__name__

		msg = str(err)
		if (len(msg) > 0):
			result += "\n" + INDENT + msg

		return result

	def _errors_long(self):
		temp = map(lambda x: TestResult._format_error(x), self._errors)
		return "\n\n".join(temp)

	def colour_result(self):
		summary = self.summary()
		error_count = self._error_count()
		if (error_count == 0):
			return "\033[92m%s\033[0m" % summary

		summary = "\033[31m%s\033[0m" % summary
		errors_summary = self._errors_summary()
		errors_info = self._errors_long()

		return errors_info + "\n\n\n" + errors_summary + "\n\n" + summary


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
		except Exception as err:
			result.test_failed(self._name, err)

		self.teardown()
		return result

	def get_test_names(self):
		result = set(dir(self)) - set(dir(TestCase))
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
