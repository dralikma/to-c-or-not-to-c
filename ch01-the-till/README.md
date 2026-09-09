# Chapter 1: The till that never balances

*CS50x Week 1. Six to eight hours, spread over as many sittings as you like. You need the Toolbench finished and How the Machine Thinks read.*

---

## A shop that's losing money to nobody

Maria runs a bakery and coffee place called Sourdough & Co. Six days a week, around four hundred customers.

Every evening she cashes up. She counts the drawer, reads the total off the card terminal, adds the two together, and compares that against what the till software says the day should have brought in. For eleven years those numbers matched, because for eleven years she used a mechanical till and a notebook.

Then her nephew, who's good with computers, wrote her a proper till program. It prints a tidy receipt. It handles the "3 croissants for $8" deal. It works out the sales tax. Everyone likes it.

And since the day it went in, the takings have been short. Not by much. Two dollars, four dollars, sometimes six. Never the same amount twice. Never enough to be one missing sale, and never so little she can tell herself she miscounted.

She's counted the drawer three times a night for a month. She's checked the card statements against the till log, line by line. She watched the CCTV of her own counter, which made her feel awful, because the two people who work that counter have been with her for years and she likes them both.

Nobody is stealing from Maria. The money is being destroyed, one cent at a time, by about forty lines of C, and I've picked this scenario because some version of it has happened everywhere money meets software.

Here's what it comes to. Say the average loss is four dollars a day, six days a week, fifty-two weeks:

```
4 × 6 × 52 = 1248
```

One thousand two hundred and forty-eight dollars a year. Plus a month of a small business owner's evenings, plus a permanent little dent in how she feels about two people who did nothing wrong.

That's what a bug in money arithmetic costs. It isn't an abstraction and it isn't a rounding quirk to be waved away.

You're going to write Maria's program, watch it eat her money, work out exactly where the money goes, and fix it properly. Along the way you'll meet nearly every idea in a first course on C, because "add up some prices and print them" turns out to touch almost all of them.

## What you'll be able to do at the end

Do, not "understand" and not "be familiar with." If you finish this and can't do these, the chapter failed you.

- Write, compile and run a multi-function C program and explain every single line of it.
- Say what a variable actually is, choose a type for one, and say what that type costs in bytes and what it can't hold.
- Explain why `0.1 + 0.2` isn't `0.3`, and demonstrate it on your own machine.
- Explain why money must never live in a `float` or a `double`, and store it correctly instead.
- Use `printf` format specifiers on purpose, including width and precision, and say why `%d` with a `long` is a bug.
- Predict the result of whole-number division, and use `/` and `%` together deliberately.
- Recognise integer overflow, make the sanitizer prove it, and pick a type that avoids it.
- Write conditionals with `if`, `else if` and `else`, and combine tests with `&&`, `||` and `!`.
- Write `for`, `while` and `do while` loops, nest them, and know which to reach for.
- Write your own functions with inputs and outputs, declare their prototypes, and explain why a variable made inside one function is invisible inside another.
- Read a number typed by a person and reject nonsense instead of carrying on with garbage.
- Test a program's output automatically with `diff` and build it with a Makefile.

Come back to that list at the end and be honest with yourself.

## How this chapter goes

Five parts, and they build on each other in order. Do not skip ahead, because each part uses only what the earlier parts have already explained.

**Part 1** writes a small, honest, broken program. Fifteen lines. You'll understand all fifteen.

**Part 2** opens up the machine and shows you what your numbers really are once they're inside it. No new syntax, just looking.

**Part 3** rebuilds the till properly. It's the longest part and it's where the actual C lives: naming things, making decisions, repeating things, and writing your own functions.

**Part 4** hands you four broken programs and makes you find the bugs with the tools.

**Part 5** wraps it up the way a professional would: a Makefile, an automatic test, a commit.

---

## Part 1: First contact

### Somewhere to work

Make a directory for this chapter and move into it:

```
$ mkdir -p ~/toc/ch01
$ cd ~/toc/ch01
```

Everything in this chapter happens in there.

### A variable is a name for a place to keep something

Your program needs to remember a price. To remember something it needs somewhere to put it, and a way to refer to that somewhere later. That's a **variable**.

Concretely: when your program runs, the operating system gives it a block of memory. A variable is a name you attach to one small piece of that block. When you write the name in your code, the compiler turns it into "the piece of memory I set aside for that."

Two things have to happen before you can use one.

**First you declare it.** Declaring means telling the compiler that a variable exists, what it's called, and what type it is:

```c
double price;
```

Read that as "set aside room for a number that can have a fractional part, and call it `price`." Type first, then name, then a semicolon.

Why does C need to be told the type? Because of the thing you read in How the Machine Thinks: memory holds nothing but numbers, and what those numbers mean is an agreement applied from outside. The machine has no way of knowing whether the bits at that address are a whole number, a fraction, or a letter. The type is you telling it which agreement applies, and it also decides how much room to set aside.

**Then you give it a value.** That's assignment, and it uses a single equals sign:

```c
price = 4.25;
```

Here's where the first real trap in C lives, so read this bit slowly.

`=` doesn't mean "is equal to." It means "take the value on the right and put it in the box named on the left." It's an instruction, and it works right to left. `price = 4.25;` is a command to store 4.25. It isn't a statement of fact about the world.

That distinction is why `x = x + 1;` is perfectly sensible C even though it's nonsense as mathematics. It means "take whatever's in x, add one, put the result back in x."

You can do both steps at once, and almost always you should:

```c
double price = 4.25;
```

Declare and give it a starting value on one line. That's called **initialising** the variable, and getting into the habit now will save you a whole category of bug you already met in the Toolbench, where you printed a variable in `gdb` before line 5 had run and got 21845 out of it. A variable you've declared but not given a value holds whatever bits the previous occupant of that memory left behind. It isn't zero. It isn't empty. It's rubbish, and C will happily do arithmetic with rubbish.

### Your first calculation

Open a new file:

```
$ nano till.c
```

Type this. All of it, by hand. You know why from the house rules.

```c
#include <stdio.h>

int main(void)
{
    double loaf = 4.25;
    double coffee = 12.99;
    double oil = 19.99;

    double total = loaf + coffee + oil;

    printf("Total is %f\n", total);

    return 0;
}
```

You've seen the first four lines and the last two before, in the Toolbench. `#include <stdio.h>` pastes in the descriptions of the input and output functions so the compiler knows what `printf` is. `int main(void)` is the function that runs when the program starts. `return 0` hands zero back to the shell to mean success. Braces group the body together.

The three new ideas are all in the middle.

**Three variables, declared and initialised.** Each sets aside room for a `double` and puts a price in it.

**A fourth variable built out of the first three.** The right-hand side, `loaf + coffee + oil`, is an **expression**: something that produces a value. C works out the value first, then the assignment puts it into `total`. The four arithmetic operators are `+`, `-`, `*` for multiply and `/` for divide, and they follow the precedence you learned at school, so `2 + 3 * 4` is 14 rather than 20. Brackets override it, exactly as you'd expect.

**A `printf` with something in it.** Up to now every `printf` you've written just printed fixed text. This one has two parts:

```c
printf("Total is %f\n", total);
        ^^^^^^^^^^^^^^^  ^^^^^
        the format string   the value to plug in
```

The `%f` is a **placeholder**. It says "when you print this text, stop here and print the value I gave you afterwards, formatted as a number with a fractional part." The `f` stands for floating point, which is the technical name for the kind of number a `double` holds.

The comma separates the format string from the values. You can have several placeholders and several values, in order.

Save with Ctrl+O, Enter, then Ctrl+X. Compile it with the house command from the Toolbench:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o till till.c
$ ./till
Total is 37.230000
```

The arithmetic's right. 4.25 plus 12.99 plus 19.99 is 37.23. But nobody prints a price like that.

### Making it look like money

`%f` prints six digits after the point, because that's its default and nobody ever changed it. You want two.

You can tell a placeholder how many digits you want by putting a dot and a number in front of the `f`:

```c
    printf("Total is $%.2f\n", total);
```

Read `%.2f` as "a floating point number, with exactly 2 digits after the decimal point." The number after the dot is the **precision**.

Change that line, recompile, and run:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o till till.c
$ ./till
Total is $37.23
```

The `$` is just a character sitting in the format string. Anything in there that isn't a placeholder gets printed exactly as you typed it, which is how `Total is` got there too.

Hold on to the fact that `%.2f` rounded something to fit. It printed two digits out of a number that had more. That'll matter enormously in about ten minutes.

### Now build Maria's actual basket

Here's a real basket from Maria's shop.

Two sourdough loaves at $4.25 each. Three croissants, on the "3 for $8.00" deal. One bag of coffee beans, $12.99. One bottle of olive oil, $19.99.

The croissant deal is the interesting one. Three of them cost $8.00 together, so one costs eight dollars divided by three. Let C do that division:

```c
    double croissant = 8.00 / 3;
```

Replace the whole of `till.c` with this. It's longer, but there's nothing in it beyond what you just learned: variables, arithmetic, and `printf` with a placeholder.

```c
#include <stdio.h>

int main(void)
{
    double loaf = 4.25;
    double croissant = 8.00 / 3;
    double coffee = 12.99;
    double oil = 19.99;

    double total = loaf + loaf
                 + croissant + croissant + croissant
                 + coffee + oil;

    printf("SOURDOUGH & CO\n");
    printf("\n");
    printf("Sourdough loaf        $%.2f\n", loaf);
    printf("Sourdough loaf        $%.2f\n", loaf);
    printf("Croissant             $%.2f\n", croissant);
    printf("Croissant             $%.2f\n", croissant);
    printf("Croissant             $%.2f\n", croissant);
    printf("Coffee beans 250g     $%.2f\n", coffee);
    printf("Olive oil 500ml       $%.2f\n", oil);
    printf("\n");
    printf("TOTAL                 $%.2f\n", total);

    return 0;
}
```

Two small things while you type.

The `total` calculation runs over three lines. C doesn't care about line breaks inside an expression, it reads until it finds the semicolon. Breaking a long calculation across lines to make it readable is normal and I'd encourage it.

The spacing that lines the prices up is just spaces typed into the format strings. Crude, but completely transparent, and you can see exactly where every character comes from. There's a proper way to do columns and you'll meet it in Part 3, once you've got a reason to want it.

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o till till.c
$ ./till
SOURDOUGH & CO

Sourdough loaf        $4.25
Sourdough loaf        $4.25
Croissant             $2.67
Croissant             $2.67
Croissant             $2.67
Coffee beans 250g     $12.99
Olive oil 500ml       $19.99

TOTAL                 $49.48
```

That's a receipt. It compiled with no warnings at the strictest settings we have. The prices are right, the layout's tidy, the total looks entirely plausible.

Maria's nephew looked at this and shipped it.

### Now be Maria

Add up the item lines by hand. Not the total. The lines.

```
 4.25
 4.25
 2.67
 2.67
 2.67
12.99
19.99
```

That comes to **49.49**.

The receipt says the total is **49.48**.

Read that again, because it's the whole chapter. Your program printed seven numbers, then printed an eighth that claims to be their sum, and it isn't their sum. It's one cent less.

Nothing on that receipt looks wrong. No warning fired. No sanitizer would complain. The program did exactly what you told it to do.

### What you've just found

Maria's stock system adds up the line items to work out what each basket should have brought in. The card terminal charges the total. Those two numbers now disagree by one cent, on every basket containing a "3 for" deal, and she sells those all day.

There's the missing money.

Before we fix it, get one clue. Add a temporary line right after the croissant variable to look at what the program is actually holding:

```c
    double croissant = 8.00 / 3;
    printf("[debug] croissant = %.20f\n", croissant);
```

`%.20f` is the same placeholder with the precision turned up to twenty digits.

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o till till.c
$ ./till
SOURDOUGH & CO

[debug] croissant = 2.66666666666666651864
Sourdough loaf        $4.25
...
```

