# The Toolbench

*Front matter. Read this before anything else. About two hours, spread over as many sittings as you like.*

---

## Two evenings

Two people sit down with the same broken program. It's meant to print a total. It prints zero.

The first one opens the file and reads it. Looks fine. Adds a `printf` in the middle to see what the total is at that point. Recompiles. Runs. Still zero, and now there's a stray line of output in the way. Adds another `printf` inside the loop. Recompiles. Two hundred lines scroll past. Scrolls back up. Squints. Deletes one print, adds another somewhere else. Recompiles. It's 11:40pm. Around midnight they change something at random, it starts working, they don't know why, and they never find out.

The second one compiles the same file and the compiler immediately says:

```
total.c:14:9: warning: suggest parentheses around assignment used as truth value
```

They look at line 14. It says `if (total = 0)` where it should say `if (total == 0)`. One character. Recompile, done. Forty seconds.

Same bug. Same person, honestly, on a different night. The only difference was the bench.

This chapter builds you that bench. None of it is C. All of it is the difference between those two evenings, repeated every day for the rest of the book.

---

## What you'll have when this is done

- A complete C toolchain on Debian 13, installed and verified.
- The ability to move around a terminal, redirect a program's output into a file, and read the exit status nobody shows you.
- A way to answer your own questions from the manual instead of a search engine.
- A first C program, compiled and run, with an explanation of every part of the command that built it.
- Six flags you've watched catch something, so you know why each one is there.
- Both sanitizers, and the ability to read the report they produce.
- `gdb`: break, run, step, inspect, and read a backtrace after a crash.
- `diff` as your judge, instead of your eyes.
- Four planted bugs, diagnosed, one per tool.
- A Makefile so you stop retyping, and your work under version control.

Tick those off honestly at the end. Anything you can't do, redo that section. It costs less now than it will in Chapter 4.

---

## Part 1: The terminal

### What it actually is

When you open a terminal you're looking at two things stacked together. The terminal itself is a window that shows text and accepts keystrokes. Behind it runs a **shell**, an ordinary program whose entire job is to read the line you typed, find the program you named, run it, and show you what it printed. On Debian that shell is `bash`.

That's the whole model. You type a name, the shell runs a program with that name. `ls` is a program. `gcc` is a program. Every command in this book is a program sitting in a file somewhere on your disk.

Open your terminal now. You'll see something like:

```
you@debian:~$
```

Read it left to right. `you` is your username. `debian` is the machine's name. `~` is where you are, and the tilde is shorthand for your home directory, `/home/you`. The `$` means the shell is ready. When you see `$` at the start of a line in this book, type what comes after it, not the `$` itself.

### The eleven commands this book needs

The README assumed you can already find your way around a terminal, so this is a refresher rather than a lesson. Run each one anyway.

```
$ pwd
/home/you
```

`pwd` prints the working directory, meaning where you are. Every command you run happens relative to this place.

```
$ ls
Desktop  Documents  Downloads
```

`ls` lists what's here. Add `-l` for detail and `-a` to include hidden files, which on Linux just means files whose names start with a dot.

```
$ mkdir toolbench
$ cd toolbench
$ pwd
/home/you/toolbench
```

`mkdir` makes a directory, `cd` moves into it. `cd ..` goes up one level. `cd` on its own takes you home from anywhere, which is handy when you're lost.

```
$ cat somefile.txt
```

`cat` dumps a file to the screen. Fine for short files, terrible for long ones.

```
$ less somefile.txt
```

`less` shows a long file one screen at a time. Arrows scroll, `/word` searches, `q` quits. You'll use `q` to escape a lot of programs in this book, so burn it into your fingers now.

```
$ rm oldfile.txt
```

`rm` deletes. There's no recycle bin. It's gone.

```
$ cp notes.txt notes-backup.txt
```

`cp` copies. First the file you have, then the name you want the copy to have. Useful when you're about to change something that currently works.

```
$ mv notes-backup.txt old-notes.txt
```

`mv` moves a file somewhere else, and since moving a file to a new name in the same directory is the same operation, `mv` is also how you rename things. There's no separate rename command.

```
$ mkdir spare
$ rmdir spare
```

`rmdir` removes a directory and refuses if there's anything in it. That refusal is a feature. It means you can't delete an afternoon's work with one mistyped word.

```
$ clear
```

`clear` wipes the screen. Ctrl+L does the same and is faster. Neither deletes anything or affects your program. This book uses it between exercises without saying so.

Everything from here happens inside `~/toolbench`, so stay there.

### Three keys that save you an hour a week

Press **Tab** while typing a filename and the shell finishes it. Type `cd tool`, press Tab, and it becomes `cd toolbench/`. Several matches? Press Tab twice to see them. This isn't a luxury. It prevents typos in filenames, which are a genuinely common source of "why isn't my program updating."

Press **Up arrow** to bring back the previous command, repeatedly to walk back through your history. You're about to type the same longish compile command several hundred times in this book, and you'll type it in full maybe twenty of those.

Press **Ctrl+R** and start typing to search your history. Type `gcc` and it finds your last gcc command. Ctrl+R again goes further back. Enter runs it, right arrow lets you edit it first.

### Redirection, or where output goes

Every program you run has three channels open to it, with fairly unglamorous names.

**stdin**, standard input, is where it reads from. By default, your keyboard.

**stdout**, standard output, is where it writes normal results. By default, your screen.

**stderr**, standard error, is where it writes complaints. Also your screen by default, which is why it all looks like one stream.

The shell lets you redirect any of them, and that matters because `diff` compares files while your programs currently print to a screen.

```
$ ls > listing.txt
$ cat listing.txt
listing.txt
```

The `>` sent `ls`'s normal output into a file instead of your screen. Nothing appeared, which surprises people the first time. The output went where you told it.

Note that the file already existed by the time `ls` ran, which is why it lists itself. That's the shell creating the file first and then running the command.

`>` overwrites. `>>` appends:

```
$ echo "first line" > notes.txt
$ echo "second line" >> notes.txt
$ cat notes.txt
first line
second line
```

Now watch the two output channels behave differently:

```
$ ls nosuchfile > listing.txt
ls: cannot access 'nosuchfile': No such file or directory
```

The error still landed on your screen even though you redirected output to a file, because errors travel on stderr and `>` only redirects stdout. Catch errors with `2>`:

```
$ ls nosuchfile 2> errors.txt
$ cat errors.txt
ls: cannot access 'nosuchfile': No such file or directory
```

This separation is deliberate and useful. It means you can pipe a program's real output somewhere while still seeing its complaints. In Chapter 6 you'll make `logtool` follow the rule properly: results to stdout, problems to stderr, so somebody can redirect one without losing the other.

### Exit status, the number you can't see

Every program hands the shell a single number when it finishes. Zero means it worked. Anything else means it didn't, and different numbers can mean different failures.

You never see this number unless you ask.

```
$ ls
listing.txt  notes.txt  errors.txt
$ echo $?
0
```

```
$ ls nosuchfile
ls: cannot access 'nosuchfile': No such file or directory
$ echo $?
2
```

`$?` is a shell variable holding the exit status of the last command. `echo` prints it.

That looks like trivia. It's the foundation of every automated test you'll ever run, including the ones in this book, because a test script can't read your screen but it can check a number. When you write `return 0;` at the bottom of a C program in twenty minutes, that zero is this number. The connection is direct and literal.

### The manual, and how to answer your own questions

Debian ships a manual for almost everything installed on it. Learning to read it is the difference between a programmer who can work and one who needs an internet connection and a friendly stranger.

