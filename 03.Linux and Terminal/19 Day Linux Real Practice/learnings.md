# Day 19 — Linux Real Practice

Second to last Linux day. Today moved from isolated command practice into writing scripts that actually do something useful — checking a real project structure, manipulating strings, taking user input, polling for files, and checking the environment. Also hit two interesting bugs worth documenting.

---

## Exercise 1 — Project Structure Checker

```bash
#!/bin/bash

PROJECT_DIR="/mnt/c/Users/sai charan/OneDrive/Desktop/MLops Learning Grind"

echo "---------------------------------"
echo "  Mlops project structure check"
echo "---------------------------------"

FOLDERS=(
    "01.Python For Production"
    "02.Git and GitHub"
    "03.Linux and Terminal"
)

echo "checking folders..."
for folder in "${FOLDERS[@]}"
do
    if [ -d "$PROJECT_DIR/$folder" ]; then
        echo "   FOUND: $folder"
    else
        echo "   MISSING: $folder"
    fi
done

TOTAL_DAYS=$(ls "$PROJECT_DIR/01.Python For Production" | wc -l)
echo "Total day folders in topic 01 : $TOTAL_DAYS"

echo "check complete !"
```

Output —
```
FOUND: 01.Python For Production
FOUND: 02.Git and GitHub
FOUND: 03.Linux and Terminal
Total day folders in topic 01: 12
```

`[ -d "$folder" ]` checks if a directory exists — same as `[ -f ]` from earlier but `d` for directory instead of `f` for file. The `$(ls ... | wc -l)` counts how many items are inside a folder — command substitution feeding into wc -l.

This ran clean with no issues first try.

---

## Exercise 2 — String Operations

Typo in the filename — saved as `string.sh` instead of `strings.sh`. Hit the same pattern as always —

```bash
chmod +x strings.sh
# cannot access 'strings.sh': No such file or directory
chmod +x string.sh   # fixed
./string.sh
```

```bash
MODEL="iris-classifier-v1.0"

echo "Length: ${#MODEL}"            # 20
echo "Uppercase: ${MODEL^^}"        # IRIS-CLASSIFIER-V1.0
echo "Lowercase: ${MODEL,,}"        # iris-classifier-v1.0
echo "Replace: ${MODEL/iris/flower}" # flower-classifier-v1.0
echo "First 4 chars: ${MODEL:0:4}"  # iris
```

Output —
```
length : 20
Uppercase : IRIS-CLASSIFIER-V1.0
lowercase : iris-classifier-v1.0
replace : flower-classifier-v1.0
first 4 chars : iris
model name contains 'iris'
model name starts with 'iris'
```

All string operations worked correctly. `${MODEL^^}` for uppercase and `${MODEL,,}` for lowercase are bash-specific — they don't exist in all shells. `${MODEL:0:4}` is substring extraction — start at index 0, take 4 characters.

`[[ "$MODEL" == *"iris"* ]]` — the double brackets `[[ ]]` are needed for pattern matching. Single brackets `[ ]` don't support the `*` wildcard for string matching. This is a subtle but important difference in bash.

---

## Exercise 3 — User Input

```bash
read -p "enter model name :" MODEL_NAME
read -p "enter version name :" VERSION
read -p "enter features (space separated) :" FEATURES
```

Ran it with test values — typed "sai" for the model, "v.01" for version, "nah" for features. Everything captured correctly and echoed back.

```
running model : sai
version : v.01
features : nah
Confirm ? (y/n) : y
running prediction...
done
```

`read -p "prompt" VARIABLE` shows the prompt text and waits for input. The `-p` flag keeps the prompt on the same line as the cursor. Without `-p` you'd need a separate `echo` to show the prompt and then a plain `read` on the next line.

`[[ "$CONFIRM" == "y" || "$CONFIRM" == "Y" ]]` handles both lowercase and uppercase y — real scripts need to handle both or users will get confused when nothing happens after typing "Y".

