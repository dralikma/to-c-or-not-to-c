# Chapter 2: Scrubbing the log

*CS50x Week 2. Six to eight hours, spread over as many sittings as you like. You need Chapter 1 finished.*

---

## Forty thousand lines, and one of them will get you sued

Maria's bakery has a website now. People order sourdough for collection, they sign up for the newsletter, they unsubscribe from the newsletter, and the whole thing has been getting slower every month.

So she's hired a small consultancy to work out why. They asked for one thing: the web server's access log for the last thirty days. It's a plain text file, one line per request, about forty thousand lines. It records who asked for what page and how long the server took.

You open it to check before sending. Line two says this:

```
192.168.4.11 - - [07/Sep/2026:08:15:03] "GET /orders?email=hana.k@example.com HTTP/1.1" 200 1204
```

There's a customer's email address sitting in the middle of it.

It's there because the ordering page passes the address in the URL, and the web server writes URLs into the log. Nobody designed that. It just happened, the way most of these things happen.

Now count. Around four hundred of those forty thousand lines have an address in them. The consultancy is a legitimate business and will almost certainly do nothing wrong with the file. That isn't the point. The point is that the moment you attach it to an email, four hundred of Maria's customers have had their personal data handed to a third party they never agreed to, and under the data protection law in most of the world that's a reportable breach with Maria's name on it.

You can't just delete those four hundred lines either. They're the ordering and signup pages, which are exactly the slow ones. Strip them and the consultancy is analysing the wrong website.

So the addresses come out and everything else stays. Four hundred times, without missing one, in a file too big to check by eye.

That's this chapter. By the end you'll have written the tool, and along the way you'll find out what a piece of text actually is inside your program, which is the thing Chapter 1 kept promising and couldn't deliver.

## What you'll be able to do at the end

- Explain what happens between typing `gcc` and getting a program, in four named stages, and run each stage separately.
- Read the assembly your C became, find your own loop in it, and explain why nobody writes it by hand.
- Declare an array, put values in it, read them back, and say exactly what happens when you go past the end.
- Explain what a string really is in C, and why `"Hi!"` takes four bytes rather than three.
- Find the end of a piece of text without being told how long it is.
- Write a function that takes text as an input, which is the thing Chapter 1 left you unable to do.
- Use `strlen`, and explain why calling it in a loop condition is a small crime.
- Read lines of input safely with `fgets`, check its return value, and deal with the newline it leaves behind.
- Classify and convert characters with `isalpha`, `isdigit`, `isspace` and `toupper`, and do the same arithmetic yourself when you want to.
- Take arguments from the command line with `argc` and `argv`, and validate them.
- Return a meaningful exit code and check it from the shell.
- Build a text tool that reads standard input and writes standard output, the way every Unix tool does.

## How this chapter goes

Same five parts as Chapter 1, and they build in order.

**Part 1** writes a working, honest, useless redactor. It reads the log, tries to hide the addresses, and fails in a way you can see.

**Part 2** takes the lid off `gcc`. Four stages, run one at a time, with the output of each in front of you. No new C at all, just looking.

**Part 3** is the C. Arrays, strings, the null terminator, `char *`, the string and character libraries, command line arguments, exit codes. Then the real redactor.

**Part 4** hands you four broken programs.

**Part 5** ships it with a Makefile, a test and a commit.

---

## Part 1: First contact

### Get the log

The sample log lives in this chapter's directory. It's twelve lines rather than forty thousand, so you can see the whole thing at once and check the work by eye while you're learning.

```
$ mkdir -p ~/toc/ch02
$ cd ~/toc/ch02
$ cp ~/to-c-or-not-to-c/ch02-scrubbing-the-log/data/access.log .
$ cat access.log
```

```
192.168.4.11 - - [07/Sep/2026:08:14:22] "GET /menu HTTP/1.1" 200 4821
192.168.4.11 - - [07/Sep/2026:08:15:03] "GET /orders?email=hana.k@example.com HTTP/1.1" 200 1204
10.0.0.7 - - [07/Sep/2026:08:15:44] "GET /menu HTTP/1.1" 200 4821
10.0.0.7 - - [07/Sep/2026:08:16:10] "GET /basket HTTP/1.1" 200 3310
172.16.2.9 - - [07/Sep/2026:08:17:02] "POST /signup?email=t.oyelaran@mail.example HTTP/1.1" 302 0
192.168.4.11 - - [07/Sep/2026:08:18:31] "GET /menu HTTP/1.1" 200 4821
10.0.0.7 - - [07/Sep/2026:08:19:57] "GET /share?from=ines@example.org&to=jp.mbeki@example.net HTTP/1.1" 200 512
172.16.2.9 - - [07/Sep/2026:08:20:14] "GET /menu HTTP/1.1" 200 4821
203.0.113.5 - - [07/Sep/2026:08:21:40] "GET /basket HTTP/1.1" 200 3310
10.0.0.7 - - [07/Sep/2026:08:22:03] "GET /unsubscribe?email=w.tanaka@example.com HTTP/1.1" 200 88
203.0.113.5 - - [07/Sep/2026:08:23:19] "GET /menu HTTP/1.1" 200 4821
192.168.4.11 - - [07/Sep/2026:08:24:55] "GET /basket HTTP/1.1" 200 3310
```

Four lines have addresses in them. Look at line seven, because it's the one that'll catch you out later. It has two.

### Reading it, one line at a time

Every program you wrote in Chapter 1 had its data typed into the source code. This one can't. The data is a file, and the file is bigger than the program.

The tool for that is `fgets`. Open a new file, `redact.c`, and type this:

```c
#include <stdio.h>

int main(void)
{
    char line[1024];

    while (fgets(line, sizeof line, stdin) != NULL)
    {
        printf("%s\n", line);
    }

    return 0;
}
```

Four new things in there. Take them one at a time, because all four turn up in every program for the rest of the book.

**`char line[1024]`** sets aside room for 1024 characters and calls the whole lot `line`. That's an **array**, and it's the main subject of Part 3. For now, read it as "room for a long line of text."

**`fgets`** reads one line and puts it there. It takes three things: where to put the text, how much room is available, and where to read from.

**`sizeof line`** is that middle argument. You met `sizeof` in Chapter 1 asking how many bytes a type takes. Here it asks how many bytes the array takes, which is 1024. Writing `sizeof line` rather than `1024` means that if you later make the box bigger, this line updates itself. Two places that have to agree is one place too many.

**`stdin`** is standard input, which the Toolbench introduced as the channel a program reads from. By default that's your keyboard. Use `<` at the shell and it's a file instead, and the program can't tell the difference and doesn't need to.

**`!= NULL`** is how you know when to stop. `fgets` hands back `NULL`, a special value meaning "nothing," when there's no more input. So the loop reads lines until the file runs out. This is your first `while` loop where the number of passes is genuinely unknown in advance, which is exactly what `while` is for.

Compile and run it. Note the `<`, which tells the shell to feed the file in as standard input:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o redact redact.c
$ ./redact < access.log
```

```
192.168.4.11 - - [07/Sep/2026:08:14:22] "GET /menu HTTP/1.1" 200 4821

192.168.4.11 - - [07/Sep/2026:08:15:03] "GET /orders?email=hana.k@example.com HTTP/1.1" 200 1204

10.0.0.7 - - [07/Sep/2026:08:15:44] "GET /menu HTTP/1.1" 200 4821

```

Every line has a blank line after it. The log didn't look like that.

### The first thing text does that numbers never did

Here's the cause, and it's worth pausing on because it's the first hint that text has a shape nobody has told you about.

`fgets` reads a line including the newline character at the end of it. That newline is part of the file. It's what makes the file have lines at all. So when `fgets` hands you a line, the `\n` comes along with it.

Then your `printf("%s\n", line)` adds a second one.

You can see this rather than take my word for it. `cat -A` shows invisible characters and marks the end of each line with `$`, the same trick the Toolbench used to catch a trailing space:

```
$ ./redact < access.log | cat -A | head -4
```

```
192.168.4.11 - - [07/Sep/2026:08:14:22] "GET /menu HTTP/1.1" 200 4821$
$
192.168.4.11 - - [07/Sep/2026:08:15:03] "GET /orders?email=hana.k@example.com HTTP/1.1" 200 1204$
$
```

The lone `$` on its own line is the newline you added, sitting on a line with nothing else on it.

The fix is to stop adding one:

```c
        printf("%s", line);
```

Recompile, run, and the output matches the log exactly.

```
$ ./redact < access.log | diff - access.log && echo "identical"
identical
```

That `-` in the middle of the `diff` command means "read from standard input instead of a file," so you're comparing your program's output against the original without saving anything. A useful trick, and one you'll use constantly from here.

Your program now reads a log and copies it out unchanged. Sounds like nothing. It's actually the shape of every Unix text tool ever written: read standard input, do something, write standard output. Everything else in this chapter is filling in the "do something."

### Now hide the addresses

The addresses all contain an `@`. Nothing else in the log does. So the obvious first move is to find every `@` and replace it with something harmless.

Add this inside the loop, before the `printf`:

```c
        for (int i = 0; line[i] != '\0'; i++)
        {
            if (line[i] == '@')
            {
                line[i] = '*';
            }
        }
