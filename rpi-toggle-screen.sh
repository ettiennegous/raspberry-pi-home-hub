#!/bin/sh

# Enable and disable Display Link output on the Raspberry Pi

case $1 in
	off)
		xset -display :0.0 dpms force off
	;;
	on)
		xset -display :0.0 dpms force on
	;;
	status)
		echo "No idea what the status is sorry"
	;;
	*)
		echo "Usage: $0 on|off|status" >&2
		exit 2
	;;
esac

exit 0
