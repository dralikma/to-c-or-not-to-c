# To C or not to C

A hands-on C book for people who have never written a line of code, built around the C material from Harvard's CS50x.

Not affiliated with Harvard or CS50. It follows the same shape and covers the same ground, because that shape works.

---

## Why this exists

Most books that teach programming teach you which words to type. You type them, something appears on screen, and you move on with a vague feeling that magic happened somewhere in the middle.

That feeling doesn't go away on its own. It turns into a ceiling.

I wrote this because I got tired of watching people hit that ceiling and conclude they weren't cut out for it. They usually were. Nobody had shown them what was under the floor.

So this book keeps taking the floor up. When you write a variable, you'll see where it lives in memory. When you compile, you'll run the compiler one stage at a time and read what falls out of each one. When your program crashes, you won't guess. You'll attach a debugger, walk the thing line by line, and watch the exact moment it goes wrong.

Nothing here asks you to take my word for it.

## What you'll actually be able to do

Not "understand." Not "be familiar with." Do. If you finish this and can't do these, the book failed you and I'd like to hear about it.

- Write, compile and run a C program on Debian from a terminal, with no IDE holding your hand.
- Read a compiler error and know which line to look at, including the ones that point at the wrong line.
- Explain what happens between typing `gcc` and getting a program, and run each of the four stages separately.
- Pick the right type for a piece of data and say what it costs in bytes and what it can't hold.
- Use pointers on purpose: pass by reference, walk an array, ask for memory, give it back exactly once.
- Find a memory bug with AddressSanitizer or Valgrind and fix the cause rather than the symptom.
- Step through a running program in `gdb`, inspect variables, break on a condition, read a backtrace after a crash.
- Write linear search, binary search, selection sort, insertion sort and merge sort from scratch, and say which one you'd reach for.
- Build a linked list, a hash table, a stack and a queue, and free every byte you asked for.
- Read a file bigger than your available memory, one line at a time, without falling over.
- Handle command line arguments, reject bad input, and return an exit code a script can check.
- Write a Makefile with separate debug and release builds.
- Test your own program automatically, and keep it under version control.

Come back to that list at the end and be honest with yourself. Anything you can't do, go back and redo that part. It's cheaper now than it will be later.

## Who I wrote it for

You're an adult who has never programmed, or who has poked at some Python and wants to know what's underneath. You can open a terminal, change directory, list files, and edit a file without help. If `cd`, `ls`, `mkdir` and `nano` mean something to you, that's enough.

You don't need maths beyond arithmetic. There's one chapter where we count how long things take, and the heaviest idea in it is that doubling the size of a list roughly doubles the work for one approach and adds a single step to another. That's the whole of it.

You do need patience with the terminal. C doesn't come with a friendly playground. The terminal is the playground. By the end of the Toolbench you'll be comfortable there, and by Chapter 3 you'll prefer it.

This book won't suit you if you want a website or a phone app by Friday. C is a bad tool for both. What C gives you is the layer everything else sits on. Learn it and Python stops being a mystery box, because you'll know what's in the box. It doesn't work the other way round.

## What you need

A machine running **Debian 13 (trixie)**. A virtual machine is fine. A Raspberry Pi is fine. An old laptop you rescued from a drawer is more than fine.

About 2 GB of disk for the toolchain and the sample data. Two to four hours a week, and the willingness to type code instead of pasting it.

Everything else is free software you'll install with one `apt` command in the Toolbench. Nothing here costs money and nothing needs an account.

On Ubuntu the commands are identical. On Fedora or Arch, swap `apt` for your package manager and the rest holds. On macOS most of it works, but `gdb` and Valgrind fight with Apple's security model, so run Debian in a VM and save yourself an evening.

## The bench

Six tools do the work on your code and two more keep the work from becoming a chore. That's the whole bench. No IDE, no framework, no plugin ecosystem.

