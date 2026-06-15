# Day 16 — Shell Scripting and curl Basics

Shell scripting turns a list of terminal commands into a reusable program. Instead of typing the same 10 commands every time you want to run a pipeline — you put them in a `.sh` file and run it once. curl is how you talk to APIs from the terminal. Both of these show up constantly in real MLOps work.

---

## Exercise 1 — First Shell Script

```bash
#!/bin/bash

echo "starting MLops pipeline.."
echo "step 1 : Loading data"
echo "step 2 : Training model"
echo "step 3 : saving model"
echo "pipeline complete"
```

```bash
chmod +x run_pipeline.sh
./run_pipeline.sh
```

Output —
```
starting MLops pipeline..
step 1 : Loading data
step 2 : Training model
step 3 : saving model
pipeline complete
```

`#!/bin/bash` is called a shebang line. It tells the operating system which interpreter to use for this script. Without it Linux doesn't know what to do with the file.

`chmod +x` adds execute permission. Without it you get Permission denied when trying to run it.

`./` means run this file from the current directory. Linux doesn't look in the current folder by default when running commands — `./` explicitly tells it to.

---

## Exercise 2 — Variables in Scripts

```bash
#!/bin/bash

MODEL_NAME="iris_classifier"
VERSION="1.0"
DATA_PATH="/home/sai_charan/data"

echo "Model : $MODEL_NAME"
echo "Version : $VERSION"
echo "data path : $DATA_PATH"
echo "running $MODEL_NAME version $VERSION"
```

Output —
```
Model : iris_classifier
Version : 1.0
data path : /home/sai_charan/data
running iris_classifier version 1.0
```

Variables in bash have no spaces around `=`. `MODEL_NAME="iris"` works. `MODEL_NAME = "iris"` breaks. Read a variable with `$` prefix — `$MODEL_NAME`.

Typo I made — named the file `vraiables.sh` instead of `variables.sh`. Fixed with `mv` —

```bash
mv vraiables.sh variables.sh
```

---

## Exercise 3 — if/else in Scripts

```bash
#!/bin/bash

MODEL_FILE="iris_model.pkl"

if [ -f "$MODEL_FILE" ]; then
    echo "model file found : $MODEL_FILE"
else
    echo "model file not found : $MODEL_FILE"
    echo "please train the model first"
fi
```

First run — model file didn't exist —
```
model file not found : iris_model.pkl
please train the model first
```

Created the file and ran again —
```bash
touch iris_model.pkl
./check_model.sh
# model file found : iris_model.pkl
```