```

Two things there are new and one of them is a genuine surprise.

**`line[i]`** reaches into the array and gets the character at position `i`. The square brackets are how you get at one item out of many, and positions count from zero, exactly as loop counters have since Chapter 1. That's why the habit mattered.

**`line[i] != '\0'`** is the loop's stopping condition, and it's the surprise. It says "keep going while the character here isn't `'\0'`." That thing in single quotes is one character, and it's the answer to a question you haven't asked yet: how does the loop know where the line ends? Part 2 answers it properly. For now, copy it and notice that it works.

Note the single quotes around `'@'` and `'*'` and `'\0'`. Chapter 1 said single quotes mean one character and double quotes mean text, and warned the difference would bite. Here's where it starts to matter, because `line[i]` is a single character and can only be compared against a single character.

Compile and run:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o redact redact.c
$ ./redact < access.log
```

```
...
192.168.4.11 - - [07/Sep/2026:08:15:03] "GET /orders?email=hana.k*example.com HTTP/1.1" 200 1204
...
172.16.2.9 - - [07/Sep/2026:08:17:02] "POST /signup?email=t.oyelaran*mail.example HTTP/1.1" 302 0
...
10.0.0.7 - - [07/Sep/2026:08:19:57] "GET /share?from=ines*example.org&to=jp.mbeki*example.net HTTP/1.1" 200 512
...
```

That isn't redaction. That's an email address with one character changed. `hana.k*example.com` identifies exactly the same person `hana.k@example.com` does, and anybody who has seen an email address before can read it.

### Why the obvious next step doesn't work either

Fine, replace more. Replace the `@` and the ten characters after it, say.

You can't, and the reason is the whole chapter.

Look at what has to happen. To hide `hana.k@example.com` you have to find where it starts, which is six characters to the left of the `@`, and where it ends, which is eleven to the right. Those numbers are different for every address in the file. `ines@example.org` starts four to the left. `t.oyelaran@mail.example` starts ten to the left.

So you can't count. You have to look. You have to walk left from the `@` one character at a time asking "is this still part of an address?" until the answer is no, then walk right doing the same.

Which means you need three things you currently can't do. Move around inside a piece of text one character at a time, forwards and backwards. Ask a character what kind of character it is. And know for certain where the text stops, so walking right doesn't walk off the end into whatever's next in memory.

None of those are hard. All three depend on knowing what a piece of text actually is, which nobody has told you. Chapter 1 handed you `"Sourdough loaf"` and said keep text inside `printf` calls and don't ask questions.

Time to ask.

---

## Part 2: Under the hood

No new C in this part. Half an hour of taking the lid off `gcc` and looking at what it does, one stage at a time. You won't need to remember the details. You will need to stop thinking of compilation as a single magic step, because from Chapter 4 onward the difference between the stages is the difference between an error you fix in ten seconds and one you stare at for an hour.

### `gcc` is four programs wearing one coat

Since the Toolbench you've typed variations on this:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o hello hello.c
```

and got a program out. The Toolbench mentioned in passing that four things happen in there. Now you run them yourself.

Make a fresh file to work with. Small, so the output stays readable:

```c
#include <stdio.h>

int main(void)
{
    printf("Hello, world!\n");
    return 0;
}
```

```
$ wc -l hello.c
7 hello.c
```

Seven lines. Remember that number.

### Stage 1: the preprocessor

The preprocessor handles everything beginning with `#`. It doesn't understand C at all. It's a text substitution machine, and its main job is `#include`.

`#include <stdio.h>` means "find the file `stdio.h` and paste the whole thing here." Not a reference, not a link. Paste.

The `-E` flag says "stop after preprocessing and show me the result":

```
$ gcc -std=c17 -E hello.c > hello.i
$ wc -l hello.i
548 hello.i
```

Your number will differ, because it depends on your gcc and C library versions. Mine says 548. Yours might say 700. The point is the same either way.

Your seven lines became several hundred. All of `stdio.h` is now sitting at the top of your file, and everything `stdio.h` itself includes is sitting above that.

Look at the end of it, where your own code finally turns up:

```
$ tail -7 hello.i
```

```
# 3 "hello.c"
int main(void)
{
    printf("Hello, world!\n");
    return 0;
}
```

Your code, untouched, at the bottom of a large pile of other people's declarations. That's what `#include` does.

Now look at what came with it:

```
$ grep "int printf" hello.i
```

```
extern int printf (const char *__restrict __format, ...);
```

There's `printf`'s prototype. Chapter 1 taught you prototypes: a function's name, what goes in, what comes out, ending in a semicolon instead of a body. This is exactly that, for `printf`, written by whoever wrote the C library, and pasted into your file by the preprocessor a moment ago.

That's the whole reason `#include <stdio.h>` exists. Without it the compiler reaches line 5, meets `printf`, has never heard of it, and on gcc 14 refuses to build. With it, the prototype arrives first and the compiler knows what to check your call against.

The header doesn't contain the code for `printf`. Only the description. Where the code lives is stage 4.

> **Trap: `stdio.h` isn't `studio.h`.** Every year a non-zero number of people lose twenty minutes to this. There's no `u`. It's short for standard input and output.

### Stage 2: the compiler proper

Now the actual translation, from C into the processor's own language. `-S` stops after this stage:

```
$ gcc -std=c17 -S hello.c -o hello.s
$ wc -l hello.s
45 hello.s
```

Open `hello.s` and it'll look alarming. It's **assembly language**, a readable spelling of the numeric instructions your processor actually runs. There's one of these languages per processor family, and the one on your machine is x86-64.

You aren't going to learn it. You're going to look at it once so it stops being mysterious, and then never open it again unless you take a course on computer architecture.

Two things are worth finding.

```
$ grep -nE "main:|\.string|call" hello.s
```

```
5:	.string	"Hello, world!"
9:main:
20:	call	puts@PLT
```

Your text is in there, on line 5, exactly as you typed it. And there's `main`, on line 9, with the name you gave it.

But look at line 20. You wrote `printf`, and the assembly calls `puts`.

That isn't a mistake. `puts` is a simpler function that prints a string and adds a newline, and gcc noticed your `printf` had no placeholders in it and ended in `\n`, which makes it exactly a `puts`. So it quietly swapped in the cheaper one.

That's your first sighting of the compiler being cleverer than the code you wrote. It happens constantly and it's why the assembly doesn't always match your source line for line.

> **Try it yourself.** Put a `%s` in that `printf` and pass it something, recompile with `-S`, and `grep` again. The `puts` becomes a `printf`, because now there's formatting to do and the shortcut no longer applies.

### Finding your own loop

The Toolbench ended with a Stretch exercise asking you to find a loop in the assembly. Here it is properly. Write `count.c`:

```c
#include <stdio.h>

int main(void)
{
    for (int i = 0; i < 3; i++)
    {
        printf("%d\n", i);
    }

    return 0;
}
```

```
$ gcc -std=c17 -S count.c -o count.s
```

Strip out the bookkeeping lines and the middle of `main` looks like this:

```
	movl	$0, -4(%rbp)      set i to 0
	jmp	.L2               go and test the condition first
.L3:
	...
	call	printf@PLT        the body of the loop
	addl	$1, -4(%rbp)      i++
.L2:
	cmpl	$2, -4(%rbp)      compare i against 2
	jle	.L3               if less than or equal, jump back to .L3
```

Read it top to bottom and your `for` loop is right there, taken apart into its four pieces.

`movl $0` is the initialisation. `.L3` is a **label**, a name for a place in the code you can jump back to, and it marks the body. `addl $1` is the increment. `cmpl` then `jle` is the condition, and `jle` means "jump if less than or equal."

There's no `for` here. There's no loop instruction at all. A loop, at this level, is a comparison and a jump backwards. That's all a loop has ever been.

Notice one detail: you wrote `i < 3` and the machine compares against 2 with "less than or equal." Same thing, and the compiler picked whichever suited the instruction it had.

Notice a second: the very first thing it does is `jmp .L2`, straight to the test, before running the body at all. That's the compiler making sure a loop whose condition is false from the start runs zero times, which is exactly what `for` promises.

> **Your assembly may differ from mine.** Different gcc versions make different choices, and so does a different processor. The shape will be the same: set up, jump to a test, a labelled body, an increment, a comparison, a jump back.

### Stage 3: the assembler

Assembly is readable text. Your processor can't read text. Stage three converts one to the other. `-c` stops here:

```
$ gcc -std=c17 -c hello.c -o hello.o
$ file hello.o
hello.o: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), not stripped
```

That `.o` is an **object file** and it holds the actual machine instructions. Try to read it and you get nonsense, because it isn't text. But `strings` pulls out any runs of readable characters that happen to be inside:

```
$ strings hello.o | head -3
```

