#!/usr/bin/env python3
"""
check-book.py - verify every hand-written fact in the book against reality.

Run this before every push:

    $ python3 tools/check-book.py

The book makes a lot of specific claims. It says the Toolbench teaches eleven
shell commands, that the gdb walkthrough breaks on line 38 of receipt.c, that
`subtotal += part;` is on that line. Every one of those is a fact that can
quietly stop being true the moment something above it is edited.

Three of them already had. The heading said "Two keys" over a list of three.
The gdb section said line 37 after a rewrite pushed it to 38. The Makefile
notes said three special rules when there were five. None of that was caught by
reading, because reading is exactly what does not catch it.

So this file checks them instead. Exit status is 0 when everything holds and 1
when it does not, which means it can go in a git hook or a CI job.
"""

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

failures = []
checks_run = 0


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def check(label, got, want):
    """Assert got == want, recording the result."""
    global checks_run
    checks_run += 1
    if got == want:
        print(f"  ok    {label}")
    else:
        print(f"  FAIL  {label}: found {got}, text claims {want}")
        failures.append(label)


def check_true(label, condition, detail=""):
    global checks_run
    checks_run += 1
    if condition:
        print(f"  ok    {label}")
    else:
        print(f"  FAIL  {label}{': ' + detail if detail else ''}")
        failures.append(label)


def section(text, start_pat, end_pat):
    """Return the slice of text between two headings."""
    a = re.search(start_pat, text, re.M)
    if not a:
        return ""
    rest = text[a.end():]
    b = re.search(end_pat, rest, re.M)
    return rest[:b.start()] if b else rest


# ---------------------------------------------------------------- links
print("\nInternal links")

link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
broken = []
working = 0
for dirpath, dirnames, files in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in (".git", "build")]
    for f in files:
        if not f.endswith(".md"):
            continue
        p = os.path.join(dirpath, f)
        with open(p, encoding="utf-8") as fh:
            for m in link_re.finditer(fh.read()):
                target = m.group(2)
                if target.startswith("http"):
                    continue
                path = target.split("#")[0]
                if not path:
                    continue
                if os.path.exists(os.path.normpath(os.path.join(dirpath, path))):
                    working += 1
                else:
                    broken.append(f"{os.path.relpath(p, ROOT)} -> {target}")
check_true(f"all {working} internal links resolve", not broken, "; ".join(broken))


# ------------------------------------------------- chapter/code agreement
print("\nChapter text against the code it ships")

chapter = read("ch01-the-till/README.md")
receipt_src = read("ch01-the-till/code/receipt.c")

listing = chapter[chapter.index("// receipt.c"):]
listing = listing[:listing.index("```")].rstrip() + "\n"
check_true("code/receipt.c is byte-identical to the chapter listing",
           listing == receipt_src,
           "the listing and the file have drifted apart")

# the gdb walkthrough breaks on a specific line, which shifts if the file changes
claimed = re.search(r"is line (\d+) of `receipt\.c`", chapter)
actual = next(i for i, l in enumerate(receipt_src.split("\n"), 1)
              if l.strip() == "subtotal += part;")
check("gdb breakpoint line matches receipt.c", actual,
      int(claimed.group(1)) if claimed else None)

for form in [f"(gdb) break {actual}", f"file receipt.c, line {actual}.",
             f"main () at receipt.c:{actual}"]:
    check_true(f"gdb transcript uses line {actual}: {form!r}", form in chapter)

# Every code listing printed in the chapter must be byte-identical to the file
# shipped beside it, or a reader following the book gets different line numbers
# from a reader running the repository.
for n in (1, 2, 4):
    head = chapter.index(f"### Bug {n}\n")
    blk = chapter.index("```c\n", head) + len("```c\n")
    listing = chapter[blk:chapter.index("```", blk)]
    shipped = read(f"ch01-the-till/code/bugs/bug{n}.c")
    check_true(f"code/bugs/bug{n}.c matches its chapter listing", listing == shipped,
               "a header comment or edit has shifted the line numbers apart")

# A gdb session echoes the source line it stopped on, as "38<TAB>  subtotal...".
# Each one is a claim about a specific file, and the file is named a line or two
# earlier by "at receipt.c:38" or "file bug2.c, line 8.". Track which file is in
# play and check every echo against it. Without this, adding one line anywhere
# above a breakpoint silently invalidates the whole session.
SOURCES = {
    "receipt.c": "ch01-the-till/code/receipt.c",
    "bug2.c":    "ch01-the-till/code/bugs/bug2.c",
    "bug3.c":    "ch01-the-till/code/bugs/bug3.c",
}
current = None
checked = 0
wrong = []
for raw in chapter.split("\n"):
    named = re.search(r"(?:at |file )([a-z0-9-]+\.c)[:,]", raw)
    if named:
        current = named.group(1)
    echo = re.match(r"^(\d+)\t(.+)$", raw)
    if echo and current in SOURCES:
        n, text = int(echo.group(1)), echo.group(2)
        lines = read(SOURCES[current]).split("\n")
        checked += 1
        real = lines[n - 1].strip() if n <= len(lines) else "(past end of file)"
        if real != text.strip():
            wrong.append(f"{current}:{n} transcript says {text.strip()!r}, file has {real!r}")
check_true(f"all {checked} source lines echoed in gdb transcripts are real",
           not wrong, "; ".join(wrong))


# ---------------------------------------------------------------- counts
print("\nNumeric claims in the prose")