The program isn't holding 2.67. It never was. It's holding 2.66666666666666651864.

When it prints that with `%.2f`, it rounds to 2.67, because that's what rounding to two places does. When it adds it into the total, it adds all the sixes. Three lots of all-the-sixes is 8.00, not 8.01.

So the receipt is telling two different stories at once. The lines come from rounded copies. The total comes from the real values. Nobody decided that. It happened, because nobody thought about where rounding should happen.

That's bug number one, and it isn't really a C bug at all. It's a bug in thinking.

Bug number two is underneath it, it's much stranger, and it's the reason those digits end in `651864` rather than `666666`. Take the debug line out and read on.

---

## Part 2: Under the hood

No new syntax here. You've already got everything you need. This is thirty minutes of looking at what your machine is actually doing with the numbers you gave it, and it's the part that makes the fix in Part 3 obvious rather than arbitrary.

### Looking inside a variable

Make a new file, `probe.c`. It's a scratchpad you'll add to a few times.

```c
#include <stdio.h>

int main(void)
{
    printf("0.1     is stored as %.20f\n", 0.1);
    printf("0.2     is stored as %.20f\n", 0.2);
    printf("0.1+0.2 is stored as %.20f\n", 0.1 + 0.2);
    printf("0.5     is stored as %.20f\n", 0.5);
    printf("0.25    is stored as %.20f\n", 0.25);

    return 0;
}
```

You can hand `printf` a plain number instead of a variable. A number written directly in your code like that is a **literal**, and `0.1` on its own is a `double` just as much as a variable is.

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o probe probe.c
$ ./probe
0.1     is stored as 0.10000000000000000555
0.2     is stored as 0.20000000000000001110
0.1+0.2 is stored as 0.30000000000000004441
0.5     is stored as 0.50000000000000000000
0.25    is stored as 0.25000000000000000000
```

You typed `0.1` and your machine stored something that isn't 0.1.

You typed `0.2` and got something that isn't 0.2.

You added them and got something that isn't 0.3, and notice the error in the sum is bigger than either of the two that went into it. The addition made things worse all by itself.

But `0.5` is stored perfectly. So is `0.25`. Whatever's going wrong isn't going wrong for every number.

### Why 0.1 isn't 0.1

How the Machine Thinks gave you the short version. Here's the one that explains the pattern you just saw.

Start with a system you already trust. Write one third in decimal. You get 0.3333333, you have to stop somewhere, and wherever you stop you're slightly wrong. Add digits forever and you never land on it.

That isn't a failure of your arithmetic. Decimal is built on tens, and one third isn't any whole number of tenths, hundredths, or thousandths. There's no number of decimal places that gets you there, because the answer isn't in the set of numbers decimal can express.

Your machine has the same problem with a different set of numbers, because it's built on twos.

A `double` stores a number the way scientific notation does, except in base two. It keeps a sign, an exponent, and 53 bits' worth of significant digits. Whatever value you want, it has to be expressed as some whole number multiplied by some power of two. If your value can't be written that way, the machine can't store it, full stop, and it stores the closest one it can instead.

Now look back at your output and the pattern falls out.

**0.5** is 1 × 2⁻¹. One whole number times a power of two. Exact.

**0.25** is 1 × 2⁻². Exact.

**0.75** is 3 × 2⁻². Exact.

**0.1** isn't any whole number times any power of two. There's no such pair, and no amount of extra bits creates one. Inexact, forever.

The gap between 0.1 and the nearest number your machine can store is about one part in ten thousand trillion. Small enough that it'll never bother you on its own.

It doesn't stay on its own.

### The errors pile up

Add this to `probe.c`:

```c
    double tenths = 0.1 + 0.1 + 0.1 + 0.1 + 0.1
                    + 0.1 + 0.1 + 0.1 + 0.1 + 0.1;

    printf("ten tenths     = %.20f\n", tenths);
    printf("off by         = %.20f\n", 1.0 - tenths);
```

Ten tenths. One. Nothing controversial about the arithmetic.

```
ten tenths     = 0.99999999999999988898
off by         = 0.00000000000000011102
```

Add one tenth ten times and you don't get one. You get a number very slightly less than one, because each of the nine additions brought in a bit more error and they all leaned the same way.

Now imagine that's not ten additions but four hundred, which is Maria's Tuesday. Or a hundred thousand, which is a payroll run.

This is also the single most common way floating point ruins somebody's afternoon, and it has nothing to do with printing. A program that checks whether the drawer balances by asking `if (counted == expected)` will say no when a human looking at the same two numbers would say yes, and the programmer will stare at two identical-looking numbers on screen for an hour. Don't compare floating point values for exact equality. There's a compiler flag that enforces that, and you'll turn it on in Part 3 once you've met `if` and it'll mean something.

### `float` is worse than `double`, and here's how much worse

There are two floating point types in ordinary use. A `float` takes 4 bytes. A `double` takes 8. More bytes means more bits for the significant digits, which means smaller gaps between the numbers you can store.

The name `float` looks like the obvious choice for "a number with a decimal point," so beginners reach for it constantly. Look at what it does to one of Maria's prices. Add this to `probe.c`:

```c
    float f = 19.99f;
    printf("19.99 in a float = %.20f\n", f);
```

One oddity in that snippet, worth a sentence. The `f` on the end of `19.99f` says "this literal is a `float`." Without it, `19.99` is a `double` that then gets squeezed down into a `float`, which works but is worth being explicit about.

You might expect `%f` to be wrong here, since it's the placeholder for a `double`. It isn't. When a `float` is handed to `printf`, C automatically widens it to a `double` on the way in, so `%f` is correct and there's no separate placeholder for `float` at all. That widening is why the digits below are the exact contents of the `float`, faithfully copied into a bigger box.

```
19.99 in a float = 19.98999977111816406250
```

Your machine can't hold 19.99 in a `float` at all. It holds 19.9899997711, which is wrong by about two millionths of a dollar. After a few thousand additions that's real money.

I'll give you a rule I've never regretted: if you've decided to use floating point, use `double`. `float` exists for graphics work and for enormous arrays where halving the memory matters more than the digits do. It isn't a general purpose type and it isn't the one you want.

### How big is a box, and what fits in it?

You've been told a `double` is 8 bytes and a `float` is 4. Don't take my word for it. Ask the machine.

Write `sizes.c`. This one's worth keeping around.

```c
#include <stdio.h>
#include <limits.h>
#include <float.h>

int main(void)
{
    printf("char   %zu byte   %d to %d\n", sizeof(char), CHAR_MIN, CHAR_MAX);
    printf("int    %zu bytes  %d to %d\n", sizeof(int), INT_MIN, INT_MAX);
    printf("long   %zu bytes  %ld to %ld\n", sizeof(long), LONG_MIN, LONG_MAX);
    printf("float  %zu bytes  about %d significant digits\n", sizeof(float), FLT_DIG);
    printf("double %zu bytes  about %d significant digits\n", sizeof(double), DBL_DIG);

    return 0;
}
```

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o sizes sizes.c
$ ./sizes
char   1 byte   -128 to 127
int    4 bytes  -2147483648 to 2147483647
long   8 bytes  -9223372036854775808 to 9223372036854775807
float  4 bytes  about 6 significant digits
double 8 bytes  about 15 significant digits
```

Five new things in that little program. Take them one at a time.

**`sizeof`** isn't a function even though it looks like one. It's an operator built into the language, like `+`. Give it a type and it tells you how many bytes that type takes on this machine. It's worked out at compile time, so it costs nothing at runtime.

**`%zu`** is the placeholder for whatever type `sizeof` produces, which is called `size_t`. It's a whole number type, it can never be negative, and it's guaranteed big enough to describe the size of anything. Use `%zu` for it. Using `%d` there is a bug and `-Wall` will catch it.

**`<limits.h>` and `<float.h>`** are headers containing nothing but names for values. `INT_MAX` isn't a variable. It's a name the preprocessor swaps for `2147483647` before the compiler ever sees your file. Using the name rather than the number keeps your code correct on a machine where the number is different.

**`%ld`** is the placeholder for a `long`. Not `%d`. That distinction is about to become a bug you can name.

**Two new types.** A `char` holds one byte, and you'll meet it properly at the end of Part 3. An `int` holds a whole number with no fractional part, and it's what you'll use for counting things.

Now read the output for what it tells you. Six significant digits in a `float`, which is exactly why 19.99 came out as 19.9899997: the digits ran out. Fifteen in a `double`, which is a lot, and is still a fixed number, and money arithmetic in a real business chews through fixed numbers.

### Whole numbers run out too

Floating point is inexact, which is why we're heading towards whole numbers. Whole numbers are exact. But they're exact only inside a fence, and what happens at the fence is worse than being slightly off.

Add this to `probe.c`:

```c
    int dollars = 1073741824;
    printf("one billion doubled = %d\n", dollars * 2);
```

That starting number is a bit over a billion. Doubling it should give a bit over two billion.

```
one billion doubled = -2147483648
```

You've just doubled a billion dollars and ended up two billion in debt.

Here's why, and it's worth the paragraph. An `int` is 32 bits. One of those records the sign, so the largest value it holds is 2147483647, which is exactly the `INT_MAX` you printed a minute ago. The correct answer, 2147483648, needs one more bit than exists. In ordinary arithmetic you'd carry into the next column. There is no next column. The carry lands in the sign bit instead, and the number comes out as the most negative value the type can hold.

That's **integer overflow**, and the compiler can't warn you about it in general, because it has no way of knowing at compile time what'll be in that variable when the program runs. So ask the sanitizer, exactly as you did in the Toolbench:

```
$ gcc -std=c17 -Wall -Wextra -g -fsanitize=undefined -o probe-ub probe.c
$ ./probe-ub
...
probe.c:23:47: runtime error: signed integer overflow: 1073741824 * 2 cannot be represented in type 'int'
one billion doubled = -2147483648
```

File, line, the two numbers involved, and the type that couldn't hold the result. It reported and let the program carry on, which is what the undefined behaviour sanitizer does.

The fix is a bigger fence. Change `int` to `long` and `%d` to `%ld` and the same sum is fine, because a `long` reaches to about nine quintillion. Still a fence, just much further out.

> **Under the hood: this has taken down real things.**
>
> A Boeing 787 had a counter that ticked up ten times a second into a 32-bit integer. After 248 days of continuous power it overflowed, and the failure mode was every generator control unit dropping into failsafe at once. Boeing's interim instruction to airlines was to power each aircraft down completely every so often, which is the aviation version of turning it off and on again.
>
> The original Pac-Man stored the level number in one byte, which holds 0 to 255. Nobody at the company imagined a human reaching level 256. When one did, the level rendered as garbage and the game was unplayable.
>
> On 19 January 2038, any system still counting seconds since 1970 in a 32-bit signed integer runs out of fence. The fix is what it was for the year 2000 problem: more bits, applied early.
>
> Every one of those is the two lines you just wrote.

### Whole-number division throws away the part you wanted

One more thing about whole numbers. Add this to `probe.c`:

```c
    printf("7 / 2 = %d\n", 7 / 2);
    printf("1 / 3 = %d\n", 1 / 3);
    printf("7 %% 2 = %d\n", 7 % 2);
    printf("8 %% 3 = %d\n", 8 % 3);
```

```
7 / 2 = 3
1 / 3 = 0
7 % 2 = 1
8 % 3 = 2
```

In C, a whole number divided by a whole number gives a whole number. Not a rounded one. A **truncated** one: everything after the decimal point gets thrown away, including 0.99999.

That isn't an accident or an oversight, it's a decision. Whole-number division is a single machine instruction and it's fast, and C gives you a second operator that hands you exactly what the division discarded.

That second operator is `%`, and it gives the **remainder**. `7 / 2` is 3 and `7 % 2` is 1, and together they say "seven is three twos with one left over."