```
Hello, world!
GCC: (Debian 14.2.0-19) 14.2.0
hello.c
```

Your message is in there, sitting in a file that's otherwise unreadable.

The word **relocatable** in that `file` output is the important one. This object file isn't a program and you can't run it. Try:

```
$ ./hello.o
bash: ./hello.o: cannot execute binary file: Exec format error
```

It contains your compiled code and a list of things it still needs from elsewhere. `printf` is one of them. Nobody has told it where `printf` lives.

### Stage 4: the linker

The last stage takes your object file, finds the compiled code for every function you called but didn't write, and joins them into one runnable program.

```
$ gcc hello.o -o hello
$ ./hello
Hello, world!
```

Note there's no `.c` in that command. The compiling is already done. This is purely assembly of the parts.

The code for `printf` came from the C library, compiled by somebody else years ago and sitting on your machine already. The linker found it and stitched it in.

And this is the error you already met. In Chapter 1 you called `round` and got this:

```
/usr/bin/ld: /tmp/ccbIIt9I.o: in function `main':
two.c:8: undefined reference to `round'
```

Now you can read it exactly. `/usr/bin/ld` is the linker. Your code compiled perfectly, produced an object file with a note saying "I need something called `round`," and the linker went looking, wasn't given the maths library, and couldn't find it. `-lm` is how you hand it the extra library to search.

`undefined reference` always means stage four. The compiler was happy. Something you called has no code behind it.

> **Why your program is 16 KB and not 800 KB.** The C library is large and your program used one function out of it. Most systems link it **dynamically**, meaning the linker writes down "I need `printf` from the C library" and the real code is found when the program starts, shared with every other running program that wants it. The alternative, **static** linking, copies the code into your file, giving a bigger program that depends on nothing at runtime. Both are in use, you don't have to choose today, and it's worth having the words.

### The whole pipeline, in one table

Run all four by hand and compare:

```
$ ls -l hello.c hello.i hello.s hello.o hello
```

| File | Stage | What it is | Size |
|---|---|---|---|
| `hello.c` | you wrote it | C source | 84 bytes |
| `hello.i` | preprocessed | C source plus all of `stdio.h` | 14,880 bytes |
| `hello.s` | compiled | assembly text | 668 bytes |
| `hello.o` | assembled | machine code, incomplete | 1,504 bytes |
| `hello` | linked | a program you can run | 15,960 bytes |

Your byte counts will differ. Watch the shape: it balloons at preprocessing, shrinks hard at compilation because all those declarations produced no code, and grows again at linking because the C library's actual instructions arrive.

Every one of those stages happens every time you run `gcc`. It cleans up the intermediate files afterwards so you never see them.

### Can you run it backwards?

If C becomes machine code, can machine code become C?

Partly, and less usefully than you'd hope. Tools exist that read machine code and produce something C-like. What they can't recover is everything that was never in the machine code to begin with.

Your variable names are gone. `subtotal` and `x` compile identically. Your comments are gone, thrown away by the preprocessor before the compiler even looked. And the structure is ambiguous: a `for` loop, a `while` loop and a `do while` loop can all compile to the same comparison and jump, so nothing in the output tells you which you wrote.

You'd get something that behaves the same and reads like it was written by nobody. For a small program that's enough to understand it. For anything the size of a real application, working out what those instructions mean would take longer than writing the program yourself, which is roughly the bet commercial software makes.

Worth knowing this is specific to compiled languages. Later in your career you'll meet JavaScript, which ships as source to every browser that asks. Anyone can read it. Different trade, made on purpose.

### Two ways to see inside a running program

While the lid's off, one more thing that belongs here.

You've got a debugger, and the Toolbench and Chapter 1 both made you use it. There are two more techniques, both older and cruder, and both used constantly by people who know better.

The first costs nothing and sounds ridiculous. Explain the broken code, out loud, line by line, to something that can't help you. A colleague works. So does a houseplant. Traditionally it's a rubber duck, which is why programmers call this **rubber duck debugging**.

It works because explaining forces you to say what each line does, and somewhere in that you'll say a sentence you don't believe. That's the bug. Reading code silently lets your eye slide over the line you assumed was fine. Saying it aloud doesn't. Nowadays people do this to an AI, which talks back, and that's fine as long as you're the one doing the explaining. The moment you ask it for the answer instead, you've skipped the part that was going to work.

The second is `printf`. When something in a loop is wrong and you don't know which pass, put a line in that prints what you want to know:

```c
    for (int i = 0; i < 3; i++)
    {
        printf("[debug] i is %d\n", i);
        printf("#\n");
    }
```

```
[debug] i is 0
#
[debug] i is 1
#
[debug] i is 2
#
```

That's it. No tool, no breakpoints, no learning curve. You saw a version of it in Chapter 1 when a single `%.20f` revealed the croissant price wasn't what anybody thought it was.

`printf` is the right choice when the question is "does this line even run," or "what is this value on each pass," and you want the answer in five seconds. When the bug happens somewhere in a thousand iterations and you want to see the shape of all thousand at once. When the program is fast and you want to run it fifty times with small changes.

The debugger is the right choice when you don't yet know which variable is wrong, so there's nothing specific to print. When the program crashes and you need a backtrace. When you want to stop on one condition out of many, which `gdb` does with `break 38 if part == 266` and `printf` can't do at all without editing and recompiling. And when the value you want is in a function you didn't write.

The two aren't rivals. Reach for `printf` first because it costs nothing, and switch to `gdb` the moment you find yourself adding a fourth print statement.

> **Where the word "bug" comes from.** Not from the moth, although the moth is real. In 1947 the team running the Harvard Mark II found an actual moth caught in a relay, taped it into the logbook, and wrote "first actual case of bug being found." The joke only works because engineers had already been calling faults bugs for decades; Thomas Edison used the word that way in 1878. Grace Hopper, who was on that team and did much to spread the story, is worth reading about for considerably better reasons than the moth.

One discipline. Mark your debug output so you can find it again. Every `printf` in this book that exists to debug says `[debug]` at the front, and that isn't decoration. When you're done, `grep -n "\[debug\]" *.c` finds every one in seconds so none of them ship. A stray debug line in delivered output has failed more automated tests than almost anything else.

Now back to the log.

---

## Part 3: Build it properly

### One name for many values

Imagine Maria wants to average three exam scores. In Chapter 1 you'd write:

```c
    int score1 = 72;
    int score2 = 73;
    int score3 = 33;

    printf("Average: %f\n", (score1 + score2 + score3) / 3.0);
```

Correct, and it falls apart the moment there are four scores. You add a variable, then you have to remember to add it to the sum as well. With ten scores it's unmaintainable. With a hundred it's absurd.

What you want is one name that holds all of them. That's an **array**: a run of values, all of the same type, sitting next to each other in memory.

```c
    int scores[3];
```

Read it as "set aside room for three `int`s and call the lot `scores`." The square brackets and the number say how many.

Put values in and take them out with the same brackets, this time holding a **position**:

```c
    scores[0] = 72;
    scores[1] = 73;
    scores[2] = 33;

    printf("Average: %f\n", (scores[0] + scores[1] + scores[2]) / 3.0);
```

Positions count from zero. The first is `scores[0]`, the second is `scores[1]`, the third is `scores[2]`. There is no `scores[3]`.

That's jarring at first and there's a real reason for it, which arrives in Chapter 4. For now, notice the payoff: it's exactly why Chapter 1 insisted you write `for (int i = 0; i < 3; i++)` rather than counting from one. That loop produces 0, 1, 2, which are precisely the valid positions. The habit was being built for this moment.

```c
    for (int i = 0; i < 3; i++)
    {
        printf("Score %d is %d\n", i, scores[i]);
    }
```

`scores[i]` uses the loop counter as the position, so one line of code touches every element. That's the entire point of arrays.

You can also fill one at the moment you create it:

```c
    int scores[3] = {72, 73, 33};
```

### `#define`, and a promise from Chapter 1 kept

The number 3 now appears in the declaration, the loop and the division. Chapter 1 called that a magic number and told you to name it with `const`. Try it:

```c
    const int N = 3;
    int scores[N];
```

```
error: variably modified 'scores' at file scope
```

Chapter 1 warned you about exactly this in a Trap: a `const` in C is a read-only variable rather than a value the compiler can substitute in, so it can't be used as an array size. It said the tool for that job is `#define`, and here's that job.

```c
#define N 3

int main(void)
{
    int scores[N] = {72, 73, 33};
    ...
```

`#define N 3` is a preprocessor instruction, which you now know exactly how to picture. Before the compiler sees anything, the preprocessor walks your file and replaces every `N` with `3`. By compile time there's no `N`. There never was.

You can prove that with the tool from Part 2:

```
$ gcc -std=c17 -E scores.c | tail -6
```

The `N` is gone from the output, replaced by `3` everywhere it appeared.

Two conventions. `#define` has no semicolon and no `=`, because it isn't a statement, it's a substitution. And names go in capitals for the same reason `const` ones did: so a reader can tell at a glance that this is fixed.

