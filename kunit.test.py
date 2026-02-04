from collections import Counter
from kunit import test, is_test, TestCase, TestSuite

class WasRun(TestCase):
	def __init__(self):
		self.log = ""
		super().__init__()

	def setup(self):
		self.log += "setup "

	def teardown(self):
		self.log += "tearDown "

	@test
	def test_method(self):
		self.log += "test_Method "

	@test
	def marked_test(self):
		pass

	def not_a_test(self):
		pass

	@test
	def broken_test(self):
		raise Exception


class BrokenSetup(WasRun):
	def setup(self):
		raise Exception


class TestCaseTest(TestCase):
	def _createWasRun(self, testName):
		test = WasRun()
		test.set_name(testName)
		return test

	@test
	def correct_test_flow(self):
		test = self._createWasRun("test_method")
		test.run()
		assert test.log == "setup test_Method tearDown "

	@test
	def run_tests_are_counted(self):
		test = self._createWasRun("test_method")
		result = test.run()
		assert result.summary() == "1 run, 0 failed"

	@test
	def failed_tests_are_counted(self):
		test = self._createWasRun("broken_test")
		result = test.run()
		assert result.summary() == "1 run, 1 failed"

	@test
	def wrong_test_name_causes_exception(self):
		"""Show other tests would fail if wrong name for test method was used"""
		test = self._createWasRun("non_existing_test")
		try:
			result = test.run()
		except:
			return

		assert False

	@test
	def test_suite_runs_contained_tests(self):
		suite = TestSuite()
		suite.add(self._createWasRun("test_method"))
		suite.add(self._createWasRun("broken_test"))
		result = suite.run()
		assert result.summary() == "2 run, 1 failed"

	@test
	def failed_setup_causes_test_fail(self):
		test = BrokenSetup()
		test.set_name("test_method")
		result = test.run()
		assert result.summary() == "1 run, 1 failed"

	@test
	def teardown_runs_on_error(self):
		test = self._createWasRun("broken_test")
		test.run()
		assert test.log == "setup tearDown "

	@test
	def test_get_test_names(self):
		result = WasRun().get_test_names()
		assert "test_method" in result
		assert "broken_test" in result
		assert "marked_test" in result
		assert len(result) == 3

	@test
	def test_get_test_for(self):
		name = "test_method"
		test = WasRun().get_test_for(name)
		result = test.run()
		assert test._name == name
		assert result.summary() == "1 run, 0 failed"

	@test
	def create_test_suite_from_test_class(self):
		suite = WasRun().get_test_suite()
		result = suite.run()
		assert result.summary() == "3 run, 1 failed"
		assert Counter(result.failed_tests()) == Counter(["broken_test"])

	@test
	def normal_function_not_marked_as_test(self):
		test_class = WasRun()
		test = test_class.not_a_test
		assert not is_test(test)

	@test
	def test_method_marked_as_test(self):
		test_class = WasRun()
		test = test_class.marked_test
		assert is_test(test)


def run_with_stack_trace(name):
	test = TestCaseTest()
	method = getattr(test, name)
	method()


suite = TestCaseTest().get_test_suite()
result = suite.run()
print(result.colour_result())

# run_with_stack_trace("test_case")