```
$ man ls
```

You're now in `less`, so the same keys work. Arrows scroll, `/` searches, `n` finds the next match, `q` quits. Quit now.

Manual pages come in numbered sections, and the numbers matter enormously in C.

**Section 1** is commands you run in the shell. `man 1 ls`.

**Section 2** is system calls, requests your program makes directly to the Linux kernel. `man 2 open`.

**Section 3** is C library functions. `man 3 printf`. This is the section you'll live in.

Leave the number off and `man` gives you the lowest-numbered match, which is often the wrong one. There's a shell command called `printf` as well as the C function:

```
$ man printf      # the shell command, section 1
$ man 3 printf    # the C function you actually want
```

Try `man 3 printf` now and scroll to the table of conversion specifiers. That table is the definitive answer to "which one do I use for a `double`", and it's on your machine, offline, forever. You don't have to remember what's in it. You have to remember it exists.

> **Debian note.** If `man 3 printf` says there's no manual entry, you're missing the `manpages-dev` package. The next section installs it.

---

## Part 2: Installing the bench

### One command, then an explanation

```
$ sudo apt update
$ sudo apt install build-essential gdb valgrind clang git man-db manpages-dev
```

Say yes when it asks. It'll download somewhere around 400 MB.

Now the explanation, because typing commands you don't understand is exactly the habit this book exists to prevent.

**`sudo`** runs the command that follows as the administrator. Installing software touches directories your normal account can't, so it needs elevation. It'll ask for your password, and nothing appears as you type it. That's deliberate, not a broken keyboard.

**`apt`** is Debian's package manager. A package is a bundle of software plus a description of what else it needs. `apt` fetches packages from Debian's servers, works out the dependencies, and installs everything in the right order.

**`apt update`** doesn't update any software. It refreshes the local list of what's available and at which version. You run it before installing because otherwise `apt` may be working from a list that's months old and try to fetch a file that's since been replaced. This trips up nearly everybody once.

**`apt install`** does the actual installing.

Now the packages.

**`build-essential`** is a meta-package: it installs nothing itself and instead pulls in the set of things you need to compile software on Debian. That includes `gcc` (the compiler), `make` (which you meet at the end of this chapter), and `libc6-dev`, which holds the header files and the compiled standard library every C program links against. When you write `#include <stdio.h>`, that file got onto your machine through this package.

**`gdb`** is the debugger.

**`valgrind`** is a memory analysis tool. You'll barely touch it until Chapter 4, but installing it now means the bench is complete.

**`clang`** is a second, independent C compiler. You don't need two compilers to write C. You want two because when gcc's error message means nothing to you, clang has often phrased the same complaint more clearly, and reading both is sometimes all it takes. It's a second opinion and it costs nothing to have on the shelf.

**`git`** is version control, your undo button across days rather than keystrokes.

**`man-db` and `manpages-dev`** are the manual system and the section 3 pages for C library functions. Without `manpages-dev`, `man 3 printf` fails.

> **Debian note: `sudo: command not found`.** On a fresh Debian install, if you set a root password during setup, your user account deliberately doesn't get administrator rights and `sudo` may not even be installed. Fix it once:
>
> ```
> $ su -
> Password:            (the root password, not yours)
> # apt install sudo
> # usermod -aG sudo yourusername
> # exit
> ```
>
> Then log out of your desktop session and back in, or reboot. Group membership is only read at login, so that step isn't optional. After that, `sudo` works normally.

### Verify, and write it down

Don't trust me that these are installed. Ask the machine.

```
$ gcc --version
gcc (Debian 14.2.0-19) 14.2.0
...
$ gdb --version
GNU gdb (Debian 16.3-1) 16.3
...
$ valgrind --version
valgrind-3.24.0
$ clang --version
Debian clang version 19.1.7
$ git --version
git version 2.47.3
$ make --version
GNU Make 4.4.1
```

Your version numbers will differ from mine, possibly by a lot if you're reading this a year after I wrote it. That's fine and expected. Write yours down somewhere you can find them, because when something in this book behaves differently from what I describe, the first question is always which version you're running. Six commands, one minute, and you've removed a whole category of future confusion.

> **Debian note: gcc 14 is stricter than the internet thinks.** Debian 13 ships gcc 14, which turned four long-standing warnings into hard errors for C code. Call a function you never declared, use the wrong pointer type, or return a value from a `void` function, and older gcc versions grumbled and compiled it anyway. gcc 14 refuses. Tutorials written before 2024 will tell you to expect a warning where you get an error and a program that doesn't build.
>
> That's good news. Every one of those four was a bug you'd otherwise have shipped. But when a five-year-old Stack Overflow answer doesn't match your machine, this is usually why.

### Make yourself a workspace

```
$ cd ~/toolbench
$ ls
errors.txt  listing.txt  notes.txt  old-notes.txt
$ rm errors.txt listing.txt notes.txt old-notes.txt
```

Clean slate. Everything from here lives in `~/toolbench`.

---

## Part 3: The editor

### nano, and why I'm starting you here

You need a program that puts characters into a file. C source is plain text. No fonts, no bold, no formatting, nothing invisible. A word processor would actively ruin it by inserting smart quotes and typographic characters the compiler can't read.

Debian comes with `nano`, and I'm starting you there for one reason: it'll never get in your way. The shortcuts are printed along the bottom of the screen at all times and there's no mode to be trapped in. Every minute you spend fighting your editor in the first fortnight is a minute stolen from learning C.

```
$ nano hello.c
```

You're looking at an empty file. Type something. Anything.

The bar at the bottom shows shortcuts. `^` means the Ctrl key, so `^O` is Ctrl and O together. Three of them matter.

**Ctrl+O** writes the file to disk. It asks you to confirm the filename. Press Enter.

**Ctrl+X** exits, and asks first if you've got unsaved changes.

**Ctrl+K** cuts the current line. **Ctrl+U** pastes it back.

Save and exit now.

### Configure it once, benefit forever

`nano` has a settings file. It doesn't exist yet, so make it:

```
$ nano ~/.nanorc
```

Type these four lines:

```
set linenumbers
set tabsize 4
set tabstospaces
set autoindent
```

Save with Ctrl+O, Enter, then Ctrl+X.

Here's what you just turned on and why each one earns its place.

**`linenumbers`** puts a line number down the left edge. This is the important one. The compiler talks to you exclusively in line numbers, and when it says `hello.c:14:9` you want to find line 14 by looking rather than counting.

**`tabsize 4`** makes indentation four columns wide, which is what this book's code uses.

**`tabstospaces`** inserts actual spaces when you press Tab. C doesn't care either way, but mixing tabs and spaces makes code look correctly indented on your machine and wrong on somebody else's. Pick one and stop thinking about it. There's exactly one file in this book where this setting bites you, and it's the Makefile at the end of this chapter, because `make` demands real tabs. I'll warn you again when we get there, with the fix.

**`autoindent`** keeps your indentation when you press Enter, so nested code stays lined up without retyping spaces.

Reopen `hello.c` and confirm you now see line numbers down the side.

> **Using a different editor?** Use it. The book never depends on which one you picked. If you already know `vim`, you know more than enough. If you want VS Code, install it and get the C/C++ extension. My only advice is to spend the first two chapters in `nano` regardless, then switch when you've got enough C in your head to spare attention for tooling. Configuring an IDE is a very comfortable way to avoid learning to program.

---

## Part 4: The compiler

### Your first program, typed by hand

Open `hello.c` and type this. Type it. Don't copy it. That's the rule from the README and this is the first place it applies.

