# Publishing a chapter

The same steps every time, for every chapter. Bookmark this page and stop
thinking about it.

There are three commands. Two of them a machine can run for you and one of them
needs your eyes. Run all three, then push.

---

## The short version

```
$ cd ~/to-c-or-not-to-c

$ python3 tools/check-book.py                 # 1. the book against itself
$ cd ch0N-whatever/code && make test && cd -   # 2. the code against its output
$ bash tools/verify-on-debian.sh              # 3. the claims a script cannot settle

$ git add .
$ git commit -m "Chapter N: what it does"
$ git push
```

If all three are clean, publish. The rest of this page explains what each one
proves, what it cannot prove, and what to do when one of them complains.

---

## 1. `check-book.py`, the automatic checks

```
$ python3 tools/check-book.py
```

You want the last line to read `All N checks passed.` Anything else means stop.

**What it proves.**

- Every internal link resolves, so no reader hits a 404 mid-chapter.
- Every count the prose claims matches the thing being counted. A heading cannot
  say "two keys" over a list of three.
- Section numbering runs 1..n with no gaps in Parts, Flags, Bugs, and exercises.
- Every code listing printed in a chapter is **byte-identical** to the file
  shipped beside it, so a reader typing from the book and a reader running the
  repository get the same line numbers.
- Every `gdb` breakpoint in every chapter lands on a line that exists and that
  gdb can actually stop on. Not a comment, not a blank line, not a lone brace.
- Every source line echoed in a `gdb` transcript matches the real file.
- No em dashes, and every chapter directory has a README.
- Both test suites pass.

**What it cannot prove.** It knows a breakpoint line is real code. It cannot know
whether it is the line you *meant*. `break 47` and `break 55` are both valid
lines in the same file, and only running gdb tells you which one stops where you
wanted. That is what step 3 is for.

Every one of those checks exists because the thing it checks had already gone
wrong at least once while writing this book. None of them were caught by reading.

---

## 2. `make test`, the code against its expected output

```
$ cd ch02-scrubbing-the-log/code
$ make test
21 passed, 0 failed
```

`check-book.py` runs this for you, so it is not strictly a separate step. Run it
on its own while you are working on a chapter, because it is faster and the
output is easier to read.

**Two kinds of check live in there**, and a chapter should have both.

The ordinary kind compares a program's output against a saved file. That proves
the output has not **changed**.

The other kind states the requirement directly. Chapter 2 has:

```
no address survives redaction
```

which runs the redactor and counts `@` characters. That proves the program still
does its **job**. If someone regenerates an expected file carelessly from a
broken build, the first kind passes and the second still fails.

**When a test fails after a deliberate change**, read the diff before you touch
anything. Then, from the chapter's `code/` directory:

```
$ ./build/redact < ../data/access.log > ../tests/redact-expected.txt
```

Check the new file by hand before you trust it. An expected-output file generated
from a buggy program locks the bug in permanently and is worse than no test.

---

## 3. `verify-on-debian.sh`, the parts only your machine can settle

```
$ bash tools/verify-on-debian.sh
```

This one prints a lot and **requires you to read it**. Nothing fails
automatically, because most of what it checks is a comparison between real output
and what the book claims, and only you can make that comparison.

**What it covers.**

| Section | What to look for |
|---|---|
| 1. Tools installed | Anything saying NOT INSTALLED |
| 2. `man 3 printf` | Should say yes; if not, install `manpages-dev` |
| 3. Chapter 1 gdb session | Compare against "Under the hood: watch the money move" |
| 3b. Chapter 2 gdb session | Compare the line numbers against Bug 3's walkthrough |
| 4. Toolbench gdb sessions | The `sum.c` and `crash.c` transcripts |
| 5. Valgrind | Should run at all |
| 6. clang as a second opinion | Both compilers on the same bug |
| 7. The Makefile tab trap | Should show `missing separator` and a `^I` |
| 8. clang-format agreement | Should say all files match |
| 9. nano toggles | Reference only |

**Why this script exists.** The machine these chapters are written on has gcc,
make, git and man. It does not have gdb, valgrind, clang, clang-format, or nano.
So every `gdb` transcript in the book was written from knowledge rather than
captured from a terminal, and this script is how that gets checked.

That is not a theoretical worry. Running it caught five real errors in Chapter 1:
a wrong line number, an `info locals` that showed two variables out of eight, two
missing `libthread_db` lines, and gcc's curly quotes. Chapter 2 had the same
class of bug in its Bug 3 walkthrough.

**Anything that disagrees with the book is a bug in the book.** Fix the chapter,
not your machine, then re-run `check-book.py` to confirm you did not break a
count while editing.

---

## The per-chapter checklist

