# Day 20 — Linux Final Review and Wrap Up

Last day of the Linux week. Started by fixing yesterday's `mlops_helper.sh` bugs, then wrote one big review script that touches almost every command from the past 6 days. This script ended up having its own set of bugs — which honestly made it a better learning exercise than if it had worked first try.

---

## Part 1 — Fixing mlops_helper.sh

Went back to yesterday's broken `log` function and fixed the two issues —

```bash
# was broken — typo or hidden character issue
local level=${2:-INFO}

# retyped manually instead of pasting, fixed it clean
```

```bash
# was using a literal % instead of $
echo "$(date '+%Y-%m-%d %H:%M:%S') [%level] $message"

# fixed to actually reference the variable
echo "$(date '+%Y-%m-%d %H:%M:%S') [$level] $message"
```

Lesson from this — when copy-pasted code throws a weird "not a valid identifier" error that looks like it shouldn't be an error at all, retype the line by hand instead of debugging the paste. Hidden characters from copying across different sources are a real and annoying thing.

---

## Part 2 — final_review.sh — The Big One

This script was meant to combine functions, variables, arrays, loops, grep, environment variables, and user input into one piece. First run failed hard —

```
./final_review.sh: line 9: data: command not found
 - Creating sample data...
./final_review.sh: line 16: $DATA_FILE: ambiguous redirect
./final_review.sh: line 17: $DATA_FILE: ambiguous redirect
...
--- full data ---
^C
```

Four separate bugs, found by reading through the script line by line.

### Bug 1 — Missing variable definitions (the root cause of everything)

`$LOG_FILE` and `$DATA_FILE` were used all over the script but never actually defined anywhere. Missing these two lines near the top —

```bash
LOG_FILE="review.log"
DATA_FILE="sample_data.txt"
```

This single omission caused two different failures —

- `ambiguous redirect` on every `echo ... >> $DATA_FILE` line, because redirecting to an empty variable breaks bash
- the script hanging at `cat $DATA_FILE`, because with the variable empty that line became just `cat` with no file — and `cat` with no file argument waits on stdin forever, exactly like the grep hangs from earlier in the week

Same root pattern as Day 17 and Day 18 — an undefined or empty variable feeding into a command that reads from a file turns into a command that reads from the keyboard instead, and just sits there.

### Bug 2 — `data` instead of `date`

```bash
# wrong
echo "$(data '+%H:%M:%S') - $message"

# correct
echo "$(date '+%H:%M:%S') - $message"
```

One missing letter, command substitution tries to run a nonexistent command called `data`, which is exactly what `data: command not found` was reporting.

### Bug 3 — Array name mismatch

```bash
# defined as MODEL (singular)
MODEL=("iris-classifiers" "spam-detector" "price-predictor" "fraud-detector")

# but looped over MODELS (plural)
for model in "${MODELS[@]}"
```

The array was named `MODEL` but the loop referenced `MODELS`. Since `MODELS` was never actually defined, the loop had nothing to iterate over. Fixed by making both names match —

```bash
MODELS=("iris-classifier" "spam-detector" "price-predictor" "fraud-detector")
```

Also fixed `"iris-classifiers"` to `"iris-classifier"` so it would actually match the real entry in the data file.

### Bug 4 — `the` instead of `then`

```bash
# wrong
if [[ "$CONFIRM" == "y" || "$CONFIRM" == "Y" ]]; the

# correct
if [[ "$CONFIRM" == "y" || "$CONFIRM" == "Y" ]]; then
```

Missing one letter on `then` breaks the whole if statement syntax.

---

## Testing Variables Outside the Script

After fixing everything inside the script, tried testing one line directly in the terminal —

```bash
grep -E "0\.9[0-9]" $DATA_FILE
# no output, no error
```

This didn't work because `$DATA_FILE` was only ever defined **inside** `final_review.sh`. Once that script finishes running, any variables it set disappear — they never existed in the actual terminal session to begin with. Each script runs in its own subshell unless you explicitly source it.

Fixed by either typing the real filename directly —

```bash
grep -E "0\.9[0-9]" sample_data.txt
```

or defining the variable in the terminal itself first —

```bash
DATA_FILE="sample_data.txt"
grep -E "0\.9[0-9]" $DATA_FILE
```

This was a genuinely useful realization — variables are scoped to where they're defined, and a script's internal state doesn't leak out into your shell once it finishes.

---

## What the Script Does Once Fixed

- `log()` function timestamps every message and writes it to both terminal and `review.log` using `tee -a`
- Creates `sample_data.txt` with model names and accuracy scores
- `grep -E "0\.9[0-9]"` filters for any accuracy between 0.90 and 0.99
- Loops through an array of model names and checks each one exists in the data using `grep -q`
- Prints environment info — `$USER`, `$HOME`, current directory
- Ends with a `read -p` prompt asking whether to delete the data file, respecting both `y` and `Y`

Chose `n` at the cleanup prompt to keep the data file around for review.

---

## What to Remember

| Concept | What it means |
|---|---|
| Undefined variable in redirect | causes "ambiguous redirect" error |
| Command with empty file argument | hangs waiting on stdin, looks frozen |
| Variables set inside a script | don't exist in the terminal after the script ends |
| Array name must match exactly | between definition and the loop using it |
| Copy-pasted code with weird errors | retype manually, hidden characters are real |
| `grep -E "0\.9[0-9]"` | extended regex, matches 0.90 through 0.99 |
| `tee -a file` | output to terminal and file at the same time |

---

## Linux Week — Looking Back

Six days, same handful of bug patterns kept showing up — typos in filenames, undefined variables feeding into commands that then hang waiting on stdin, missing spaces around brackets, and variable name mismatches between definition and use. By Day 20 these stopped being mysterious — seeing "ambiguous redirect" or a frozen terminal now immediately points to "check if the variable feeding this command is actually defined" rather than feeling like a random failure.

That diagnostic instinct is really the whole point of this week. Linux doesn't stop here — every topic from here on (Docker, MLflow, deployments) runs through this same terminal, and the debugging patterns learned this week carry forward into all of it.

---

*Linux and Terminal topic complete. Next — Topic 04: HTTP and APIs.*