```c
#include <stdio.h>

int main(void)
{
    printf("Hello, world!\n");
    return 0;
}
```

Save and exit. Before compiling, here's what every character means. Six lines, six paragraphs, because these appear at the top of every program you write for the rest of the book and you should never wonder about them again.

**`#include <stdio.h>`** The `#` marks this as an instruction to the preprocessor, a program that runs before the compiler proper and does simple text manipulation on your file. `include` means "find this file and paste its entire contents here." `stdio.h` is a **header file** that came with `libc6-dev`. It lives at `/usr/include/stdio.h` and you can read it right now with `less /usr/include/stdio.h` if you're curious, though it won't be a pleasant read. What's in it are descriptions of input and output functions: their names, what arguments they take, what they return. Without this line the compiler has never heard of `printf` and, on gcc 14, refuses to build. The angle brackets mean "look in the system's standard header locations."

**`int main(void)`** declares a function. `main` is its name, and it's special, because when your program starts this is the function that runs. Every C program has exactly one. `(void)` says it takes no arguments, which you'll change in Chapter 2 when command line arguments arrive through `main`. The leading `int` says the function hands back an integer when it finishes, and that integer is the exit status you met with `echo $?`.

**`{` and `}`** group statements into a block. Everything between them is the body of `main`. Every opening brace needs a closing one, and unbalanced braces produce some of the most confusing errors in C, because the compiler often notices at the end of the file rather than where you slipped.

**`printf("Hello, world!\n");`** calls `printf`, which lives in the standard library, and hands it one argument: the text in quotes. The `\n` isn't two characters. It's one, a newline, written with a backslash because you can't type an invisible character between quotes. Leave it out and your next output starts on the same line, which looks broken. The semicolon ends the statement. C uses semicolons rather than line endings to decide where a statement stops, which is why forgetting one usually gets reported on the *following* line.

**`return 0;`** ends `main` and hands 0 back to the shell. Success. You're about to see that number come back around.

### Compile it the way most tutorials show you

```
$ gcc hello.c
$ ls
a.out  hello.c
```

Something called `a.out` appeared. That's your program, and the name is a fossil. It stands for "assembler output" and dates to Unix in the early 1970s. gcc has been using it for over fifty years and shows no sign of stopping. It's a terrible default and you'll stop accepting it in about a minute.

Run it:

```
$ ./a.out
Hello, world!
```

```
$ echo $?
0
```

There's your `return 0`, come back around.

**Why `./`?** Type `a.out` on its own and the shell says `command not found`, which feels absurd since the file is right there. When you type a bare name, the shell searches a list of directories held in a variable called `PATH`, and for security reasons the directory you happen to be standing in isn't on that list. If it were, anyone who could drop a file called `ls` into a shared folder could hijack your next `ls`. So you have to say explicitly where the program is. `.` means "this directory," and `./a.out` means "the a.out right here." Run `echo $PATH` to see the list you're not on.

### Flag 1: `-o`, because a.out is a terrible name

The problem with `a.out` is that it's the name of every program you compile, so each one destroys the last.

```
$ gcc hello.c
$ gcc somethingelse.c
$ ls
a.out
```

One file. Your first program is gone. `-o` names the output:

```
$ gcc -o hello hello.c
$ ls
a.out  hello  hello.c
$ ./hello
Hello, world!
```

Read `-o hello` as "output to a file called hello." Get rid of the leftover with `rm a.out`.

### Flag 2: `-Wall`, the one that pays for itself hourly

Here's why a bare `gcc` command isn't good enough. Make a new file, `count.c`:

```c
#include <stdio.h>

int main(void)
{
    int count = 3;

    if (count = 0)
    {
        printf("There is nothing left.\n");
    }

    printf("Count is %d\n", count);
    return 0;
}
```

Read it as a human. It sets `count` to 3, checks whether it's zero, and reports. `count` is 3, so it should print `Count is 3`.

```
$ gcc -o count count.c
$ ./count
Count is 0
```

Silence from the compiler. A confident, wrong answer from the program.

There's one character wrong. `=` assigns a value. `==` compares two values. I wrote `if (count = 0)`, which sets `count` to zero and then tests the result of that assignment, which is zero, which C treats as false. So the message doesn't print, and the variable gets quietly destroyed on the way past.

This is legal C. There are rare cases where assigning inside a condition is exactly what you want, so the language permits it. It's also, overwhelmingly, a typo. Ask the compiler what it thinks:

```
$ gcc -Wall -o count count.c
count.c: In function 'main':
count.c:7:15: warning: suggest parentheses around assignment used as truth value [-Wparentheses]
    7 |     if (count = 0)
      |         ~~~~~~^~~
```

Same compiler, same code, one flag. It found the bug, pointed a caret at the exact character, and named the specific check in brackets so you can look it up.

`-Wall` means "enable the warnings," though the name overpromises since it isn't literally all of them. It's the set gcc's maintainers consider both useful and unlikely to fire on correct code. There's close to no reason ever to compile without it.

> **Debian note: gcc's quotation marks.** On a normal Debian desktop your locale is UTF-8, so gcc writes `In function ‘main’:` with curly typographic quotes. This book prints straight ones throughout, because they survive copying and pasting into a search box. The words are identical, only the quote characters differ. If you want gcc to match the book exactly, put `LC_ALL=C` in front of the command.

Fix the typo to `==`, recompile, and confirm you get `Count is 3` and a silent compiler.

### Flag 3: `-Wextra`, the next tier

`-Wall` isn't all of them, so here's what it misses. New file, `add.c`:

```c
#include <stdio.h>

int add(int a, int b, int c)
{
    return a + b;
}

int main(void)
{
    printf("2 + 3 + 4 = %d\n", add(2, 3, 4));
    return 0;
}
```

The function is meant to add three numbers. It adds two and forgets `c`.

```
$ gcc -Wall -o add add.c
$ ./add
2 + 3 + 4 = 5
```

Clean compile under `-Wall`. A wrong answer no test would catch unless somebody bothered to check the arithmetic. Now:

```
$ gcc -Wall -Wextra -o add add.c
add.c: In function 'add':
add.c:3:28: warning: unused parameter 'c' [-Wunused-parameter]
    3 | int add(int a, int b, int c)
      |                       ~~~~^
```

"You asked for a value and then never used it." That's almost always a sign you meant to use it and forgot, which is exactly what happened.

`-Wextra` turns on a second tier of checks that are still valuable but fire a bit more often on code that's technically fine. At the scale you're working, the noise is near zero and the payoff is real. Fix `add` to return `a + b + c` and confirm you get 9.

### Flag 4: `-Wpedantic`, the standards enforcer

This one guards against something subtler. gcc supports features that aren't part of the C standard, its own extensions. They work perfectly on gcc and fail on other compilers. Learn one without realising it's an extension and you'll write code that only builds on your machine.

`-Wpedantic` tells gcc to complain whenever you rely on one. Here's a small example. You won't fully understand this code until Chapter 4, so read only the warning:

```c
#include <stdio.h>

int main(void)
{
    int n = 5;
    void *p = &n;
    printf("%p\n", p + 1);
    return 0;
}
```

```
$ gcc -Wall -Wextra -o pedant pedant.c
$ gcc -Wall -Wextra -Wpedantic -o pedant pedant.c
pedant.c: In function 'main':
pedant.c:7:22: warning: pointer of type 'void *' used in arithmetic [-Wpointer-arith]
```

The first command is silent because gcc allows it. The second says the standard doesn't, and another compiler may reject it.

In practice `-Wpedantic` will fire on you maybe twice in this entire book. That's the point. It's a quiet guard that stops you picking up a habit you'd have to unlearn later. Delete `pedant.c`, we're done with it.

