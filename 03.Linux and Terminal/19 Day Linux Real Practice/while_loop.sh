#!/bin/bash


echo "waiting for model file"

COUNT=0
MAX_TRIES=5


while [ ! -f "ready_model.pkl" ]
do
	COUNT=$((COUNT +1))
	echo "  attempt $COUNT - model not ready yet,..."
	sleep 1

	if [ $COUNT -ge $MAX_TRIES ]; then
		echo "timeout - model never appeared after $MAX_TRIES attempts"
		exit 1
	fi
done

echo "model is ready"

