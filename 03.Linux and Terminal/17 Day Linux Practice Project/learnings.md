# Day 17 — Linux Practice Project (Log Analyzer)

Consolidation day. No new commands — just combined everything from Day 15 and Day 16 into one small project. Built a fake log file and wrote scripts to analyze it. Also ran into a real hang that needed `Ctrl+C` to escape, which turned out to be a useful lesson on its own.

---

## Setup

```bash
mkdir linux_project
cd linnux_project       # typo — missing folder
cd linux_project        # fixed
```

Small typo at the start, nothing major. `cd` into a folder that doesn't exist just throws "No such file or directory" — easy to spot and fix.

---

## Step 1 — generate_logs.sh

```bash
chmod +x generate_logs.sh
./generate_logs.sh
# log file generated: app.log
```

This script wrote 10 fake log lines into `app.log`, mixing log levels — INFO, DEBUG, WARNING, ERROR, CRITICAL — to simulate what a real running application's log file looks like.

```bash
cat app.log
```

```
2026-06-17 10:00:01 INFO model loaded successfully
2026-06-17 10:00:05 INFO prediction request received
2026-06-17 10:00:06 DEBUG features validated
2026-06-17 10:00:07 INFO prediction complete: setosa
2026-06-17 10:01:15 ERROR invalid feature count
2026-06-17 10:02:30 WARNING low confidence score
2026-06-17 10:03:00 INFO prediction complete: versicolor
2026-06-17 10:04:45 ERROR model file not found
2026-06-17 10:05:10 INFO prediction complete: virginica
2026-06-17 10:06:00 CRITICAL system out of memory
```

This worked first try, no issues.

---

## Step 2 — analyze_logs.sh

First attempt had a typo —

```bash
./analyse_logs.sh
# No such file or directory
```

Wrote "analyse" instead of "analyze" — British vs American spelling, but the filename was created with American spelling so the British version simply doesn't exist as a file. Fixed by typing the correct name.

```bash
./analyze_logs.sh
```

Most of the script ran fine —

```
Total log lines: 10
--- Error count ---
2
--- WARNING count ---
1
--- CRITICAL entries ---
2026-06-17 10:06:00 CRITICAL system out of memory
```

`grep -c` counted matches correctly — 2 errors, 1 warning. `grep "CRITICAL" app.log` pulled the exact matching line.

Then things got strange. The "All ERROR lines" section showed —

```
--- All ERROR lines ---
ERROR app.log
```

That's not a real log line — it looks like grep printed something unexpected rather than the actual ERROR entries. And then the script hung completely at —

```
--- searching foro specific class: setosa ---
^C
```

Had to press `Ctrl+C` to break out of it.

### Why it hung

This is the most useful debugging lesson from today. When `grep` is run **without a file argument**, it doesn't error out — it waits for input from the keyboard instead, because by default grep reads from stdin when no file is given. The terminal looked "frozen" but it was actually just sitting there waiting for me to type something.

The fix is to always make sure the file argument is actually being passed to grep —

```bash
# this can hang if $LOG_FILE is somehow empty or missing
grep "setosa" $LOG_FILE

# safer — quote the variable so it doesn't break if it's empty
grep "setosa" "$LOG_FILE"
```

If `$LOG_FILE` was unset or empty at that point in the script, `grep "setosa"` effectively became `grep "setosa"` with no file — which waits on stdin forever until you press `Ctrl+C` or type something and hit `Ctrl+D`.

---

## Step 3 — Same Hang While Redirecting

```bash
./analyze_logs.sh > report.txt
^C
```

Redirecting output to a file doesn't fix a hang — the script still pauses at the same broken grep line waiting for keyboard input. Redirection only controls where the output goes once it's produced; it does nothing about a command that's stuck waiting for input.

`cat report.txt` afterward showed the report up to the point where it hung — everything before the broken line saved correctly, nothing after it.

---

## Step 4 — count_levels.sh

```bash
./count_level.sh
# No such file or directory
```

Missing the `s` in "levels" — typo again, same pattern as before.

```bash
./count_levels.sh
log level breakdown:
^C
```

Same hang issue. Printed the header line then froze on the first `grep -c "$level" $LOG_FILE` inside the loop. Same root cause likely — `$LOG_FILE` or `$level` not resolving the way the script expected, leaving grep waiting on stdin again.

---

## The Pattern Across All Three Hangs

Every hang today had the same shape — a `grep` command silently waiting for keyboard input instead of failing loudly. The general lesson:

> If a script looks "frozen" with no error and no output, check whether a command further down is waiting on stdin because it didn't get the argument it expected.

Always double check variable names match exactly between where they're defined and where they're used, and quote variables in grep so an empty value doesn't accidentally turn into "read from keyboard" mode.

---

## What Worked

Despite the hangs, the core exercise still proved the point —

- `app.log` got generated correctly with realistic mixed log levels
- `grep -c` correctly counted ERROR and WARNING occurrences
- `grep "CRITICAL"` pulled the exact critical line out of 10 total lines
- Copying files from Ubuntu into the Windows repo folder worked cleanly

```bash
cp ~/linux_project/*.sh /mnt/c/Users/sai\ charan/OneDrive/Desktop/MLops\ Learning\ Grind/03.Linux\ and\ Terminal/17\ Day\ Linux\ Practice\ Project/
cp ~/linux_project/app.log /mnt/c/Users/sai\ charan/OneDrive/Desktop/MLops\ Learning\ Grind/03.Linux\ and\ Terminal/17\ Day\ Linux\ Practice\ Project/
cp ~/linux_project/report.txt /mnt/c/Users/sai\ charan/OneDrive/Desktop/MLops\ Learning\ Grind/03.Linux\ and\ Terminal/17\ Day\ Linux\ Practice\ Project/
```

---

## What to Remember

| Concept | What it means |
|---|---|
| `grep "text" file` | always pass the file, or grep waits on stdin |
| frozen terminal, no error | check for a command stuck reading from keyboard |
| `Ctrl+C` | force-stop a stuck command and get the prompt back |
| redirecting output (`>`) | doesn't fix a hang, just controls where output lands |
| typo in filename | "No such file or directory" — check spelling first |
| `grep -c` | counts matching lines instead of printing them |

---

## Why This Matters in MLOps

This exact scenario happens in real production debugging — a deployment script or cron job looks "stuck" with no output, and the actual cause is some command quietly waiting on input that will never come. Recognizing that pattern quickly, instead of waiting and wondering, is exactly the kind of practical debugging skill that separates someone comfortable with Linux from someone who panics the first time a terminal goes quiet.

---

*Day 17 done. One more Linux day planned this week before moving to HTTP and APIs.*