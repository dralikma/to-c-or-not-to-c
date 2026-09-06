# How the Machine Thinks

*Between the Toolbench and Chapter 1. About twenty minutes. No code, no exercises, nothing to install. Just read it.*

---

CS50 spends its first week on Scratch, dragging coloured blocks around to teach loops and conditionals without syntax getting in the way. It is a good idea for a lecture hall. For a book you are reading alone, it is a detour.

So this is the replacement. It is short, and it is the only part of the book with nothing to type. It exists so that nothing in Chapter 1 arrives without context, and so that when floating point arithmetic loses a shop three pennies a day, you already know why before I tell you.

Read it once now. Come back to it after Chapter 4 and it will read differently.

---

## The machine only knows numbers

Your processor is a very fast, very literal clerk. It cannot read. It has no concept of a letter, a word, a colour, or a price. It handles numbers, and only numbers, and those numbers are stored as patterns of high and low voltage in transistors.

A single one of those on-or-off slots is a **bit**. One bit can hold two values, 0 or 1. Two bits give you four combinations: 00, 01, 10, 11. Three bits give you eight. Every bit you add doubles the possibilities.

Eight bits give you 256 combinations, and eight bits grouped together is called a **byte**. The byte is the smallest unit most machines bother to address individually, which is why it turns up everywhere. When Chapter 1 tells you an `int` occupies four bytes, that means 32 bits, which means it can hold a little over four billion distinct values. Not infinite. Four billion and change, and then it runs out.

That is the entire foundation. Everything above it is agreement.

---

## Everything else is an agreement about what numbers mean

If the machine only stores numbers, how does it store the letter `A`?

It does not. It stores the number 65, and everybody agrees that when we are treating that byte as text, 65 means `A`. That agreement is called **ASCII**, and it was written down in the 1960s. `B` is 66, `C` is 67, and so on up the alphabet. Lowercase `a` is 97, which is exactly 32 more than uppercase `A`. A space is 32. The digit character `0` is 48.

This is not a metaphor or a simplification. In C it is literally true, and you will prove it in one line in Chapter 1. The character `'A'` and the number 65 are the same value wearing different clothes. C will let you do arithmetic on letters because to C they were never letters in the first place.

That fact does real work. Converting a letter from lowercase to uppercase is subtraction. Checking whether a character is a digit is a range check. In Chapter 2 you will write a cipher that shifts letters through the alphabet, and the whole thing rests on the alphabet being a run of consecutive numbers.

The same trick runs the entire machine. A colour is three numbers, for how much red, green, and blue. An image is a grid of those. A sound is a long list of numbers describing air pressure tens of thousands of times a second. A file on disk is a run of bytes, and what those bytes *mean* depends entirely on which agreement you apply when you read them.

Nothing in the file says "I am a photograph." The agreement lives outside the data. That is why renaming a file from `.jpg` to `.txt` does not change the file at all, and why opening a photograph in a text editor shows you garbage. Same bytes, wrong agreement.

In Chapter 4 you will take a file that looks like a photograph, read its raw bytes yourself, and recover deleted images from a corrupted memory card by recognising the specific byte pattern that means "a JPEG starts here." At that point this paragraph will stop being an abstraction.

---

## Numbers with decimal points are where the trouble starts

Whole numbers are easy. Two bytes hold any whole number from 0 to 65,535, exactly, with no argument and no rounding.

Fractions are not easy, and the reason is worth sitting with for a minute because it is the plot of Chapter 1.

Try writing one third in decimal. You get 0.3333333, and you have to stop somewhere, and wherever you stop you are slightly wrong. There is no length of decimal that gets you there. This is not a flaw in your arithmetic. It is that one third cannot be expressed exactly in a system built on tens.

Binary has the same problem with a different set of numbers, because it is built on twos rather than tens. And one of the numbers it cannot express exactly is **0.1**.

Your machine has a fixed number of bits, so it stores something extremely close to 0.1 and moves on. The error is tiny, around one part in ten thousand trillion. Invisible. Irrelevant.

Until you add it up.

Do arithmetic on thousands of those very-close numbers and the tiny errors accumulate. Multiply, and they compound rather than merely adding. Round the result to two decimal places for display and the display looks perfect while the stored value has drifted. Then run that for a day across four hundred transactions and the till is short by an amount somebody will eventually notice.

This is not a hypothetical. It is the reason banks, payroll systems, and point-of-sale terminals do not store money in the way most beginners' first instinct suggests. And it is why Chapter 1 opens with a shop that is a few pennies short most days and nobody can find where the money went.

The fix is not "use more decimal places." More decimal places postpones the problem and makes it harder to see. The fix is to stop storing fractions at all, and you will build it.

---

## Why we do not write the numbers ourselves

The processor's actual language is a short list of numeric instructions. Copy this value into that register. Add these two registers together. Jump to this address if the last result was zero. Real instructions, real programs, all of it numbers.