**The terminal** is where you run things. It's the only interface that shows you the command, the exact output, and the exit status all at once. Buttons hide the evidence. Everything in this book happens here.

**The editor** is where you write. C source is plain text, so `nano` is plenty and it'll never get between you and the work. Use `vim` or VS Code if you already know them. The book never depends on which you picked.

**The compiler** is `gcc`. It's also your first line of defence, and this is the part beginners waste. It'll name whole classes of mistake before your program runs, but only if you ask, and asking is a matter of flags. Its default output filename is `a.out`, which is a terrible name it has been using since 1971 and shows no sign of stopping.

**The sanitizer** catches what the compiler can't see, the bugs that only exist while the program runs. C will happily let you read memory that isn't yours and carry on as though nothing happened. AddressSanitizer stops at the exact instruction and names the variable you overran. Valgrind does a related job by a different route and catches memory you asked for and forgot to give back.

**The debugger** is `gdb`, and it lets you watch your program think. Stop on a line, look at any variable, run one line at a time, and after a crash ask which chain of calls got you there. Without it, your only window into a running program is `printf`, which works in roughly the sense that hitting a nail with a rock works.

**The judge** is `diff`. "It looks right" isn't a test. It's an opinion formed by a tired person at 11pm who already believes the code works. `diff` has no opinions and doesn't skim, which is how it catches the trailing space your eyes can't see.

Then two that aren't about C at all. **`make`** remembers the compile command so you stop retyping it and stop quietly dropping flags when you're in a hurry. **`git`** takes snapshots so a bad hour is never a lost week.

The Toolbench installs all eight and teaches each one by showing you what life looks like without it. It also puts `clang` on the shelf as a second compiler, purely so you have another phrasing to read when gcc's wording means nothing to you.

## The loop

Almost everything you do in this book is one turn of this cycle.

```
        write  ->  compile  ->  run  ->  judge
          ^           |          |         |
          |           |          |         |
          +-----------+----------+---------+
                    debug
```

Write a small piece. Small. One behaviour.

Compile it with warnings on. If the compiler complains, fix it now, before running anything. Warnings aren't noise to scroll past.

Run it and see what it does.

Judge the output against what it should be, with `diff` rather than your own eyes.

If it's wrong, debug. Sanitizer for memory, `gdb` for logic. Find the cause. Don't patch the symptom.

Then back to the top with the next small piece.

The most common beginner mistake is writing 200 lines before compiling once. You then get 60 errors, most of them caused by the first one, and it feels hopeless because it is. Compile every few lines. Ten seconds of feedback beats an hour of archaeology.

## How I introduce flags

A flag is an option you add to a command, like `-Wall`. C tooling has hundreds of them, and most books either dump a magic incantation on you in chapter one and never explain it, or bury them in an appendix you skip.

I do neither. Every flag in this book arrives the same way.

You run the command **without** it and watch the problem happen. You run the identical command **with** it and see what changed. Then I explain what it's actually doing and what it costs.

You'll never be told to type something you don't understand. If you catch me doing it anyway, open an issue, because I got it wrong.

By the end of the Toolbench you'll have earned this line one piece at a time and be able to say what every part of it does:

```
gcc -std=c17 -Wall -Wextra -Wpedantic -g -o program program.c
```

And this one, for when something smells like a memory problem:

```
gcc -std=c17 -Wall -Wextra -g -fsanitize=address,undefined -o program program.c
```

## Debugging is a habit, not a chapter

Most courses introduce the debugger once, in one lecture, then quietly go back to `printf` for the rest of the term. Students take the hint and never open it again.

Here you practise it every chapter, like scales. Every chapter has a section called **Break it on purpose** where I hand you a program with a bug I planted, tell you the symptom, and don't tell you the cause. You find it with the tools. Then I walk through how I'd have found it, so you can compare your route to mine.