### Flag 5: `-std=c17`, pinning the language itself

C has been revised several times: C89, C99, C11, C17, C23. Each revision changed things. gcc has to pick a default, and gcc 14's default is a version of C23 with GNU extensions layered on.

That matters more than it sounds. Between C17 and C23, `bool`, `true` and `false` became built-in keywords, empty parentheses in a function declaration changed meaning, and several other details moved. If your compiler assumes one version and your book assumes another, you'll occasionally see behaviour I didn't describe.

Prove the default with a small program, `version.c`:

```c
#include <stdio.h>

int main(void)
{
    printf("%ld\n", __STDC_VERSION__);
    return 0;
}
```

`__STDC_VERSION__` is a value the compiler defines for you, encoding which standard it's following as a year and month.

```
$ gcc -o version version.c
$ ./version
202311

$ gcc -std=c17 -o version version.c
$ ./version
201710
```

202311 is November 2023, which is C23. 201710 is October 2017, which is C17. The flag changed which language you're writing.

This book uses C17 throughout. It's the last revision universally supported everywhere, it's what almost all existing C code in the world is written against, and the C23 changes are conveniences rather than fundamentals. Pinning it means what you see matches what I wrote, on your machine and in three years.

Delete `version.c` when you've seen it work.

### Flag 6: `-g`, for the debugger

I'm introducing this one now and demonstrating it in Part 7, because its benefit only shows up when `gdb` is on the table. Short version: `-g` embeds a map inside the executable connecting machine instructions back to your source lines and variable names. Without it, the debugger can show you the program but not your program.

Two things people get wrong about `-g`.

It does not make your program slower. It adds information alongside the code, not instructions to it.

It does make the file bigger. Watch:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -o hello hello.c
$ ls -l hello
-rwxr-xr-x 1 you you 16056 Sep  4 10:22 hello

$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o hello-g hello.c
$ ls -l hello-g
-rwxr-xr-x 1 you you 21520 Sep  4 10:22 hello-g
```

Your byte counts will differ. The point is that the second file is meaningfully larger, and that extra space is the map. It's a trade you should take every single time while learning, and it costs nothing at runtime.

### The house command

That's the whole set. From here on, this book compiles like this:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o program program.c
```

Read it aloud: use C17, warn me about the common problems and the next tier, complain if I use a gcc-only extension, include the debugging map, name the output `program`, compile `program.c`.

You've watched every one of those earn its place. None of it is magic, and in Part 9 you'll stop typing it entirely.

> **Under the hood: four stages, not one.**
> That single `gcc` command is really running four programs in sequence. The **preprocessor** handles your `#include` and pastes the header in. The **compiler** turns the result into assembly, the human-readable form of machine instructions. The **assembler** turns assembly into raw machine code in an object file. The **linker** joins your object file to the standard library, where the real `printf` lives, and produces the executable.
>
> You can stop after any stage and look at what came out, using `-E`, `-S` and `-c`. Chapter 2 does exactly that, one stage at a time, and it's one of the more clarifying hours in the book. For now, just know that "compiling" is four things wearing one coat.

### The second opinion

Occasionally gcc phrases a complaint in a way that means nothing to you. `clang` reads the same C and often explains itself differently:

```
$ clang -std=c17 -Wall -Wextra -o count count.c
```

On the `if (count = 0)` bug, gcc says "suggest parentheses around assignment used as truth value." Clang says "using the result of an assignment as a condition without parentheses" and then adds a second line telling you where to put them. Same fault, and one of those two sentences is going to land for you.

Try it on any file that's confused you. It's a free extra angle on the same problem, and reading two descriptions of a bug is sometimes all it takes for it to click. That's the whole role clang plays in this book.

---

## Part 5: The judge

### Why your eyes don't count as a test

You're going to look at your program's output and decide whether it's right. You'll do this while tired, at the end of a session, already believing the code works. Human beings are astonishingly bad at it. A missing space at the end of a line is invisible. So is a capital letter where a lowercase belongs, if you're skimming.

`diff` has no beliefs and doesn't skim.

### Using it

Write `greet.c`:

```c
#include <stdio.h>

int main(void)
{
    printf("Hello, world!\n");
    printf("Welcome to C.\n");
    printf("Let us begin.\n");
    return 0;
}
```

Compile it and save what it prints into a file:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o greet greet.c
$ ./greet > mine.txt
```

Nothing appeared on screen because the output went to `mine.txt`. Now make a file of what the output should be. Use `nano expected.txt` and type:

```
Hello, world!
Welcome to C.
Let us begin.
```

Make sure there's a newline at the end of the last line, which `nano` handles for you.

```
$ diff mine.txt expected.txt
$ echo $?
0
```

Nothing. Silence. That's `diff` telling you the files are identical, and the exit status of 0 confirming it.

Unix tools are quiet when things go well. It feels wrong at first, like the tool didn't run. Get used to it, because a bare prompt after a `diff` is one of the more satisfying sights in this book.

### Now break it

Edit `greet.c` and change the second line to `printf("Welcome to C!\n");` with an exclamation mark. Recompile, rerun, rejudge:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o greet greet.c
$ ./greet > mine.txt
$ diff mine.txt expected.txt
2c2
< Welcome to C!
---
> Welcome to C.
$ echo $?
1
```

Read the report. **`2c2`** means line 2 of the first file corresponds to line 2 of the second, and it changed. You'll also see `a` for added lines and `d` for deleted ones when the files differ in length. **`<`** marks lines from the first file, yours. **`>`** marks lines from the second, the expected one. **`---`** separates them. And the exit status is now 1, meaning they differ. That number is what makes automated testing possible, because a script can't look at your screen but it can check a number.

Try a whitespace difference too. Add a trailing space to one line in `expected.txt` and run `diff` again. It catches something your eyes cannot see at all. That's the entire argument for using it.

Put the exclamation mark back or fix `expected.txt`, whichever you prefer, and confirm you get silence again.

Every chapter in this book ships expected output files. This is how you use them.

---

## Part 6: The sanitizer

### The bugs the compiler can't see

The compiler reads your source code. It can't know what value a variable will hold three seconds into a run, so an entire family of bugs is invisible to it: the ones that depend on what actually happens at runtime.

Write `scores.c`:

```c
#include <stdio.h>

int main(void)
{
    int scores[3] = {90, 85, 78};
    printf("The third score is %d\n", scores[3]);
    return 0;
}
```

There are three scores. In C, array positions are numbered from zero, so they're `scores[0]`, `scores[1]` and `scores[2]`. `scores[3]` is one past the end. It doesn't exist.

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o scores scores.c
$ ./scores
The third score is 0
```

Perfectly clean compile with every warning we have. It ran. It printed a number.

That number is whatever bytes happened to sit in memory immediately after your array. Today that's harmless nonsense. In a real program those bytes belong to another variable, and you've just read data that wasn't yours. Write to that spot instead of reading and you've corrupted somebody else's value, and the program will keep running perfectly for another forty minutes before failing somewhere with no visible connection to what you did.

C won't stop you. That's the trade C makes.

### Making it loud

```
$ gcc -std=c17 -Wall -Wextra -g -fsanitize=address -o scores scores.c
$ ./scores
=================================================================
==5183==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffd21c0a58c at pc 0x55d3f8a01b47
READ of size 4 at 0x7ffd21c0a58c thread T0
    #0 0x55d3f8a01b46 in main /home/you/toolbench/scores.c:6
    #1 0x7f2b4c02a1c9 in __libc_start_call_main
    #2 0x7f2b4c02a284 in __libc_start_main
    #3 0x55d3f8a01760 in _start