### Going past the end

There's no `scores[3]`. What happens if you ask for it anyway?

```c
    int scores[3] = {72, 73, 33};
    printf("%d\n", scores[3]);
```

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o scores scores.c
$ ./scores
0
```

No warning. No crash. A number.

You've seen this before in the Toolbench, and it's worth meeting again now that you know what an array is. C doesn't check. It works out where `scores` starts, jumps three `int`s along, reads four bytes, and hands them to you. Whatever's sitting there is what you get.

Today it's a harmless 0. In a bigger program those bytes belong to another variable, and reading them means reading data that isn't yours. Writing to them means silently corrupting something that'll fail much later, somewhere unrelated.

The sanitizer makes it loud, exactly as it did before:

```
$ gcc -std=c17 -Wall -Wextra -g -fsanitize=address -o scores scores.c
$ ./scores
=================================================================
==5183==ERROR: AddressSanitizer: stack-buffer-overflow
READ of size 4 at 0x7ffd21c0a58c thread T0
    #0 in main /home/you/toc/ch02/scores.c:8

  This frame has 1 object(s):
    [32, 44) 'scores' (line 7) <== Memory access at offset 44 overflows this variable
```

Twelve bytes for three `int`s, and you touched byte 44, the first one past the end. This is the most common serious bug in C, and the loop convention exists to prevent it. `i < 3` never produces 3. `i <= 3` does.

### What an array looks like in memory

Everything so far describes arrays by how you use them. Here's what one actually is, because from Chapter 4 onward you need this picture and it's easier to build now while the examples are small.

How the Machine Thinks said memory is a very long run of bytes. Give every byte a number, counting from the start, and that number is its **address**.

When you write:

```c
    int scores[3] = {72, 73, 33};
```

the machine sets aside twelve bytes in a row, because an `int` is four bytes and you asked for three of them. If the first byte happens to be at address 1000, the picture is this:

```
 address:  1000      1004      1008
          +---------+---------+---------+
 scores:  |   72    |   73    |   33    |
          +---------+---------+---------+
            [0]       [1]       [2]
```

In a row is the important part. That's what "array" means and it's why `scores[i]` is fast: the machine doesn't search for element `i`, it multiplies. Element `i` starts at 1000 plus `i` times 4. One addition and one multiplication, however big the array is.

It's also, finally, why counting starts at zero. `scores[0]` is at the start plus nothing. The index isn't "which one" so much as how far from the beginning, and the first element is no distance at all. Once you read it that way, counting from zero stops being an oddity.

And it explains `scores[3]`. There's nothing to stop the machine computing 1000 plus 3 times 4 and reading the four bytes at 1012. Those bytes exist. They belong to something else. C hands them over without comment.

A string is the same picture with one-byte elements:

```
 address:  2000 2001 2002 2003 2004 2005
          +----+----+----+----+----+----+
   word:  | H  | i  | !  | \0 |    |    |
          +----+----+----+----+----+----+
            [0]  [1]  [2]  [3]
```

Four bytes used out of however many you declared, and the fourth is the marker that says stop.

### What's in an array before you put anything there

One consequence of that picture is worth meeting head on, because it produces bugs that look like magic.

```c
#include <stdio.h>

int main(void)
{
    int scores[3];
    char word[8];

    printf("scores holds: %d %d %d\n", scores[0], scores[1], scores[2]);
    printf("word[0] is:   %d\n", word[0]);

    return 0;
}
```

```
$ ./garbage
scores holds: 0 1112517360 32620
word[0] is:   80

$ ./garbage
scores holds: 0 -775456016 32513
word[0] is:   -48
```

Same program, run twice, different answers.

Setting aside memory doesn't clean it. Those twelve bytes were used by something else a moment ago, and whatever bits that left behind are what you're now reading as integers. Programmers call this a **garbage value**, and the defining feature is that it isn't reliably anything. It isn't zero. It isn't random in a useful way. It's leftovers.

You've met this twice already without the name. In the Toolbench, `gdb` showed `total` holding 21845 before the line that set it had run. In Chapter 1, `info locals` showed `coffee` and `oil` holding 0 before the program reached them, and I said that today it prints as 0 and won't always. This is why.

`-Wall` does catch the simple cases. Compile that program and gcc says so before you ever run it:

```
garbage.c:16:5: warning: 'scores' is used uninitialized [-Wuninitialized]
garbage.c:17:38: warning: 'word' is used uninitialized [-Wuninitialized]
```

What it can't catch is the general case, because whether a variable was set often depends on which way an `if` went at runtime, and the compiler can't know that.

The habit is the fix: give every variable a value when you declare it, and every array too if you're going to read from it before filling it.

```c
    int scores[3] = {0};
```

That sets the first element to 0 and, because of a rule about partial initialisation, fills the rest with zeros as well. For a string, `char word[8] = "";` does the same job.

### Giving an array to a function

Chapter 1 said every argument in C is a copy, and proved it: a function that changed its parameter left the caller's variable untouched.

Arrays break that rule, and it isn't a small exception.

```c
#include <stdio.h>

void zero_out(int values[], int count);

int main(void)
{
    int scores[3] = {72, 73, 33};

    zero_out(scores, 3);

    printf("%d %d %d\n", scores[0], scores[1], scores[2]);
    return 0;
}

void zero_out(int values[], int count)
{
    for (int i = 0; i < count; i++)
    {
        values[i] = 0;
    }
}
```

```
0 0 0
```

`main`'s array was changed by another function. With an `int` that couldn't happen. With an array it does.

The parameter is written `int values[]`, with empty brackets, because the function isn't told how big the array is. It can't be. So you have to pass the length as a second argument, which is why `count` is there. Forget it and there's no way for the function to know where to stop, and no warning if you guess wrong.

Why arrays behave differently is Chapter 4's subject. The short version, which is true and which you should hold on to: an array parameter is a way in to the caller's array rather than a copy of it. Chapter 4 explains the mechanism and it'll make complete sense then.

For now, two practical consequences. A function that takes an array can change your data, which is sometimes exactly what you want and is what the redactor will do, and is sometimes a nasty surprise. And an array parameter always needs a length parameter beside it. Always, unless the array is a string, and the next section is about why strings get to be the exception.

### A string is an array of characters

Here's the sentence this chapter has been walking towards.

A **string** is an array of `char`, with one extra rule.

You already believe half of that. A `char` holds one character. Chapter 1 proved a `char` is really a small number, with `'A'` being 65. An array is a run of values of one type. So a run of `char`s is a run of characters, which is text.

Write `peek.c` and see for yourself:

```c
#include <stdio.h>

int main(void)
{
    char word[10] = "Hi!";

    printf("as a string:  %s\n", word);
    printf("as numbers:   %d %d %d %d\n", word[0], word[1], word[2], word[3]);
    printf("as chars:     %c %c %c\n", word[0], word[1], word[2]);

    return 0;
}
```

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o peek peek.c
$ ./peek
as a string:  Hi!
as numbers:   72 105 33 0
as chars:     H i !
```

One array, printed three ways. `%s` prints the whole thing as text. `%c` prints one position as a character. `%d` prints that same position as the number it actually is.

72, 105, 33 are `H`, `i`, `!` in ASCII, exactly as Chapter 1 promised.

### The extra rule, and the zero at the end

Now look at the fourth number. You put three characters in. Position 3 holds **0**.

That zero is the extra rule, and it answers the question Part 1 left hanging: how does anything know where the text ends?

An array doesn't carry its length around. `zero_out` above had to be told. But `printf("%s", word)` was told nothing and still stopped in exactly the right place.

It stopped because C marks the end of a string with a byte containing zero. `printf` walks forward printing characters until it hits that zero, then stops. Your loop in Part 1 did the same thing with `line[i] != '\0'`, which you copied without explanation. Now you know what it says: keep going until you reach the marker.

That byte is the **null terminator**, written `'\0'` in code. The backslash marks it as a special character, the same way `'\n'` is a newline. It isn't the digit zero, which is the character `'0'` and has the value 48. It's the number 0.

Which means:

```c
    char word[10] = "Hi!";
```

occupies four bytes of that array, not three. Three for the letters and one for the marker. The double quotes are what put it there. Writing `"Hi!"` in C means "these three characters, followed by a null terminator, please."

That's why Chapter 1 insisted single and double quotes are different types rather than a style choice. `'H'` is one byte. `"H"` is two: the letter and the terminator.

> **Trap: leave no room for the terminator and everything still looks fine.**
>
> ```c
> char word[3] = {'H', 'i', '!'};
> printf("The word is %s and it is %zu characters\n", word, strlen(word));
> ```
>
> Three characters, three slots, no room for the marker. It compiles clean under every warning we have, and it runs:
>
> ```
> The word is Hi! and it is 3 characters
> ```
>
> Correct, by luck. The next byte in memory happened to be zero. Change anything nearby and it stops being correct, at a moment unrelated to the bug.
>
> ```
> $ gcc -std=c17 -Wall -Wextra -g -fsanitize=address -o word word.c
> $ ./word
> ==576==ERROR: AddressSanitizer: stack-buffer-overflow
> READ of size 4 at 0x7f146fb00023 thread T0
>     #0 in strlen
>     #1 in main /home/you/toc/ch02/word.c:7
> ```
>
> `strlen` walked off the end looking for a terminator that was never written. Always leave room, or better, use double quotes and let C count for you.

