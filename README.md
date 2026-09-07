# To C or not to C

A hands-on textbook for people who have never written a line of code, built around the C material from Harvard's CS50x.

This book is not affiliated with Harvard or CS50. It follows the same shape and covers the same ground, because that shape works. What it adds is a machine underneath: every chapter shows you what your code becomes after the compiler is done with it, and every chapter makes you break something on purpose so that debugging becomes a reflex instead of a panic.

You will write real programs from the first ten minutes. You will not write a single line of pseudocode that never runs.

---

## Table of contents

1. [What this book is](#what-this-book-is)
2. [What you will be able to do at the end](#what-you-will-be-able-to-do-at-the-end)
3. [Who this is for](#who-this-is-for)
4. [What you need](#what-you-need)
5. [The workbench: your tools](#the-workbench-your-tools)
6. [The loop](#the-loop)
7. [How I introduce flags](#how-i-introduce-flags)
8. [Debugging is a habit, not a chapter](#debugging-is-a-habit-not-a-chapter)
9. [How every chapter is built](#how-every-chapter-is-built)
10. [The map](#the-map)
11. [What you will be holding at the end of Chapter 6](#what-you-will-be-holding-at-the-end-of-chapter-6)
12. [How to use this repository](#how-to-use-this-repository)
13. [House rules](#house-rules)
14. [When you get stuck](#when-you-get-stuck)
15. [What I changed from CS50, and why](#what-i-changed-from-cs50-and-why)
16. [Feedback and license](#feedback-and-license)

---

## What this book is

Most beginner programming books teach you which words to type. You type them, something appears on screen, and you move on with a vague feeling that magic happened somewhere in the middle. That feeling never goes away on its own. It turns into a ceiling.

This book is built to remove the magic. When you write a variable, you will see where it lives in memory. When you compile, you will run the compiler one stage at a time and read what comes out of each stage. When your program crashes, you will not guess. You will attach a debugger, walk the program line by line, and watch the exact moment it goes wrong.

There are eight parts: a setup chapter called **The Toolbench**, a short reading section called **How the Machine Thinks**, five chapters of C, and a capstone. Each C chapter is one scenario. Something is broken, or slow, or about to embarrass somebody, and you fix it with the specific C features that chapter is about. You are never learning arrays because it is Tuesday and arrays come next. You are learning arrays because you have a log file full of customer email addresses that you need to redact before you send it to a vendor, and there is no way to do that without them.

The five C chapters map one to one onto weeks 1 through 5 of CS50x. If you are working through the course alongside this book, Chapter 1 is Week 1, Chapter 2 is Week 2, and so on. Every chapter ends with a parity box that names the CS50 problem set it corresponds to, so you can hand in the course work if you want to.

---

## What you will be able to do at the end

Not "understand" and not "be familiar with." Do. If you finish this book and cannot do these things, the book failed you and I want to hear about it.

- Write, compile, and run a C program on Debian from a terminal, without an IDE holding your hand.
- Read a compiler error and know which line to look at and what to change, including errors that point at the wrong line.
- Explain what happens to your source code between typing `gcc` and getting an executable, and demonstrate each stage with a command.
- Choose the right type for a piece of data and explain what it costs in bytes and in precision.
- Use pointers deliberately: pass by reference, walk an array, allocate memory on the heap, and free it exactly once.
- Find a memory bug with AddressSanitizer or Valgrind and fix the cause rather than the symptom.
- Step through a running program in `gdb`, inspect variables, set a breakpoint on a condition, and read a backtrace after a crash.
- Implement linear search, binary search, selection sort, insertion sort, and merge sort from scratch, and say which one you would reach for and why.
- Build a linked list, a hash table, a stack, and a queue, and free every byte you allocated.
- Read a file that is larger than your available memory, one line at a time, without your program falling over.
- Handle command line arguments, validate input, fail loudly with a useful message, and return a meaningful exit code.
- Write a Makefile with separate debug and release builds.
- Test your own program against expected output automatically, and put it under version control.

---

## Who this is for

You are an adult who has never programmed, or who has poked at a bit of Python or JavaScript and wants to understand what is under it. You can open a terminal, change directories, list files, and edit a file without help. If `cd`, `ls`, `mkdir`, and `nano` mean something to you, you have enough.

You do not need mathematics beyond arithmetic. There is one chapter where we count how long things take, and the heaviest idea in it is that doubling the size of a list roughly doubles the work for one approach and adds a single step to another. That is the whole of it.

You do need patience with the terminal. C does not come with a friendly playground. The terminal is the playground. By the end of the Toolbench chapter you will be comfortable there, and by Chapter 3 you will prefer it.

This book will not suit you if you want to build a website or a phone app by Friday. C is a poor tool for both. What C gives you is the layer everything else sits on. Learn it, and Python stops being a mystery box, because you will know what the box is doing.

---

## What you need

- A machine running **Debian 13 (trixie)**. A virtual machine is fine. A Raspberry Pi is fine. An old laptop you rescued from a drawer is more than fine.
- About 2 GB of free disk space for the compiler toolchain and the sample data files.
- Two to four hours a week, and the willingness to type code instead of copying it.

Everything else is free software you will install in the Toolbench chapter with one `apt` command. Nothing in this book costs money and nothing requires an account.

If you are on Ubuntu, the commands are identical. If you are on Fedora or Arch, swap `apt` for your package manager and everything else holds. If you are on macOS, most of it works but `gdb` and Valgrind fight with Apple's security model, so run Debian in a VM and save yourself an evening.

---

## The workbench: your tools

Six tools do the work on your code, and two more keep the work from becoming a chore. That is the whole bench. No IDE, no framework, no plugin ecosystem.

**The terminal** is where you run things. It is the only interface that shows you the whole loop at once: the command you ran, the exact output it produced, and the exit status it returned. Buttons hide that evidence. Everything in this book happens here.

**The editor** is where you write code. C source is plain text, so `nano` is enough and will never get between you and the work. Use `vim` or VS Code instead if you already know them. The book never depends on which you chose.

**The compiler** is `gcc`, which turns your C into a program the processor can run. It is also your first line of defence, and this is the part beginners waste. It will name entire classes of mistake before your program ever runs, but only if you ask it to. Asking is a matter of flags, and you will earn every flag one at a time.

**The sanitizer** catches the bugs the compiler cannot see, the ones that only exist while the program is running. C will happily let you read memory that is not yours and carry on as if nothing happened. AddressSanitizer stops the program at the exact instruction and names the variable you overran. Valgrind does a related job by a different route and catches memory you allocated and forgot to release.

**The debugger** is `gdb`, and it lets you watch your program think. Stop at a chosen line, look at any variable, run one line at a time, and after a crash ask which chain of calls got you there. Without it, your only window into a running program is `printf`, which works in the same sense that hitting a nail with a rock works.

**The judge** is `diff`, which compares your program's output against the output it should have produced. "It looks right" is not a test. It is an opinion formed by a tired person at 11pm who already believes the code works. `diff` has no opinions and does not skim, which is how it catches the trailing space your eyes cannot see.

Then two more that are not about C at all. **`make`** remembers your compile command so you stop retyping it and stop quietly dropping flags when you are in a hurry. **`git`** takes snapshots of your work so a bad hour is never a lost week.

The Toolbench chapter installs all eight, and teaches each one by showing you what life looks like without it first. It also adds `clang` to the shelf as a second compiler, purely so you have another phrasing to read when gcc's wording means nothing to you.

---

## The loop

Those tools form a cycle. Almost everything you do in this book, and everything you will do afterward as a programmer, is a turn of this cycle.

```
        write  ->  compile  ->  run  ->  judge
          ^           |          |         |
          |           |          |         |
          +-----------+----------+---------+
                    debug
```

Written out:

1. **Write** a small piece of the program in the editor. Small. One behaviour.
2. **Compile** it with warnings on. If the compiler complains, fix it now, before running anything. Warnings are not noise to scroll past.
3. **Run** it and see what it does.
4. **Judge** the output against what it should be, using `diff` rather than your own eyes.
5. If it is wrong, **debug**: sanitizer for memory problems, `gdb` for logic problems. Find the cause. Do not patch the symptom.
6. Back to step 1 with the next small piece.

The single most common beginner mistake is writing 200 lines before compiling once. You then get 60 errors, most of them caused by the first one, and the situation feels hopeless because it is. Compile every few lines. Ten seconds of feedback beats an hour of archaeology, every time.

---

## How I introduce flags

A flag is an option you add to a command, like the `-Wall` you will meet in the Toolbench. C tooling has hundreds of them and most books either dump a magic incantation on you in chapter 1 and never explain it, or explain them all in an appendix you skip.

Neither happens here. Every flag in this book gets introduced the same way, the way `-Wall` and `-fsanitize=address` were introduced a few paragraphs ago:

1. You run the command **without** the flag and see the problem for yourself.
2. You run the identical command **with** the flag and see what changed.
3. I explain what the flag is actually doing underneath and what it costs.

You will never be told to type something you do not understand. If you catch me doing it anyway, open an issue, because I got it wrong.

By the end of the Toolbench chapter you will have earned this line one piece at a time, and you will be able to say what every part of it does:

```
gcc -std=c17 -Wall -Wextra -Wpedantic -g -o program program.c
```

And this one, which you will use whenever something smells like a memory problem:

```
gcc -std=c17 -Wall -Wextra -g -fsanitize=address,undefined -o program program.c
```

---

## Debugging is a habit, not a chapter

Most courses introduce the debugger once, in one lecture, and then quietly go back to `printf` for the rest of the term. Students take the hint and never open it again.

This book treats debugging as something you practise every single chapter, like scales. Every chapter has a section called **Break it on purpose**. I hand you a version of the chapter's program with a bug I planted, tell you the symptom, and do not tell you the cause. You find it with the tools. Then I walk you through how I would have found it, so you can compare your route to mine.

The bugs get nastier as you go, and they are the bugs that actually happen:

- An off-by-one in a loop that silently corrupts one byte.
- A `%d` where a `%f` belonged, printing garbage that looks plausible.
- A missing null terminator that makes a string print the contents of unrelated memory.
- A pointer used after the memory was freed, which works fine until the day it does not.
- A `malloc` whose return value was never checked, on a machine that ran out of memory.
- A recursive function with no base case, eating the stack until the program dies.

The goal is that by Chapter 6 your reaction to a crash is not a feeling in your stomach. It is your hands already typing `gdb ./program`. That is the actual skill. Syntax you can look up forever. Knowing how to find out what is really happening is what separates someone who can program from someone who has read about programming.

---

## How every chapter is built

Every chapter has the same eight sections in the same order. Once you have been through Chapter 1 you will know exactly where you are and what is coming.

**1. Cold open.** A specific situation with a specific cost. Somebody's program is wrong, slow, or about to leak something it should not. No abstract preamble.

**2. What you will be able to do.** A short checklist for this chapter. Come back to it at the end and test yourself honestly.

**3. First contact.** You write a working but flawed version immediately, in the first ten minutes, and run it. It produces a wrong or fragile result. Now the explanations have somewhere to land, because you have already felt the problem.

**4. Under the hood.** What is really happening in the machine. This is the section other books skip. You will use real tools to look: `gcc -S` to read the assembly your loop became, `gdb` to watch a stack frame appear and disappear, `/proc` to see your program's memory laid out while it runs.

**5. Build it properly.** The real version, in stages, compiling and running after every stage. Every code block is small enough to type by hand, and no block appears before you have run the one before it.

**6. Break it on purpose.** The planted bug. Your turn with the tools.

**7. Ship it.** Add it to the Makefile, get the build clean under full warnings, run the tests, commit it to git. Boring on purpose. Boring is how professionals work.

**8. Where people go wrong, and exercises.** The mental models that trip nearly everyone at this stage, stated plainly with the correct version next to them. Then exercises in three sizes, and a parity box mapping the chapter to CS50.

Four kinds of sidebar appear throughout:

> **Under the hood** goes one level deeper than the main text needs. Skippable on the first pass, worth returning to.

> **Debian note** covers anything specific to Debian 13, package names, or gcc version behaviour that differs from what you will find in older tutorials online.

> **Trap** marks the mistake almost everyone makes at that exact line. It is there because I made it too.

> **Parity** connects what you just did to CS50 vocabulary and problem sets.

Exercises come in three sizes so you can pace yourself:

- **Drill**: about 15 minutes, one idea, answer provided.
- **Build**: about an hour, the chapter's real problem set, answer provided but read it only after you have something working.
- **Stretch**: open-ended, no answer provided. You get a description of correct behaviour and a test file. This is the closest thing in the book to real work.

---

## Where this is up to

This book is being written in public. Nothing here is a placeholder for its own
sake: what is marked done is finished, tested, and safe to work through.

| Part | Status | Code |
|---|---|---|
| The Toolbench | **Done** | |
| How the Machine Thinks | **Done** | no code, by design |
| Chapter 1: The till that never balances | **Done** | programs and tests |
| Chapter 2: Scrubbing the log | **Done** | programs and tests |
| Chapter 3: Two million lines and a deadline | Writing | |
| Chapter 4: The file that won't fit | Planned | |
| Chapter 5: Counting unique things fast | Planned | |
| Chapter 6: Ship it | Planned | |

Every code sample in a finished chapter has been compiled and run on Debian 13
before it was written into the text, and the expected output files in each
`tests/` directory were generated from those runs.

## The map

### The Toolbench

*Before everything. About two hours.*

Set up Debian 13 and drive every tool on the bench until they are ordinary. Install the toolchain with one `apt` command and understand what each package is for. Write, compile, and run your first program. Build the house compile command one flag at a time, watching each flag catch something the previous one missed. Learn the manual pages so you can answer your own questions. Then diagnose four planted bugs, each one needing a different tool. Finish with a Makefile and your first git commit.

You come out of it with a working machine and a reflex: compile with warnings, run, judge, and reach for the right tool when something is off.

**Start here:** [`toolbench/`](toolbench/README.md)

### How the Machine Thinks

*Between the Toolbench and Chapter 1. About twenty minutes, no code.*

The only pure reading in the book. What your processor actually does and why it only understands numbers. Why the letter `A` is the number 65 and what that means for C. Why the number 0.1 cannot be stored exactly and what that costs a shop at the end of a trading day. Why compilers exist and what C refuses to do for you. And one idea about algorithms, using a phone book, which Chapter 3 will come back and give a name to.

This replaces CS50's Week 0. It exists so that nothing in Chapter 1 arrives without context.

**Read it here:** [`00-how-the-machine-thinks/`](00-how-the-machine-thinks/README.md)

### Chapter 1: The till that never balances

*(CS50 Week 1)*

A small shop's receipt program is short by a few pennies most days. Nobody can find the missing money. You will build the program, watch floating point arithmetic quietly lose value, and fix it properly by representing money as whole numbers of cents.

**You learn:** the structure of a C program and what `#include` and `main` actually mean, types and their sizes, integers versus floating point and why the difference matters commercially, operators, truncation in integer division, conditionals, loops, writing your own functions, scope, and what `printf` format specifiers really do.

**You build:** a receipt calculator that is correct to the penny, and a change-making program.

**Parity:** Mario, Cash, Credit.

### Chapter 2: Scrubbing the log

*(CS50 Week 2)*

Your team needs to send a server log to an outside vendor, and the log is full of customer email addresses. They have to come out first, and there are 40,000 lines. You will write the tool that redacts them.

**You learn:** arrays, strings as arrays of characters, the null terminator and why forgetting it is catastrophic, `argc` and `argv` for command line arguments, exit codes, reading input safely with `fgets`, and the four stages of compilation performed by hand with `-E`, `-S`, and `-c` so you can see your code at each step of its journey.

**You build:** a redaction tool, a text analyser that scores reading difficulty, and two working ciphers.

**Parity:** Readability, Caesar, Substitution.

### Chapter 3: Two million lines and a deadline

*(CS50 Week 3)*

You need the ten most requested pages from a two-million-line log, and your first working version takes long enough that you assume it has hung. It has not. It is just doing far more work than it needs to.

**You learn:** measuring your own code with `clock_gettime` before any theory arrives, linear search, binary search, selection sort, insertion sort, merge sort, recursion and how it uses the stack, `struct` for grouping related data, and the standard library's `qsort`. Big-O notation shows up only after you have measured the difference yourself, as a name for something you already understand.

**You build:** a top-ten report over real data, fast enough to run while you wait.

**Parity:** Plurality, Runoff, Tideman.

### Chapter 4: The file that won't fit

*(CS50 Week 4)*

Your log reader has been working perfectly for weeks. Then a request with a 4,000 character URL arrives, and the program corrupts its own memory and dies. The fixed-size buffer that was fine on day one is the bug.

**You learn:** hexadecimal and why everyone in systems programming uses it, pointers properly and slowly with pictures and with `gdb`, pointer arithmetic, the difference between the stack and the heap and what lives where, `malloc`, `realloc`, and `free`, memory leaks, use-after-free, Valgrind, AddressSanitizer, and file input and output.

**You build:** your own hexdump tool for reading raw bytes, a growable buffer that handles a line of any length, an image filter, and a recovery program that pulls deleted JPEGs off a corrupted memory card image.

**Parity:** Volume, Filter, Recover.

### Chapter 5: Counting unique things fast

*(CS50 Week 5)*

Counting unique visitors by comparing every address against every address already seen takes minutes on real data and gets worse every day. You will make it take under a second, and you will measure each step so the improvement is a number rather than a claim.

**You learn:** linked lists and pointer-to-pointer manipulation, why an array is the wrong shape for this problem, hash functions and what makes one good, collisions and how to survive them, load factor and resizing, freeing an entire data structure without leaking, plus stacks, queues, and a working tour of trees and tries.

**You build:** a hash table from scratch, and a spell checker that loads a 140,000 word dictionary and checks a novel in well under a second.

**Parity:** Speller, including its timing harness.

### Chapter 6: Ship it

*(Capstone)*

No new syntax. This chapter is about turning code that works on your machine into a product that works on someone else's.

You write the specification first, then assemble the tool from parts you already built: argument parsing with real validation, error handling that never fails silently, streaming input that handles a file bigger than your memory, the hash table from Chapter 5, the top-N logic from Chapter 3, a `--help` that reads like a proper manual page, a Makefile with debug and release targets, a shell test suite that runs every case in one command, a clean Valgrind run, and a tagged release on GitHub with a README somebody else could follow.

Then you hand it to a friend and watch them break it in ninety seconds, which is the most useful ninety seconds in the book.

---

## What you will be holding at the end of Chapter 6

One program, called `logtool`, that you wrote every line of.

It reads a web server access log, either from a file you name or from standard input so it can be piped into. It streams the file rather than loading it, so a 10 GB log works on a machine with 2 GB of memory. It parses each line into fields, counts unique visitors with your own hash table, reports the most requested endpoints and the busiest hours, and handles flags like `--top 20`, `--since`, and `--format csv`.

When you give it a file that does not exist, it says so clearly and exits with a code a shell script can check. When it meets a malformed line it reports the line number and keeps going instead of dying. It compiles with zero warnings under `-Wall -Wextra -Wpedantic`. It runs clean under Valgrind with zero bytes leaked. It has a test suite you can run with `make test`, and a `make release` target that builds an optimised binary.

You will not have built it in Chapter 6. You will have built it across the whole book, one piece per chapter, which is why finishing it is realistic rather than a heroic effort at the end.

Sample logs come with the repository, including some deliberately awful ones.

---

## How to use this repository

```
to-c-or-not-to-c/
├── README.md                    you are here
├── PUBLISHING.md                how to verify a chapter and push it
├── LICENSE                      how you may use the text and the code
├── toolbench/
│   └── README.md                set up your machine
├── 00-how-the-machine-thinks/
│   └── README.md                short reading, no code
├── ch01-the-till/
│   ├── README.md                the chapter text
│   ├── code/                    every program in the chapter
│   │   ├── steps/               the small versions, in order
│   │   └── bugs/                the four planted bugs
│   └── tests/                   expected output, and the test runner
├── ch02-scrubbing-the-log/
│   ├── README.md                the chapter text
│   ├── code/                    every program in the chapter
│   ├── data/                    the sample access log
│   └── tests/                   expected output, and the test runner
├── ch03-two-million-lines/
├── ch04-the-file-that-wont-fit/
├── ch05-counting-unique-things/
├── ch06-ship-it/
└── tools/
    ├── check-book.py        verifies the book against itself
    └── verify-on-debian.sh  checks the claims that need a real Debian box
```

Chapters 3 to 6 currently hold a stub describing the scenario and what it
teaches. The directories fill out as each chapter is written.

Get a copy:

```
$ git clone https://github.com/dralikma/to-c-or-not-to-c.git
$ cd to-c-or-not-to-c
```

Read each chapter's `README.md`. Type the code into your own files rather than running the ones in `code/`. Those are there so you can compare when something will not work, not so you can skip the typing.

You can read the chapters here on GitHub in your browser, which is the easiest way. You can also read them in a terminal with `less`, or convert them to PDF or EPUB with `pandoc` if you want them on a tablet. The chapters are plain Markdown with no special extensions, so anything that reads Markdown will render them.

---

## House rules

These are not decoration. Each one exists because breaking it is a known way to waste a month.

**Type the code. Do not copy and paste it.** Typing forces you to read every character. You will make typos, the compiler will complain, and you will learn to read compiler errors, which is a skill you need far more than you need the fifteen seconds you saved. This is the rule people break most and regret most.

**Run every single snippet.** If a code block is in this book, it is because running it teaches you something that reading it does not.

**Compile after every few lines.** Not after every function. Not after every file. Every few lines.

**Never scroll past a warning.** A warning is the compiler saying "this is legal but I am fairly sure you did not mean it." It is usually right. Fix it before you move on.

**Sit with an error before you search for it.** Read the message. All of it, and the first error first, since later errors are often just wreckage from the first. Then look at the line, then the line above. Give it a genuine five minutes before you paste it into a search engine or an AI. That five minutes is where the learning is.

**Commit at the end of every session.** Even broken code. Especially broken code. `git commit -m "loop still off by one, stopping here"` costs you eight seconds and means you can always get back.

**A note on AI assistants.** They will write all of this code for you instantly and correctly. If you let them, you will finish the book and be able to do none of the things in the list at the top. Use them the way you would use a knowledgeable friend: ask them to explain a concept you are stuck on, ask them why an error message says what it says, ask them to review code you already wrote. Do not ask them for the answer. You are not trying to produce a working `logtool`. Working `logtool` binaries are worthless. You are trying to become someone who can write one.

---

## When you get stuck

You will get stuck. Everyone does, permanently, forever. Getting unstuck is a procedure, and here it is.

**If it will not compile:**

1. Read the **first** error, not the last. Later errors are usually consequences.
2. Look at the line it names. Then look at the line above it. A missing semicolon or brace reports itself on the following line.
3. Check the obvious four: semicolons, matching braces, matching parentheses, matching quotes.
4. Check that you included the header for every function you called. `printf` needs `stdio.h`. `strlen` needs `string.h`.
5. If gcc's wording means nothing to you, compile the same file with `clang` and read its version of the complaint.

**If it compiles but the output is wrong:**

1. Do not guess. Run it under `gdb`, set a breakpoint before the suspicious part, and print the variables.
2. Check your format specifiers. `%d` for `int`, `%f` for `float` and `double`, `%s` for strings, `%c` for a single character, `%lu` for `size_t`.
3. Check your loop boundaries. `<` and `<=` are different by exactly one, and that one is the most common bug in this book.

**If it crashes, or works sometimes:**

1. Rebuild with `-fsanitize=address,undefined` and run it again. This finds the cause perhaps four times out of five, immediately.
2. If that comes up clean, run it under `valgrind ./program`.
3. If it crashed, `gdb ./program`, then `run`, then `backtrace` when it dies.

**If none of that worked**, open an issue on this repository. Include what you expected, what happened, the exact error text copied and pasted, and the smallest program that still shows the problem. Producing that smallest program solves the bug on its own surprisingly often, and when it does not, it is the only kind of question anyone can actually answer.

---

## What I changed from CS50, and why

The scope, sequence, and problem sets follow CS50x weeks 1 through 5 closely, so parity is real. A few deliberate departures:

**No CS50 library, at all.** The course provides a helper library with functions like `get_string` and a `string` type. It smooths the first two weeks and then becomes a wall, because `string` is not a C type, it never was, and no C code anywhere outside that course uses it. Learners hit real C and discover that a chunk of what they learned was scaffolding. This book uses real C from line one: `char *` is a `char *`, and you read input with `fgets`. It is slightly harder in Chapter 1 and considerably easier from Chapter 3 onward, because nothing has to be unlearned.

**No Scratch.** CS50 spends Week 0 dragging coloured blocks to teach loops and conditionals without syntax in the way. It is a good idea in a lecture hall and a detour in a book you are reading alone. The conceptual load of that week lives in **How the Machine Thinks**, which sits between the Toolbench and Chapter 1 and takes twenty minutes.

**Local machine, not a cloud IDE.** CS50 gives you a preconfigured VS Code in the browser. This book has you build the bench yourself on Debian, which costs two hours and buys you a machine you understand and a skill that outlives any one course.

**Debugging in every chapter.** The course introduces the debugger and moves on. Here it is a recurring section with planted bugs, so it becomes a habit rather than a fact you once heard.

**Under the hood in every chapter.** The compiler pipeline, stack frames, heap layout, and pointer arithmetic get shown with real tools rather than described. This is the main thing this book adds.

**One project across the whole book.** CS50's problem sets are self-contained, which is right for a course with graders. For someone learning alone, having one artifact that visibly grows is a much stronger reason to open the book on a Tuesday night. All the CS50 problem sets are still here as exercises.

**A shipping chapter.** The gap between "my code works" and "my code is a thing another person can use" is where most self-taught programmers stall. Chapter 6 is that gap, on purpose.

---

## Feedback and license

If something is unclear, wrong, or does not work on your machine, open an issue. Confusion is a bug in the book, not a bug in you, and knowing where readers snag is the only way this gets better.

**If you are editing the book**, [`PUBLISHING.md`](PUBLISHING.md) is the whole
routine on one page: the three commands, what each proves, the per-chapter
checklist, and the git workflow. The short version is to run the checker before
you push:

```
$ python3 tools/check-book.py
All 27 checks passed.
```

It verifies the things that go wrong silently. Every internal link. Every count
the prose claims, so a heading cannot say "two keys" over a list of three. That
`code/receipt.c` still matches the listing printed in the chapter. That the line
number the gdb walkthrough breaks on is still the line it says it is. And that
the test suite passes.

All four of those had already broken at least once during writing, and not one
was caught by reading, because reading is exactly what does not catch them.

There is a second script for the claims a checker cannot settle on its own:

```
$ bash tools/verify-on-debian.sh
```

The book's `gdb` sessions, `valgrind` output, and `clang` comparisons need those
programs installed to be checked, and the machine the book was written on did
not have them. This script runs each of those sessions for real and prints what
your machine says, so you can compare it against what the book claims. Anything
that differs is a bug in the book.

The prose is licensed CC BY-NC-SA 4.0, so you may share it, translate it, and
build on it, as long as you credit it, do not sell it, and pass the same freedom
on. All the code is MIT, so you may take it anywhere at all, including into
commercial work. See [`LICENSE`](LICENSE) for the details and the reasoning.

Now go to [the Toolbench](toolbench/README.md) and set up your machine. It takes about two hours and you will write your first C program partway through.