The bugs get nastier and they're the ones that actually happen. An off-by-one that silently corrupts a byte. A `%d` where a `%f` belonged, printing garbage that looks plausible. A missing null terminator that makes a string print somebody else's memory. A pointer used after the memory was freed, which works fine until the day it doesn't. A `malloc` whose return value nobody checked. Recursion with no base case, eating the stack until the program dies.

What I'm after is that by Chapter 6 your reaction to a crash isn't a feeling in your stomach. It's your hands already typing `gdb ./program`.

That's the actual skill. Syntax you can look up forever. Knowing how to find out what's really happening is what separates someone who can program from someone who has read about programming.

## How every chapter is built

Every chapter has the same eight sections in the same order. After Chapter 1 you'll know exactly where you are and what's coming.

**1. Cold open.** A specific situation with a specific cost. Somebody's program is wrong, slow, or about to leak something it shouldn't.

**2. What you'll be able to do.** A short checklist. Come back at the end and test yourself honestly.

**3. First contact.** You write a working but flawed version in the first ten minutes and run it. It produces something wrong or fragile. Now the explanations have somewhere to land, because you've felt the problem.

**4. Under the hood.** What's really happening in the machine, shown with real tools rather than described. `gcc -S` to read the assembly your loop became. `gdb` to watch a stack frame appear and vanish. `/proc` to see your program's memory while it runs.

**5. Build it properly.** The real version, in stages, compiling and running after each one. Every block is small enough to type, and no block appears before you've run the one before it.

**6. Break it on purpose.** The planted bug. Your turn.

**7. Ship it.** Add it to the Makefile, get a clean build under full warnings, run the tests, commit. Boring on purpose. Boring is how professionals work.

**8. Where people go wrong, and exercises.** The mental models that trip nearly everybody at that stage, stated plainly with the correct version beside them. Then exercises in three sizes, and a box mapping the chapter to CS50.

Four kinds of sidebar turn up throughout:

> **Under the hood** goes a level deeper than the main text needs. Skippable on a first read, worth coming back to.

> **Debian note** is anything specific to Debian 13, a package name, or gcc behaviour that differs from what you'll find on the internet.

> **Trap** is the mistake almost everybody makes at that exact line. It's there because I made it too.

> **Parity** connects what you just did to CS50's vocabulary and problem sets.

Exercises come in three sizes so you can pace yourself. **Drill** is fifteen minutes on one idea, answer provided. **Build** is about an hour, the chapter's real problem set, answer provided but don't read it until you have something working. **Stretch** is open-ended with no answer at all: you get a description of correct behaviour and a test file, which is the closest thing here to real work.

## Where this is up to

I'm writing this in public. Nothing here is a placeholder for its own sake. What's marked done is finished, tested, and safe to work through.

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

Every code sample in a finished chapter was compiled and run on Debian 13 before it went into the text, and the expected output files in each `tests/` directory came from those runs.

## The map

There are eight parts. They go in order and each one leans on the last.

### The Toolbench

*Before everything. About two hours.*

Set up Debian and drive all eight tools until they're ordinary. Install the toolchain with one `apt` command and understand what each package is for. Write, compile and run your first program. Build the house compile command one flag at a time, watching each flag catch something the one before it missed. Learn the manual pages so you can answer your own questions. Then diagnose four planted bugs, each needing a different tool. Finish with a Makefile and your first commit.

You come out with a working machine and a reflex: compile with warnings, run, judge, and reach for the right tool when something's off.

**Start here:** [`toolbench/`](toolbench/README.md)

### How the Machine Thinks

*Twenty minutes, no code.*

The only pure reading in the book. What your processor actually does and why it only understands numbers. Why the letter `A` is the number 65. Why 0.1 can't be stored exactly and what that costs a shop at the end of a trading day. Why compilers exist and what C refuses to do for you. And one idea about algorithms that Chapter 3 comes back and measures.

This replaces CS50's Week 0. It's here so nothing in Chapter 1 arrives without context.