### Finally: a function that takes text

Chapter 1 ended with an itch. Six items on a receipt, three near-identical lines of code each, and no way to write the one function that would collapse them, because you couldn't write down the type of a parameter that holds text.

You can now, because you know what text is.

```c
void shout(char text[])
{
    for (int i = 0; text[i] != '\0'; i++)
    {
        printf("%c", toupper(text[i]));
    }
    printf("\n");
}
```

`char text[]` is an array parameter with empty brackets, exactly like `int values[]` above. And notice what's missing: no length parameter. A string doesn't need one, because it carries its own end marker. That's what the terminator buys you.

```c
    shout("sourdough loaf");
```

```
SOURDOUGH LOAF
```

There's the thing you couldn't do in Chapter 1. Go back to `receipt.c` afterwards and collapse those eighteen lines into six.

One more spelling to recognise. You'll see that same parameter written like this:

```c
void shout(char *text)
```

`char *text` and `char text[]` mean the same thing in a parameter list. Both mean "text that lives somewhere else and that this function can reach." The `*` version is far more common in real code, so get used to seeing it.

What the `*` actually says is Chapter 4, and I'm not going to hand-wave it now. Read it for the moment as "the type for a piece of text," use whichever spelling you prefer, and know the honest explanation is coming.

### `strlen`, and calling it once

You could write the length-finding loop yourself. In fact do, once, because it's four lines and it makes the terminator concrete:

```c
int string_length(char text[])
{
    int n = 0;

    while (text[n] != '\0')
    {
        n++;
    }

    return n;
}
```

Walk forward, counting, stop at the marker. `"Hi!"` gives 3, because the terminator is where you stop rather than something you count.

Now throw it away. The C library has done this since before you were born, in a header called `string.h`:

```c
#include <string.h>

    printf("%zu\n", strlen("Hi!"));
```

```
3
```

`strlen` gives back a `size_t`, the unsigned counting type you met with `sizeof` in Chapter 1, so print it with `%zu`.

And now a real point about design. Look at this loop:

```c
    for (int i = 0; i < strlen(text); i++)
```

It's correct and it's wasteful. The condition is checked before every single pass, which means `strlen` runs before every single pass, which means the string is walked from the beginning every time. For a line of 100 characters that's 100 walks of 100 characters. For a 40,000 line log it's real time spent on an answer that never changes.

The compiler may or may not spot that the string isn't changing. Don't rely on it. Ask once:

```c
    int n = strlen(text);

    for (int i = 0; i < n; i++)
```

Or declare both in the loop header, which keeps `n` where it belongs:

```c
    for (int i = 0, n = strlen(text); i < n; i++)
```

The first slot of a `for` runs exactly once, so `strlen` is called exactly once. Both variables have to be the same type, which they are.

Chapter 3 is entirely about this kind of thing. Whether the code works is settled by then. The question becomes how much work you asked the machine to do.

### The rest of the string library

`strlen` is one function out of a couple of dozen in `string.h`. Three more are worth knowing now, and one of them is worth being afraid of.

**`strcmp` compares two strings.** You can't use `==`, and the reason follows directly from the memory picture. A string is an array, and its name stands for where it starts. So `a == b` asks whether the two are in the same place rather than whether they say the same thing. Two identical words stored separately are in different places, so the answer is false.

```c
    if (strcmp(argv[1], "Ali") == 0)
    {
        printf("Hello, boss\n");
    }
```

`strcmp` walks both strings comparing characters and returns 0 when they're identical. Zero meaning "no difference," the same convention as exit codes and as `diff`. Read `strcmp(a, b) == 0` in your head as "if there's no difference between a and b" and it stops feeling backwards.

When they differ it returns a negative or positive number depending on which comes first alphabetically, which is exactly what a sorting routine needs. That matters in Chapter 3.

**`strcspn` finds the first character from a set.** This is the one that strips the newline `fgets` leaves behind:

```c
    line[strcspn(line, "\n")] = '\0';
```

It gives the position of the first newline, or the position of the terminator if there isn't one, and overwriting that position with a terminator ends the string there. Safe either way, which is why it's the standard idiom.

**`strcpy` copies one string into another, and it's a loaded gun.**

```c
    char small[8];
    strcpy(small, "this is far too long to fit");
```

Eight bytes of room, twenty-eight bytes of text. `strcpy` doesn't know how big the destination is, because an array doesn't carry its size, so it writes all twenty-eight and keeps going into whatever's next.

Here the size is visible at compile time and gcc catches it:

```
cpy.c:7:5: warning: '__builtin_memcpy' writing 28 bytes into a region of size 8
overflows the destination [-Wstringop-overflow=]
```

Change the source to something the compiler can't see the length of, a line read from a file for instance, and that warning disappears while the danger doesn't. Then only the sanitizer finds it:

```
==666==ERROR: AddressSanitizer: stack-buffer-overflow
WRITE of size 28 at 0x7f7452500028 thread T0
```

Note the word WRITE. Reading past the end of an array gives you nonsense. Writing past the end corrupts whatever was there, and that's how a large fraction of the security holes in the world got made.

You don't need `strcpy` in this chapter and I'd rather you learned the suspicion than the function. Chapter 4 shows the safe way, once you can ask for memory of the right size in the first place.

### `fgets`, properly

You used `fgets` in Part 1 on trust. Here's what it actually does, because three of its behaviours will catch you.

```c
    char line[MAX_LINE];

    while (fgets(line, sizeof line, stdin) != NULL)
```

It returns `NULL` when there's no more input. That's your loop's exit. Ignore the return value and you'll loop forever on an empty file, using whatever was left in `line` from last time.

It keeps the newline. You found that in Part 1 when everything double-spaced. `strlen` counts it too:

```c
    char line[64];
    fgets(line, sizeof line, stdin);
    printf("strlen says %zu\n", strlen(line));
    printf("last char is %d\n", line[strlen(line) - 1]);
```

```
$ printf 'David\n' | ./len
strlen says 6
last char is 10
```

Six, not five. And the last character is 10, which is `'\n'` in ASCII. When you need the text without it, `strcspn` from a moment ago is the standard removal.

The redactor doesn't need that, because it puts the line straight back out and the newline belongs there.

And it won't overrun your array, which is the whole reason to prefer it. That second argument is a promise it keeps. What it does instead, when a line is longer than the space you gave it, is read as much as fits and leave the rest for the next call, which silently turns one long line into two short ones. That's Chapter 4's opening problem and it's why `MAX_LINE` is a lie you're telling yourself. For a log with lines under 200 characters, 1024 is fine.

> **A word about `scanf`, from Chapter 1.** Chapter 1 used `scanf` for numbers and promised something better. This is it. `fgets` reads a whole line into a buffer you control, tells you when input ends, and can't be made to overrun. From here on this book reads input with `fgets` and converts to numbers afterwards when it needs to.

### Asking a character what it is

The redactor has to decide, for each character, whether it could be part of an email address. Doing that by hand is tedious and easy to get wrong:

```c
    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9'))
```

That works, and it works because characters are numbers in a sensible order, so `>=` and `<=` do what you'd hope. But `ctype.h` has already written it:

| Function | True when the character is |
|---|---|
| `isalpha(c)` | a letter |
| `isdigit(c)` | a digit |
| `isalnum(c)` | a letter or a digit |
| `isspace(c)` | a space, tab, or newline |
| `isupper(c)` / `islower(c)` | an upper or lower case letter |
| `toupper(c)` / `tolower(c)` | converts, leaving anything else alone |

```c
#include <ctype.h>

    printf("isalpha('7') = %d   isdigit('7') = %d\n", isalpha('7') != 0, isdigit('7') != 0);
    printf("toupper('d') gives %c\n", toupper('d'));
```

```
isalpha('7') = 0   isdigit('7') = 1
toupper('d') gives D
```

The `!= 0` is there because these functions promise only "zero or non-zero," rather than "0 or 1." Compare against zero rather than against 1.

### The 32 that runs the alphabet

Worth doing once by hand, because it explains something about ASCII that keeps being useful.

```c
    printf("'a' is %d, 'A' is %d, apart by %d\n", 'a', 'A', 'a' - 'A');
    printf("'d' - 32 gives %c\n", 'd' - 32);
```

```
'a' is 97, 'A' is 65, apart by 32
'd' - 32 gives D
```

Every lowercase letter is exactly 32 above its uppercase twin, all the way through the alphabet, because whoever laid out ASCII in the 1960s put the two runs 32 apart on purpose.

So `toupper` could be written `c - 32`. It shouldn't be, for two reasons. It's wrong for anything that isn't a lowercase letter, turning `'5'` into something meaningless. And `c - 32` tells a reader nothing, while `toupper(c)` tells them everything.

