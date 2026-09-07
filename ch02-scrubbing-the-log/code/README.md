# Chapter 2 code

Every program from the chapter, in order, plus a Makefile that builds them all
and a test suite that checks them all.

**Type each program into your own file as the chapter asks.** These are here so
you can compare when something will not work, not so you can skip the typing.

## Build and test

```
$ cd code
$ make
$ make test
```

Everything builds into `build/`, which is not in version control. `make clean`
removes it.

## Watching the four stages

```
$ make stages
```

That runs preprocessing, compiling, assembling, and linking one at a time on
`hello.c`, leaves the intermediate files in `build/`, and prints the line counts
so you can see seven lines become several hundred and then shrink again.

Then go and read them:

```
$ tail -7 build/hello.i          your code, under a pile of stdio.h
$ grep -nE "main:|call" build/hello.s
$ strings build/hello.o | head -3
```

## What is here

### The finished thing

| File | What it is |
|---|---|
| `redact.c` | **The deliverable.** Reads a log on standard input, removes every email address, writes it out. |

### Part 1: the naive redactor

| File | Chapter section |
|---|---|
| `steps/01-echo.c` | Reads the log with `fgets` and prints it. Has the double-spacing bug. |
| `steps/02-echo-fixed.c` | The same with the extra `\n` removed. Output matches the input byte for byte. |
| `steps/03-redact-at.c` | Replaces the `@` and nothing else, which leaves the address readable. This is the program that motivates the chapter. |

### Part 2: compilation

| File | Chapter section |
|---|---|
| `hello.c` | The program you take apart in four stages. |
| `count.c` | Compile with `-S` and find your own `for` loop in the assembly. |

### Part 3: arrays, strings, arguments

| File | Chapter section |
|---|---|
| `scores.c` | Arrays, and `#define` for the size. |
| `peek.c` | One array printed as a string, as numbers, and as characters. Shows the null terminator. |
| `garbage.c` | What is in an array before you fill it. **Run it twice.** Not in the test suite, because its output changes every run. |
| `shout.c` | A function that takes text. The thing Chapter 1 could not do. |
| `len.c` | `fgets` keeps the newline, and how to strip it. |
| `chars.c` | `ctype`, and the 32 between the cases. |
| `greet.c` | `argc` and `argv`. |
| `status.c` | A `Usage:` line and a meaningful exit code. |
| `argvchars.c` | `argv[1][i]`, getting one character of one argument, and validating it. |

### Part 4: the planted bugs

No header comments on these, on purpose. They are byte-identical to the listings
in the chapter, so the line numbers in the book's `gdb` session match the files
you have here. See `bugs/README.md`.

## Not shipped on purpose

`rot`, the Caesar cipher used to demonstrate ROT13 before the exercises, is
exercise 6. Writing it is the point, so there is no copy here to peek at.

## Useful targets

```
$ make                       build everything
$ make test                  build, then run the whole suite
$ make stages                the four compilation stages, one at a time
$ make redact-debug          the redactor with both sanitizers
$ make build/bugs/bug2-asan  bug 2 with AddressSanitizer, which is the only
                             thing that finds it
$ make clean                 delete build/
```
