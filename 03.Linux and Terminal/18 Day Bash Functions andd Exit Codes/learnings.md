# Day 18 — Bash Functions, Exit Codes, and Arrays

Started today by going back and fixing yesterday's hang in `analyze_logs.sh`. Found two separate bugs — an `echo` where a `grep` should have been, and a typo'd variable name `$LOF_FILE` instead of `$LOG_FILE` that left grep waiting on empty input forever. Fixed both, then moved on to new material — functions, exit codes, and arrays in bash.

---

## Fixing Yesterday's Bug First

Two real bugs found in `analyze_logs.sh` —

```bash
# bug 1 — this was just echoing text, not searching the file
echo "ERROR" $LOG_FILE

# fixed to
grep "ERROR" $LOG_FILE
```

```bash
# bug 2 — typo'd variable name, this is what caused the hang
grep "setosa" $LOF_FILE

# fixed to
grep "setosa" $LOG_FILE
```

`$LOF_FILE` was never defined anywhere in the script, so it expanded to nothing. `grep "setosa"` with no file argument doesn't error — it just sits there waiting for keyboard input, which is exactly why the script froze and needed `Ctrl+C` yesterday. Good reminder that a frozen terminal with no error message usually means something is waiting on stdin, not actually broken.

---

## Exercise 1 — Functions

```bash
#!/bin/bash

greet() {
    echo "Hello, $1!"
}

validate_features() {
    local count=$1
    if [ "$count" -eq 4 ]; then
        echo "Valid: $count features"
    else
        echo "Invalid: expected 4, got $count"
    fi
}

greet "Sai Charan"
validate_features 4
validate_features 2
```

Output —
```
hello, sai charan!
valid: 4 features
Invalid: expected 4, got 2
```

A function in bash is just a named block of commands you can call later. `$1` inside the function is whatever value you passed when calling it — `greet "Sai Charan"` makes `$1` equal to `"Sai Charan"` inside that function.

`local count=$1` keeps `count` scoped to just this function. Without `local` the variable would leak into the rest of the script, which can cause subtle bugs in longer scripts.

This ran clean on the first try, no issues.

---

## Exercise 2 — Exit Codes

```bash
#!/bin/bash

echo "Running a command that succeeds..."
ls ~ > /dev/null
echo "Exit code: $?"

echo ""
echo "Running a command that fails..."
ls /this/does/not/exist > /dev/null 2>&1
echo "Exit code: $?"

echo ""
echo "Custom exit code from a function..."
check_model() {
    if [ -f "iris_model.pkl" ]; then
        return 0
    else
        return 1
    fi
}

check_model
if [ $? -eq 0 ]; then
    echo "Model check passed"
else
    echo "Model check failed"
fi
```

Output —
```
running a command that succeeds...
exit code: 0
running a command that fails
exit code: 2
custom exit code from a function
model check failed
```

`$?` always holds the exit code of whatever ran right before it. `0` means success. The failing `ls` command returned `2` — Linux uses different non-zero numbers for different kinds of failures, but the only thing that really matters in scripting is whether it's `0` or not-`0`.

`check_model` returned `1` because `iris_model.pkl` didn't exist yet at that point, so the script correctly printed "Model check failed."

---

## Exercise 3 — Arrays

First attempt hit a syntax error —

```bash
MODELS = ("iris-classifier" "spam-detector" "price-predictor")
```