If you ever do want the arithmetic, write `c - ('a' - 'A')` rather than `c - 32`. It computes the same thing and says why.

### Arguments from the command line

Every program you've written takes no input except through `stdin`. But you've been giving programs arguments since the Toolbench:

```
$ gcc -o hello hello.c
$ diff mine.txt expected.txt
```

`-o`, `hello`, `hello.c`, `mine.txt` are **command line arguments**: extra words typed after the program's name that change what it does.

To accept them, change `main`. All this time you've written `int main(void)`, meaning "takes nothing." The other form is:

```c
int main(int argc, char *argv[])
```

Two parameters, and you now have the vocabulary for both.

**`argc`** is the argument count, an ordinary `int`: how many words were typed, including the program's own name.

**`argv`** is the argument vector, and `char *argv[]` is an array of the thing you met a page ago. An array of strings. One entry per word.

Write `greet.c`:

```c
#include <stdio.h>

int main(int argc, char *argv[])
{
    printf("argc is %d\n", argc);

    for (int i = 0; i < argc; i++)
    {
        printf("argv[%d] is %s\n", i, argv[i]);
    }

    return 0;
}
```

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o greet greet.c
$ ./greet David Malan
argc is 3
argv[0] is ./greet
argv[1] is David
argv[2] is Malan
```

Three, not two. `argv[0]` is always the program's own name, exactly as typed. So the words you actually care about start at `argv[1]`, and `argc` is always at least 1.

That trips people up once. It's also occasionally useful: it's how a program prints its own name in an error message without having it hard-coded, which matters if somebody renames it.

### Getting at one character of one argument

`argv` is an array of strings. A string is itself an array of characters. So `argv` is an array of arrays, and you can use square brackets twice:

```c
    printf("argv[1] is        %s\n", argv[1]);
    printf("argv[1][0] is     %c\n", argv[1][0]);
```

```
$ ./argvchars 13
argv[1] is        13
argv[1][0] is     1
```

Read it left to right. The first pair of brackets picks which argument. The second picks which character of it. The placeholders change too: `%s` for the whole argument, `%c` for one character out of it.

That's how you check an argument is the shape you wanted, which is the difference between a program that validates its input and one that hopes:

```c
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Key must be all digits. '%c' is not.\n", argv[1][i]);
            return 1;
        }
    }
```

```
$ ./argvchars 1x3
Key must be all digits. 'x' is not.
$ echo $?
1
```

You need exactly this in the Caesar exercise, where the key arrives on the command line and anything that isn't a number has to be refused rather than quietly treated as zero.

### Saying no properly

A program given the wrong arguments should say so and stop. Chapter 1 introduced that habit with `scanf`. Here it gets its proper form.

```c
#include <stdio.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s NAME\n", argv[0]);
        return 1;
    }

    printf("Hello, %s\n", argv[1]);
    return 0;
}
```

```
$ ./status
Usage: ./status NAME
$ echo $?
1

$ ./status Ali
Hello, Ali
$ echo $?
0
```

That `return 1` is the **exit code**, the same number you met in the Toolbench with `echo $?`. Chapter 1 told you `main` returns an `int` and that the `int` was this. Here's where it earns its place.

Zero means success. Anything else means failure. That feels backwards, since 0 is usually false. The reason is that there's exactly one way to succeed and an unlimited number of ways to fail, so 0 is reserved for the one and every other number is available to say which failure it was.

You've been reading these numbers all along without knowing. HTTP's 404 is the same idea. So is every cryptic error code a program has ever shown you.

It matters because nothing else can read your screen. When Chapter 6 builds a test suite it'll run your program and check a number, and `make test` in Chapter 1 already does exactly that with `diff`'s exit code.

The `Usage:` line is a convention I'd adopt now. When a program gets the wrong arguments, print the shape it expected. It costs one line and it's the difference between a tool somebody can use and one they have to read the source of.

### The redactor, properly

Everything's explained. Here's the tool.

```c
// redact.c
// Reads a web server log on standard input, replaces every email
// address with X, and writes the result to standard output.
//
//     ./redact < access.log > clean.log

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

// Longer than any line the server writes. Chapter 4 removes this limit.
#define MAX_LINE 1024

bool is_address_char(char c);
void redact_line(char line[]);

int main(void)
{
    char line[MAX_LINE];

    while (fgets(line, sizeof line, stdin) != NULL)
    {
        redact_line(line);
        printf("%s", line);
    }

    return 0;
}

// True for characters that can appear inside an email address, not
// counting the @ itself. Anything else marks the edge of one.
bool is_address_char(char c)
{
    return isalnum(c) || c == '.' || c == '_' || c == '-' || c == '+';
}

// Finds every email address in the line and overwrites it with X.
// Changes the caller's array directly, because an array parameter is a
// way in rather than a copy.
void redact_line(char line[])
{
    int n = strlen(line);

    for (int i = 0; i < n; i++)
    {
        if (line[i] != '@')
        {
            continue;
        }

        // Walk left from the @ until the character before us is not
        // part of an address.
        int start = i;
        while (start > 0 && is_address_char(line[start - 1]))
        {
            start--;
        }

        // Walk right the same way. The null terminator is not an
        // address character, so this stops at the end of the line.
        int end = i;
        while (is_address_char(line[end + 1]))
        {
            end++;
        }

        for (int j = start; j <= end; j++)
        {
            line[j] = 'X';
        }

        // Carry on scanning after this address, not inside it. Line 7
        // of the sample log has two.
        i = end;
    }
}
```

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o redact redact.c
$ ./redact < access.log
```

```
192.168.4.11 - - [07/Sep/2026:08:14:22] "GET /menu HTTP/1.1" 200 4821
192.168.4.11 - - [07/Sep/2026:08:15:03] "GET /orders?email=XXXXXXXXXXXXXXXXXX HTTP/1.1" 200 1204
10.0.0.7 - - [07/Sep/2026:08:15:44] "GET /menu HTTP/1.1" 200 4821
10.0.0.7 - - [07/Sep/2026:08:16:10] "GET /basket HTTP/1.1" 200 3310
172.16.2.9 - - [07/Sep/2026:08:17:02] "POST /signup?email=XXXXXXXXXXXXXXXXXXXXXXX HTTP/1.1" 302 0
192.168.4.11 - - [07/Sep/2026:08:18:31] "GET /menu HTTP/1.1" 200 4821
10.0.0.7 - - [07/Sep/2026:08:19:57] "GET /share?from=XXXXXXXXXXXXXXXX&to=XXXXXXXXXXXXXXXXXXXX HTTP/1.1" 200 512
172.16.2.9 - - [07/Sep/2026:08:20:14] "GET /menu HTTP/1.1" 200 4821
203.0.113.5 - - [07/Sep/2026:08:21:40] "GET /basket HTTP/1.1" 200 3310
10.0.0.7 - - [07/Sep/2026:08:22:03] "GET /unsubscribe?email=XXXXXXXXXXXXXXXXXXXX HTTP/1.1" 200 88
203.0.113.5 - - [07/Sep/2026:08:23:19] "GET /menu HTTP/1.1" 200 4821
192.168.4.11 - - [07/Sep/2026:08:24:55] "GET /basket HTTP/1.1" 200 3310
```

Check it the only way that counts:

```
$ ./redact < access.log | grep -c "@"
0
```

Zero. Including line seven, which had two.

Four details worth naming.

`i = end` at the bottom of the loop is what makes line seven work. Without it the scan carries on from just after the `@`, which is now inside the X's it just wrote, and the second address is missed. The bug would be invisible on eleven of the twelve lines.

`while (is_address_char(line[end + 1]))` has no separate check for the end of the line, and doesn't need one. The null terminator isn't a letter, a digit, or any of the punctuation in that list, so `is_address_char` returns false and the walk stops. The terminator is doing exactly the job it exists for.

`redact_line(line)` changes `main`'s array with nothing handed back. That's the array rule from earlier, put to work.

And it isn't perfect, which you should notice yourself. The X's are the same length as the address they replaced, so the file still says how long each address was. That's a small leak and Stretch exercise 9 closes it.

### Ready to send

```
$ ./redact < access.log > clean.log
$ grep -c "@" clean.log
0
```

On the real forty thousand line file that takes a fraction of a second, and Maria can send `clean.log` without anybody's name on a breach report.

---

## Part 4: Break it on purpose

Four programs, one bug each, one tool each. Symptoms only. Use the tools rather than your eyes, because the point is the route.

Save a known-good output first, and check it by hand before you trust it:

```
$ mkdir -p tests
$ ./redact < access.log > tests/redact-expected.txt
$ grep -c "@" tests/redact-expected.txt
0
```

### Bug 1

`bug1.c`. Symptom: it should only greet Ali, but it greets everybody.

```c
#include <stdio.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s NAME\n", argv[0]);
        return 1;
    }

    if (argv[1] == "Ali")
    {
        printf("Hello, boss\n");
    }
    else
    {
        printf("Hello, stranger\n");
    }

    return 0;
}
```