Those two working as a pair are about to do all the real work in this chapter, so spend a minute getting comfortable. `17 / 5` is 3 and `17 % 5` is 2, because seventeen is three fives and two left over. `9 / 3` is 3 and `9 % 3` is 0, because it divides exactly.

> **Two traps with `%`.**
>
> It only works on whole numbers. `7.5 % 2` won't compile. There's a function called `fmod` in `<math.h>` for the floating point version.
>
> With negative numbers, C truncates towards zero, so `-7 % 3` is `-1` and not `2`. If you're used to the mathematician's modulo, that'll surprise you. It matters in Chapter 2 when you write a cipher that wraps around the alphabet.

### Casting: telling C to treat a value as a different type

Sometimes the type C infers isn't the one you want for a particular calculation. Look at what happens when you try to get a fractional answer out of two whole numbers:

```c
    int a = 1;
    int b = 3;
    printf("%f\n", (double) a / b);
```

Without the cast, `a / b` is whole-number division and gives 0, and you'd be printing 0.000000 and wondering where your fraction went.

A **cast** is a type name in brackets, in front of a value. `(double) a` means "take the value in `a` and treat it as a `double`, right here." Once one side of the division is a `double`, C widens the other to match and does floating point division:

```
0.333333
```

Two rules about casting that'll save you time.

Cast before the operation, not after. `(double) (a / b)` is too late: the division already happened in whole numbers and gave 0, and you've carefully converted 0 into 0.0.

A cast to a narrower type throws information away, silently. `(int) 7.9` is 7, not 8. It truncates, exactly like division does. That's occasionally what you want and more often a bug.

### Escape sequences, and printing a percent sign

Did you notice `%%` in the remainder examples above?

Inside a format string, `%` starts a placeholder. So to print an actual percent sign you type two of them and `printf` prints one. Type a single one and `printf` reads the next character as a placeholder type and does something baffling.

There's a matching idea for characters you can't type directly, and you've been using one since the Toolbench without a proper introduction.

`\n` isn't a backslash and an n. It's one character, a newline, and the backslash is how you write a character that has no key of its own. That's an **escape sequence**. The backslash escapes the normal meaning of the character after it.

The ones you'll actually use:

| You type | You get |
|---|---|
| `\n` | a newline, moving to the start of the next line |
| `\t` | a tab |
| `\"` | a double quote, without ending the string |
| `\\` | one backslash |
| `%%` | one percent sign (a `printf` thing rather than an escape sequence) |

`\"` is the one worth pausing on. If you want quotation marks in your output you can't just type them, because the first one you type ends the string as far as the compiler is concerned and everything after it becomes gibberish. So:

```c
    printf("She said \"no receipt, thanks\".\n");
```

```
She said "no receipt, thanks".
```

And since the backslash now has a special job, printing a literal backslash takes two of them.

You've now got everything you need to fix Maria's till.

---

## Part 3: Build it properly

We're going to rebuild Maria's till from scratch. Not by patching the old one, because the old one is built on a decision nobody made on purpose.

But first, the two fixes everybody tries. Both fail. Understanding why is what makes the third one stick instead of feeling like a rule somebody handed you.

### Failed fix number one: use more precision

The croissant price was wrong in the fifteenth digit. So use a bigger type?

There's nothing meaningfully bigger than `double` in standard C. `long double` exists and just moves the fence further out. And look at what actually went wrong on the receipt: it wasn't off by a fifteenth of a cent. It was off by a whole cent, because the lines and the total got rounded at different moments.

Precision was never the problem. Move on.

### Failed fix number two: just round everything

This is the one that feels right. There's a `round` function in the standard library. Round each value to the nearest cent as you go and surely everything lines up.

Write `two.c`:

```c
#include <stdio.h>
#include <math.h>

int main(void)
{
    double price = 2.675;

    printf("printf rounds it to   %.2f\n", price);
    printf("round() rounds it to  %.2f\n", round(price * 100) / 100);

    return 0;
}
```

`round` lives in `<math.h>`, so that header goes at the top alongside `<stdio.h>`. The expression `round(price * 100) / 100` is the standard trick for rounding to two places: multiply by 100 so the cents become whole numbers, round to the nearest whole number, divide by 100 to put the decimal point back.

Compile it the usual way:

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o two two.c
/usr/bin/ld: /tmp/ccbIIt9I.o: in function `main':
/home/you/toc/ch01/two.c:8: undefined reference to `round'
collect2: error: ld returned 1 exit status
```

Stop and read that, because it's a new kind of error and recognising it will save you an evening one day.

Look at what produced it: `/usr/bin/ld`. That's the **linker**, not the compiler. The Toolbench mentioned that "compiling" is really four programs in a row, and the linker is the last of them. Its job is to join your code to the library code that contains the real `printf`, `round` and everything else.

So your code compiled perfectly. The complaint came later, when the linker went looking for a function called `round` and couldn't find it in any of the libraries it was given.

The reason is a piece of history nobody has ever cleaned up. The maths functions live in a separate library file from the rest of the standard library. Including `<math.h>` tells the compiler what `round` looks like, but you also have to tell the linker where to find it.

> **New flag: `-lm`.**
>
> `-l` means "link against a library" and `m` is the maths one. So `-lm` is "also look in the maths library."
>
> It goes at the end of the command, after your source file. That isn't a style preference. The linker processes its inputs left to right and only pulls a function out of a library if something it's already read has asked for it. Put `-lm` first and it looks at the maths library before it knows it needs anything from it, finds nothing wanted, and moves on.
>
> ```
> $ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o two two.c -lm
> $ ./two
> printf rounds it to   2.67
> round() rounds it to  2.68
> ```

Now look at what it printed.

The same number. Two different answers. One cent apart.

`printf("%.2f", 2.675)` gives 2.67 because the value actually stored is 2.674999999999999822, which is below the halfway point, so it rounds down. `round(2.675 * 100) / 100` gives 2.68 because multiplying that stored value by 100 lands on exactly 267.5, and `round` sends halves away from zero.

So rounding didn't fix anything. I find this the single most convincing demonstration in the chapter, because the instinct to reach for `round` is so strong and it produces a second, differently wrong answer, and now you've got two rounding behaviours inside one program that disagree about the same money.

> **Trap: `printf` rounds ties to even.**
>
> On Debian, which uses the GNU C library, `printf("%.2f", 0.125)` prints `0.12` while `printf("%.2f", 0.375)` prints `0.38`. Both are exact halves. Rather than always rounding up, glibc rounds towards the even digit.
>
> There are good statistical reasons for that and it's completely astonishing the first time a client asks why one invoice went down and another went up. Note it, and take it as one more argument for not letting `printf` decide where your money goes.

### The fix: money isn't a decimal number, it's a count

Here it is, and it's a change of mind rather than a change of syntax.

Maria doesn't have 49.48 dollars. She has **4948 cents**.

A cent is the smallest unit that exists in her world. There's no such thing as half a cent in her drawer, in her bank account, or on her tax return. The decimal point on a receipt is a display convention for humans. It isn't a fact about the money.

So stop storing a fraction of a dollar. Start storing a count of cents.

`$4.25` becomes `425`. `$19.99` becomes `1999`. `$8.00` becomes `800`.

A count is a whole number. Whole numbers are exact. There's nothing to round, because there's nothing after the decimal point to round away. The value you put in the variable is the value that comes out, through any number of additions, forever.

I want to be clear this isn't a trick I invented for teaching. It's what every payments system, bank ledger and point of sale terminal in the world does. When you see a price stored as `1999` in a database, that's why.

**Which whole-number type?** An `int` reaches 2,147,483,647, which as cents is $21,474,836.47. Maria will never take that in a day, but a business with several shops adding up a year could get closer than you'd like, and no program should have an arithmetic ceiling it didn't choose. Use `long`, which reaches about ninety-two quadrillion cents.

And remember: a `long` prints with `%ld`, never `%d`.

### Printing a count as money

If the variable holds 850, how do you print `$8.50`?

Use the two operators from Part 2 together. Whole-number division gives you the dollars, and the remainder gives you the cents.

```
850 / 100  is 8      (the dollars, with the rest thrown away)
850 % 100  is 50     (the rest, which is exactly the cents)
```

Start the new program. Open `receipt.c` and type just this much:

```c
#include <stdio.h>

int main(void)
{
    long loaves = 2 * 425;

    printf("Two loaves cost $%ld.%ld\n", loaves / 100, loaves % 100);

    return 0;
}
```

Notice there are now two placeholders and two values after the format string, in order. The first `%ld` gets `loaves / 100` and the second gets `loaves % 100`. The `.` between them is just a character in the string, like the `$`.

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o receipt receipt.c
$ ./receipt
Two loaves cost $8.50
```

No floating point involved anywhere. That number is exact and it'll stay exact.

Now break it on purpose, because there's a bug hiding in that line. Change `425` to `402` and run it again:

```
Two loaves cost $8.4
```

Two loaves at $4.02 is $8.04, and it printed $8.4.

`804 % 100` is 4, and `%ld` prints the number 4 as one character. You want it padded to two digits with a zero in front.

That's what the extra characters in a placeholder are for. Change the second placeholder to `%02ld`:

```c
    printf("Two loaves cost $%ld.%02ld\n", loaves / 100, loaves % 100);
```

```
Two loaves cost $8.04
```

Read `%02ld` in pieces, right to left. `ld` is the type, a `long`. The `2` is a **minimum field width**, meaning "make this at least 2 characters wide." The `0` is a **flag**, meaning "pad it with zeros rather than spaces."

Field width is worth understanding properly because you'll use it constantly.

- `%ld` prints `4`
- `%2ld` prints ` 4` (padded with a space)
- `%02ld` prints `04` (padded with a zero)
- `%6ld` prints `     4` (padded to six characters)

Width is a minimum, never a maximum. A number too big for the field never gets chopped, it just overflows and pushes your columns out of line. That's why a receipt suddenly goes crooked when one price is unexpectedly large.

> **Reference: everything that can go in a placeholder.**
>
> You've now got all the pieces, so here they are in one place. A placeholder is `%`, then optional flags, then an optional width, then an optional precision, then the type letter. Only the `%` and the letter are required.
>
> ```
>       %  -0   6   .2   f
>          ^^   ^   ^^   ^
>       flags width prec type
> ```
>
> **Type letter.** This has to match what you actually pass, or `-Wall` will tell you off.
>
> | Letter | For | Example output |
> |---|---|---|
> | `%d` | `int` | `42` |
> | `%ld` | `long` | `9000000000` |
> | `%zu` | `size_t`, what `sizeof` gives | `8` |
> | `%f` | `double` (a `float` gets widened to one) | `4.082100` |
> | `%c` | one `char` | `y` |
> | `%s` | text | `Croissant` |
> | `%%` | a literal percent sign | `%` |
>
> **Width** is a number before the letter, and it's a minimum. `%6ld` prints at least six characters, padding on the left with spaces.
>
> **Precision** is a dot and a number. For `%f` it means digits after the point: `%.2f` gives two, `%.20f` gives twenty. The default is six, which is why `printf("%f", 4.25)` prints `4.250000`.
>
> **Flags** come first. `-` pads on the right rather than the left, which left-aligns text: `%-22s`. `0` pads numbers with zeros rather than spaces: `%02ld`.
>
> Put together, `%-22s` and `$%6ld.%02ld` are what make the receipt line up. Nothing else in the program cares how it looks.

Put `425` back and move on.

### Giving things names

The tax rate is about to appear in this program. Written as `0.0825` it drags you straight back into floating point. So write it as a whole number instead.

Finance has a unit for exactly this. A **basis point** is one hundredth of one percent, so 8.25% is 825 basis points, and tax on an amount becomes:

```
tax = amount × 825 ÷ 10000
```

All whole numbers. But a bare `825` sitting in the middle of an expression is a problem, and it has a name. Programmers call it a **magic number**. Nobody reading it can tell whether it's a tax rate, a product code, or a typo. Worse, when the rate changes you have to find every copy, and one day you'll miss one.