---

## Exercise 4 — While Loop with Timeout

```bash
while [ ! -f "ready_model.pkl" ]
do
    COUNT=$((COUNT + 1))
    echo "  attempt $COUNT - model not ready yet,..."
    sleep 1

    if [ $COUNT -ge $MAX_TRIES ]; then
        echo "timeout - model never appeared after $MAX_TRIES attempts"
        exit 1
    fi
done
```

First run — no file existed, looped 5 times with 1 second between each, then exited with timeout message.

```
attempt 1 - model not ready yet,...
attempt 2 - model not ready yet,...
attempt 3 - model not ready yet,...
attempt 4 - model not ready yet,...
attempt 5 - model not ready yet,...
timeout - model never appeared after 5 attempts
```

Created the file and ran again —

```bash
touch ready_model.pkl
./while_loop.sh
# waiting for model file
# model is ready
```

Immediately found the file and skipped the loop entirely. This is a real production pattern — health check loops that poll until a service or file becomes available, with a hard timeout so they don't spin forever if something is genuinely broken.

---

## Exercise 5 — mlops_helper.sh (the bug)

This one had an interesting bug —

```
./mlops_helper.sh: line 10: local: `=INFO': not a valid identifier
2026-06-18 20:33:39 [%level] python found: Python 3.14.4
```

Two problems visible in the output —

**Bug 1 — `local: '=INFO': not a valid identifier`**

The `log` function had this line —

```bash
local level=${2:-INFO}
```

This uses bash's default value syntax — if `$2` is not passed, use `INFO`. The error suggests there was a smart quote or non-standard character somewhere in the line, possibly pasted in from somewhere that converted the `-` or `{` into a different character. The fix is to retype that line manually in nano rather than copying it.

**Bug 2 — `[%level]` instead of `[$level]`**

The echo line inside the function was probably written as —

```bash
echo "$(date '+%Y-%m-%d %H:%M:%S') [%level] $message"
```

`%level` is not a variable — it's a literal string. Should be `$level` with a dollar sign. The `%` looks similar to `$` at a glance, especially when you're typing fast.

Despite both bugs the script still ran and produced useful output —

```
2026-06-18 20:33:39 [%level] python found: Python 3.14.4
2026-06-18 20:33:39 [%level] git found: git version 2.53.0
2026-06-18 20:33:39 [%level] Disk usage: 1%
```

Python 3.14.4 and git 2.53.0 were both detected correctly. Disk usage at 1% — WSL2 environment has plenty of space. The `tee -a` command correctly sent output to both terminal and `helper.log` at the same time.

---

## Copying Files

The `ls` mistake —

```bash
ls "cp ~/day19_practice/*.sh ..."
# No such file or directory
```

Accidentally passed the whole copy command as an argument to `ls` — copy command was still inside the quotes. Ran the actual `cp` first, then ran `ls` separately to verify. Both the copy and the verification worked when run correctly.

---

## What to Remember

| Concept | What it means |
|---|---|
| `[ -d "$folder" ]` | check if directory exists |
| `${#STRING}` | string length |
| `${STRING^^}` | convert to uppercase |
| `${STRING,,}` | convert to lowercase |
| `${STRING/old/new}` | replace first match |
| `${STRING:0:4}` | substring from index 0, length 4 |
| `[[ "$VAR" == *"word"* ]]` | check if string contains word |
| `read -p "prompt" VAR` | get user input with prompt |
| `while [ ! -f "file" ]` | loop while file does not exist |
| `sleep 1` | pause for 1 second |
| `$((COUNT + 1))` | arithmetic in bash |
| `${2:-INFO}` | use $2 if set, otherwise default to INFO |
| `tee -a file` | print to terminal AND append to file |
| `command -v python3` | check if a command is installed |

---

*Day 19 done. One more Linux day tomorrow then HTTP and APIs start.*