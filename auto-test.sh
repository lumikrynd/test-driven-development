#! /usr/bin/env sh
# Runs the tests every time a file is modified
# Displays a timer showing how long ago the test-suite last ran
#
# Doesn't react on files being deleted

timestamp_file='.auto-run-mark'

touch -d "1970-01-01 00:00:00" $timestamp_file
display-timer &
timer_pid=$!

function cleanup {
	rm $timestamp_file
	kill $timer_pid
}
trap cleanup EXIT

while true; do
	changes=$(find . -iname '*.py' -cnewer $timestamp_file | wc -l)
	if [ ! "$changes" = "0" ]; then
		touch $timestamp_file
		kill $timer_pid
		clear -x
		python kunit.test.py
		echo
		display-timer &
		timer_pid=$!
	fi

	sleep 0.1
done;
