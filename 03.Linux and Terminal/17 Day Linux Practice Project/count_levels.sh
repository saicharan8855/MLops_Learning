#!/bin/bash

LOG_FILE="app.log"

echo "log level breakdown: "
for level in INFO DEBUG WARNING ERROR CRITICAL
do
	count=$(grep -c "$level" $LOG_LEVEL)
	echo "   $level: $count"
done

