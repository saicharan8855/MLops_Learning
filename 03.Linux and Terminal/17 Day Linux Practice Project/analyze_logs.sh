#!/bin/bash

LOG_FILE="app.log"

if [ ! -f "$LOG_FILE" ]; then
	echo "Error: $LOG_FILE not found. run generate_logs.sh first"
	exit 1
fi

echo "================="
echo "Log analsis report"
echo "================"

TOTAL=$(wc -l < $LOG_FILE)
echo "Total log lines: $TOTAL"
echo ""

echo "--- Error count ---"
grep -c "ERROR" $LOG_FILE

echo "--- WARNING count ---"
grep -c "WARNING"  $LOG_FILE

echo "--- CRITICAL entries ---"
grep "CRITICAL" $LOG_FILE

echo ""
echo "--- All ERROR lines ---"
echo "ERROR" $LOG_FILE

echo ""
echo "--- successful predictions ---"
grep "prediction complete" $LOG_FILE

echo ""
echo "--- searching foro specific class: setosa ---"
grep "setosa" $LOF_FILE

echo ""
echo "Report saved to report.txt"