So give it a name:

```c
int main(void)
{
    // Sales tax in basis points. A basis point is one hundredth of a
    // percent, so 825 basis points means 8.25 percent.
    const long TAX_BASIS_POINTS = 825;

    long subtotal = 4948;
    long tax = subtotal * TAX_BASIS_POINTS / 10000;

    printf("Tax: $%ld.%02ld\n", tax / 100, tax % 100);

    return 0;
}
```

Two new things there.

**A comment.** Everything from `//` to the end of the line is ignored by the compiler completely. It's a note for whoever reads this next, which is usually you in six months with no memory of having written it. There's also `/* ... */`, which can run across several lines.

Write comments that say why, not what. `// add one to i` is noise, because the code already says that. `// basis points, so 825 means 8.25 percent` is the difference between the next reader understanding this file and breaking it.

**`const`.** This says the value must never change after it's set. Try adding `TAX_BASIS_POINTS = 900;` on the next line and the compiler refuses to build:

```
receipt.c:12:23: error: assignment of read-only variable 'TAX_BASIS_POINTS'
```

That's the whole point. You're protecting the program from a future edit, quite possibly by you, quite possibly at 11pm.

**The capital letters** are a convention rather than a rule. C programmers write constants in `UPPER_CASE` so a reader can tell at a glance that a name refers to something fixed. Ordinary variables get `lower_case`. Follow it and your code will look like everyone else's, which is the entire goal of a convention.

### Working out the tax, correctly

Run what you just wrote:

```
Tax: $4.08
```

Correct. 49.48 × 0.0825 is 4.0821, which as money is $4.08.

But it's correct by luck, and a right answer for the wrong reason is worse than a wrong one, because you won't go looking for it.

Work through what the machine actually did:

```
4948 × 825       = 4082100
4082100 / 10000  = 408        (the remainder, 2100, is thrown away)
```

Whole-number division truncates, and this time truncating happened to be right. Now suppose the basket had been slightly different and the exact tax was 4.087 dollars. The customer owes $4.09. Truncation would give $4.08, Maria loses a cent, and we're back where we started with a different mechanism.

The fix is one term, and it's worth understanding rather than memorising.

You want to round to the nearest whole number, but the only tool you have throws the remainder away. So push the number over the line before the truncation happens, by adding half of what you're about to divide by.

Half of 10000 is 5000.

```c
    long tax = (subtotal * TAX_BASIS_POINTS + 5000) / 10000;
```

Check it by hand on the two cases.

When it should round down, the exact answer is 4.0821, so `4948 × 825 = 4082100`. Add 5000 to get 4087100. Divide by 10000 and truncate: **408**. Correct, still $4.08.

When it should round up, imagine a product of 4087000, which is 408.7 after dividing. Truncation alone gives 408. Add 5000 to get 4092000, divide and truncate: **409**. Correct.

The added 5000 pushes anything with a remainder of 5000 or more up into the next whole number and leaves everything below it alone. That's round-half-up, done exactly, with no floating point and no arguments about ties.

This pattern turns up everywhere once you notice it. To round `a / b` to the nearest whole number in integer arithmetic, write `(a + b / 2) / b`.

### Making decisions

Maria wants two rules in the till. Baskets over $50 get 10% off. And a quantity that's zero or negative should be refused rather than printed.

Both need the program to choose, and choosing is what `if` is for.

```c
    if (subtotal > 5000)
    {
        printf("Discount applied.\n");
    }
```

The parentheses hold a **condition**, a question the program asks itself. The braces hold a **block**, the code to run if the answer is yes. If it's no, the whole block is skipped and the program carries on below it.

The comparison operators:

| Operator | Means |
|---|---|
| `<` | less than |
| `>` | greater than |
| `<=` | less than or equal to |
| `>=` | greater than or equal to |
| `==` | equal to |
| `!=` | not equal to |

The last two need explaining.

`<=` and `>=` are spelled with two characters because there's no key on your keyboard for the proper mathematical symbols. Nothing deeper than that.

`==` is two equals signs because one was already taken for assignment, which you learned at the start of Part 1. `price = 425` puts 425 into price. `price == 425` asks whether price holds 425. Confusing them is the single most common typo in the C language, which is why `-Wall` has a warning dedicated to it and why you met that warning in the Toolbench.

A second branch with `else`:

```c
    if (subtotal > 5000)
    {
        printf("Discount applied.\n");
    }
    else
    {
        printf("No discount today.\n");
    }
```

`else` has no condition of its own. It runs when the `if` didn't.

A chain with `else if`:

```c
    if (quantity < 0)
    {
        printf("Quantity cannot be negative.\n");
    }
    else if (quantity == 0)
    {
        printf("Nothing to sell.\n");
    }
    else
    {
        printf("Selling %d.\n", quantity);
    }
```

Exactly one branch of that chain runs. As soon as one condition is true, the rest aren't even asked.

That last `else` deliberately has no condition, and it's a small piece of design worth absorbing now. If quantity isn't negative and isn't zero, it must be positive. Asking a third question whose answer you've already worked out is work the machine does for nothing. Worse, it's a habit that produces genuinely broken code once the conditions get complicated enough for you to miscount a boundary and leave a case with no branch at all.

**Combining conditions.** Three more operators:

```c
    if (quantity > 0 && quantity <= 100)    // both must be true
    if (day == 6 || day == 0)               // either one is enough
    if (!is_member)                         // true when is_member is false
```

`&&` is "and", `||` is "or", `!` is "not". The doubled characters are again because the single ones mean something else.

These **short circuit**, meaning C stops as soon as it knows the answer. In `a && b`, if `a` is false the whole thing is false, so `b` is never evaluated at all. That's a guarantee in the language standard rather than an optimisation you're hoping for, and you'll lean on it heavily in Chapter 4.

**True and false.** C17 doesn't have those words built in. Add a header:

```c
#include <stdbool.h>

    bool is_member = true;

    if (is_member && subtotal > 5000)
    {
        printf("Member discount.\n");
    }
```

A `bool` holds one of exactly two values.

> **Under the hood: C's idea of true is looser than you'd think.**
>
> Underneath, C treats zero as false and anything else as true. That's why `if (!is_member)` works, and why `if (count)` is a legal way to write "if count isn't zero."
>
> It's also why the `= instead of ==` typo is so dangerous. `if (total = 0)` assigns zero to total, and the value of that assignment is zero, which is false, so the block silently never runs and your variable has been wiped on the way past.

> **Debian note.** In C23, which is what gcc 14 uses when you don't pin a standard, `bool`, `true` and `false` became keywords and `<stdbool.h>` is no longer needed. Because this book pins `-std=c17`, you do need the header. If you ever drop the `-std` flag and it suddenly compiles without it, that's why. Keep the pin and keep the header.

Now that you know what `if` means, we can close something Part 2 left open.

> **New flag: `-Wfloat-equal`.**
>
> Part 2 showed that ten tenths don't add up to one. Here's that as a bug a program would actually contain:
>
> ```c
> double tenths = 0.1 + 0.1 + 0.1 + 0.1 + 0.1
>                 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1;
>
> if (tenths == 1.0)
> {
>     printf("balanced\n");
> }
> else
> {
>     printf("OFF\n");
> }
> ```
>
> The house flags say nothing about it:
>
> ```
> $ gcc -std=c17 -Wall -Wextra -Wpedantic -o feq feq.c
> $ ./feq
> OFF
> ```
>
> Add one flag:
>
> ```
> $ gcc -std=c17 -Wall -Wextra -Wpedantic -Wfloat-equal -o feq feq.c
> feq.c: In function 'main':
> feq.c:6:15: warning: comparing floating-point with '==' or '!=' is unsafe [-Wfloat-equal]
>     6 |     if (tenths == 1.0)
>       |                ^~
> ```
>
> It isn't in `-Wall` or `-Wextra` because there are a few legitimate reasons to compare floating point values exactly and the maintainers didn't want to nag every C programmer in the world. For a program that handles money, you want it on. It goes into this chapter's Makefile at the end.

### Doing something more than once

Look back at the program you wrote in Part 1. Three identical croissant lines, typed out three times. If Maria sells six croissants you type three more. If the layout changes you edit all of them and miss one.

Copying is the signal. Whenever I catch myself copying a line and changing one number in it, I stop, because what I want is a loop.

**The `for` loop** is the one you'll use most, and it packs three separate ideas onto one line, which is why it looks intimidating at first. Take it apart:

```c
    for (int i = 0; i < 3; i++)
    {
        printf("Croissant\n");
    }
```

Inside the parentheses are three parts, separated by semicolons.

`int i = 0` runs once, before anything else. It creates a counting variable. `i` is the traditional name, short for index.

`i < 3` is a condition, checked before every pass including the first. True and the block runs. False and the loop is finished and the program moves on past it.

`i++` runs after every pass, before the condition is checked again. It means "add one to i."

So the machine does this. Make `i` zero. Is 0 less than 3? Yes, run the block. Add one, `i` is 1. Is 1 less than 3? Yes, run the block. Add one, `i` is 2. Is 2 less than 3? Yes, run the block. Add one, `i` is 3. Is 3 less than 3? No. Stop.

Three passes, with `i` holding 0, then 1, then 2.

**Changing a variable by a bit.** `i++` adds one. So does `i += 1`, and so does `i = i + 1`. All three compile to the same thing and you'll see all three in real code.

`+=` works with any amount, and it's how you'll accumulate a total:

```c
    subtotal += loaves;      // exactly the same as subtotal = subtotal + loaves;
```

There are matching `-=`, `*=` and `/=`. And `i--` subtracts one.

There's also `++i`, which differs from `i++` only when you use the result in a larger expression: `i++` hands back the old value and then increments, `++i` increments and hands back the new one. In a `for` loop's third slot the result is discarded, so they're identical there. Write code that doesn't depend on the difference and you'll never have to think about it.

> **Trap: start at zero and use `<`.**
>
> You could write `for (int i = 1; i <= 3; i++)`. It also gives three passes. Don't.
>
> Counting from zero with a strict `<` is the universal convention in C, and the reason arrives in Chapter 2: positions in an array start at zero, so `i < count` lines up exactly with the valid positions while `i <= count` runs one step off the end and reads memory that isn't yours.
>
> Build the habit here, on a loop where it makes no difference, so it's automatic there, where it's the difference between working code and a security hole. One of the bugs in Part 4 is exactly this mistake.

**The `while` loop** is simpler. It has a condition and nothing else:

```c
    long remaining = 4948;

    while (remaining >= 2500)
    {
        printf("Hand over a $25 note.\n");
        remaining -= 2500;
    }
```

It checks the condition, runs the block if true, and goes back to check again. Reach for `while` when you don't know in advance how many passes you need. Reach for `for` when you're counting.

Something inside the block has to eventually make the condition false. Forget `remaining -= 2500` and the loop runs forever. If that happens, Ctrl+C in the terminal stops it. Press it twice if the first doesn't take.

**The `do while` loop** checks the condition at the end, so the block always runs at least once:

```c
    int quantity;

    do
    {
        printf("Quantity: ");
        quantity = read_a_number();
    }
    while (quantity <= 0);
```

That shape exists for asking a person something until they answer sensibly. You can't do it with a plain `while` without writing the question twice, once before the loop and once inside it.

Note the semicolon after the closing `while`. It's required, it's easy to forget, and the error you get when you forget it is unhelpful.

**Getting out early with `break`.** Sometimes you can't write the exit test at the top, because you don't know you're finished until you're halfway through a pass. For that, run the loop forever and leave it from the inside:

```c
#include <stdio.h>
#include <stdbool.h>

int main(void)
{
    long lost = 0;    // cents the old till has thrown away
    int day = 0;

    while (true)
    {
        day++;
        lost += 400;             // 400 baskets, one cent each

        if (lost >= 100000)      // $1000
        {
            break;
        }
    }

    printf("The loss passes $1000 on day %d\n", day);
    return 0;
}
```

