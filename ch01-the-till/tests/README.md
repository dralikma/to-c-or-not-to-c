# Chapter 1 tests

Expected output for every program in `../code/`, plus a runner that
compares them.

```
$ cd ../code
$ make test
```

Or from anywhere:

```
$ ./tests/run-tests.sh
```

## How this works

There is nothing clever here. Each program is run, its output is captured,
and `diff` compares it against `<name>-expected.txt`. Silence from `diff`
means a match, exactly as in the Toolbench.

The runner exits with status 0 when everything passes and non-zero when
anything fails, so it can be wired into anything that checks a number.

`receipt-expected.txt` is the one the chapter names directly, in the Bug 3
walkthrough.

## Programs that need input

Four tests feed a file to the program on standard input, using the `<`
redirection you met in the Toolbench:

| Test | Input | Also checks |
|---|---|---|
| `quantity-good` | `3` | exit status 0 |
| `quantity-bad` | `twelve` | **exit status 1** |
| `confirm-yes` | `y` | |
| `confirm-no` | `n` | |

`quantity-bad` is the interesting one. It is not enough that the program
prints a complaint; it also has to *exit with a failure status*, so that a
script calling it can tell something went wrong. That is the habit the
chapter asks you to build, and this is the test that enforces it.

## Why `sizes` is not tested

`sizes.c` prints how many bytes each type takes on the machine running it.
On 64-bit Debian a `long` is 8 bytes. On a 32-bit Raspberry Pi it is 4.
Neither is wrong.

Pinning that in an expected-output file would turn a true fact about your
machine into a test failure, so it is left out on purpose. Run it and read
it; do not test it.

## The gap that `tax-cases` fills

This is worth reading even if you never touch the tests again, because it
is the single most useful thing in this directory.

`receipt-expected.txt` looks like a thorough test. It checks eleven lines
of output including every price, the subtotal, the tax, and the total.

It does not test the tax rounding rule at all.

The basket comes to 4948 cents. `4948 * 825` is `4082100`, and the
leftover after dividing by 10000 is 2100, which is below half. So the
tax comes to 408 cents whether you round properly or let the division
truncate. Delete the `+ 5000` from `tax_on` in `receipt.c`, rebuild, and
every single test still passes.

Try it. It is a two second edit and the lesson lands harder than reading
about it.

`tax-cases.c` exists to close that hole. It runs the tax calculation
across amounts on both sides of the rounding boundary, including $10.00,
which sits exactly on it and comes out as 83 cents when rounded and 82
when truncated. With that test in place, the sabotage above fails
immediately.

The general lesson, which is exercise 10 in the chapter: **a test that
passes tells you nothing until you have watched it fail.** Break the thing
it is supposed to protect, confirm the test catches it, then put it back.
A test suite that cannot catch your own deliberate sabotage would not have
caught Maria's nephew either.

## Regenerating the expected files

If you change a program on purpose and the test now fails, look at the
diff first and satisfy yourself the new output is genuinely correct. Then:

```
$ cd ../code
$ ./build/receipt > ../tests/receipt-expected.txt
```

Check it by hand before you trust it. An expected-output file generated
from a buggy program locks the bug in permanently and is worse than having
no test at all.
