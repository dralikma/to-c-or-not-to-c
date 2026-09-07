# Chapter 2 tests

Expected output for every program in `../code/`, plus a runner.

```
$ cd ../code && make test
```

21 checks. Each program is run, its output captured, and `diff` compares it
against `<name>-expected.txt`. Silence from `diff` means a match.

## Two kinds of check

Most tests compare output against a saved file. That proves the output has not
**changed**.

The last one is different:

```
no address survives redaction
```

That runs the redactor and counts `@` characters in the result. It proves the
program still does its **job**, which is not the same thing. If someone
regenerates the expected file carelessly from a broken build, the saved-output
test happily passes and this one still fails.

Write both kinds when the job matters. Chapter 1's `tax-cases.c` exists for the
same reason.

## Why `argv[0]` made the runner awkward

The runner does `cd` into `code/` and calls programs as `./build/greet` rather
than by an absolute path. That is not tidiness.

`argv[0]` is the program's name **as typed**, which the chapter makes a point of.
So `/home/ali/toc/code/build/greet` and `./build/greet` produce different output
from the same program, and `greet` and `status` both print it. Generating the
expected files one way and running the tests the other way makes them fail for a
reason that has nothing to do with the code.

This caught me out while writing the chapter, which is a fair demonstration that
the lesson is real.

## Two programs whose output is never pinned

`garbage.c` reads uninitialised memory. `bugs/bug2.c` reads past the end of an
array. Both have **undefined** output: it depends on what the stack happened to
hold, which differs between compiler versions and machines.

I learned this the hard way. `bug2`'s output was pinned in an expected file
generated on the machine the chapter was written on, where it happened to print
`The word is Hi! and it is 3 characters`. On Debian with gcc 14 it printed
something else, and the suite failed for a reason that had nothing to do with the
reader's code.

**Never pin undefined behaviour in a test.** What can be tested is the thing that
is actually true about `bug2`, which is that AddressSanitizer catches it:

```
bug2 still overruns its array (sanitizer catches it)
```

That check greps the sanitizer's report for `stack-buffer-overflow`. It is stable
everywhere, and it is a better test besides, because it states the fault rather
than a symptom of it.

## Why `garbage` is not tested

`garbage.c` prints whatever was in memory before it ran, and that changes between
runs. Pinning it in an expected file would turn a true fact about your machine
into a test failure. Run it twice and read it; do not test it.

## Regenerating

If you change a program on purpose and a test fails, read the diff first and
satisfy yourself the new output is right. Then, from `code/`:

```
$ ./build/redact < ../data/access.log > ../tests/redact-expected.txt
```

Check it by hand before you trust it. An expected file generated from a buggy
program locks the bug in permanently.