**Read it here:** [`00-how-the-machine-thinks/`](00-how-the-machine-thinks/README.md)

### Chapter 1: The till that never balances

*(CS50 Week 1)*

A bakery's receipt program is short a few pennies most days and nobody can find the missing money. You'll build it, watch floating point quietly lose value, and fix it properly by holding money as whole numbers of cents.

**You learn:** the structure of a C program and what `#include` and `main` actually mean, types and their sizes, integers against floating point and why the difference matters commercially, operators, truncation, conditionals, loops, your own functions, scope, and what `printf` format specifiers really do.

**You build:** a receipt calculator correct to the penny, and a change-making program.

**Parity:** Mario, Cash, Credit.

### Chapter 2: Scrubbing the log

*(CS50 Week 2)*

Your team needs to send a 40,000 line server log to an outside consultancy, and 400 of those lines have a customer's email address sitting in the URL. Delete them and you've removed the pages the consultancy needs. So the addresses come out and everything else stays.

**You learn:** arrays, strings as arrays of characters, the null terminator and why forgetting it is catastrophic, `argc` and `argv`, exit codes, reading input safely with `fgets`, `strlen` and `ctype`, and the four stages of compilation taken apart by hand with `-E`, `-S` and `-c`.

**You build:** a redaction tool that reads standard input and writes standard output, a reading-level scorer, and two working ciphers.

**Parity:** Readability, Caesar, Substitution.

### Chapter 3: Two million lines and a deadline

*(CS50 Week 3)*

You need the ten most requested pages from a two-million-line log, and your first working version takes long enough that you'll assume it has hung. It hasn't. It's doing far more work than it needs to.

**You learn:** measuring your own code with `clock_gettime` before any theory arrives, linear and binary search, selection, insertion and merge sort, recursion and how it uses the stack, `struct`, and the standard library's `qsort`. Big-O notation shows up only after you've measured the difference yourself.

**You build:** a top-ten report over real data, fast enough to run while you wait.

**Parity:** Plurality, Runoff, Tideman.

### Chapter 4: The file that won't fit

*(CS50 Week 4)*

Your log reader has worked perfectly for weeks. Then a request with a 4,000 character URL arrives and the program corrupts its own memory and dies. The fixed-size buffer that was fine on day one is the bug.

**You learn:** hexadecimal, pointers properly and slowly with pictures and with `gdb`, pointer arithmetic, the stack and the heap, `malloc`, `realloc` and `free`, leaks, use-after-free, Valgrind, AddressSanitizer, and file input and output.

**You build:** your own hexdump tool, a growable buffer that handles a line of any length, an image filter, and a program that recovers deleted JPEGs from a corrupted memory card.

**Parity:** Volume, Filter, Recover.

### Chapter 5: Counting unique things fast

*(CS50 Week 5)*

Counting unique visitors by comparing every address against every address already seen takes minutes on real data and gets worse every day. You'll make it take under a second, and measure each step so the improvement is a number rather than a claim.

**You learn:** linked lists and pointer-to-pointer work, why an array is the wrong shape here, hash functions and what makes one good, collisions, load factor, resizing, freeing a whole structure without leaking, plus stacks, queues, trees and tries.

**You build:** a hash table from scratch, and a spell checker that loads a 140,000 word dictionary and checks a novel in well under a second.

**Parity:** Speller, with its timing harness.

### Chapter 6: Ship it

*(Capstone)*

No new syntax. This one is about turning code that works on your machine into a product that works on somebody else's.

You write the specification first, then assemble `logtool` from parts you already built: argument parsing with real validation, error handling that never fails silently, streaming input that copes with a file bigger than your memory, the hash table from Chapter 5, the top-N logic from Chapter 3, a `--help` that reads like a manual page, a Makefile with debug and release targets, a shell test suite, a clean Valgrind run, and a tagged release with a README somebody else could follow.