tb = read("toolbench/README.md")
readme = read("README.md")
machine = read("00-how-the-machine-thinks/README.md")
tests_readme = read("ch01-the-till/tests/README.md")
runner = read("ch01-the-till/tests/run-tests.sh")

WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
         "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
         "twelve": 12}


def claimed(text, pattern):
    """Pull the number a heading or sentence claims."""
    m = re.search(pattern, text, re.I | re.M)
    if not m:
        return None
    tok = m.group(1).lower()
    return WORDS.get(tok, int(tok) if tok.isdigit() else None)


# Toolbench: the shell commands taught in one section
cmds = section(tb, r"### The \w+ commands this book needs", r"### \w+ keys")
check("Toolbench shell commands",
      len(set(re.findall(r"^\$ ([a-z]+)", cmds, re.M))),
      claimed(tb, r"### The (\w+) commands this book needs"))

# Toolbench: keyboard shortcuts
keys = section(tb, r"### \w+ keys that save you", r"### Redirection")
check("Toolbench keyboard shortcuts",
      len(re.findall(r"^Press ", keys, re.M)),
      claimed(tb, r"### (\w+) keys that save you"))

# Toolbench: gdb command table
gdb = section(tb, r"### Your \w+ commands", r"^> \*\*Optional")
check("gdb commands in the table",
      len(set(re.findall(r"^\| `([a-z]+)", gdb, re.M))),
      claimed(tb, r"### Your (\w+) commands"))

# Toolbench: the closing bench table
bench = section(tb, r"^\| Tool \| Job \|", r"^\s*$")
check("tools in the closing bench table",
      len([l for l in bench.split("\n") if re.match(r"^\| [A-Za-z]", l)]),
      claimed(tb, r"(\w+) things\. You have now used every one"))

# Toolbench and Chapter 1: the planted bugs
check("Toolbench planted bugs", len(re.findall(r"^### Bug \d+", tb, re.M)),
      claimed(tb, r"(\w+) programs\. Each has exactly one bug"))
check("Chapter 1 planted bugs", len(re.findall(r"^### Bug \d+", chapter, re.M)),
      claimed(chapter, r"(\w+) programs\. Each has exactly one bug"))

# README: the shape of the book
check("book parts", 1 + 1 + 5 + 1, claimed(readme, r"There are (\w+) parts"))
check("chapter beats", len(re.findall(r"^\*\*\d\. ", readme, re.M)),
      claimed(readme, r"the same (\w+) sections in the same order"))
check("sidebar kinds",
      len(re.findall(r"^> \*\*", section(readme, r"(\w+) kinds of sidebar",
                                        r"Exercises come in three sizes"), re.M)),
      claimed(readme, r"(\w+) kinds of sidebar"))

# Chapter 1 and How the Machine Thinks
check("Chapter 1 parts", len(re.findall(r"^## Part \d+", chapter, re.M)),
      claimed(chapter, r"^(\w+) parts, and they build"))
check("takeaways in How the Machine Thinks",
      len(re.findall(r"^\d+\. \*\*", machine, re.M)),
      claimed(machine, r"^(\w+) things\. If you remember nothing else"))

# tests README: how many cases feed stdin
check("tests that feed stdin", runner.count('"$HERE/inputs/'),
      claimed(tests_readme, r"(\w+) tests feed a file to the program"))


# ------------------------------------------------------------- numbering
print("\nSection numbering is contiguous")

for label, text, pat in [
    ("Toolbench parts", tb, r"^## Part (\d+)"),
    ("Toolbench flags", tb, r"^### Flag (\d+)"),
    ("Toolbench bugs", tb, r"^### Bug (\d+)"),
    ("Chapter 1 parts", chapter, r"^## Part (\d+)"),
    ("Chapter 1 bugs", chapter, r"^### Bug (\d+)"),
    ("Chapter 1 exercises", chapter, r"^\*\*(\d+)\. "),
]:
    nums = [int(n) for n in re.findall(pat, text, re.M)]
    check_true(f"{label} run 1..{len(nums)}",
               nums == list(range(1, len(nums) + 1)), f"got {nums}")


# ------------------------------------------------------------------ style
print("\nHouse style")

md_files = []
for dirpath, dirnames, files in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in (".git", "build")]
    md_files += [os.path.join(dirpath, f) for f in files if f.endswith(".md")]

em = [os.path.relpath(p, ROOT) for p in md_files if "\u2014" in open(p, encoding="utf-8").read()]
check_true("no em dashes", not em, ", ".join(em))

stubs = [d for d in os.listdir(ROOT)
         if d.startswith(("ch0", "toolbench", "00-"))
         and os.path.isdir(os.path.join(ROOT, d))
         and not os.path.exists(os.path.join(ROOT, d, "README.md"))]
check_true("every chapter directory has a README", not stubs, ", ".join(stubs))


# ------------------------------------------------------------------ tests
print("\nChapter 1 test suite")

code_dir = os.path.join(ROOT, "ch01-the-till", "code")
if os.path.isdir(code_dir):
    r = subprocess.run(["make", "test"], cwd=code_dir,
                       capture_output=True, text=True)
    m = re.search(r"(\d+) passed, (\d+) failed", r.stdout)
    if m:
        check_true(f"{m.group(1)} passed, {m.group(2)} failed",
                   m.group(2) == "0", "some tests fail")
    else:
        check_true("test suite ran", False, "could not parse the output")


# ----------------------------------------------------------------- verdict
print()
if failures:
    print(f"{len(failures)} of {checks_run} checks FAILED:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

print(f"All {checks_run} checks passed.")
sys.exit(0)