```
The loss passes $1000 on day 250
```

`while (true)` is a loop whose condition is never false, so it'd run until you killed it. `break` leaves the loop immediately, skipping whatever's left in the block and continuing after the closing brace.

Note the extra header. `true` isn't a keyword in C17, so `<stdbool.h>` has to come along, exactly as it did for `bool` a moment ago. Leave it out and gcc says `'true' undeclared`.

Two honest notes. This particular loop could have been a `for` loop, and 250 is just 100000 divided by 400. The shape earns its place when the finishing condition genuinely can't be written at the top, and the clearest case is reading input until it runs out, which is exactly what your log reader does in Chapter 2.

And a loop with no `break` inside it never ends. If you run one by accident, Ctrl+C stops it.

**Skipping one pass with `continue`.** Where `break` abandons the loop, `continue` abandons only the current pass and jumps to the next:

```c
    int trading_days = 0;

    for (int d = 1; d <= 14; d++)
    {
        if (d % 7 == 0)
        {
            continue;        // every seventh day the shop is shut
        }

        trading_days++;
    }
```

That counts 12, because days 7 and 14 are skipped. Note `%` earning its keep again: `d % 7 == 0` is how you ask "is this a multiple of seven."

Both are easy to overdo. If you find three `break`s in one loop, that loop probably wants to be a function with `return`s in it, which you'll meet shortly.

### A loop inside a loop

Maria wants a quick picture of which hours are busy. One row per hour, one hash per sale.

That needs a loop for the rows and, inside it, another loop for the hashes on that row. It's the classic nested loop, and getting it wrong is a rite of passage, so let's get it wrong first on purpose.

Write `chart.c`:

```c
#include <stdio.h>

int main(void)
{
    for (int hour = 9; hour < 13; hour++)
    {
        int sales = hour * 2;

        printf("%2d:00 ", hour);

        for (int bar = 0; bar < sales; bar++)
        {
            printf("#");
        }
    }

    return 0;
}
```

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o chart chart.c
$ ./chart
 9:00 ##################10:00 ####################11:00 ...
```

Everything on one line, because nothing ever prints a newline. Now try putting one in the obvious place, inside the inner loop, right after the hash:

```c
            printf("#\n");
```

```
 9:00 #
#
#
...
```

Now every single hash is on its own line.

The newline belongs after the inner loop finishes but still inside the outer loop, so it happens once per row:

```c
        for (int bar = 0; bar < sales; bar++)
        {
            printf("#");
        }

        printf("\n");
```

```
$ ./chart
 9:00 ##################
10:00 ####################
11:00 ######################
12:00 ########################
```

Two things to take from that.

When a shape comes out wrong, it's the newline. It's almost always the newline, and it's almost always in the wrong one of those three positions.

And the two counters have different names, `hour` and `bar`, and they have to. Reuse `i` for both and the inner loop resets and tramples the outer loop's count, and the whole thing falls apart in a way that's genuinely hard to see. Give nested loop counters meaningful names and the problem disappears.

The `%2d` prints a whole number in a field at least two characters wide, so `9` and `12` line up down the left edge. Same field width idea as `%02ld`, without the zero-padding flag.

### Putting text into a placeholder

Your receipt lines still have their labels typed into the format string, with the spacing done by hand. That works, and every character is accounted for, but it's fragile: change one label's length and the column moves.

There's a placeholder for text. It's `%s`.

```c
    printf("%s costs $%ld.%02ld\n", "Sourdough loaf", 425 / 100, 425 % 100);
```

```
Sourdough loaf costs $4.25
```

Text in double quotes is a **string literal**, and you can hand one to `printf` as a value just as you've been handing it numbers.

`%s` takes a field width like everything else, and this is what makes columns work properly. `%22s` pads on the left, pushing the text right. `%-22s` pads on the right, keeping the text left and the column edge straight.

The `-` is a flag, exactly like the `0` in `%02ld`. For a receipt you want labels left-aligned and money right-aligned:

```c
    printf("%-22s$%6ld.%02ld\n", "Sourdough loaf", 425 / 100, 425 % 100);
```

```
Sourdough loaf        $     4.25
```

The label takes 22 characters however long it is. The money takes 10: a `$`, six characters for the dollars, a dot, two for the cents. Thirty-two characters total, which is why the separator lines in the finished program are exactly 32 dashes.

> **Trap: `%s` only works one direction, for now.**
>
> You can hand a string literal to `printf`, but you can't yet write your own function that takes text as an input. The reason is that C doesn't really hand the text over at all. It hands over the address of the text, and to write a function that accepts one you have to be able to write down the type of an address.
>
> That type is `char *`, it's the subject of Chapter 2, and the machinery underneath it is Chapter 4. For now, string literals go directly into `printf` calls and nowhere else. When Chapter 2 gives you `char *`, come back to the finished program in this chapter and watch it collapse to a third of its size.

### Writing your own functions

Look at what the finished till is going to need.

Turning a count of cents into `$49.48` happens on every line and three more times at the bottom. Working out the tax happens more than once. Splitting a deal price into equal shares happens for every multi-buy offer.

Copy those calculations around and you'll one day fix the tax rounding in three places and miss the fourth. So write each one once, give it a name, and call it by name. That's a **function**.

You've been calling functions since your first program. `printf` is one. `round` is one. `main` is one. Now you write your own.

Here's the tax calculation as a function:

```c
long tax_on(long amount_cents)
{
    return (amount_cents * TAX_BASIS_POINTS + 5000) / 10000;
}
```

Four parts, and every one is doing a job.

**`long`** at the very front is the type of the value that comes back out. This function hands back a count of cents, so `long`.

**`tax_on`** is the name you'll call it by.

**`(long amount_cents)`** is what goes in. That's a **parameter**. Inside the function, `amount_cents` behaves like an ordinary variable that already has a value in it: whatever the caller passed.

**`return`** hands a value back to whoever called the function, and ends the function immediately. Anything written after a `return` never runs.

Calling it looks like this:

```c
    long tax = tax_on(subtotal);
```

`tax_on(subtotal)` is an expression, exactly like `2 + 2` is an expression. It produces a value, and you can use it anywhere a `long` is allowed: assign it to a variable, hand it to `printf`, or add it to something.

A function can take more than one input, separated by commas:

```c
long line_total(int quantity, long unit_cents)
{
    return quantity * unit_cents;
}
```

Called as `line_total(2, 425)`, which gives 850.

A function that hands nothing back uses `void` as its return type:

```c
void print_money(long cents)
{
    printf("$%6ld.%02ld", cents / 100, cents % 100);
}
```

This one does its work by printing. There's nothing to hand back. You call it as a statement all on its own:

```c
    print_money(total);
```

A function that takes nothing uses `void` in the parentheses, which is why `main` has always been written `int main(void)`. It takes no inputs and hands back an `int`, and that `int` is the exit status you checked with `echo $?` in the Toolbench. All of that was true from your very first program. You just didn't have the words for it yet.

### Prototypes, and why C makes you write them

C reads your file top to bottom, once, and it never looks ahead.

So if `main` calls `tax_on` and `tax_on` is defined further down the file, then at the moment the compiler reads the call it has never heard of anything called `tax_on`. Try it:

```
receipt.c:22:19: error: implicit declaration of function 'tax_on' [-Wimplicit-function-declaration]
```

An error, not a warning. Your program doesn't build.

That strictness is new. Older gcc versions let this through with a warning and guessed at the types, which produced a long tail of horrible bugs where the guess was wrong. gcc 14, which is what Debian 13 ships, finally made it fatal. This is the change the Toolbench warned you about, and it's on your side.

There are two ways to fix it.

Move every function above the first thing that calls it. That works right up until two functions call each other, at which point no ordering exists and you're stuck.

Or declare it near the top and define it wherever you like:

```c
long tax_on(long amount_cents);
```

That single line, ending in a semicolon where the body would have been, is a **prototype**. It tells the compiler the name, what goes in, and what comes out, which is everything needed to check a call. The actual body can be at the bottom of the file.

The convention this book follows, and which most C code follows: prototypes at the top, `main` first, all the other function bodies below it. `main` goes first because it's the summary of what the program does, and that's what a reader wants to see first.

### Scope: where a variable exists

Here's a rule that'll save you a lot of confusion, and you've already half met it.

A variable exists only inside the braces where it was declared.

```c
long tax_on(long amount_cents)
{
    long rounded = amount_cents * TAX_BASIS_POINTS + 5000;
    return rounded / 10000;
}

int main(void)
{
    printf("%ld\n", rounded);      // error: 'rounded' undeclared
    return 0;
}
```

`rounded` lives inside `tax_on` and stops existing the moment `tax_on` returns. `main` can't see it, and neither can anything else. The region where a name is visible is its **scope**.

That isn't an inconvenience to work around. It's the feature that lets you write a function without first checking every variable name used anywhere else in the program.

The same rule applies to blocks inside a function:

```c
    for (int i = 0; i < 3; i++)
    {
        long part = share_of(800, 3, i);
    }

    printf("%ld\n", part);         // error: 'part' undeclared
```

`part` is created fresh on each pass and gone at the closing brace. So is `i`, which was declared in the loop header. If you need a value after the loop finishes, declare it before the loop.

**Which brings back `const`.** Earlier you put `TAX_BASIS_POINTS` inside `main`. But `tax_on` needs it too, and by that rule it can't see it.

The fix is to declare it outside every function, at the top of the file:

```c
#include <stdio.h>

const long TAX_BASIS_POINTS = 825;