Then you hand it to a friend and watch them break it in ninety seconds, which is the most useful ninety seconds in the book.

## What you'll have at the end

One program, called `logtool`, that you wrote every line of.

It reads a web server access log, either from a file you name or from standard input so it can be piped into. It streams rather than loading, so a 10 GB log works on a machine with 2 GB of memory. It parses each line into fields, counts unique visitors with your own hash table, reports the most requested endpoints and the busiest hours, and handles flags like `--top 20`, `--since` and `--format csv`.

Give it a file that doesn't exist and it says so clearly and exits with a code a shell script can check. Feed it a malformed line and it reports the line number and keeps going instead of dying. It compiles with zero warnings under `-Wall -Wextra -Wpedantic`. It runs clean under Valgrind with zero bytes leaked. It has a test suite you run with `make test` and a `make release` target that builds an optimised binary.

You won't build it in Chapter 6. You'll have built it across the whole book, one piece per chapter, which is why finishing it is realistic instead of heroic.

Sample logs come with the repository, including some deliberately awful ones.

## Getting the book

```
$ git clone https://github.com/dralikma/to-c-or-not-to-c.git
$ cd to-c-or-not-to-c
```

```
to-c-or-not-to-c/
├── README.md                    you are here
├── STYLE.md                     how this book is written, and why
├── LICENSE                      how you may use the text and the code
├── toolbench/
│   └── README.md                set up your machine
├── 00-how-the-machine-thinks/
│   └── README.md                short reading, no code
├── ch01-the-till/
│   ├── README.md                the chapter text
│   ├── code/                    every program in the chapter
│   └── tests/                   expected output, and the test runner
├── ch02-scrubbing-the-log/
│   ├── README.md
│   ├── code/
│   ├── data/                    the sample access log
│   └── tests/
├── ch03-two-million-lines/
├── ch04-the-file-that-wont-fit/
├── ch05-counting-unique-things/
├── ch06-ship-it/
└── tools/
    └── verify-on-debian.sh      checks your machine matches the book
```

Chapters 3 to 6 currently hold a stub describing the scenario and what it teaches. The directories fill out as each chapter is written.

Read each chapter's `README.md`, on GitHub in your browser or in a terminal with `less`. They're plain Markdown with no extensions, so `pandoc` will turn them into PDF or EPUB if you'd rather read on a tablet.

Type the code into your own files. The ones in `code/` are there so you can compare when something won't work, not so you can skip the typing.

Once the Toolbench has you set up, this is worth running once:

```
$ bash tools/verify-on-debian.sh
```

It checks that the tools the book assumes are installed and that the `gdb` sessions printed in the chapters match what your machine actually says. Anything that disagrees is a bug in the book, and I'd like to know about it.

## House rules

These aren't decoration. Each one is here because breaking it is a known way to waste a month.

**Type the code. Don't paste it.** Typing forces you to read every character. You'll make typos, the compiler will complain, and you'll learn to read compiler errors, which you need far more than the fifteen seconds you saved. This is the rule people break most and regret most.

**Run every snippet.** If a code block is in this book, running it teaches you something reading it doesn't.

**Compile after every few lines.** Not after every function. Not after every file.

**Never scroll past a warning.** A warning is the compiler saying "this is legal but I'm fairly sure you didn't mean it," and it's usually right.

**Sit with an error before you search for it.** Read the message, all of it, and read the first error first, since later ones are often wreckage from the first. Then look at the line, then the line above. Give it five real minutes before you paste it into a search engine or an AI. Those five minutes are where the learning is.

**Commit at the end of every session.** Even broken code, especially broken code. `git commit -m "loop still off by one, stopping here"` costs eight seconds and means you can always get back.

**About AI assistants.** They'll write all of this for you, instantly and correctly. Let them and you'll finish the book able to do none of the things in the list at the top. Use one the way you'd use a knowledgeable friend: ask it to explain a concept you're stuck on, ask why an error says what it says, ask it to review code you already wrote. Don't ask it for the answer. You're not trying to produce a working `logtool`. Working `logtool` binaries are worthless. You're trying to become somebody who can write one.