<details>
<summary>Walkthrough</summary>

House flags first, always:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o bug1 bug1.c
bug1.c: In function 'main':
bug1.c:11:15: warning: comparison with string literal results in unspecified behavior [-Waddress]
   11 |     if (argv[1] == "Ali")
      |               ^~
```

Found before running.

`==` compares two values. On numbers that's what you want. On strings it compares where the two pieces of text are rather than what they say, so it's almost always false even when the words match. That's why the greeting is wrong for everyone including Ali.

`string.h` has the right tool:

```c
    if (strcmp(argv[1], "Ali") == 0)
```

`strcmp` compares two strings character by character and returns 0 when they're the same. Zero meaning "no difference," the same logic as exit codes and `diff`. It returns a negative or positive number otherwise, which tells you which sorts first, and that's how sorting text works in Chapter 3.

`if (strcmp(a, b) == 0)` reads as "if there's no difference." Say it that way in your head and it stops being backwards.

</details>

### Bug 2

`bug2.c`. Symptom: it prints the right word and the right length. Then somebody adds a line somewhere else in the program and it starts printing rubbish.

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char word[3] = {'H', 'i', '!'};

    printf("The word is %s and it is %zu characters\n", word, strlen(word));

    return 0;
}
```

<details>
<summary>Walkthrough</summary>

Compiles clean under every warning. Runs and gives the right answer:

```
The word is Hi! and it is 3 characters
```

Which is the trap. It's right by accident. Ask the sanitizer:

```
$ gcc -std=c17 -Wall -Wextra -g -fsanitize=address -o bug2 bug2.c
$ ./bug2
==576==ERROR: AddressSanitizer: stack-buffer-overflow
READ of size 4 at 0x7f146fb00023 thread T0
    #0 in strlen
    #1 in main /home/you/toc/ch02/bug2.c:8
```

The overflow is inside `strlen` rather than inside your code, which is the shape of most string bugs. `strlen` walks forward looking for a null terminator. Three characters were written into three slots, so there's no terminator, so it walks straight off the end and keeps going.

It printed correctly because the next byte in memory happened to be zero. Nothing guarantees that, and nothing warns you when it stops being true.

Fix: `char word[4] = {'H', 'i', '!', '\0'};` or, better, `char word[] = "Hi!";` and let C count and terminate for you.

</details>

### Bug 3

`bug3.c`. Symptom: it's `redact.c` with one character changed. It looks like it works.

```c
        int start = i;
        while (start > 0 && is_address_char(line[start]))
        {
            start--;
        }
```

<details>
<summary>Walkthrough</summary>

Clean compile, clean sanitizers, and output that looks redacted at a glance:

```
$ ./bug3 < access.log | sed -n '2p;7p'
192.168.4.11 - - [...] "GET /orders?email=hana.kXXXXXXXXXXXX HTTP/1.1" 200 1204
10.0.0.7 - - [...] "GET /share?from=inesXXXXXXXXXXXX&to=jp.mbekiXXXXXXXXXXXX HTTP/1.1" 200 512
```

Every address has kept its local part. `hana.k`, `ines`, `jp.mbeki`. Combined with the domain, which anyone can guess from the company, that's still enough to identify a person. The breach is intact and the file looks scrubbed.

Nothing crashed, so this is a `gdb` job.

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o bug3 bug3.c
$ gdb ./bug3
(gdb) break redact_line
Breakpoint 1 at 0x...: file bug3.c, line 43.
(gdb) run < access.log
```

Note the line number gdb reports. You asked to break on the function; gdb broke on line 43, the first line that actually does something. Lines 41 and 42 are the signature and a brace, and line 40 is a comment. Comments are gone before the compiler even sees the file, as Part 2 showed you, so there's nothing there to stop on.

The first log line has no `@`, so let it through and stop on one that does:

```
(gdb) continue
(gdb) print line
$1 = "192.168.4.11 - - [07/Sep/2026:08:15:03] \"GET /orders?email=hana.k@example.com...
```

Good, that's the line with the address. Now break on the loop that walks left, which is line 55, and watch it:

```
(gdb) break 55
(gdb) continue
(gdb) print i
$2 = 65
(gdb) print start
$3 = 65
(gdb) print line[start]
$4 = 64 '@'
```

Check that 55 against your own file before you trust it. `nano` shows line numbers, and if you typed an extra blank line anywhere above, yours will differ.

There it is. `start` is still sitting on the `@`, and `is_address_char('@')` is false, because `@` is deliberately not in that list. So the loop stops immediately and never walks left at all.

The correct version tests `line[start - 1]`, the character before the current position, because the question is "should I step onto that one?" rather than "am I standing on one?"

That distinction, testing the place you're about to move to rather than the place you are, is worth holding on to. It comes back in Chapter 5 when you walk a linked list.

</details>

### Bug 4

`bug4.c`. Symptom: the redacted file looks perfect on screen. The consultancy says their parser rejects it.

```c
        redact_line(line);
        printf("%s\n", line);
```

<details>
<summary>Walkthrough</summary>

Compiles clean, sanitizes clean, and on screen the addresses really are gone. Everything about it looks finished.

```
$ ./bug4 < access.log > mine.txt
$ diff mine.txt tests/redact-expected.txt
```

`diff` produces a long complaint. The quickest way to see the shape of it:

```
$ wc -l mine.txt tests/redact-expected.txt
  24 mine.txt
  12 tests/redact-expected.txt
```

Twice as many lines. The file has a blank line after every real one, because `fgets` kept the newline and `printf("%s\n", ...)` added a second.

You met this in Part 1 and fixed it. It came back because somebody edited that line later and put the `\n` back out of habit, and nothing objected. Your eyes won't catch it, because a blank line between records looks like formatting rather than a fault.

This is why the expected-output file exists. Not for the bugs you're hunting, but for the ones you've already fixed once.

</details>

---

## Part 5: Ship it

### A Makefile

```make
CC = gcc
CFLAGS = -std=c17 -Wall -Wextra -Wpedantic -g
SANFLAGS = -fsanitize=address,undefined

all: redact

redact: redact.c
	$(CC) $(CFLAGS) -o redact redact.c

redact-debug: redact.c
	$(CC) $(CFLAGS) $(SANFLAGS) -o redact-debug redact.c

test: redact
	./redact < data/access.log > /tmp/redact-out.txt
	diff /tmp/redact-out.txt tests/redact-expected.txt && echo "PASS output"
	test "$$(./redact < data/access.log | grep -c '@')" -eq 0 && echo "PASS no addresses left"

clean:
	rm -f redact redact-debug peek greet status scores word len
```

> **Trap: real tabs.** Same as Chapter 1. Comment out `set tabstospaces` in `~/.nanorc` while you write it, then check with `cat -A Makefile` and look for `^I`.

Two things are new in that `test` target.

There are now two checks rather than one. The `diff` proves the output is exactly right. The `grep -c '@'` proves the specific thing that matters, which is that no address survived. If somebody later changes the expected file carelessly, the second check still fails.

I'd build the habit around that. A test that compares against a saved file only proves the output hasn't changed. A test that states the actual requirement, no addresses in the output, proves the program still does its job. Write both when the job matters.

The `$$` isn't a typo. `make` uses `$` for its own variables, so a `$` meant for the shell has to be doubled.

### It's a Unix tool now, so use it like one

Reading standard input and writing standard output was a deliberate choice, and this is the payoff. Your redactor composes with everything else on the machine without knowing anything about it.

```
$ ./redact < access.log | grep "signup"
172.16.2.9 - - [07/Sep/2026:08:17:02] "POST /signup?email=XXXXXXXXXXXXXXXXXXXXXXX HTTP/1.1" 302 0
```

The `|` is a **pipe**: it connects one program's standard output to the next program's standard input. `redact` has no idea `grep` exists. `grep` has no idea where its input came from. Neither had to be changed.

```
$ ./redact < access.log | wc -l
12
$ ./redact < access.log | sort | uniq -c | sort -rn | head -3
```

That last one counts duplicate lines and shows the three most common, which is a crude version of the report Chapter 3 makes you build properly.

Contrast that with a program that prompts for a filename and prints a menu. It can only ever be used by a human sitting in front of it. Yours can be used by a script, at three in the morning, on a file nobody has looked at.

This is the shape Chapter 6 builds on. `logtool` reads standard input, writes standard output, and reports problems on standard error. You've just written your first one.

### Style, and the formatter

Chapter 1 handed style to a tool. Same here, and the settings are already in the repository:

```
$ clang-format --style=file -i redact.c
$ git diff
```

If that changes nothing, your code is already in the book's style. If it changes something, read the diff and decide once: change the code, or change `.clang-format`.

### Commit

```
$ cd ~/toc/ch02
$ git add .
$ git commit -m "Chapter 2: log redactor, no addresses survive"
```

---

## Where people go wrong

**"A string is a type."** It's an array of `char` with a null terminator, and once you hold that, most string bugs explain themselves.

**"`"Hi!"` is three bytes."** Four. The terminator is real and it takes up room. Every array holding a string needs space for it.

**"I can compare strings with `==`."** That compares locations, not contents. Use `strcmp`, and remember it returns 0 for equal.

**"`fgets` gives me the line."** It gives you the line and the newline. `strlen` counts it. Half of all "why is my output double spaced" is this.

**"An array parameter is a copy, like everything else."** It isn't. A function given an array can change your data. That's the one real exception to Chapter 1's rule, and Chapter 4 explains why.

**"An array knows how long it is."** Only a string does, and only because of the terminator. Every other array needs its length passed alongside it.

**"`argv[0]` is the first argument."** It's the program's name. Your arguments start at `argv[1]`.

**"`i <= n` is fine, it's only one more."** That one more is the byte after your array, and it belongs to something else. This is the most common serious bug in C and the sanitizer exists largely for it.

**"`strlen` in a loop condition is tidier."** It is, and it walks the whole string on every pass. Call it once.

**"The compiler will optimise that for me."** Sometimes. Don't design around a maybe.

**"An uninitialised array is full of zeros."** It's full of whatever was there before, and it changes between runs. Initialise it.

**"`strcpy` copies a string."** It copies a string and keeps writing until it meets a terminator, whether or not the destination has room. Know the size before you copy.

**"The preprocessor understands C."** It doesn't. `#define N 3` is a text substitution done before the compiler ever looks, which is why it takes no semicolon and why `#define N 3;` produces baffling errors later.

