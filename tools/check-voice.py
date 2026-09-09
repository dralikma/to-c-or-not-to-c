#!/usr/bin/env python3
"""
check-voice.py - measure the prose against the house style.

    $ python3 tools/check-voice.py           report every file
    $ python3 tools/check-voice.py ch03      report one file

check-book.py checks facts. This one checks voice, and the difference matters:
a fact is right or wrong, while voice is a rate you push in one direction.

It cannot tell you whether a paragraph sounds like a person. Read it aloud for
that. Exit status is 0 when every file is inside the thresholds, 1 otherwise,
so it doubles as a worklist while a rewrite is in progress.

THE HOUSE STYLE, in full, because this is the only place it is written down.

  One author, one voice, first page to last. Second person for the reader,
  first person singular for an opinion or a war story. If a chapter runs 4,000
  words without the author appearing, something is wrong.

  Contractions throughout. Drop one only when a sentence needs weight: "Do not
  put that in a test suite" hits harder than "don't". Rarely, or it stops
  working.

  Varied sentence length. Some paragraphs are one sentence.

  Opinions, stated. If a default is bad, say so. a.out is a terrible name.
  scanf is a trap. A reader can disagree with an opinion and can do nothing
  with mush.

  Admit difficulty. "Everyone gets this wrong the first time" beats
  reassurance. When the author made the mistake, say so.

  Let the reader fail on purpose. "Type this. Run it. It'll break. That's the
  point."

  Concrete, always. Not "a large file", forty thousand lines. Not "slow", four
  hundred baskets a day at one cent each is $1,248 a year.

  Never an em dash, and never its disguises: no spaced hyphen doing the same
  job, no semicolon as a dramatic pause. Recast the sentence.

  Banned constructions: "it's not X, it's Y"; colon-then-reveal as a habit;
  three-item lists by default; opening a section by restating its heading;
  closing one by summarising it; rhetorical questions as openers; "by the end
  of this chapter you will be able to"; "let's dive in"; stacked hedges;
  praising the reader; stock analogies (git is not save points, a pointer is
  not a house address, a variable is not a box).

  Bold is for a defined term on first use and for box labels. Not emphasis.

  Four kinds of box and no others: Under the hood, Debian note, Trap, Parity.
  No emoji anywhere.

  An analogy earns its place only if it is specific to this book and does real
  work. The phone book in How the Machine Thinks stays because Chapter 3
  measures it. Most do not clear that bar.

The test that matters: read the paragraph aloud. If it sounds like a
conference abstract, a press release, or a product page, rewrite it.
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
    # Nothing is exempt any more. The rules live in this file's docstring,
    # which is not prose the checker reads.
    defines_the_rules = False
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
