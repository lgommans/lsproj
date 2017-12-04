#!/usr/bin/env bash

for target in 10.0.0.1 10.0.0.2 10.0.0.4 10.0.0.5; do
	echo Copying to $target
	scp disciple.py shared.py $target:
done

echo todo: windows at .3