People did write programs this way, and it was miserable. Worse, every family of processor spoke a different dialect, so nothing you wrote could move to another machine without being rewritten from scratch.

So we write in a language a human can hold in their head, and get a program to do the translation. That translator is a **compiler**. You write C, the compiler turns it into the processor's numeric instructions, and the result is a file you can run. You already did this in the Toolbench, and `gcc` is that translator.

C sits unusually close to the machine. When you write `x = x + 1` in C, that becomes roughly one processor instruction. When you write the same thing in Python, an interpreter reads your line, works out what type `x` currently holds, looks up the right addition routine for that type, checks whether the result needs a bigger container, and calls into a pile of machinery. Python is doing an enormous amount for you. C is doing almost nothing for you.

Doing almost nothing is the point. It makes C fast, it makes C portable to anything with a processor, and it makes C honest. There is very little distance between what you wrote and what runs, which means you can actually see the machine through it.

That visibility is the entire reason this book teaches programming with C rather than something gentler. Learn C and Python stops being a mystery box, because you will know what is inside the box. It does not work the other way around.

---

## What C will not do for you

C will not check that the array position you asked for is inside the array. It will read the memory just past the end and hand you whatever was sitting there. You watched this happen in the Toolbench with `scores[3]`.

C will not tell you that you forgot to give a variable a starting value. It will use whatever bits the previous occupant of that memory left behind. You watched this too, in `gdb`, when `total` held 21845 before line 5 had run.

C will not clean up memory you asked for and stopped using. That is your job, permanently, and forgetting is called a leak.

C will not stop you writing to memory you no longer own. It will let you do it, the program will keep running, and it will fail forty minutes later somewhere with no visible connection to what you did.

None of this is a design flaw. It is a trade, made deliberately in 1972 and kept ever since. C hands you the raw machine and trusts you with it. Every check it declines to perform is a check that costs time at runtime, and C's bargain is that you get the speed and you accept the responsibility.

The consequence is that C has a whole category of bug that friendlier languages simply do not have, and the defining feature of those bugs is that they are quiet. They do not announce themselves. They corrupt something and let you carry on.

This is exactly why your bench has a sanitizer and a debugger on it. Those two tools exist to make quiet bugs loud. You installed them before writing a single real program on purpose.

---

## One idea about algorithms

An **algorithm** is a procedure precise enough that a very literal clerk could follow it without asking questions. That is all the word means. It is not a mathematical object and there is nothing intimidating about it.

Here is the only algorithmic idea you need before Chapter 1.

You have a printed phone book with a thousand pages and you want to find one name.

**One approach.** Open page 1, check. Open page 2, check. Keep going. In the worst case, where the name is on the last page or not there at all, you turn a thousand pages.

**Another approach.** Open to the middle. Look at the names on that page. If the one you want comes alphabetically before them, you can throw away the entire second half of the book without ever looking at it. Open to the middle of what is left. Throw half of that away. Repeat.

A thousand pages becomes 500, then 250, then 125, then 63, and you are finished in about ten steps rather than a thousand.

Now double the phone book to two thousand pages. The first approach doubles to two thousand steps. The second approach needs eleven.

That gap is not a matter of efficiency in the abstract. It is the difference between a program that finishes while you wait and a program you assume has crashed. In Chapter 3 you will write both versions, time them yourself against two million lines of real data, and watch the numbers diverge. Only after you have measured it will I introduce the notation people use to talk about the difference.

You will have felt the thing before anyone gives it a name. That order is deliberate and it is how the whole book works.

Notice also that the second approach only works because the phone book is sorted. Take that away and it collapses instantly, because you can no longer throw half away with confidence. That is why sorting turns out to matter so much, and why Chapter 3 spends real time on it.

---

## What to carry into Chapter 1

Six things. If you remember nothing else from this section, remember these.

1. **Everything in memory is a number.** Letters, colours, prices, images. What a number *means* is an agreement applied from outside, not a property of the bytes.
2. **`'A'` is 65.** Characters are small integers, and C treats them that way, which makes some surprising things possible.
3. **Whole numbers are exact and fractions are not.** Binary cannot represent 0.1 precisely, the error is tiny, and tiny errors accumulate into money that has visibly gone missing.
4. **A compiler translates your C into instructions the processor runs.** It is a program, not magic, and it runs in four stages you will take apart in Chapter 2.
5. **C does not check anything you did not ask it to check.** The speed and the honesty come from that, and so does an entire family of quiet bugs, which is why your bench has a sanitizer on it.
6. **How you go about a task can matter more than how fast the machine is.** Halving beats scanning, and it beats it by more as the data grows.

---

## Now, Chapter 1

A shop is short a few pennies most days. The owner has counted the till three times, checked the CCTV, and quietly started wondering about the staff. The money is not being stolen. It is being lost by the program that prints the receipts, at a rate of a fraction of a penny per line, four hundred times a day.

You are going to write that program, watch it lose the money, and then fix it properly.

**Next:** [`ch01-the-till/`](../ch01-the-till/README.md)
