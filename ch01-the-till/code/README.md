# Chapter 1 code

Every program from the chapter, in the order it appears, plus a Makefile
that builds all of them and a test suite that checks all of them.

**These files are here so you can compare when something will not work.**
They are not here so you can skip the typing. Type each program into your
own file as the chapter asks. That is where the learning is.

## Build and test everything

```
$ cd code
$ make
$ make test
```

`make test` builds everything and then runs every program, comparing its
output against the matching file in `../tests/`. Every test should pass and
none should fail; the runner prints a count at the end and exits non-zero if
anything failed.

Everything is built into `build/`, which is deliberately not in version
control. `make clean` removes it.

## What is here

### The finished thing

| File | What it is |
|---|---|
| `receipt.c` | **The chapter's deliverable.** Maria's till, correct to the cent. |
| `tax-cases.c` | A regression test for the tax rounding rule. Read the comment at the top; it explains a hole this fills. |

### Part 1: first contact

Run these in order. Each one is a few lines longer than the last.

| File | Chapter section |
|---|---|
| `steps/01-till-first.c` | Your first calculation. Three variables, one expression, `%f`. |
| `steps/02-till-money.c` | Making it look like money. `%f` becomes `%.2f`. |
| `steps/03-till-broken.c` | Maria's actual basket. **This is the broken till.** Add up the seven item lines by hand: they come to 49.49 and the program prints 49.48. |
| `steps/04-till-debug.c` | The same thing with one temporary line showing what the croissant price really is. |

### Part 2: under the hood

| File | Chapter section |
|---|---|
| `probe.c` | The scratchpad, with everything the chapter tells you to add, assembled in order. |
| `sizes.c` | Type sizes and limits on **your** machine. Deliberately not in the test suite, because its output depends on the machine and that is the whole point of running it. |

### Part 3: build it properly

| File | Chapter section |
|---|---|
| `two.c` | The failed "just round it" fix. Needs `-lm`; leave it off to see your first linker error. |
| `steps/05-receipt-money.c` | Printing a count of cents as money with `/` and `%`. |
| `steps/06-receipt-padded.c` | Why `%02ld` and not `%ld`. This one prints `$8.04`, which the version above would print as `$8.4`. |
| `steps/07-receipt-tax.c` | `const`, comments, and the `+ 5000` that makes the tax round instead of truncate. |
| `feq.c` | The `-Wfloat-equal` demonstration. Build it twice, with and without the flag. |
| `chart.c` | A loop inside a loop. Move the `printf("\n")` to the two wrong places and watch what happens. |
| `day.c` | Maria's missing four dollars, as a number. |
| `quantity.c` | Reading a number with `scanf`, including the return value check. |
| `confirm.c` | `getchar`, single quotes, and the proof that `'A'` is 65. |

### Part 4: the planted bugs

Each has exactly one bug, and each is best caught by a different tool.
Read the comment at the top of each file for the symptom, then work it out
before reading the walkthrough in the chapter.

| File | Best tool | The bug in one phrase |
|---|---|---|
| `bugs/bug1.c` | the compiler | `%d` where `%ld` belongs |
| `bugs/bug2.c` | `gdb` | dividing before multiplying |
| `bugs/bug3.c` | `diff` | a loop counting from 1 instead of 0 |
| `bugs/bug4.c` | the sanitizer | `int` overflow |

## Useful targets

```
$ make                    # build everything
$ make test               # build, then run the whole suite
$ make clean              # delete build/
$ make build/bugs/bug4-ub # bug4 with the undefined behaviour sanitizer
$ make receipt-debug      # the till with both sanitizers on
$ make build/feq-warn     # feq with -Wfloat-equal, to see the warning
```

## A note on this Makefile

It is bigger than the one you type yourself in Part 5 of the chapter,
because it has to build twenty-odd programs rather than one. The one rule
that does most of the work is:

```make
build/%: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -o $@ $<
```

`%` matches any name. `$@` is the target being built and `$<` is the first
thing it depends on. So that says: to make `build/anything`, compile
`anything.c` into it. A few programs need something different, and each has
its own rule underneath with a comment saying why: `two` needs `-lm`,
`bug1-quiet` needs warnings switched off, `bug4-ub` needs the sanitizer, and
`feq` is built both with and without `-Wfloat-equal` so you can compare.