**"`'0'` and `'\0'` are the same."** `'0'` is the character zero, value 48. `'\0'` is the terminator, value 0. Confusing them produces strings that never end.

---

## Before the exercises: a short vocabulary for ciphers

Two of the Build exercises are ciphers, and they come with words worth having.

**Encryption** is scrambling a message so only the intended reader can unscramble it, and it has to be **reversible**. Scramble something you can't unscramble and you haven't encrypted it, you've destroyed it.

The original message is the **plaintext**. The scrambled version is the **ciphertext**. The method is the **cipher**. And the cipher takes a second input, the **key**, which is the secret. That last piece is the whole point: everybody can know the method, and without your key they still can't read your message. A cipher whose safety depends on nobody knowing the method isn't a cipher, it's a hope.

The **Caesar cipher** shifts every letter forward by the key, wrapping round from `z` to `a`, and leaves everything else alone. With a key of 1:

```
plaintext:   HI!
ciphertext:  IJ!
```

Decrypting is shifting back by the same amount, which is why the key has to be shared in advance and kept secret.

**ROT13** is the Caesar cipher with a key of 13, and it has a pleasing property. Thirteen is half of twenty-six, so applying it twice returns you to the start:

```
$ echo "HI!" | ./rot 13
UV!
$ echo "UV!" | ./rot 13
HI!
```

Encrypting and decrypting are the same operation. It's used online for hiding spoilers rather than secrets, because it protects against nothing.

Which sets up the joke that ROT26 is twice as secure as ROT13. Twenty-six letters, shifted twenty-six places, is every letter back where it started:

```
$ echo "HI!" | ./rot 26
HI!
```

> **`rot` isn't in `code/`.** It's the program you write in exercise 6. The output above is what yours will do once it works, which gives you something concrete to check against: run it twice with a key of 13 and you should get your original text back.

**Brute force** is why a Caesar cipher isn't security. There are only 25 useful keys, so anyone can try all of them in under a second and read whichever result is English. Real ciphers have so many possible keys that trying them all would take longer than the universe has been running. The idea is identical. Only the arithmetic got serious.

---

## Exercises

### Drill (about 15 minutes each)

**1. Predict, then check.** Write down what each prints before running it.

```c
char a[] = "Hi!";
char b[10] = "Hi!";
printf("%zu %zu\n", sizeof a, sizeof b);
printf("%zu %zu\n", strlen(a), strlen(b));
printf("%d\n", a[3]);
printf("%d\n", 'a' - 'A');
printf("%d\n", strcmp("apple", "apple"));
printf("%d\n", strcmp("apple", "banana"));
```

The gap between `sizeof` and `strlen` is the one to sit with.

**2. Write `string_length` yourself**, without `strlen`, using the loop from Part 3. Test it on `""`, `"a"`, and a line from the log. Then check your answers against `strlen`.

**3. Count the vowels** in a line read with `fgets`, using `tolower` so that `A` and `a` both count. Then count the words, defined as runs of non-space characters. The second is harder than it looks; decide what to do about two spaces in a row before you write any code.

**4. Print the arguments backwards.** Write a program that prints its command line arguments in reverse order, one per line, excluding its own name.

### Build (about an hour each)

**5. Reading level (CS50 parity: Readability).** Write `readability.c` that reads a passage on standard input and reports the US grade level a reader needs for it, using the Coleman-Liau index:

```
index = 0.0588 * L - 0.296 * S - 15.8
```

where `L` is the average number of letters per 100 words and `S` the average number of sentences per 100 words. Count a letter with `isalpha`, a word as a run ending in a space, and a sentence as ending in `.`, `!` or `?`. Round to the nearest whole number. Below 1, print `Before Grade 1`. At 16 or above, print `Grade 16+`.

`"One fish, two fish, red fish, blue fish."` should come out before grade 1. The opening of *Nineteen Eighty-Four* should come out around grade 10.

**6. Caesar (CS50 parity).** Write `caesar.c` that takes a key on the command line and shifts every letter forward by that many places, wrapping `z` round to `a`, leaving punctuation, digits and spaces untouched, and preserving case.

```
$ ./caesar 1
This is CS50
Uijt jt DT50
```

Reject a missing or non-numeric key with a `Usage:` line and exit code 1. The wrap is the interesting part: `%` from Chapter 1 and `'a'` as your zero point. Work out `(c - 'a' + key) % 26` on paper for `z` and key 1 before you code it.

**7. Substitution (CS50 parity).** Write `substitution.c` that takes a 26-letter key on the command line, where the first letter is what `a` becomes, the second what `b` becomes, and so on. Validate the key properly: exactly 26 characters, all letters, no repeats. Each of those is a real check and one of them needs an array.

### Stretch (no solution provided)

**8. Redact more than addresses.** Extend `redact.c` to also hide anything that looks like a credit card number, meaning a run of 13 to 16 digits, possibly with spaces or dashes in it. Decide what to do about the byte counts at the end of every log line, which are also digits, and write down your rule before you code it.

**9. Stop leaking the length.** The X's give away how long each address was. Replace every address with the fixed text `[REDACTED]` instead, which means shifting the rest of the line left or right to fit. You'll need to be careful with the terminator, and `memmove` from `string.h` is worth reading about. Prove with `diff` that no line loses characters it should have kept.

**10. Break your own test.** Sabotage `redact.c` so it fails on exactly one line of a 40,000 line file and looks perfect on the other 39,999. Then write the test that catches it. If your test suite can't catch your own sabotage, it wouldn't have caught anyone else's.

---

> **Parity: CS50x Week 2.**
>
> Same ground as Week 2: the four compilation stages, `clang` versus `make`, `-o` and `-l`, decompiling, debugging with print statements and with a debugger, arrays, magic numbers and `const`, passing arrays to functions, strings as arrays of characters, the null terminator, `strlen` and the string library, `ctype`, ASCII arithmetic, `argc` and `argv`, and exit codes. The three problem sets are exercises 5, 6 and 7.
>
> **What's different.**
>
> The course uses `get_string` from its own library and its `string` type. This book has never had either, so where the course spends the week revealing that `string` was `char *` all along, you spend it building up to `char *` from `char` and arrays, and Chapter 1's unfinished receipt is the thing that motivates it.
>
> Input comes from `fgets` on standard input rather than a prompt, which means the tool reads files, composes with `<` and `|`, and is already the shape of the thing Chapter 6 builds.
>
> The course demonstrates the four stages with slides. Here you run each one and read its output, including finding your own `for` loop in the assembly, which the Toolbench set up as a Stretch exercise and this chapter pays off.
>
> **What this chapter adds.** A scenario where the null terminator isn't trivia. Bug 3 leaks every customer's name while the file looks scrubbed, and it's one character different from correct.

---

## What you have

A tool that reads a log on standard input, removes every email address, and writes the result out. It composes with other Unix tools, it has a Makefile, and its test checks both that the output hasn't changed and that the requirement still holds.

You've also got the piece Chapter 1 couldn't give you. Go back to `receipt.c` and write the function it was missing:

```c
void print_line(char label[], long cents);
```

Eighteen lines become six. That's the reward, and it's worth the ten minutes.

**Next:** Chapter 3. The log is no longer twelve lines. It's two million, you need the ten most requested pages out of it, and your first working version takes long enough that you'll assume it has hung.

It hasn't. It's just doing far more work than it needs to, and you're going to measure exactly how much before anybody gives it a name.

**Go to:** [`ch03-two-million-lines/`](../ch03-two-million-lines/README.md)