Address 0x7ffd21c0a58c is located in stack of thread T0 at offset 44 in frame
    #0 0x55d3f8a01a58 in main /home/you/toolbench/scores.c:4

  This frame has 1 object(s):
    [32, 44) 'scores' (line 5) <== Memory access at offset 44 overflows this variable
```

Your addresses will differ. Everything that matters won't.

Read it slowly, because sanitizer reports look intimidating and are actually well organised.

**`ERROR: AddressSanitizer: stack-buffer-overflow`** is the kind of mistake. It happened to a buffer living on the stack, which is the memory area for local variables.

**`READ of size 4`** is what you did. Read four bytes, the size of an `int`.

**`#0 ... in main /home/you/toolbench/scores.c:6`** is where. File and line, exactly. Frame `#0` is where it happened and the frames below are how you got there.

**`[32, 44) 'scores' (line 5)`** is the good part. Your array occupies bytes 32 up to 44 of the stack frame, which is 12 bytes, which is three 4-byte integers. You touched offset 44, the very first byte past the end. It named the variable, told you its real extent, and told you exactly how far outside you went.

Notice what `-fsanitize=address` didn't need. It didn't need me to explain the bug, and it didn't need you to suspect anything. You ran the program and it told you.

What the flag does is rewrite your program during compilation, adding a check before every memory access and surrounding each variable with poisoned regions it calls redzones. Touch a redzone and the program stops and reports. The cost is roughly two times slower and two to three times more memory. For a program that prints three numbers, irrelevant. For a shipped product, unacceptable, which is why this is a separate build rather than something you leave on.

### The second sanitizer

Address sanitizer watches memory. Undefined behaviour sanitizer watches arithmetic and other operations the C standard declares meaningless. Write `overflow.c`:

```c
#include <stdio.h>

int main(void)
{
    volatile int big = 2147483647;
    int result = big + 1;
    printf("%d\n", result);
    return 0;
}
```

