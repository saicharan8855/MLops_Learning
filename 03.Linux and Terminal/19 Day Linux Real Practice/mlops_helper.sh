#!/bin/bash

# script for MLOps helper


LOG_FILE="helper.log"

log() {
	local message=$1
	local level =${2:-INFO}
	echo "$(date '+%Y-%m-%d %H:%M:%S') [%level] $message" | tee -a $LOG_FILE
}


check_python() {
	if command -v python3 &> /dev/null; then
		VERSION=$(python3 --version)
		log "python found: $VERSION"
		return 0
	else
		log "python not found" "ERROR"
		return 1
	fi
}

check_git() {
	if command -v git &> /dev/null; then
		VERSION=$(git --version)
		log "git found: $VERSION"
		return 0
	else
		log "git not found" "ERROR"
		return 1
	fi
}


check_disk() {
	USAGE=$(df -h / | awk 'NR==2 {print $5}')
	log "Disk usage: $USAGE"
}


echo "running MLOps environment check ..."
echo ""


check_python
check_git
check_disk


echo ""
echo "log saved to $LOG_FILE"
cat $LOG_FILE