## When you're stuck

You will get stuck. Everybody does, permanently, forever. Getting unstuck is a procedure and here it is.

**If it won't compile.** Read the first error, not the last, since later ones are usually consequences. Look at the line it names, then the line above it, because a missing semicolon or brace reports itself on the following line. Check semicolons, matching braces, matching parentheses, matching quotes. Check you included the header for every function you called: `printf` needs `stdio.h`, `strlen` needs `string.h`. If gcc's wording means nothing to you, compile the same file with `clang` and read its version of the complaint.

**If it compiles but the output is wrong.** Don't guess. Run it under `gdb`, break before the suspicious part, print the variables. Check your format specifiers: `%d` for `int`, `%f` for `float` and `double`, `%s` for strings, `%c` for one character, `%zu` for `size_t`. Check your loop boundaries, because `<` and `<=` differ by exactly one and that one is the most common bug in this book.

**If it crashes, or works sometimes.** Rebuild with `-fsanitize=address,undefined` and run it again. That finds the cause outright maybe four times out of five. If it comes up clean, try `valgrind ./program`. If it crashed, `gdb ./program`, then `run`, then `backtrace` when it dies.

**If none of that worked**, open an issue. Include what you expected, what happened, the exact error text pasted rather than described, and the smallest program that still shows the problem. Producing that smallest program solves the bug on its own surprisingly often, and when it doesn't, it's the only kind of question anybody can actually answer.

## What I changed from CS50, and why

The scope, sequence and problem sets follow CS50x weeks 1 to 5 closely, so the parity is real. A few departures are deliberate.

**No CS50 library, at all.** The course ships a helper library with `get_string` and a `string` type. It smooths the first fortnight and then becomes a wall, because `string` isn't a C type, never was, and no C code outside that course uses it. Learners hit real C and find that a chunk of what they learned was scaffolding. This book uses real C from line one. `char *` is a `char *`, and you read input with `fgets`. Slightly harder in Chapter 1, considerably easier from Chapter 3 on, because nothing has to be unlearned.

**No Scratch.** Week 0 drags coloured blocks to teach loops without syntax in the way. Good idea in a lecture hall, detour in a book you work through alone. That week's ideas live in How the Machine Thinks, which takes twenty minutes.

**Your own machine, not a cloud IDE.** CS50 gives you a preconfigured VS Code in the browser. Here you build the bench yourself on Debian. It costs two hours and buys you a machine you understand and a skill that outlives any one course.

**Debugging in every chapter.** The course introduces the debugger and moves on. Here it's a recurring section with planted bugs, so it becomes a habit rather than a fact you once heard.

**Under the hood in every chapter.** The compiler pipeline, stack frames, heap layout and pointer arithmetic get shown with real tools rather than described. This is the main thing I've added.

**One project across the whole book.** CS50's problem sets are self-contained, which is right for a course with graders. Working alone, having one artifact that visibly grows is a much stronger reason to open the book on a Tuesday night. All the problem sets are still here as exercises.

**A shipping chapter.** The gap between "my code works" and "my code is something another person can use" is where most self-taught programmers stall. Chapter 6 is that gap, on purpose.

## Feedback and licence

If something's unclear, wrong, or doesn't work on your machine, open an issue. Confusion is a bug in the book rather than a bug in you, and knowing where readers snag is the only way this gets better.

The prose is under CC BY-NC-SA 4.0, so you can share it, translate it and build on it as long as you credit it, don't sell it, and pass the same freedom on. All the code is MIT, so take it anywhere at all, including into commercial work. [`LICENSE`](LICENSE) has the details and the reasoning.

Now go to [the Toolbench](toolbench/README.md) and set up your machine. It takes about two hours and you'll write your first C program partway through.
