#!/usr/bin/env python3
"""
check-voice.py - measure the prose against STYLE.md.

    $ python3 tools/check-voice.py           report every file
    $ python3 tools/check-voice.py ch03      report one file

check-book.py checks facts. This one checks voice, and the difference matters:
a fact is right or wrong, while voice is a rate you push in one direction.

It cannot tell you whether a paragraph sounds like a person. Read it aloud for
that. What it can do is catch the mechanical failures, which in the first draft
of this book were nearly all of them: one contraction in 1,132 opportunities and
not a single first-person sentence in 46,000 words.

Exit status is 0 when every file is inside the thresholds, 1 otherwise, so it
doubles as a worklist while a rewrite is in progress.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# A chapter should read as if a person wrote it. These are the two numbers that
# moved the needle most, so they are the two that gate.
MIN_CONTRACTION_RATE = 55      # percent of contractable phrases actually contracted
MIN_AUTHOR_PER_10K = 4         # first-person singular sentences per 10,000 words

FILES = [
    "README.md",
    "STYLE.md",
    "toolbench/README.md",
    "00-how-the-machine-thinks/README.md",
    "ch01-the-till/README.md",
    "ch02-scrubbing-the-log/README.md",
    "ch03-two-million-lines/README.md",
    "ch04-the-file-that-wont-fit/README.md",
    "ch05-counting-unique-things/README.md",
    "ch06-ship-it/README.md",
]

CONTRACTED = re.compile(
    r"\b(it's|that's|you're|you'll|you've|don't|doesn't|won't|can't|isn't"
    r"|aren't|didn't|haven't|hasn't|wasn't|weren't|I'm|I've|I'll|here's"
    r"|there's|let's|we're|we'll|they're|couldn't|wouldn't|shouldn't"
    r"|what's|who's|nothing's|something's)\b", re.I)

EXPANDED = re.compile(
    r"\b(it is|that is|you are|you will|you have|do not|does not|will not"
    r"|cannot|is not|are not|did not|have not|has not|was not|were not"
    r"|I am|I have|I will|here is|there is|we are|we will|they are"
    r"|could not|would not|should not|what is|who is)\b", re.I)

AUTHOR = re.compile(r"(?<![A-Za-z])I(?: |'m|'ve|'ll|\.|,)")

BANNED_WORDS = ["delve", "leverage", "seamless", "robust", "crucial", "vital",
                "essential", "powerful", "elegant", "game-changer", "journey",
                "landscape", "realm", "tapestry", "testament"]

BANNED_PHRASES = ["it's worth noting", "it is worth noting", "that said",
                  "at the end of the day", "here's the thing", "let's dive",
                  "let's unpack", "buckle up", "where the magic happens",
                  "by the end of this chapter", "great job", "well done",
                  "save points", "house address"]

# "not X, it's Y" and "not just X but Y"
FAKE_REVEAL = re.compile(r"\bnot (?:just |only )?[^,.\n]{3,45}[,.] (?:it is|it's|but) ")

# a spaced hyphen doing an em dash's job
FAKE_DASH = re.compile(r"\S \- \S")

# a rhetorical question opening a paragraph
RHETORICAL = re.compile(r"^(So what|Why is that|What's really|But what if)\b.*\?", re.M)

# Bold is allowed for a defined term on first use and for box labels. It is not
# allowed for emphasis. Flag only the emphasis case, which is bold wrapped
# around a word that defines nothing.
EMPHASIS_WORDS = {
    "never", "always", "must", "exactly", "not", "every", "all", "only",
    "really", "before", "after", "is", "was", "does", "do", "cannot", "very",
    "one", "two", "three", "four", "zero", "no", "yes", "much", "far",
}
MID_BOLD = re.compile(r"[a-z,] \*\*([^*]{1,40})\*\*[ ,.]")


def emphasis_bold(text):
    return [m for m in MID_BOLD.findall(text)
            if m.lower().strip(".,") in EMPHASIS_WORDS]


def prose_only(text):
    """Strip fenced code, indented transcripts, tables, and inline code.

    Inline code matters: `1.0 - tenths` is subtraction, not a hyphen doing an
    em dash's job, and counting it as prose produced false alarms.
    """
    out, in_fence = [], False
    for line in text.split("\n"):
        stripped = line.lstrip("> ").strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if stripped.startswith("|"):
            continue
        if line.startswith("    ") or line.startswith("\t"):
            continue
        out.append(re.sub(r"`[^`]*`", "CODE", line))
    return "\n".join(out)


def report(path):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return None
    raw = open(full, encoding="utf-8").read()
    text = prose_only(raw)
    words = len(text.split())
    if words < 200:
        return None            # a stub, nothing to judge yet

    c = len(CONTRACTED.findall(text))
    e = len(EXPANDED.findall(text))
    rate = round(c / (c + e) * 100) if (c + e) else 100
    author = len(AUTHOR.findall(text))
    per10k = round(author / words * 10000, 1)

    problems = []
    low = text.lower()
    # STYLE.md lists the banned words in order to ban them, so it is exempt
    # from its own vocabulary rules. Everything else is not.
    defines_the_rules = path == "STYLE.md"
    for w in ([] if defines_the_rules else BANNED_WORDS):
        # Do not flag a banned word when it is part of a real identifier.
        # "build-essential" is a Debian package name, not a choice of adjective.
        n = len(re.findall(r"(?<![-\w])" + re.escape(w), low))
        if n:
            problems.append(f"{n}x banned word: {w}")
    for p in ([] if defines_the_rules else BANNED_PHRASES):
        # Word boundary at the front, so "here's the thing" does not fire
        # inside "There's the thing you couldn't do in Chapter 1."
        n = len(re.findall(r"(?<![a-z])" + re.escape(p), low))
        if n:
            problems.append(f"{n}x banned phrase: {p}")
    for label, rx in [("fake reveal (not X, it's Y)", FAKE_REVEAL),
                      ("spaced hyphen as em dash", FAKE_DASH),
                      ("rhetorical question opener", RHETORICAL)]:
        n = len(rx.findall(text))
        if n and not defines_the_rules:
            problems.append(f"{n}x {label}")
    eb = emphasis_bold(text)
    if eb:
        problems.append(f"{len(eb)}x bold for emphasis: " + ", ".join(sorted(set(eb))[:6]))
    if "\u2014" in raw:
        problems.append(f"{raw.count(chr(8212))}x EM DASH")

    ok = rate >= MIN_CONTRACTION_RATE and per10k >= MIN_AUTHOR_PER_10K and not problems
    return dict(path=path, words=words, rate=rate, author=author,
                per10k=per10k, problems=problems, ok=ok)


def main():
    wanted = sys.argv[1] if len(sys.argv) > 1 else None
    rows = []
    for f in FILES:
        if wanted and wanted not in f:
            continue
        r = report(f)
        if r:
            rows.append(r)

    print(f"\n{'file':<38} {'words':>6} {'contr':>6} {'I/10k':>6}  status")
    print("-" * 74)
    failing = 0
    for r in rows:
        status = "ok" if r["ok"] else "REWRITE"
        if not r["ok"]:
            failing += 1
        print(f"{r['path']:<38} {r['words']:>6} {r['rate']:>5}% {r['per10k']:>6}  {status}")

    for r in rows:
        if r["problems"]:
            print(f"\n{r['path']}")
            for p in r["problems"]:
                print(f"    {p}")

    print(f"\nthresholds: contractions >= {MIN_CONTRACTION_RATE}%, "
          f"author >= {MIN_AUTHOR_PER_10K} per 10k words")
    if failing:
        print(f"{failing} of {len(rows)} files still need a voice pass.")
        sys.exit(1)
    print(f"All {len(rows)} files read like a person wrote them.")
    sys.exit(0)


if __name__ == "__main__":
    main()