When a new chapter arrives, before it goes anywhere:

- [ ] `python3 tools/check-book.py` says all checks passed
- [ ] `cd ch0N-*/code && make test` says 0 failed
- [ ] `bash tools/verify-on-debian.sh` and **read sections 3 onward**
- [ ] Section 8 says every file matches `.clang-format`
- [ ] Click the links at the top and bottom of the new chapter
- [ ] Update the status table in the root `README.md`
- [ ] Commit and push

The status table is the one thing no script checks, because "done" is a judgment
rather than a fact. It lives under **Where this is up to** in the root README.

---

## Getting it onto GitHub

### The first time only

Done once, on this machine, and never again.

```
$ git config --global user.name "Your Name"
$ git config --global user.email "the-address-on-your-github-account"
```

GitHub matches commits to accounts by email. Get it wrong and your commits show
as belonging to nobody.

```
$ ssh-keygen -t ed25519 -C "you@example.com"
$ cat ~/.ssh/id_ed25519.pub
```

Paste that one line into GitHub under **Settings → SSH and GPG keys → New SSH
key**. The file *without* `.pub` is the private half: it never leaves your
machine and never gets pasted anywhere.

```
$ ssh -T git@github.com
Hi dralikma! You've successfully authenticated...
```

Do not skip that test. If it fails, `git push` will fail too with a less helpful
message.

### Every time after

```
$ git status                    # what changed
$ git add .
$ git commit -m "Chapter 2: log redactor, no addresses survive"
$ git push
```

Write real commit messages. "update" and "stuff" are worthless to you in three
weeks.

**At the end of every session, even a bad one.** `git commit -m "ch3 timing
section is not landing, stopping here"` costs eight seconds and means tomorrow's
you can always get back to today's you.

### Tagging a chapter

When a chapter is finished and pushed, mark it so readers can point at a version
rather than a moving target:

```
$ git tag -a v0.2 -m "Chapter 2: Scrubbing the log"
$ git push origin v0.2
```

---

## Updating from a new archive

New chapters arrive as a zip. **Never unzip it over your repository**, because
that is how you lose the hidden `.git` directory and with it your whole history.

Unpack to a staging area and copy the contents across:

```
$ cd ~/Downloads
$ rm -rf staging && mkdir staging
$ unzip -q to-c-or-not-to-c.zip -d staging
$ cp -a staging/to-c-or-not-to-c/. ~/to-c-or-not-to-c/
```

The `.` on the end of the source path carries the hidden files. Without it,
`.gitignore`, `.gitattributes` and `.clang-format` get left behind.

Then let git tell you what actually arrived:

```
$ cd ~/to-c-or-not-to-c
$ git status
$ git diff
```

This is what version control is for. A new archive stops being a scary overwrite
and becomes a diff you read before accepting, with `git checkout .` to throw it
all away if you disagree.

Then run the three checks and push.

---

## When something goes wrong

**`fatal: not a git repository`** means the `.git` directory is gone, almost
always because an archive was unzipped over the folder instead of staged. Nothing
is lost:

```
$ cd ~/to-c-or-not-to-c
$ git init && git branch -M main
$ git add . && git commit -m "restoring history"
$ git remote add origin git@github.com:dralikma/to-c-or-not-to-c.git
```

**`Permission denied (publickey)`** means SSH cannot use your key. Test it on its
own with `ssh -T git@github.com` before touching `git push`.

**`Updates were rejected`** means GitHub has a commit you do not, almost always
because a README or licence was ticked when the repository was created. Delete
the GitHub repository, create it again empty, and push.

**`src refspec main does not match any`** means you have no commits yet, or your
branch is still called `master`. Check with `git branch --show-current`.

**A binary got committed.** Add it to `.gitignore`, then `git rm --cached
path/to/it`, then commit. The `--cached` matters: without it you delete the real
file too.

**`make test` says MISSING (not built).** Run `make` first, or `make clean &&
make`.

**`git status` shows hundreds of files.** `.gitignore` did not survive a copy.
Check with `ls -a` that it is there, and note that plain `ls` will not show it.

---

## A note on the checks themselves

Every check in `check-book.py` was added *after* the thing it checks had already
broken. The counts, because a heading said "two keys" over a list of three. The
listing comparison, because a bug file grew a header comment and shifted every
line number in a `gdb` walkthrough. The breakpoint validation, because a chapter
told readers to break on a comment.

None of those were caught by reading, which is the whole argument for having a
script do it. When you find a new class of mistake, add a check for it rather
than only fixing the instance. That is the same lesson `tax-cases.c` teaches in
Chapter 1 and `no address survives redaction` teaches in Chapter 2, applied to
the book itself.
