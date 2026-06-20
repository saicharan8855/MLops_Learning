# 03. Linux and Terminal - Summary

## Days Covered

| Day | Topic |
|---|---|
| 15 | Navigation, files, search, pipes, environment variables, permissions, processes |
| 16 | Shell scripting basics and `curl` |
| 17 | Practice project: log analyzer |
| 18 | Bash functions, exit codes, arrays |
| 19 | Real projects: project checker, strings, user input, while loops |
| 20 | Final review and wrap-up |

## Key Commands Mastered

- Navigation: `pwd`, `cd`, `ls`
- Files: `touch`, `cat`, `cp`, `mv`, `rm`, `mkdir`
- Reading: `head`, `tail`, `less`, `wc`
- Searching: `grep`, `grep -E`, `find`
- Piping and redirection: `|`, `>`, `>>`
- Scripting: functions, `if/else`, `for`, `while`, arrays
- Environment: `export`, `$VAR`, `$?`
- Permissions: `chmod +x`

## Biggest Lessons

- A frozen terminal usually means a command is waiting on standard input.
- `grep` needs a file argument or another input source, otherwise it can appear to hang.
- Bash test brackets like `[ ]` need spaces around them or the command breaks.
- `$?` only reflects the exit status of the command that ran immediately before it.
- Always quote variables in conditions to avoid unexpected errors.

## What's Next

**Topic 04 — HTTP and APIs**