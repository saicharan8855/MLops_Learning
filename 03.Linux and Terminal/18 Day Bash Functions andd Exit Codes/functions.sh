#!/bin/bash

greet() {
	echo "hello, $1!"
}


validate_features() {
	local count=$1
	if [ "$count" -eq 4 ]; then
		echo "valid: $count features"
	else
		echo "Invalid: expected 4, got $count"
	fi
}


greet "sai charan"
validate_features 4
validate_features 2 
