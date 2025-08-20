#! /usr/bin/env sh
# Runs the tests every time enter is pressed
# Displays a timer showing how long ago the test-suite last ran

while true; do
	clear -x
	python kunit.test.py
	echo
	stopwatch
done;