int main(void)
{
    ...
```

A name declared outside all functions has **file scope**: it's visible to every function in the file, from its declaration to the bottom. That's the right home for a genuine constant of the program.

It isn't the right home for ordinary variables. A variable at file scope can be changed by any function, from anywhere, which means when its value is wrong you've got the whole file to search. Keep variables in the smallest scope that works. Constants are the exception because nothing can change them.

> **Trap: a `const` in C isn't a compile-time constant.**
>
> This surprises people coming from other languages. `const long TAX_BASIS_POINTS = 825;` creates a read-only variable rather than a value the compiler substitutes wherever the name appears. Which means you can't use it as the size of an array, and you'll want to do that in Chapter 2. The tool for that job is `#define`. For values used in arithmetic, `const` is better, and it's what we use here.

### Arguments are copies

One more rule about functions, and it catches absolutely everybody once.

```c
void try_to_change(long n)
{
    n = 9999;
}

int main(void)
{
    long total = 100;

    try_to_change(total);

    printf("%ld\n", total);        // prints 100, not 9999
    return 0;
}
```

The function didn't receive `total`. It received a copy of the value that was in `total`. Changing the copy does nothing to the original, and the copy gets thrown away when the function returns.

Every argument in C works this way, always, with no exceptions.

That raises an obvious question: how does a function ever change something belonging to its caller? The answer is that you hand it the address of the thing rather than the value, so the function can go and write to that place directly. That's what Chapter 4 is about, and it's why `scanf` is going to look slightly strange at the end of this part.

### Splitting a price that won't divide

One piece left before the finished program: the croissant deal.

Three croissants for $8.00 means 800 cents split three ways. But 800 doesn't divide by three. `800 / 3` is 266 with 2 left over. Print three lines of 266 and they add up to 798, and you've lost two cents in a new and exciting way.

So the leftover has to go somewhere, and the only honest answer is to give it to specific lines and say which. Two croissants cost 267 and one costs 266. Together, exactly 800.

Here's a function that does it:

```c
// One share of total_cents split into `parts` shares, where `which`
// counts from 0. The first few shares get the leftover cents, one
// each, so that all the shares together add up to exactly total_cents.
long share_of(long total_cents, int parts, int which)
{
    long base = total_cents / parts;
    long remainder = total_cents % parts;

    if (which < remainder)
    {
        return base + 1;
    }

    return base;
}
```

Walk it through with real numbers, because reading it isn't the same as following it.

`total_cents` is 800 and `parts` is 3.

```
base      = 800 / 3 = 266
remainder = 800 % 3 = 2
```

So every share gets at least 266, and there are 2 cents spare. Give them to the first 2 shares, which are shares 0 and 1:

| `which` | `which < 2`? | returns |
|---|---|---|
| 0 | yes | 267 |
| 1 | yes | 267 |
| 2 | no | 266 |

267 + 267 + 266 = **800**. Exactly.

Notice how `remainder` is doing double duty. It's both how many cents are spare and how many shares should get an extra one, and those are the same number by definition. That's why the condition is `which < remainder` rather than something more complicated.

Notice too that this function has two `return` statements. That's fine. `return` ends the function on the spot, so if the `if` is true the second one is never reached.

And notice what the old program did instead: it pretended all three croissants cost 2.67 and let the difference fall on the floor. I've seen that exact bug in production systems handling a great deal more than eight dollars. This one puts the leftover somewhere specific and visible. That's what a correct answer to "split this evenly" looks like when the thing doesn't split evenly. Not a lie, but a decision you can point at.

### The whole till

Everything's explained. Here's the tool. Type it out.

```c
// receipt.c
// Prints one receipt for the Sourdough & Co till.
// All money is held as a whole number of cents in a long.

#include <stdio.h>

// Sales tax in basis points. A basis point is one hundredth of a
// percent, so 825 basis points means 8.25 percent.
const long TAX_BASIS_POINTS = 825;

// Prototypes. The bodies are at the bottom of the file.
long line_total(int quantity, long unit_cents);
long tax_on(long amount_cents);
long share_of(long total_cents, int parts, int which);
void print_money(long cents);

int main(void)
{
    long subtotal = 0;

    printf("SOURDOUGH & CO\n");
    printf("--------------------------------\n");

    long loaves = line_total(2, 425);
    printf("%-22s", "2 x Sourdough loaf");
    print_money(loaves);
    printf("\n");
    subtotal += loaves;

    // The 3-for-$8.00 deal does not divide evenly into three prices,
    // so split it into parts that add up to exactly 800 cents.
    for (int i = 0; i < 3; i++)
    {
        long part = share_of(800, 3, i);
        printf("%-22s", "1 x Croissant (3/8)");
        print_money(part);
        printf("\n");
        subtotal += part;
    }

    long coffee = line_total(1, 1299);
    printf("%-22s", "1 x Coffee beans 250g");
    print_money(coffee);
    printf("\n");
    subtotal += coffee;

    long oil = line_total(1, 1999);
    printf("%-22s", "1 x Olive oil 500ml");
    print_money(oil);
    printf("\n");
    subtotal += oil;

    long tax = tax_on(subtotal);
    long total = subtotal + tax;

    printf("--------------------------------\n");

    printf("%-22s", "Subtotal");
    print_money(subtotal);
    printf("\n");

    printf("%-22s", "Tax 8.25%");
    print_money(tax);
    printf("\n");

    printf("%-22s", "TOTAL");
    print_money(total);
    printf("\n");

    return 0;
}

// The cost of `quantity` items at `unit_cents` each.
long line_total(int quantity, long unit_cents)
{
    return quantity * unit_cents;
}

// Sales tax on an amount, rounded to the nearest cent.
long tax_on(long amount_cents)
{
    return (amount_cents * TAX_BASIS_POINTS + 5000) / 10000;
}

// One share of total_cents split into `parts` shares, where `which`
// counts from 0. The first few shares get the leftover cents, one
// each, so that all the shares together add up to exactly total_cents.
long share_of(long total_cents, int parts, int which)
{
    long base = total_cents / parts;
    long remainder = total_cents % parts;

    if (which < remainder)
    {
        return base + 1;
    }

    return base;
}

// Prints an amount as dollars and cents. Does not print a newline,
// so the caller decides what comes next on the line.
void print_money(long cents)
{
    if (cents < 0)
    {
        printf("-$%6ld.%02ld", -cents / 100, -cents % 100);
    }
    else
    {
        printf("$%6ld.%02ld", cents / 100, cents % 100);
    }
}
```

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -Wfloat-equal -g -o receipt receipt.c
$ ./receipt
SOURDOUGH & CO
--------------------------------
2 x Sourdough loaf    $     8.50
1 x Croissant (3/8)   $     2.67
1 x Croissant (3/8)   $     2.67
1 x Croissant (3/8)   $     2.66
1 x Coffee beans 250g $    12.99
1 x Olive oil 500ml   $    19.99
--------------------------------
Subtotal              $    49.48
Tax 8.25%             $     4.08
TOTAL                 $    53.56
```

Add up the lines.

```
8.50 + 2.67 + 2.67 + 2.66 + 12.99 + 19.99 = 49.48
```

They add up. Maria's books and Maria's drawer will agree tonight, and every night after.

> **Under the hood: why `print_money` treats negatives separately.**
>
> Remember that `%` truncates towards zero with negatives. So for a seven cent refund, `-7 / 100` is 0 and `-7 % 100` is `-7`, and the simple version of that function would print `$0.-7`.
>
> Negating first and putting the minus sign into the format string by hand is the fix. This is exactly the kind of thing that only surfaces on the day somebody processes their first return, which is usually the day after launch.

Notice the repetition. Three lines per item, six times over, differing only in the label and the numbers. It itches, and it should.

You can't factor it out yet, because the function that would fix it needs to take the label as a parameter, and text as a parameter needs `char *`. Hold the itch. When Chapter 2 hands you `char *`, come back and collapse this to one line per item. It'll feel like a reward, because it is one.

### Under the hood: watch the money move

You've got a correct program. Use it to practise the debugger, because practising on an easy case is the only way the tool is available to you on a hard one.

The line `subtotal += part;` inside the croissant loop is line 38 of `receipt.c`. Stop there and watch the cents accumulate.

Check that number against your own file rather than trusting mine. You turned on line numbers in `nano` back in the Toolbench for exactly this kind of moment, and if you've typed an extra blank line anywhere above, yours will differ by one. Everything below still works, you just break on your number instead of mine.

```
$ gdb ./receipt
GNU gdb (Debian 16.3-1) 16.3
Reading symbols from ./receipt...
(gdb) break 38
Breakpoint 1 at 0x1229: file receipt.c, line 38.
(gdb) run
Starting program: /home/you/toc/ch01/receipt 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
SOURDOUGH & CO
--------------------------------
2 x Sourdough loaf    $     8.50
1 x Croissant (3/8)   $     2.67

Breakpoint 1, main () at receipt.c:38
38	        subtotal += part;
```

Three things before you type anything else.

Those two `libthread_db` lines are noise. Every `gdb run` on Debian prints them. They mean gdb has loaded the library that lets it inspect threads, which your program doesn't use. Ignore them, here and forever.

Your program's own output appeared. The program and the debugger share one terminal, so the receipt lines come out as they happen, mixed in with the debugger's messages. That's normal and it confuses everyone the first time.

And the breakpoint stopped before line 38 ran. Line 38 is displayed as the next thing that'll happen rather than the thing that just happened. So `subtotal` still holds only the loaves:

```
(gdb) print subtotal
$1 = 850
(gdb) print part
$2 = 267
(gdb) print i
$3 = 0
```

850 cents of bread, a 267 cent share, and this is share number zero. Exactly what the table in the `share_of` section predicted. Now run one line and look again:

```
(gdb) next
32	    for (int i = 0; i < 3; i++)
(gdb) print subtotal
$4 = 1117
```

850 plus 267. Let it run round the loop and stop again:

```
(gdb) continue
Continuing.
1 x Croissant (3/8)   $     2.67

Breakpoint 1, main () at receipt.c:38
38	        subtotal += part;
(gdb) print i
$5 = 1
(gdb) print part
$6 = 267
(gdb) continue
Continuing.
1 x Croissant (3/8)   $     2.66

Breakpoint 1, main () at receipt.c:38
38	        subtotal += part;
(gdb) info locals
part = 266
i = 2
subtotal = 1384
loaves = 850
coffee = 0
oil = 0
tax = 0
total = 0
```

There's `share_of` doing its job, live. Shares 0 and 1 got the spare cent, share 2 didn't, and the three together are exactly 800. You didn't work that out by reading. You watched it happen.

Look at the bottom four lines of that `info locals` too, because they're a free lesson. `coffee`, `oil`, `tax` and `total` are declared further down `main` and the program hasn't reached them yet. They already exist, they already have memory set aside, and they hold nothing you put there. Today that nothing prints as 0. It won't always. This is the uninitialised variable from Part 1 of the Toolbench, caught in the act.

```
(gdb) continue
Continuing.
1 x Coffee beans 250g $    12.99
1 x Olive oil 500ml   $    19.99
--------------------------------
Subtotal              $    49.48
Tax 8.25%             $     4.08
TOTAL                 $    53.56
[Inferior 1 (process 8891) exited normally]
(gdb) quit
```

Your addresses and process numbers will be different. Everything that matters won't.

Try a conditional breakpoint too, because it's the move that makes `gdb` decisively better than scattering print statements:

```
(gdb) break 38 if part == 266
```

That runs the first two passes at full speed and stops only on the odd one out. On a loop of three it saves you nothing. On the loop in Chapter 5 that runs 140,000 times, it's the difference between finding a bug and giving up.

### Closing the loop on Maria

One last program and the chapter's story is finished. Write `day.c`:

```c
#include <stdio.h>

int main(void)
{
    long correct_cents = 0;
    double naive_dollars = 0.0;

    for (int basket = 0; basket < 400; basket++)
    {
        correct_cents += 5357;      // what the books say each basket is worth
        naive_dollars += 53.56;     // what the old till actually charged
    }

    printf("Books say:      $%ld.%02ld\n", correct_cents / 100, correct_cents % 100);
    printf("Till took:      $%.2f\n", naive_dollars);
    printf("Till took, raw: $%.10f\n", naive_dollars);
    printf("Short by:       $%.2f\n", correct_cents / 100.0 - naive_dollars);

    return 0;
}
```

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -Wfloat-equal -g -o day day.c
$ ./day
Books say:      $21428.00
Till took:      $21424.00
Till took, raw: $21424.0000000001
Short by:       $4.00
```

Four dollars. Every day. There's Maria's missing money as a number instead of a suspicion.

Now look carefully, because there are two different bugs sitting side by side in that output and this is the clearest view of the difference you'll get.

**The four dollars is the rounding policy bug.** One cent per basket, four hundred baskets. It has nothing whatsoever to do with binary fractions. A till using whole-number cents that rounded each line down and totalled the unrounded values would lose exactly the same four dollars. This is the bug that cost Maria a month of evenings, and the fix wasn't a type. It was deciding where rounding happens and doing it once, on purpose.

**The `0.0000000001` is the floating point precision bug.** Four hundred additions of a value the machine can't hold exactly, and the error has crawled up into the tenth decimal place. Today it's invisible. Across forty shops summing a year of transactions it isn't, and no amount of care removes it, because the wrongness is in the storage rather than in the arithmetic.

The whole-number version has neither. `correct_cents` is a count, and counts don't drift.

### Reading a number from a person

Everything so far has its prices typed into the source. To take a quantity from whoever's standing at the till, the program needs input.

The plain way to read a number in C is `scanf`:

```c
#include <stdio.h>

int main(void)
{
    int quantity;

    printf("Quantity: ");

    if (scanf("%d", &quantity) != 1)
    {
        printf("That is not a number.\n");
        return 1;
    }

    printf("Selling %d.\n", quantity);
    return 0;
}
```

`scanf` is `printf` in reverse. It takes a format string describing what to look for, and somewhere to put what it finds. Two things in there need explaining properly rather than waving past.

**The `&`.** You learned a page ago that every argument in C is a copy. So `scanf` can't be handed `quantity`, because it'd get a copy, and filling in a copy achieves nothing at all.

It has to be told where `quantity` lives, so it can go to that place and write into it. `&` means "the address of." `&quantity` is the address of the variable, and with that in hand `scanf` can reach the real thing.

Chapter 4 explains what an address actually is, and from that point you'll use them every day. For now: `scanf` needs `&` in front of the variable, and forgetting it is a crash rather than a warning. I'd rather not be teaching you this function at all, and Chapter 2 replaces it, but you need input from somewhere before then.

**Checking the return value.** `scanf` hands back how many values it successfully read. Ask for one and get 1 back, and it worked. Get 0 and the person typed something that isn't a number at all.

Most tutorials throw that return value away. Their programs then carry on with an uninitialised variable holding whatever rubbish was in that memory, and print a total based on it.

Here's the habit to build, starting today. When a function can fail, check whether it did, and stop if it did. Printing a clear message and returning a non-zero exit status is a complete, professional response. It's also exactly the behaviour Chapter 6 builds `logtool` around.

> **Trap: don't loop on `scanf` to retry.**
>
> The obvious next thought is to wrap it in a `do while` and keep asking until they type a number. Don't, not yet.
>
> When `scanf` fails to convert something, it leaves the offending text sitting in the input buffer. So the next call reads the same text, fails the same way, and your loop spins forever at full speed. You have to clear the buffer first, and doing that properly needs tools from Chapter 2.
>
> Until then: read once, check, exit on failure. Chapter 2 replaces `scanf` with `fgets` and `strtol`, which is what production C actually uses and which doesn't have this problem.

**Reading a single character** is simpler, and you want it for a yes-or-no prompt:

```c
    printf("Print receipt? (y/n) ");

    int answer = getchar();

    if (answer == 'y' || answer == 'Y')
    {
        printf("Printing.\n");
    }
```

`getchar` reads one character and hands it back as an `int` rather than a `char`, so it has room to also return a special value called `EOF` when the input runs out. Store it in an `int`.

The single quotes matter enormously. `'y'` is one character. `"y"` is a piece of text. They're different types, they aren't interchangeable, and this is the first place that difference will bite you.

> **Under the hood: `'y'` really is a number.**
>
> How the Machine Thinks told you the letter A is stored as 65. Prove it:
>
> ```c
> printf("%d %d %d\n", 'A', 'a', 'y');
> ```
> ```
> 65 97 121
> ```
>
> `'A'` and `65` are the same value. The only thing that decides which one you see is the placeholder you print it with. `%c` shows the character, `%d` shows the number:
>
> ```c
> char grade = 'A';
>
> printf("%c is stored as the number %d\n", grade, grade);
> printf("Add 32 and you get %c\n", grade + 32);
> ```
> ```
> A is stored as the number 65
> Add 32 and you get a
> ```
>
> The same variable, printed twice, two completely different-looking results. Nothing about the byte changed between those two lines.
>
> And the arithmetic is real. `'a' - 'A'` is 32, which is exactly the gap between the cases, so adding 32 to an uppercase letter gives you its lowercase twin and subtracting 32 goes back the other way.
>
> Chapter 2 builds a working cipher on that fact. For now, register that a `char` is a small whole number wearing a costume, that `%c` puts the costume on, and that `%d` takes it off.

---

## Part 4: Break it on purpose

Four programs. Each has exactly one bug, and each bug is best caught by a different tool. I'll tell you the symptom and nothing else.

The ground rule: use the tools, not your eyes. For most of these you could find the bug by staring hard enough. That isn't the point. The point is to walk the route while the route is easy, so it's available to you when the bug is one you could never have found by staring.

Before you start, save a known-good copy of the correct output so you've got something to compare against:

```
$ mkdir -p tests
$ ./receipt > tests/receipt-expected.txt
```

Look at that file and check it by hand before you trust it. An expected-output file generated from a buggy program locks the bug in permanently and is worse than having no test at all.

### Bug 1

`bug1.c`. Symptom: it reports small daily takings correctly and reports large ones as nonsense.

```c
#include <stdio.h>

int main(void)
{
    long takings = 4948;
    printf("Small day: %d cents\n", takings);

    takings = 9000000000L;
    printf("Big day:   %d cents\n", takings);

    return 0;
}
```

(The `L` on the end of `9000000000L` marks the literal as a `long`. Without it the compiler would try to read a number too big for an `int`.)

Find it before reading on.

<details>
<summary>Walkthrough</summary>

Compile with the house flags. That's always step one, before running anything.

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o bug1 bug1.c
bug1.c:6:24: warning: format '%d' expects argument of type 'int', but argument 2 has type 'long int' [-Wformat=]
    6 |     printf("Small day: %d cents\n", takings);
      |                        ~^           ~~~~~~~
      |                         |           |
      |                         int         long int
      |                        %ld
```

Found before the program ever ran, with the fix printed at the bottom of the warning.

Here's why it matters. `%d` tells `printf` to read four bytes and treat them as an `int`. A `long` is eight. So `printf` reads half the number and prints that.

Which means the bug is invisible for small values, because the half it reads happens to contain the whole answer:

```
$ gcc -std=c17 -w -o bug1-quiet bug1.c
$ ./bug1-quiet
Small day: 4948 cents
Big day:   410065408 cents
```

> **Debian note: `-w` isn't a typo for `-Wall`.**
>
> Lowercase `-w` means the opposite: silence every warning. It's used here only to show you what the world looks like when the compiler is ignored, and it isn't a flag you should ever use on real work.
>
> It's needed because Debian patches gcc to switch printf format checking on by default, so gcc on your machine catches this particular bug even without `-Wall`. That's Debian being helpful. Most warnings are still off by default, which is why `-Wall` earns its place, but this one you get for free.

This is the worst kind of bug there is. It works perfectly in testing, where your numbers are small, and fails in production, where they aren't. `-Wall` costs nothing and caught it in the first second.

Fix: `%ld` in both places.

</details>

### Bug 2

`bug2.c`. Symptom: it should report the tax as roughly 8% of the bill. It reports 0%.

```c
#include <stdio.h>

int main(void)
{
    int tax = 408;
    int total = 5356;

    int percent = (tax / total) * 100;

    printf("Tax is %d%% of the bill\n", percent);
    return 0;
}
```

<details>
<summary>Walkthrough</summary>

Clean under every warning we have. Clean under the sanitizers too, because nothing about memory or overflow is wrong here. The program does exactly what it says.

That combination means it's a logic bug, and logic bugs are a `gdb` job. This is the one I'd most like you to work through properly rather than reading the answer.

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o bug2 bug2.c
$ gdb ./bug2
(gdb) break 8
Breakpoint 1 at 0x1151: file bug2.c, line 8.
(gdb) run

Breakpoint 1, main () at bug2.c:8
8	    int percent = (tax / total) * 100;
(gdb) print tax
$1 = 408
(gdb) print total
$2 = 5356
```

Both inputs are correct, so the bug is in the calculation. Now use something you may not have realised `gdb` can do: it'll evaluate any C expression you type, using the real variables, with their real types.

```
(gdb) print tax / total
$3 = 0
```

There it is. `408 / 5356` in whole numbers is 0, because whole-number division truncates and the true answer is 0.076. Multiply zero by a hundred and you still have zero.

The fix is to do the multiplication before the division, so the interesting digits are still there when the truncation happens:

```c
    int percent = (tax * 100) / total;
```

That gives 7, because 40800 / 5356 is 7.6 truncated. If you want it rounded, use the pattern from Part 3 and add half the divisor first:

```c
    int percent = (tax * 100 + total / 2) / total;
```

That gives 8.

The lesson is bigger than this one line. In whole-number arithmetic, the order of operations changes the answer. Multiplying first and dividing last isn't a style preference, it's how you keep precision that truncation would otherwise destroy.

</details>

### Bug 3

`bug3.c`. Symptom: it's `receipt.c` with one line changed. Every total is one cent low.

```c
    for (int i = 1; i <= 3; i++)
    {
        long part = share_of(800, 3, i);
```

<details>
<summary>Walkthrough</summary>

Compiles clean. Runs clean. Sanitizes clean. And on screen it looks entirely normal: three croissant lines, a subtotal, a total. Nothing about it announces itself.

This is precisely what the judge is for.

```
$ gcc -std=c17 -Wall -Wextra -Wpedantic -g -o bug3 bug3.c
$ ./bug3 > mine.txt
$ diff mine.txt tests/receipt-expected.txt
5c5
< 1 x Croissant (3/8)   $     2.66
---
> 1 x Croissant (3/8)   $     2.67
10c10
< Subtotal              $    49.47
---
> Subtotal              $    49.48
12c12
< TOTAL                 $    53.55
---
> TOTAL                 $    53.56
```

Now work out why, using the table you built in the `share_of` section.

The loop passes `which` values of 1, 2 and 3 instead of 0, 1 and 2. `share_of` gives the spare cent to shares numbered below the remainder, which is 2. So shares 0 and 1 qualify. Ask for shares 1, 2 and 3 and only one of them does:

| `which` | `which < 2`? | returns |
|---|---|---|
| 1 | yes | 267 |
| 2 | no | 266 |
| 3 | no | 266 |

267 + 266 + 266 = **799**. One cent short, on every basket.

This is the same class of bug that shipped in Maria's original till, wearing different clothes. Invisible on any single receipt. Four dollars a day.

Fix: `for (int i = 0; i < 3; i++)`. Start at zero, use `<`. The Trap in Part 3 said this would matter, and here's the first time it does.

</details>

### Bug 4

`bug4.c`. Symptom: it adds up a year of daily takings and reports that the shop owes money.

```c
#include <stdio.h>

int main(void)
{
    int year_cents = 0;

    for (int day = 0; day < 313; day++)
    {
        year_cents += 8000000;      // $80,000 a day
    }

    printf("Year takings: %d cents\n", year_cents);
    return 0;
}
```

<details>
<summary>Walkthrough</summary>

Clean compile, and a confident answer:

```
$ ./bug4
Year takings: -1790967296 cents
```

Negative, which at least has the decency to be obviously wrong. Since it's a number that's gone strange rather than a crash, reach for the sanitizer:

```
$ gcc -std=c17 -Wall -Wextra -g -fsanitize=undefined -o bug4-ub bug4.c
$ ./bug4-ub
bug4.c:9:20: runtime error: signed integer overflow: 2144000000 + 8000000 cannot be represented in type 'int'
```

Line, the two numbers, and the type that couldn't hold the result.

Check the arithmetic yourself. 313 days at 8,000,000 cents is 2,504,000,000. `INT_MAX` is 2,147,483,647, which you printed back in Part 2. It ran out of room on day 269 and everything after that was nonsense.

Fix: `long year_cents` and `%ld`.

This is exactly why the receipt program uses `long` for money rather than `int`, and it's why "the numbers in my test are small" is never a reason to choose the smaller type.

</details>

---

## Part 5: Ship it

Two things, both boring, both what separates a program from a script somebody found.

### A Makefile, so you stop retyping

You've typed the house command dozens of times today. Stop.

There's a worse problem than the typing, and it's drift: one day you're in a hurry, you leave off `-Wall`, and you lose the exact thing that would have saved you.

`make` reads a file called `Makefile` that records how to build things and then does it. You met it in the Toolbench. Create `Makefile` in `~/toc/ch01`:

```make
CC = gcc
CFLAGS = -std=c17 -Wall -Wextra -Wpedantic -Wfloat-equal -g
SANFLAGS = -fsanitize=address,undefined

all: receipt

receipt: receipt.c
	$(CC) $(CFLAGS) -o receipt receipt.c

receipt-debug: receipt.c
	$(CC) $(CFLAGS) $(SANFLAGS) -o receipt-debug receipt.c

test: receipt
	./receipt > /tmp/receipt-out.txt
	diff /tmp/receipt-out.txt tests/receipt-expected.txt && echo "PASS"

clean:
	rm -f receipt receipt-debug till probe sizes chart two day a.out
```

> **Trap: those indented lines must start with a real tab character.**
>
> Not four spaces. If you get `Makefile:8: *** missing separator.  Stop.`, that's exactly what happened.
>
> The `set tabstospaces` line in your `~/.nanorc` turns every Tab into spaces, which is right everywhere except here. Put a `#` in front of it while you write this file, then check your work with `cat -A Makefile`: a real tab shows as `^I`. The Toolbench has the full version of this warning, and it'll still get you once.

Two things changed from the Toolbench version.

`-Wfloat-equal` is now in `CFLAGS`, because this is a program about money and comparing money with `==` should be impossible to do by accident.

And there's a `test` target. Run it:

```
$ make test
gcc -std=c17 -Wall -Wextra -Wpedantic -Wfloat-equal -g -o receipt receipt.c
./receipt > /tmp/receipt-out.txt
diff /tmp/receipt-out.txt tests/receipt-expected.txt && echo "PASS"
PASS
```

You've just automated the judge. From now on, "is it still working" is one command, and it'll stay one command through Chapter 6.

The `&&` in that line is the shell's version of "and", and it works the same way as C's: run the second command only if the first succeeded. `diff` exits with 0 when the files match, so `PASS` only prints when they do.

### Correctness, design and style are three different things

People argue about code endlessly because they mix these up. Separate them and most arguments evaporate.

**Correctness** is whether it does the right thing. `diff` answers this and nothing else does. Not your eyes, not the fact that it compiled.

**Design** is whether it does the right thing sensibly. Are the functions the right size? Is the tax rate named once or spelled out four times? Are you asking questions whose answers you already have? This is the part that takes years, and it's the part actually worth thinking about.

**Style** is purely how it looks. Indentation, where the braces go, spaces around operators. Zero effect on the machine and a large effect on the human reading it at midnight.

I've watched teams lose whole afternoons to brace placement. Style isn't worth arguing about, which is exactly why you should hand it to a tool and stop thinking about it:

```
$ sudo apt install clang-format
$ clang-format --style=file -i receipt.c
```

`-i` edits the file in place. `--style=file` tells it to read the settings from the `.clang-format` file at the top of this repository, which encodes the style every listing in this book uses.

Run it, then run `git diff`. Nothing should change, because every file in this repository is already in that style and a script checks it.

That's the standard to hold yourself to. A style guide nobody can verify is a preference. One a machine can check is a decision you only have to make once. Where the tool ever does disagree with you, choose once: change the code, or change `.clang-format`. What isn't worth doing is having the argument again next week.

### Commit

```
$ cd ~/toc/ch01
$ git init
$ nano .gitignore
```

Compiled programs don't belong in version control. They're large, they change on every build, and anyone with the source can regenerate them in a second.

```
receipt
receipt-debug
till
probe
sizes
chart
two
day
bug1
bug2
bug3
bug4
a.out
*.o
mine.txt
```

```
$ git add .
$ git commit -m "Chapter 1: till correct to the cent using whole-number cents"
```

---

## Where people go wrong

The mental models that trip nearly everybody at this stage, with the correct version next to each one.

**"`double` is fine for money as long as I round at the end."** Rounding a wrong number gives you a wrong number, and you watched `printf` and `round` disagree about the same value by a whole cent. Money is a count of the smallest unit that exists. Store it as a whole number of those units.

**"`float` is for decimals and `double` is for big decimals."** Both are floating point and both are inexact. A `float` gives you about six significant digits, which isn't enough for anything real. If you've decided floating point is right for the job, use `double`.

**"`0.1 + 0.2 == 0.3` is true."** It isn't, on any machine you'll ever use. Never compare floating point values for exact equality. Compare the difference against a small tolerance, or better, arrange not to be in floating point at all.

**"`5 / 2` is 2.5."** In C it's 2. Whole number divided by whole number gives a truncated whole number. For a fractional answer, cast one side first: `(double) 5 / 2`. For a rounded whole answer, add half the divisor before dividing.

**"`(tax / total) * 100` gives me a percentage."** In whole numbers it gives zero. Multiply before you divide.

**"An `int` is big enough for anything I'll realistically do."** 2,147,483,647 isn't a large number when you're counting cents, milliseconds, or bytes. Prefer `long` whenever the value counts something that could grow.

**"`=` and `==` are basically the same."** `=` stores a value. `==` asks a question. `if (total = 0)` wipes your variable and silently skips the block. `-Wall` catches it, nothing else does.

**"The error says line 12, so the bug is on line 12."** Often it's line 11. C ends statements with semicolons, so a missing one means the compiler reads happily on to the next line before deciding something's wrong. Unbalanced braces are worse and usually get reported at the very end of the file. When line 12 looks fine, look up.

**"`%d` and `%i` are different."** In `printf` they're identical. In `scanf` they aren't: `%i` treats a leading `0x` as hexadecimal and a leading `0` as octal, so a form using it would read `010` as 8. Use `%d` for both and you'll never have to think about this again.

**"A variable declared in a loop is available after the loop."** It isn't. It stops existing at the closing brace. Declare it before the loop if you need it afterwards.

**"Passing a variable to a function lets the function change it."** It doesn't. The function gets a copy. That's why `scanf` needs `&`, and Chapter 4 explains the rest.

**"Warnings are things to clean up later."** By later there are sixty of them and the two that mattered are buried in the middle. Every bug in Part 4 that `-Wall` caught was caught in under a second, for free.

---

## Exercises

### Drill (about 15 minutes each)

**1. Predict, then check.** Before running anything, write down what you think each of these prints. Then put them all in one program and find out.

```c
printf("%d\n", 7 / 2);
printf("%d\n", -7 / 2);
printf("%d\n", 7 % 2);
printf("%d\n", -7 % 2);
printf("%f\n", 7 / 2.0);
printf("%d\n", (int) 7.9);
printf("%.2f\n", 0.125);
printf("%.2f\n", 0.135);
```

The ones you got wrong are the useful ones. Write down why, in a sentence each.

**2. Find the exact ones.** Using `%.20f`, work out which of 0.1, 0.25, 0.3, 0.5, 0.6, 0.75 and 0.9 your machine can store exactly. Then state, in one sentence, the rule that explains the pattern.

**3. Letters are numbers.** Write a loop that prints each letter from `A` to `E` with its numeric value, using a single `char` variable and arithmetic. Then extend it to also print the lowercase twin of each, without typing the alphabet out.

**4. Break `print_money`.** Call it with `-7`, `0`, `5`, `100` and `-100`. Any output that isn't a sensible amount of money is a bug. Fix whatever you find.

### Build (about an hour each)

**5. Change (CS50 parity: Cash).** Write `change.c` that takes an amount owed in cents and prints the smallest number of coins that makes it, using 25, 10, 5 and 1 cent pieces. No floating point anywhere in the program. Read the amount with `scanf`, check the return value, and reject anything negative. For 41 cents the answer is `4`. Verify it with `diff`.

The approach: take as many of the largest coin as will fit, then move down to the next. `/` tells you how many fit and `%` tells you what's left, which is the same pair of operators doing the same job as in `share_of`.

The greedy approach happens to work for these four coin values and doesn't work for every possible set. I'd encourage you to go and find a set where it fails, because working out why is more interesting than the exercise itself.

**6. The pyramid (CS50 parity: Mario).** Write `pyramid.c` that reads a height from 1 to 8 and prints a right-aligned pyramid of hashes. For height 4:

```
   #
  ##
 ###
####
```

Then extend it to the two-sided version with a two-space gap in the middle:

```
   #  #
  ##  ##
 ###  ###
####  ####
```

Each row needs a loop for the spaces and a loop for the hashes, both inside the row loop. Work out the relationship between the row number and the number of spaces before you write any code. Get the first version passing `diff` before you touch the second.

**7. Card check (CS50 parity: Credit).** Write `luhn.c` that reads a card number and reports whether it passes Luhn's checksum, which is the arithmetic test every card number in the world satisfies.

The algorithm: starting from the second-to-last digit and moving left, double every other digit. If doubling gives a two-digit result, add those two digits together instead of using the number. Sum all of those results. Add the sum of the digits you didn't double. The number is valid if the total ends in zero.

You've got no arrays yet, so pull the digits off one at a time from the right using `% 10` to get the last digit and `/ 10` to remove it. That constraint makes this a better exercise than the array version, because it forces you to understand what those two operators do together. Use a `long` for the card number; a 16-digit number doesn't fit in an `int`.

### Stretch (no solution provided)

**8. The day report.** Write `day2.c` that simulates 400 baskets and reports the day's takings twice: once using `long` cents throughout, once using `double` dollars. Print both to ten decimal places and print the difference. Prove to yourself that the gap isn't zero. Then, using the digit counts from `sizes.c`, estimate roughly how many transactions it'd take for that gap to reach a whole cent.

**9. Rounding policies.** Real tax authorities disagree about whether sales tax is computed per line or on the basket total. Extend `receipt.c` so either policy can be chosen by changing one `const`, and write an expected-output file for each. Then answer, with evidence from `diff`: does the choice ever change what the customer pays? By how much? Is there a basket where it changes by more than one cent?

**10. Sabotage your own tests.** Take the finished `receipt.c` and introduce a bug that loses exactly one cent per hundred baskets and can't be seen on any single receipt. Then write the test that catches it.

If your test suite can't catch your own deliberate sabotage, it wouldn't have caught Maria's nephew either.

---

> **Parity: CS50x Week 1.**
>
> This chapter covers the same ground as Week 1: types, variables, operators, conditionals, boolean expressions, all three kinds of loop, nested loops, user-defined functions, prototypes, scope, return values, integer overflow, truncation, floating point imprecision, casting, comments, constants, and the correctness/design/style distinction. The three problem sets are here as exercises 5, 6 and 7.
>
> **What's different.**
>
> The course provides its own library for input, so `get_int` does the job that `scanf` and `&` do here. That library makes the first week easier, and it's also a wall later, because `get_int` doesn't exist anywhere outside the course. You've met the real thing instead, including the return value check that the course version hides from you.
>
> **Two deferrals worth naming.** Week 1 also has `get_string`, and this chapter reads no text from the person at all. Real string input needs `fgets` and a `char` array, which is Chapter 2. Nothing in Mario, Cash or Credit needs it, so you lose no problem-set parity by waiting.
>
> And CS50's Cash reads dollars with `get_float`. Exercise 5 here reads cents with `scanf` instead, because a chapter that spends 4,000 words proving money must not live in a `double` can't then ask you to type one in. Same problem, same answer, better input.
>
> The course introduces overflow and floating point imprecision at the end of the lecture as a set of interesting cautionary tales. Here they're the plot, because over a career you'll meet them far more often as a live bug than as a curiosity, and knowing the story of the Boeing 787 doesn't help you at 11pm when your own total has gone negative.
>
> **Two things this chapter adds that Week 1 doesn't have.** The distinction between a rounding *policy* bug and a floating point *precision* bug, which are different problems with different fixes and get conflated constantly, including by experienced programmers. And the practice of deciding where a leftover cent goes rather than letting it fall on the floor, which is the difference between a program that computes money and a program a business can actually use.

---

## What you have

A working till that's correct to the cent. A Makefile that builds and tests it in one command. And a set of habits: warnings on always, sanitizers when something smells wrong, `gdb` when the logic is wrong, `diff` when you think you're finished.

You've also got an itch. Six items on that receipt, three near-identical lines of code each, and no way to write the one function that would collapse them all, because you can't yet hand a piece of text to a function of your own.

**Next:** Chapter 2. Your team needs to send a 40,000 line server log to an outside vendor, and it's full of customer email addresses. They have to come out first.

You'll get arrays, strings, the null terminator, command line arguments, and the four stages of compilation taken apart by hand. And you'll get `char *`, which is the thing you needed twenty minutes ago.

**Go to:** [`ch02-scrubbing-the-log/`](../ch02-scrubbing-the-log/README.md)
