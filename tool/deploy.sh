#!/usr/bin/env bash

for target in 10.0.0.1 10.0.0.2 10.0.0.4 10.0.0.5; do
	echo Copying to $target...
	scp disciple.py shared.py $target:
	echo;
done

echo Copying to Windows...

if [ ! -f ~/mnt/win/desktop.ini ]; then
	mkdir -p ~/mnt/win
	# Yes, I am aware that I'm submitting this uber secret secure password to Github.
	# The target system is never connected to the internet and it's not meant for
	# security anyway (password is only set to allow us to log in).
	sudo mount -t cifs -o user=user,pass=123123 //10.0.0.3/Desktop ~/mnt/win
fi;

sudo cp disciple.py shared.py ~/mnt/win

