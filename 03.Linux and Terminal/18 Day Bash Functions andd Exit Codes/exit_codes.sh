#!/bin/bash

echo "running a command that succeeds..."
ls ~ > /dev/null
echo "exit code: $?"

echo ""
echo "running a command that fails"
ls /this/does/not/exist > /dev/null 2>&1
echo "exit code: $?"

echo ""
echo "custom exit code from a function"
check_model() {
	if [ -f "iris_model.pkl" ]; then
		return 0
	else
		return 1
	fi
}

check_model
if [ $? -eq 0 ]; then
	echo "model check passed"
else
	echo "model check failed"
fi
