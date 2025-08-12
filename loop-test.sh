#! /usr/bin/env sh

while true; do
	clear -x
	python kunit.test.py
	echo
	date +"%T" 
	echo "Press enter to rerun" ; read
done;
