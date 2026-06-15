# Day 15 — Linux and Terminal Basics

Big day. Set up WSL2 (Ubuntu on Windows) and ran through 8 exercises covering navigation, file operations, searching, piping, environment variables, permissions, and processes. This is the foundation for everything that comes next — Docker, MLflow, deployments all assume you're comfortable in a Linux terminal.

---

## WSL2 Setup

WSL2 is Ubuntu running inside Windows as an app. Your Windows files stay exactly as they are. Ubuntu runs in a separate terminal window. Nothing breaks, nothing gets replaced.

```powershell
wsl --install
```

After installation and restart, Ubuntu launched and asked for a username and password. Set those up. Ubuntu home directory is at `/home/sai_charan`.

### The mlops alias

Typing the full Windows path every time inside Ubuntu is painful —

```bash
cd /mnt/c/Users/sai\ charan/OneDrive/Desktop/MLops\ Learning\ Grind
```

Added a shortcut to `~/.bashrc` —

```bash
echo "alias mlops='cd /mnt/c/Users/sai\ charan/OneDrive/Desktop/MLops\ Learning\ Grind'" >> ~/.bashrc
source ~/.bashrc
```

Now just type `mlops` from anywhere and it jumps straight to the project folder.

---

## Exercise 1 — Navigation

```bash
pwd          # /home/sai_charan — shows current location
cd ~         # go to home directory
ls           # list files
ls -la       # list with permissions, size, date, hidden files
cd ..        # go up one level
cd -         # go back to previous folder
```

`ls -la` output showed something interesting — files starting with `.` like `.bashrc` and `.profile`. These are hidden config files. Linux hides them by default, `-a` flag reveals them.

`cd -` is a shortcut that toggles between current and previous folder. Useful when jumping between two locations repeatedly.

---

## Exercise 2 — Files and Folders

```bash
mkdir mlops_practice        # create folder
touch file1.txt file2.txt   # create empty files
echo "hello from linux" > file1.txt   # write to file
cat file1.txt               # read file
echo "second line" >> file1.txt       # append to file
cp file1.txt file1_backup.txt         # copy
mv file2.txt file2_renamed.txt        # rename
rm file3.txt                # delete file
rm -rf mlops_practice       # delete folder and everything inside
```

Key difference —
- `>` overwrites the file completely
- `>>` adds to the end without touching what's already there

`rm -rf` is permanent — no recycle bin in Linux. Once it's gone it's gone.

---

## Exercise 3 — Reading Files

```bash
cat data.txt       # read entire file
head -3 data.txt   # first 3 lines only
tail -2 data.txt   # last 2 lines only
less data.txt      # page by page, press q to quit
wc -l data.txt     # count lines → 5
wc -w data.txt     # count words → 10
```

Typo I made — typed `wc -1` (number one) instead of `wc -l` (letter l). They look identical in terminal font. Got an error both times before catching it.

`less` is useful for large files — opens them in a pager so you don't flood the terminal with thousands of lines.

---

## Exercise 4 — Searching

```bash
grep "line 3" data.txt        # find exact match
grep -i "LINE" data.txt       # case insensitive — found all 5 lines
grep -n "line" data.txt       # show line numbers with matches
find ~ -name "data.txt"       # find file by exact name
find ~ -name "*.txt"          # find all txt files
```

`grep -i` ignores case — searching for `LINE` found `line 1` through `line 5`. Useful when you don't know the exact casing.

`grep -n` shows the line number before each match — `1:line 1`, `2:line 2` etc. Makes it easy to jump to the right line in a file.

---

## Exercise 5 — Piping and Redirection

```bash
ls -la | grep "data"      # filter ls output for "data"
ls | wc -l               # count files in folder
ls -la > filelist.txt    # save ls output to file
echo "append line" >> filelist.txt   # append to that file
cat filelist.txt         # read it back
ls -la | less            # pipe ls into pager
```

The pipe `|` sends the output of one command as input to the next. `ls -la | grep "data"` runs `ls -la` then filters the output to only show lines containing "data".

`>` creates or overwrites a file with the output. `>>` adds to the end. Both redirect output from the terminal into a file.

---

## Exercise 6 — Environment Variables

```bash
env                         # see all environment variables
echo $HOME                  # /home/sai_charan
echo $USER                  # sai_charan
echo $PATH                  # all the places Linux looks for commands
export MY_MODEL="iris-classifier"
echo $MY_MODEL              # iris-classifier
echo "Running model: $MY_MODEL"   # Running model: iris-classifier
env | grep MY_MODEL         # MY_MODEL=iris-classifier
```

`export` creates an environment variable for the current session. Variables start with `$` when reading them. `MY_MODEL` without `$` is just the string "MY_MODEL" — `$MY_MODEL` is the value stored in it.

`$PATH` is the list of folders Linux searches when you type a command. That's why `python` works from anywhere — its folder is in `$PATH`.

---

## Exercise 7 — Permissions

```bash
ls -la           # showed permissions like -rw-r--r--
echo 'echo "hello from script"' > hello.sh
./hello.sh       # Permission denied
chmod +x hello.sh
./hello.sh       # hello from script
ls -la hello.sh  # -rwxr-xr-x
```

Linux files have three permission sets — owner, group, everyone else. Each set has read (r), write (w), execute (x).

`-rw-r--r--` means owner can read+write, everyone else can only read. No one can execute.

`chmod +x` adds execute permission. After that `./hello.sh` ran the script successfully. The permissions changed from `-rw-r--r--` to `-rwxr-xr-x`.

---

## Exercise 8 — Process Management

```bash
ps aux                    # see all running processes
top                       # live process monitor, q to quit
sleep 30 &               # run sleep in background
ps aux | grep sleep      # see it running — PID 2598
kill $(pgrep sleep)      # kill it by name
ps aux | grep sleep      # confirmed terminated
```

`&` at the end runs a command in the background so the terminal stays usable.

`pgrep sleep` finds the PID (process ID) of any process named sleep. `kill` sends a termination signal to that PID. `$(...)` runs the inner command and passes its output to the outer command.

After killing — the next `ps aux | grep sleep` only showed the `grep` command itself, not the sleep process. Confirmed dead.

---

## What to Remember

| Command | What it does |
|---|---|
| `pwd` | show current directory |
| `ls -la` | list all files with details |
| `cd ~` | go home |
| `cd -` | go to previous folder |
| `touch` | create empty file |
| `cat` | read file |
| `head -n / tail -n` | first or last n lines |
| `grep -i -n` | search case insensitive with line numbers |
| `find ~ -name` | find file by name |
| `\|` pipe | chain commands together |
| `> / >>` | overwrite or append to file |
| `export VAR=value` | set environment variable |
| `chmod +x` | make file executable |
| `ps aux` | see all processes |
| `kill $(pgrep name)` | kill process by name |

---

## Why This Matters in MLOps

Docker containers run Linux. Servers run Linux. MLflow, FastAPI, everything in production runs on Linux. Being comfortable in a terminal means you can debug a crashed container, check logs, kill a stuck process, set environment variables for a deployment — all without needing a GUI. This day was the foundation for all of that.

---

*Day 15 done. Tomorrow — more Linux, shell scripting and curl basics.*