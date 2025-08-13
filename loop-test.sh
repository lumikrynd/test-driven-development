#! /usr/bin/env sh

while true; do
	clear -x
	python kunit.test.py
	echo
	stopwatch
done;
