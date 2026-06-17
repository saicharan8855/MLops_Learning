#!/bin/bash

LOG_FILE="app.log"

echo "2026-06-17 10:00:01 INFO model loaded successfully" > $LOG_FILE
echo "2026-06-17 10:00:05 INFO prediction request received" >> $LOG_FILE
echo "2026-06-17 10:00:06 DEBUG features validated" >> $LOG_FILE
echo "2026-06-17 10:00:07 INFO prediction complete: setosa" >> $LOG_FILE
echo "2026-06-17 10:01:15 ERROR invalid feature count" >> $LOG_FILE
echo "2026-06-17 10:02:30 WARNING low confidence score" >> $LOG_FILE
echo "2026-06-17 10:03:00 INFO prediction complete: versicolor" >> $LOG_FILE
echo "2026-06-17 10:04:45 ERROR model file not found" >> $LOG_FILE
echo "2026-06-17 10:05:10 INFO prediction complete: virginica" >> $LOG_FILE
echo "2026-06-17 10:06:00 CRITICAL system out of memory" >> $LOG_FILE

echo "log file generated: $LOG_FILE"