2147483647 is the largest value a 32-bit `int` can hold. Adding one to it has no defined answer in C. (`volatile` here tells the compiler not to be clever and pre-calculate the answer at compile time. You won't need that keyword again for a long while. Ignore it.)

```
$ gcc -std=c17 -Wall -Wextra -g -o overflow overflow.c
$ ./overflow
-2147483648
```

Clean compile, and a result that's not merely wrong but negative. Now:

```
$ gcc -std=c17 -Wall -Wextra -g -fsanitize=undefined -o overflow overflow.c
$ ./overflow
overflow.c:6:24: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
-2147483648
```

File, line, and a plain-English statement of what's impossible about it. Note that unlike the address sanitizer it didn't stop the program. It reported and carried on.

### The debug build

You can turn both on together, and from here this is your second command whenever anything smells wrong:

```
$ gcc -std=c17 -Wall -Wextra -g -fsanitize=address,undefined -o program program.c
```

A habit worth forming now: when a program crashes, or produces a number you can't explain, or works on Tuesday and fails on Wednesday, rebuild it with that line before you do anything else. It takes ten seconds and it finds the cause outright a surprising fraction of the time.

Valgrind is the other tool for this job. It works differently, catching things the sanitizers miss, particularly memory you asked for and never gave back. It's installed and waiting. Chapter 4 introduces it properly, when you have memory to leak.

> **`-Wpedantic` and the sanitizers.** I dropped `-Wpedantic` from the sanitizer commands above only to keep the lines readable. Leave it in when you use these for real. It costs nothing.

---

## Part 7: The debugger

This is the tool that separates the two evenings in the opening story, and it's the one most beginners skip because it looks like a lot. It's eleven commands. You'll know them all in the next twenty minutes.

### A program that's wrong but doesn't crash

Write `sum.c`:

```c
#include <stdio.h>

int sum_to(int n)
{
    int total = 0;

    for (int i = 1; i < n; i++)
    {
        total = total + i;
    }

    return total;
}

int main(void)
{
    printf("The sum of 1 to 10 is %d\n", sum_to(10));
    return 0;
}
```

The sum of 1 through 10 is 55.

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o sum sum.c
$ ./sum
The sum of 1 to 10 is 45
```

Clean compile. The sanitizers would find nothing, because nothing about memory is wrong. `diff` would tell you the answer's wrong but not why. This is a logic bug, and logic bugs are what the debugger is for.

You can probably see this one by reading. Use the debugger anyway. Practise the tool on an easy case so you can use it on a hard one.

### First, without `-g`, so you see what it buys you

```
$ gcc -std=c17 -o sum-nodebug sum.c
$ gdb ./sum-nodebug
```

```
Reading symbols from ./sum-nodebug...
(No debugging symbols found in ./sum-nodebug)
(gdb) list
No symbol table is loaded.  Use the "file" command.
(gdb) break sum_to
Breakpoint 1 at 0x1151
(gdb) quit
```

The debugger loaded your program and can tell you almost nothing about it. It set a breakpoint at a raw memory address because it has no idea your function has a name you'd recognise or that a file called `sum.c` was ever involved. The machine code is all there. The map is missing.

### Now with `-g`

```
$ gdb ./sum
GNU gdb (Debian 16.3-1) 16.3
...
Reading symbols from ./sum...
(gdb)
```

`(gdb)` is a prompt, like your shell prompt. It's waiting.

**See your source:**

```
(gdb) list
1	#include <stdio.h>
2	
3	int sum_to(int n)
4	{
5	    int total = 0;
6	
7	    for (int i = 1; i < n; i++)
8	    {
9	        total = total + i;
10	    }
```

`list` shows source with line numbers, ten at a time. Press Enter on an empty prompt to repeat the last command and see the next ten.

**Stop somewhere:**

```
(gdb) break sum_to
Breakpoint 1 at 0x1155: file sum.c, line 5.
```

A **breakpoint** is a line where the program pauses and hands control to you. Now it says `file sum.c, line 5`, which is what `-g` bought you. You can break on a function name, on a line number with `break 8`, or on another file's line with `break other.c:22`.

**Run it:**

```
(gdb) run
Starting program: /home/you/toolbench/sum 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

Breakpoint 1, sum_to (n=10) at sum.c:5
5	    int total = 0;
```

Those two `libthread_db` lines appear on every `gdb run` on Debian. They mean gdb loaded the library that lets it inspect threads, which your program doesn't use. Ignore them, here and forever.

The program started, ran until it reached `sum_to`, and stopped. It's frozen mid-execution and telling you two useful things: it was called with `n=10`, and the next line to run is line 5. Line 5 hasn't run yet. That trips up everyone once. The debugger stops *before* the displayed line.

**Look at things:**

```
(gdb) print n
$1 = 10
(gdb) print total
$2 = 21845
```

`print` shows a variable's current value. `n` is 10, as expected. `total` is garbage, because line 5 hasn't executed and the variable holds whatever was in that memory. That's a small, free lesson about uninitialised variables that you just watched happen.

The `$1` and `$2` are gdb numbering its answers so you can refer back. Ignore them.

**Move one line:**

```
(gdb) next
7	    for (int i = 1; i < n; i++)
(gdb) print total
$3 = 0
```

`next` runs the current line and stops at the following one. Now `total` is 0, because line 5 finally ran.

```
(gdb) next
9	        total = total + i;
(gdb) print i
$4 = 1
(gdb) next
7	    for (int i = 1; i < n; i++)
(gdb) next
9	        total = total + i;
(gdb) print i
$5 = 2
(gdb) print total
$6 = 1
```

You're walking the loop by hand and watching the numbers move. Do that ten or so more times, printing `i` and `total` each round, and watch what happens at the end.

```
(gdb) print i
$20 = 9
(gdb) next
7	    for (int i = 1; i < n; i++)
(gdb) next
12	    return total;
(gdb) print total
$21 = 45
```

There it is. `i` reached 9, the loop condition `i < n` with `n` at 10 became false, and the loop ended without ever adding 10. The condition should be `i <= n`.

You didn't deduce that. You watched it.

**`info locals`** saves you printing one variable at a time:

```
(gdb) info locals
total = 45
```

**`continue`** releases the program to run until the next breakpoint or the end:

```
(gdb) continue
Continuing.
The sum of 1 to 10 is 45
[Inferior 1 (process 5361) exited normally]
```

**`quit`** leaves. If the program is still mid-run it asks whether to kill it. Say `y`.

**`step` against `next`.** They differ in one way and it matters. Both run the current line. If that line calls a function you wrote, `next` runs the whole call and stops after it, while `step` goes inside and stops at the function's first line. Use `next` by default. Use `step` when you suspect the function you're about to call. If you `step` into something from the standard library and find yourself lost in unfamiliar code, type `finish` to run out of it and get back.

Fix `sum.c` to use `i <= n`, recompile, and confirm 55.

### The move that beats printf outright

Change `sum_to(10)` to `sum_to(1000)` and recompile. Suppose something goes wrong only near the end. With `printf` you'd either print a thousand lines and scroll, or add a condition and recompile.

In gdb:

```
$ gdb ./sum
(gdb) break 9 if i == 998
Breakpoint 1 at 0x1167: file sum.c, line 9.
(gdb) run
Starting program: /home/you/toolbench/sum 

Breakpoint 1, sum_to (n=1000) at sum.c:9
9	        total = total + i;
(gdb) print total
$1 = 497503
(gdb) print i
$2 = 998
```

It ran 997 iterations at full speed and stopped exactly where you asked. No recompiling, no editing, no scrolling. That's a **conditional breakpoint**, and it's the single most useful thing in this section. Any C expression that's true or false works after `if`.

### After a crash

Write `crash.c`:

```c
#include <stdio.h>

void print_first(char *message)
{
    printf("The first character is %c\n", message[0]);
}

int main(void)
{
    char *text = NULL;
    print_first(text);
    return 0;
}
```

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o crash crash.c
$ ./crash
Segmentation fault
```

"Segmentation fault" means your program touched memory it doesn't own and the kernel killed it. It's the most common crash in C and it tells you nothing about where.

```
$ gdb ./crash
(gdb) run
Starting program: /home/you/toolbench/crash 

Program received signal SIGSEGV, Segmentation fault.
0x0000555555555149 in print_first (message=0x0) at crash.c:5
5	    printf("The first character is %c\n", message[0]);
```

File, line, and the value of the argument: `message=0x0`, which is address zero, which is `NULL`. Then:

```
(gdb) backtrace
#0  0x0000555555555149 in print_first (message=0x0) at crash.c:5
#1  0x0000555555555184 in main () at crash.c:11
```

A **backtrace** is the chain of calls that led here, most recent first. Frame `#0` is the crash site. Frame `#1` shows `main` called it from line 11. In a real program that chain is ten frames deep and it's how you find out which of the forty places that call a function was the one that passed it something bad.

You can move up the chain with `frame 1` and inspect that function's variables:

```
(gdb) frame 1
#1  0x0000555555555184 in main () at crash.c:11
11	    print_first(text);
(gdb) print text
$1 = 0x0
```

`backtrace` after a crash is the most valuable ten keystrokes in this chapter.

### Your eleven commands

That's the whole set you need.

| Command | Short | What it does |
|---|---|---|
| `list` | `l` | Show source around the current spot |
| `break 12` | `b 12` | Pause at line 12, or `break funcname` |
| `break 12 if x == 5` | | Pause at line 12 only when the condition holds |
| `run` | `r` | Start the program |
| `next` | `n` | Run this line, stop at the next, stepping over calls |
| `step` | `s` | Same, but go inside function calls |
| `finish` | | Run out of the current function |
| `print x` | `p x` | Show a variable's current value |
| `info locals` | | Show all local variables at once |
| `continue` | `c` | Resume until the next breakpoint |
| `backtrace` | `bt` | Show the chain of calls that got here |
| `quit` | `q` | Leave |

The table has twelve rows because `break` earns two, the plain form and the conditional one.

Pressing Enter on an empty prompt repeats the previous command, which makes stepping through a loop a matter of tapping Enter.

> **Optional: a source window.** Type `layout src` inside gdb and the screen splits, source above and prompt below, current line highlighted. Ctrl+X then A toggles it off. Some people find it much easier and some find it visually cluttered. Try it once and use it or don't.

---

## Part 8: Break it on purpose

Four programs. Each has exactly one bug, and each bug is best caught by a different tool. I'll tell you the symptom and nothing else. Work each one before reading the walkthrough under it.

Ground rules: use the tools, not your intuition. The point isn't finding the bug, which for most of these you could do by staring. The point is practising the route, so the route is already familiar when the bug is one you couldn't have found by staring.

### Bug 1

`bug1.c`. Symptom: it should print a warning when the tank is empty, then report the level. It prints the level as 0 no matter what you set it to.

```c
#include <stdio.h>

int main(void)
{
    int fuel = 42;

    if (fuel = 0)
    {
        printf("Warning: tank empty.\n");
    }

    printf("Fuel level: %d\n", fuel);
    return 0;
}
```

Find it before reading on.

<details>
<summary>Walkthrough</summary>

Compile with the house flags first, always:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o bug1 bug1.c
bug1.c:7:14: warning: suggest parentheses around assignment used as truth value [-Wparentheses]
```

Done, before running anything. `=` where `==` belongs. This is the entire argument for making warnings the first step rather than something you look at when stuck.

</details>

### Bug 2

`bug2.c`. Symptom: it prints five temperatures and the last one is nonsense that changes between runs.

```c
#include <stdio.h>

int main(void)
{
    int temps[5] = {18, 21, 19, 23, 20};

    for (int i = 0; i <= 5; i++)
    {
        printf("Day %d: %d degrees\n", i + 1, temps[i]);
    }

    return 0;
}
```

<details>
<summary>Walkthrough</summary>

The house flags compile it clean. So does running it, more or less, which is the dangerous part. Reach for the sanitizer:

```
$ gcc -std=c17 -Wall -Wextra -g -fsanitize=address -o bug2 bug2.c
$ ./bug2
Day 1: 18 degrees
...
Day 5: 20 degrees
=================================================================
==6210==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffc9b1e0e54
READ of size 4 at 0x7ffc9b1e0e54 thread T0
    #0 0x... in main /home/you/toolbench/bug2.c:9

  This frame has 1 object(s):
    [32, 52) 'temps' (line 5) <== Memory access at offset 52 overflows this variable
```

Line 9, reading past the end of `temps`, which occupies 20 bytes for five integers, and you touched byte 52, the first one outside.

The cause is on line 7. `i <= 5` runs the loop six times, for i of 0 through 5. Five items means valid positions 0 through 4. Change `<=` to `<`.

Learn this shape. `<=` in a loop over an array is wrong more often than it's right, and it's the most common bug in all of C.

</details>

### Bug 3

`bug3.c`. Symptom: the average of these five numbers should be 30. It reports 24.

```c
#include <stdio.h>

int main(void)
{
    int values[5] = {10, 20, 30, 40, 50};
    int total = 0;

    for (int i = 0; i < 5; i++)
    {
        total = total + values[i];
    }

    int average = total / 6;

    printf("Average: %d\n", average);
    return 0;
}
```

<details>
<summary>Walkthrough</summary>

Clean under warnings. Clean under sanitizers, because nothing about memory is wrong. This is a logic bug, so it's a gdb job.

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o bug3 bug3.c
$ gdb ./bug3
(gdb) break 13
Breakpoint 1 at 0x...: file bug3.c, line 13.
(gdb) run

Breakpoint 1, main () at bug3.c:13
13	    int average = total / 6;
(gdb) print total
$1 = 150
```

The total's right. 150 divided by 5 is 30, so the loop is fine and the division isn't. Look at line 13 and there it is, dividing by 6.

Notice the shape of what you just did. You didn't read the whole program looking for something suspicious. You picked the point where the wrong answer gets produced, stopped there, and checked which of the inputs to that calculation was wrong. When `total` turned out to be correct, half the program was eliminated in one step.

That's how debugging works. Not searching. Halving.

</details>

### Bug 4

`bug4.c`. Symptom: it looks completely correct on screen. The test still fails.

```c
#include <stdio.h>

int main(void)
{
    printf("Name: Ada Lovelace\n");
    printf("Role: Mathematician \n");
    printf("Year: 1843\n");
    return 0;
}
```

The expected output is in `bug4-expected.txt`:

```
Name: Ada Lovelace
Role: Mathematician
Year: 1843
```

<details>
<summary>Walkthrough</summary>

Compiles clean, runs clean, sanitizes clean, and looks perfect. Your eyes aren't the tool here.

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o bug4 bug4.c
$ ./bug4 > mine.txt
$ diff mine.txt bug4-expected.txt
2c2
< Role: Mathematician 
---
> Role: Mathematician
```

The two lines look identical on screen because the difference is a trailing space, and a space is invisible. `diff` doesn't care what's visible.

If you want to see it directly, `cat -A mine.txt` marks line endings with `$`, so a trailing space shows up as `n $` rather than `n$`.

This is why "it looks right" isn't a test, and it's why every chapter of this book ships expected output files.

</details>

---

## Part 9: Ship it

Two tools left, and neither is about C. They're about not wasting your own time and not losing your own work.

### make, so you stop retyping

You've typed this a dozen times already:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o sum sum.c
```

Multiply by every compile in a six-chapter book. Worse than the typing is the drift: one day you leave off `-Wall` because you're in a hurry, and you lose the exact thing that would have saved you.

`make` reads a file called `Makefile` that records how to build things, then does it. Create `Makefile` in `~/toolbench`:

```make
CC = gcc
CFLAGS = -std=c17 -Wall -Wextra -Wpedantic -g
SANFLAGS = -fsanitize=address,undefined

all: sum

sum: sum.c
	$(CC) $(CFLAGS) -o sum sum.c

sum-debug: sum.c
	$(CC) $(CFLAGS) $(SANFLAGS) -o sum-debug sum.c

clean:
	rm -f sum sum-debug a.out

.PHONY: all clean
```

> **Trap: the indented lines must start with a real tab character.**
>
> Not four spaces. Not eight. An actual tab. This is a wart in `make` that's confused people since 1976, and it's the one place where the `tabstospaces` setting you put in `.nanorc` works against you: it turns every Tab you press into spaces, which is right for C and wrong for this one file.
>
> The reliable fix is to switch that setting off while you write the Makefile:
>
> ```
> $ nano ~/.nanorc
> ```
>
> Put a `#` at the front of the `set tabstospaces` line, which turns it into a comment, then save and open your Makefile in a fresh `nano`. Take the `#` off again when you're done.
>
> Then check, rather than hope. `cat -A` shows invisible characters, and a real tab appears as `^I`:
>
> ```
> $ cat -A Makefile
> all: sum$
> $
> sum: sum.c$
> ^I$(CC) $(CFLAGS) -o sum sum.c$
> ```
>
> That `^I` at the start of the recipe line is what you want. Spaces would show as spaces. The `$` marks the end of each line, which is the same trick you used earlier to find a trailing space nothing on screen could show you.
>
> If you get `Makefile:8: *** missing separator.  Stop.`, this is what happened. Every time, without exception.
>
> Two keys that won't help, so you don't waste time on them. `Alt+Y` toggles colour syntax highlighting. `Alt+P` toggles whether whitespace is drawn on screen, which lets you *see* the problem but doesn't fix it. Neither one changes what the Tab key actually inserts.
>
> There's no key that does, and `man nano` explains why. The setting exists as `-E, --tabstospaces`, a flag you give when you start the program rather than something you flip while editing. So the fix has to happen before nano opens, which is what commenting out the line in `~/.nanorc` does.

Run it:

```
$ make
gcc -std=c17 -Wall -Wextra -Wpedantic -g -o sum sum.c
```

It echoed the full command so you can see exactly what it ran, then ran it. Now run it again without changing anything:

```
$ make
make: 'sum' is up to date.
```

It did nothing, on purpose. This is the real reason `make` exists. It compared the timestamp on `sum.c` against the timestamp on `sum`, saw the source hasn't changed since the program was built, and refused to waste your time. On a project with one file that saves a second. On a project with two hundred files it's the difference between a four-second rebuild and a four-minute one.

Touch the source and it notices:

```
$ nano sum.c        (change anything, save)
$ make
gcc -std=c17 -Wall -Wextra -Wpedantic -g -o sum sum.c
```

Now read the file back, because every line of it means something.

**`CC = gcc`** and **`CFLAGS = ...`** are variables. Write them once, use them everywhere with `$(CC)`. When you want to try `clang` on everything, you change one word.

**`all: sum`** is a **target** called `all` whose **prerequisite** is `sum`. Running `make` with no arguments builds the first target in the file, so `all` conventionally goes first and depends on whatever you normally want built.

**`sum: sum.c`** says the target `sum` depends on `sum.c`. If `sum.c` is newer than `sum`, run the recipe below.

The **recipe** is the tab-indented line underneath. It's a shell command, run exactly as written.

**`sum-debug`** is the sanitizer build, available on demand with `make sum-debug`. Two builds of the same code, always with the same flags, no memory required.

**`clean`** deletes the built files. `rm -f` doesn't complain about files that are already gone.

**`.PHONY`** tells `make` that `all` and `clean` aren't really filenames. Without it, if you ever created a file called `clean`, `make clean` would decide it was up to date and stop working. Cheap insurance.

Try `make sum-debug`, then `make clean`, then `make` again.

Every chapter from here ships a Makefile. You'll extend them as the programs get bigger, and in Chapter 6 you'll write one with proper debug and release targets from scratch.

### git, so you can always get back

`git` records snapshots of your files so you can return to any of them later. You'll use maybe six commands.

Configure it once, on this machine, forever:

```
$ git config --global user.name "Your Name"
$ git config --global user.email "you@example.com"
```

Every snapshot gets stamped with these. Use whatever name and email you like, though if you plan to push to GitHub, use the address on your account.

Start tracking this directory:

```
$ cd ~/toolbench
$ git init
Initialized empty Git repository in /home/you/toolbench/.git/
```

A hidden `.git` directory now exists, holding the history. Delete it and the history goes with it, so don't.

Before the first snapshot, tell git what to ignore. Compiled programs have no business in version control: they're large, they change on every build, and anyone with the source can regenerate them in a second. Create `.gitignore`:

```
# compiled programs
a.out
sum
sum-debug
count
add
greet
scores
overflow
crash
bug1
bug2
bug3
bug4

# object files and output captured for testing
*.o
mine.txt
```

Now look at the state of things:

```
$ git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	.gitignore
	Makefile
	bug1.c
	bug2.c
	...
```

Your compiled programs are absent from that list, which means `.gitignore` is working.

Two steps to make a snapshot. First stage what you want included:

```
$ git add .
```

The `.` means everything in this directory that isn't ignored. Then commit, which writes the snapshot into history with a message:

```
$ git commit -m "Toolbench complete: bench installed and all four bugs found"
[master (root-commit) a3f1b9c] Toolbench complete: bench installed and all four bugs found
 14 files changed, 187 insertions(+)
```

```
$ git log --oneline
a3f1b9c Toolbench complete: bench installed and all four bugs found
```

That's the loop: `git add .`, then `git commit -m "what I did"`. Do it at the end of every session, including sessions that ended badly. `git commit -m "loop still off by one, stopping here"` costs eight seconds and means tomorrow's you can always get back to today's you.

Write real messages. "update" and "stuff" are worthless to you in three weeks.

> **Pushing to GitHub.** You don't need it for this book, but if you want your work backed up and visible, create an empty repository on GitHub and follow the two commands it shows you under "push an existing repository." Modern GitHub wants a personal access token or an SSH key rather than a password, and walking through that properly belongs in Chapter 6 where you publish `logtool` for real. If you want it now, GitHub's own documentation is the right source.

### Get the book's own repository

While git is fresh:

```
$ cd ~
$ git clone https://github.com/dralikma/to-c-or-not-to-c.git
$ cd to-c-or-not-to-c
$ ls
```

Every chapter's text, code, expected output and sample data. When a chapter says "the test file is in `tests/`", this is where it lives.

---

## Where people go wrong

The mistakes I see over and over at this stage, with the correction stated plainly.

**"I'll clean up the warnings later."** You won't, and by then there'll be sixty of them and the two that matter will be hidden in the noise. A warning is the compiler saying "this is legal but I'm fairly confident you didn't mean it," and it's right far more often than you are. Fix each one when it appears, while the code is still in your head.

**"The error says line 12, so the bug is on line 12."** Frequently it's on line 11. C ends statements with semicolons, so a missing one means the compiler happily reads on to the next line before deciding something's wrong. Unbalanced braces are worse: the report often lands at the very end of the file. When line 12 looks fine, look up.

**"There are 40 errors, this is hopeless."** There's usually one error and 39 consequences. Fix the first, recompile, and watch most of them evaporate. Work top down, recompile after each fix.

**`make` says `missing separator`.** A recipe line starts with spaces instead of a tab. Always. See the trap in Part 9.

**"I compiled it but nothing changed."** Three usual causes, in order of frequency. You edited one file and compiled another. You forgot to save before compiling. You ran an older binary because the compile actually failed and you didn't read the output. Check all three before suspecting anything deeper.

**"`-g` will slow my program down."** It won't. It adds a map alongside the code. The sanitizers do slow things down, meaningfully, which is why they're a separate build.

**"The sanitizer found nothing, so my program is correct."** The sanitizer proves nothing about the run you didn't do. It only inspects the paths your program actually took. Feed it different input and it may light up. Clean sanitizer output means "no memory errors on this run," not "no bugs."

**"`gdb` is too complicated, `printf` is faster."** `printf` is faster for exactly one question, once. From the second question on you're recompiling for every guess, and by the fourth you've lost. Add up the evenings, not the first two minutes.

---

## Exercises

### Drill (about 15 minutes each)

**1.** Write a program that prints your name and today's date on separate lines. Compile it with the full house command. Redirect its output to `mine.txt`, hand-write the correct output into `expected.txt`, and get `diff` to print nothing.

**2.** Deliberately delete a semicolon from a working program and compile it. Read the error carefully. Which line does it name, and which line is actually wrong? Now delete a closing brace instead and compare where that error lands.

**3.** Take `sum.c` and set a breakpoint at the line inside the loop with a condition that stops it exactly when `total` first exceeds 20. Confirm the value of `i` at that moment.

**4.** Run `man 3 printf` and find the specifier for an unsigned integer, and the one for a hexadecimal value. Write a two-line program proving you found the right ones.

### Build (about an hour)

**5.** Write `temperature.c` which prints a conversion table from 0 to 100 degrees Celsius in steps of 10, formatted as `0 C = 32 F`. Get it correct, then write the expected output file and verify with `diff`. Then extend the Makefile with a `temperature` target and a `temperature-debug` target, and confirm both build.

**6.** Take the four bug programs from Part 8 and write a two-sentence entry for each in a file called `debug-log.md`: what the symptom was, which tool found it, and what the cause turned out to be. That file is a habit that pays off. Keep adding to it through the book.

### Stretch (no solution provided)

**7.** Write a shell script called `check.sh` that compiles a named C file with the house flags, runs it, redirects the output to a temporary file, compares that against a matching `-expected.txt` file, and prints `PASS` or `FAIL`. It should exit with status 0 when the test passes and 1 when it doesn't. Test it against a program that passes and one that fails.

You'll need `$1` for the script's first argument and `if` in shell syntax. `man bash` is long but searchable. This script is a rough draft of the test runner you'll finish in Chapter 6, so keep it.

**8.** Compile `sum.c` with `gcc -S sum.c` and open the resulting `sum.s`. You won't understand most of it. Find the loop anyway. Look for a label that gets jumped back to, and for the comparison instruction that decides whether to jump. You're looking at your `for` loop as the machine sees it. Chapter 2 takes this apart properly.

---

> **Parity: what CS50 does here.**
> CS50 hands you a preconfigured VS Code in the browser with the compiler, its own `make` shortcut, and the CS50 library already installed, so students can write code in minute one. It's the right call for a course with thousands of students on every kind of laptop.
>
> You've set the same thing up locally instead, which cost you two hours and bought three things. You know what's on your machine and why. You can compile C anywhere, forever, without an internet connection or an account. And you're not using the CS50 library, so nothing you learn is scaffolding you'll have to remove later.
>
> One difference in habit worth naming: in CS50, `make hello` works with no Makefile at all, because `make` has built-in rules for simple cases. Ours is written out explicitly so you can read what it does. When you see `make hello` in course materials, that's why it works there and why you're typing more here.

---

## You're ready

Your bench:

| Tool | Job | Reach for it when |
|---|---|---|
| bash | Run things, redirect output, read exit status | Always |
| nano | Write code | Always |
| gcc | Compile, and warn you before you run | Always |
| clang | A second opinion on a confusing error | gcc's message means nothing to you |
| ASan / UBSan | Catch memory and arithmetic errors at runtime | It crashed, or the numbers make no sense |
| valgrind | Deeper memory analysis, especially leaks | Chapter 4 onward |
| gdb | Watch the program run, line by line | The logic is wrong but nothing crashed |
| diff | Judge output without opinions | Every single time you think you're done |
| make | Remember the command so you don't have to | Always, from now on |
| git | Snapshots you can return to | End of every session |

Ten things. You have now used every one of them on a real problem, and you can say what every flag in the house command does and what it caught.

Next is a short section called **How the Machine Thinks**, which has no code in it at all. It covers what your processor actually does, why the letter `A` is the number 65, and why the number 0.1 is a problem. Twenty minutes, and it's there so nothing in Chapter 1 arrives without context.

After that, a shop is losing pennies and nobody knows where they're going.

**Next:** [`00-how-the-machine-thinks/`](../00-how-the-machine-thinks/README.md)