```
syntax error near unexpected token `('
```

Spaces around the `=` sign broke it. In bash, variable assignment cannot have spaces on either side — `VAR=value` works, `VAR = value` does not. Fixed it —

```bash
MODELS=("iris-classifier" "spam-detector" "price-predictor")
```

After the fix —

```bash
#!/bin/bash

MODELS=("iris-classifier" "spam-detector" "price-predictor")

echo "all models:"
for model in "${MODELS[@]}"
do
    echo "  - $model"
done

echo ""
echo "First model : ${MODELS[0]}"
echo "total models : ${#MODELS[@]}"

MODELS+=("fraud-detector")
echo ""
echo "after adding one:"
for model in "${MODELS[@]}"
do
    echo "  - $model"
done
```

Output —
```
all models:
  - iris-classifier
  - spam-detector
  - price-predictor
First model : iris-classifier
total models : 3
after adding one:
  - iris-classifier
  - spam-detector
  - price-predictor
  - fraud-detector
```

`${MODELS[@]}` expands to every item in the array. `${MODELS[0]}` accesses just the first item — arrays are zero-indexed. `${#MODELS[@]}` gives the count. `+=` appends a new item without rebuilding the whole array.

---

## Exercise 4 — model_checker.sh

This combined everything — functions, exit codes, arrays — into one realistic pre-deployment check script.

First run hit a bug —

```
total missing: 3
./model_checker.sh: line 33: [3: command not found
cannot diploy missing models
```

The line was something like —

```bash
if [$MISSING_COUNT -eq 0]; then
```

Missing the space right after `[`. In bash, `[` is actually a command on its own — it needs a space after it and before the closing `]`. Without that space, `[$MISSING_COUNT` becomes one single word. Since `MISSING_COUNT` was `3`, bash tried to run a command literally named `[3`, which doesn't exist — hence `[3: command not found`.

Because that broken command failed, the `if` treated it as false and dropped into the `else` branch, which printed the deploy-blocked message and (presumably) exited with `1`.

Correct syntax needs spaces on both sides —

```bash
if [ $MISSING_COUNT -eq 0 ]; then
```

Second run after creating `iris_model.pkl` —

```
checking required model files ...
  FOUND: iris_model.pkl
  MISSING: spam_model.pkl
  MISSING: price_model.pkl
total missing: 2
./model_checker.sh: line 33: [2: command not found
cannot diploy missing models
```

Same bug, same pattern — `[2` instead of a properly spaced `[ $MISSING_COUNT -eq 0 ]`. The number inside the broken command literally matches whatever `MISSING_COUNT` was at the time, which is a good way to confirm exactly what's going wrong when you see this kind of error.

---

## Checking Exit Code — The Mistake That Taught the Most

Tried to check the script's exit code —

```bash
echo "script exit code: $2"
# script exit code:
```

`$2` is not the exit code — it's the second positional argument passed to the current shell, which was empty. Wrong variable entirely.

Fixed to —

```bash
echo "script exit code: $?"
# script exit code: 0
```

But this `0` is misleading. By the time this command ran, the previous command was the broken `echo "script exit code: $2"` line — which itself succeeded as a plain echo. So `$?` was reporting the exit code of that echo, not of `model_checker.sh`. The real exit code of `model_checker.sh` was already lost by the time I checked.

**The actual lesson** — `$?` only reflects the command immediately before it. If you run anything else in between — even a harmless `echo` — you lose the exit code you wanted to check. To check a script's real exit code you have to read `$?` right after running it, with nothing in between.

```bash
./model_checker.sh
echo "exit code was: $?"   # correct — nothing ran in between
```

---

## What to Remember

| Concept | What it means |
|---|---|
| `function_name() { }` | defines a reusable block of commands |
| `$1` | first argument passed into a function or script |
| `local var` | keeps a variable scoped inside the function only |
| `return 0 / return 1` | function-level success/failure signal |
| `$?` | exit code of the command immediately before it — check right away |
| `VAR=(a b c)` | array definition, no spaces around `=` |
| `${ARRAY[@]}` | all elements |
| `${ARRAY[0]}` | first element, zero-indexed |
| `${#ARRAY[@]}` | array length |
| `[ condition ]` | needs spaces after `[` and before `]`, or bash tries to run it as a command |

---

## Why This Matters in MLOps

This is exactly the shape of a real CI/CD step — check if required files exist, count what's missing, exit with a non-zero code if something's wrong. GitHub Actions and any deployment pipeline reads that exit code to decide whether to continue or stop. A script that silently swallows its real exit code, like what happened here, can let a broken deployment slip through unnoticed. Catching this kind of mistake on a toy script now is a lot cheaper than catching it in a real pipeline later.

---

*Day 18 done. Two more Linux days planned before HTTP and APIs.*