`[ -f "$FILE" ]` checks if a file exists. `-f` means regular file. The spaces inside `[ ]` are required — `[-f "$FILE"]` breaks. `fi` closes the if block (it's `if` backwards).

---

## Exercise 4 — Loops in Scripts

```bash
#!/bin/bash

echo "Training runs :"
for i in 1 2 3 4 5
do
    echo "  run $i complete"
done

echo ""
echo "files in current folder:"
for file in *
do
    echo "  $file"
done
```

Output —
```
Training runs :
  run 1 complete
  run 2 complete
  run 3 complete
  run 4 complete
  run 5 complete

files in current folder:
  check_model.sh
  iris_model.pkl
  loop_practice.sh
  run_pipeline.sh
  variables.sh
```

`for file in *` — the `*` expands to every file in the current folder. The loop runs once for each file. `done` closes the loop.

---

## Exercise 5 — Real Pipeline Script

```bash
#!/bin/bash

echo "----****----"
echo "iris mlops pipeline"
echo "----****----"

MODEL_PATH="iris_model.pkl"

if [ -f "$MODEL_PATH" ]; then
    echo "model already exists — skipping training"
else
    echo "model not found - training now"
    echo "training complete"
    touch $MODEL_PATH
fi

LOG_FILE="pipeline.log"
echo "Pipeline ran at : $(date)" >> $LOG_FILE

echo ""
echo "log saved to $LOG_FILE"
cat $LOG_FILE
```

Ran it three times. Each run appended a new timestamp to `pipeline.log` —

```
pipeline ran at : Mon Jun 15 22:35:29 UTC 2026
pipeline ran at : Mon Jun 15 22:35:49 UTC 2026
pipeline ran at : Mon Jun 15 22:35:59 UTC 2026
```

`$(date)` runs the `date` command inside the script and inserts its output inline. This is called command substitution.

Hit one error — `$LOGFILE: ambiguous redirect`. This happened because I wrote `$LOGFILE` without defining it first — the variable was empty so bash didn't know where to redirect. Fixed by using `$LOG_FILE` (with underscore) which was properly defined.

---

## Exercise 6 — curl Basics

### GET request

```bash
curl https://httpbin.org/get
```

Returns JSON showing your request headers, IP, and URL. `httpbin.org` is a test API that echoes back whatever you send — perfect for learning curl.

### Check status code only

```bash
curl -o /dev/null -s -w "%{http_code}\n" https://httpbin.org/get
# 200
```

`-o /dev/null` throws away the response body. `-s` silent mode, no progress bar. `-w` prints a custom string after — `%{http_code}` is replaced with the actual HTTP status code. Got `200` — success.

### POST request

```bash
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"model": "iris", "features": [5.1, 3.5, 1.4, 0.2]}'
```

Hit an error first time — wrote `"content - type : application/json"` with spaces around the colon. HTTP headers have strict format — `Content-Type: application/json` no spaces. Got `Bad Request` back from the server.

### Save response to file

```bash
curl https://httpbin.org/get -o response.json
cat response.json
```

`-o response.json` saves the response body to a file instead of printing it.

### Verbose mode

```bash
curl -v https://httpbin.org/get
```

Shows everything — TLS handshake, request headers (lines with `>`), response headers (lines with `<`), then the body. Useful for debugging API issues.

### coindesk API

```bash
curl "https://api.coindesk.com/v1/bpi/currentprice.json"
# curl: (6) Could not resolve host: api.coindesk.com
```

This API is down or removed. Not a curl issue — the host simply doesn't resolve anymore.

---

## Errors I Hit Today

| Error | Cause | Fix |
|---|---|---|
| `chmod: cannot access 'variables.sh'` | typo in filename — `vraiables.sh` | `mv vraiables.sh variables.sh` |
| `Protocol "htttps" not supported` | three t's in https | fixed typo |
| `command 'corl' not found` | typed `corl` instead of `curl` | fixed typo |
| `Invalid HTTP header name` | spaces in Content-Type header | removed spaces |
| `$LOGFILE: ambiguous redirect` | variable not defined | used correct variable name `$LOG_FILE` |
| `Could not resolve host: api.coindesk.com` | API is offline | not a user error |

---

## What to Remember

| Concept | What it means |
|---|---|
| `#!/bin/bash` | shebang — tells OS to use bash |
| `chmod +x script.sh` | make script executable |
| `./script.sh` | run script from current folder |
| `VAR="value"` | set variable, no spaces around = |
| `$VAR` | read variable |
| `[ -f "$FILE" ]` | check if file exists |
| `for i in ... do ... done` | loop |
| `$(command)` | command substitution |
| `curl URL` | GET request |
| `curl -X POST` | POST request |
| `curl -H "Header: value"` | add header |
| `curl -d '{"key": "val"}'` | add request body |
| `curl -o file.json` | save response to file |
| `curl -v` | verbose, see all headers |

---

## Why This Matters in MLOps

Shell scripts automate repetitive tasks — training runs, data checks, deployment steps. Every CI/CD pipeline (GitHub Actions) is basically shell scripts running automatically. curl is how you test your FastAPI endpoints from the terminal before writing any Python client code. These two skills are used daily in production MLOps work.

---

*Day 16 done. 1 week Linux grind continues. Mastering this properly.*