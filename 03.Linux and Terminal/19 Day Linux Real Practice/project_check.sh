#!/bin/bash

PROJECT_DIR="/mnt/c/Users/sai charan/OneDrive/Desktop/MLops Learning Grind"


echo "---------------------------------"
echo "  Mlops project structure check  "
echo "---------------------------------"
echo ""


FOLDERS=(
	"01.Python For Production"
	"02.Git and GitHub"
	"03.Linux and Terminal"
)


echo "checking folders..."
for folder in "${FOLDERS[@]}"
do 
	if [  -d "$PROJECT_DIR/$folder" ]; then 
		echo "   FOUND: $folder"
	else
		echo "   MISSING : $folder"
	fi
done

echo ""


TOTAL_DAYS=$(ls "$PROJECT_DIR/01.Python For Production" | wc -l)
echo "Total day folders in topic 01 : $TOTAL_DAYS"
echo ""
echo "check complete !"

