# How the Machine Thinks

*Between the Toolbench and Chapter 1. Twenty minutes. Nothing to install, nothing to type.*

---

Chapter 1 opens with a bakery that's short a few pennies most days and nobody can find where they're going. The money isn't being stolen. It's being destroyed by arithmetic, and the reason is a fact about how machines store numbers that I'd much rather you knew going in than discovered halfway through a debugging session.

There are five or six facts like that. None of them take long. All of them ambush people who skip this.

So here they are, up front, with nothing to type and nothing to run. It's the only part of the book like that, and you should read it once now and again after Chapter 4, when it'll say something different to you.

> **Why there's no Week 0.** CS50 opens with Scratch, dragging coloured blocks around to teach loops and conditionals without syntax getting in the way. In a lecture hall with several hundred people in it, that's a good idea. Working through a book on your own, with nobody to drag blocks alongside you, it's a detour. I've cut it and written this instead.

---

## The machine only knows numbers

Your processor is fast and extremely literal. It can't read. It has no idea what a letter is, or a word, or a colour, or a price. It handles numbers, and only numbers, and those numbers are patterns of high and low voltage sitting in transistors.

One of those on-or-off slots is a **bit**. One bit holds two values, 0 or 1. Two bits give you four combinations: 00, 01, 10, 11. Three give you eight. Every bit you add doubles what you can say.

Eight bits give you 256 combinations, and eight bits together is a **byte**. That's the smallest unit most machines bother to address on its own, which is why bytes turn up everywhere once you start looking. When Chapter 1 tells you an `int` takes four bytes, that's 32 bits, which is a bit over four billion distinct values. Not infinite. Four billion and change, and then it runs out, and Chapter 1 shows you what running out looks like.

That's the whole foundation. Everything above it is agreement.

## Everything else is an agreement about what the numbers mean

If the machine only stores numbers, how does it store the letter `A`?

It doesn't. It stores the number 65, and everybody has agreed that when we're treating that byte as text, 65 means `A`. The agreement is called **ASCII** and somebody wrote it down in the 1960s. `B` is 66, `C` is 67, on up the alphabet. Lowercase `a` is 97, which is exactly 32 more than uppercase `A`. A space is 32. The character `0`, the one you type, is 48.

I want to be clear that I'm not simplifying to get you moving. In C this is literally true and you'll prove it in one line in Chapter 1. The character `'A'` and the number 65 are the same value wearing different clothes. C lets you do arithmetic on letters because to C they were never letters in the first place.

That fact earns its keep almost immediately. Converting a letter to uppercase is subtraction. Checking whether a character is a digit is a range check. Chapter 2 has you write a cipher that shifts letters through the alphabet, and the whole thing works because the alphabet is a run of consecutive numbers.

The same trick runs the rest of the machine. A colour is three numbers for how much red, green and blue. An image is a grid of those. A sound is a long list of numbers describing air pressure tens of thousands of times a second. A file on disk is a run of bytes, and what those bytes *mean* depends entirely on which agreement you apply when you read them.

Nothing inside the file says "I am a photograph." The agreement lives outside the data. Which is why renaming a file from `.jpg` to `.txt` changes precisely nothing about it, and why opening a photograph in a text editor shows you garbage. Same bytes, wrong agreement.

In Chapter 4 you'll take a file that looks like a photograph, read its raw bytes yourself, and pull deleted images off a corrupted memory card by spotting the specific byte pattern that means "a JPEG starts here." At that point this stops being an abstraction and becomes a tool.

## Numbers with decimal points are where the trouble starts

Whole numbers are easy. Two bytes hold any whole number from 0 to 65,535, exactly, with no rounding and no argument.

Fractions are not easy, and this is worth a minute because it's the plot of Chapter 1.

Try writing one third in decimal. You get 0.3333333, you have to stop somewhere, and wherever you stop you're wrong. There's no number of decimal places that gets you there. That isn't a flaw in your arithmetic. Decimal is built on tens, and one third isn't any whole number of tenths, or hundredths, or thousandths, so decimal simply cannot say it.

Binary has the same problem with a different set of numbers, because it's built on twos. One of the numbers it can't say is **0.1**.

Your machine has a fixed number of bits, so it stores something extremely close to 0.1 and carries on. The error is about one part in ten thousand trillion. Invisible. Irrelevant.

Until you add it up.

Do arithmetic on thousands of those very-close numbers and the tiny errors accumulate. Multiply and they compound rather than merely adding. Round the result to two decimal places for display and the display looks perfect while the stored value has drifted. Run that across four hundred transactions a day and the till comes up short by an amount somebody eventually notices.

This isn't a cautionary tale I'm building towards. It's the reason banks, payroll systems and every point of sale terminal in the world refuse to store money the way most beginners' first instinct suggests, and if you've ever wondered why a database column holds `1999` for a price of £19.99, that's why.

The fix isn't "use more decimal places." More decimal places postpones the problem and makes it harder to spot. You have to stop storing fractions at all, and in Chapter 1 you'll build the thing that does.

## Why we don't write the numbers ourselves

The processor's actual language is a short list of numeric instructions. Copy this value into that register. Add these two registers. Jump to this address if the last result was zero. Real instructions, real programs, all of it numbers.

People did write programs that way. It was miserable, and every family of processor spoke a different dialect, so nothing you wrote could move to another machine without being rewritten from scratch.

So we write in a language a human can hold in their head and get a program to do the translation. That translator is a **compiler**. You write C, the compiler turns it into the processor's numeric instructions, and out comes a file you can run. You already did this in the Toolbench, and `gcc` is that translator.

C sits unusually close to the machine. Write `x = x + 1` in C and it becomes roughly one processor instruction. Write the same line in Python and an interpreter reads it, works out what type `x` currently holds, looks up the right addition routine for that type, checks whether the result needs a bigger container, and calls into a pile of machinery. Python is doing an enormous amount for you. C is doing almost nothing.

Doing almost nothing is the point. It makes C fast, it makes C portable to anything with a processor in it, and it makes C honest. There's very little distance between what you wrote and what runs, which means you can see the machine through it.

That's why this book teaches programming with C rather than something gentler. Learn C and Python stops being a mystery box, because you'll know what's in the box. It doesn't work the other way round, and I've watched enough people try.

## What C won't do for you

C won't check that the array position you asked for is inside the array. It'll read the memory just past the end and hand you whatever was sitting there. You watched that happen in the Toolbench with `scores[3]`.

C won't tell you that you forgot to give a variable a starting value. It'll use whatever bits the previous occupant of that memory left behind. You watched that too, in `gdb`, when `total` held 21845 before line 5 had run.

C won't clean up memory you asked for and stopped using. That's your job, permanently, and forgetting is called a leak.

C won't stop you writing to memory you no longer own. It'll let you do it, the program will keep running, and it'll fail forty minutes later somewhere with no visible connection to what you did.

None of that is a design flaw and I want to be careful not to present it as one. It's a trade, made deliberately in 1972 and kept ever since. C hands you the raw machine and trusts you with it. Every check it declines to perform is a check that would have cost time on every single run, and the bargain is that you get the speed and you accept the responsibility.

What the bargain costs you is a category of bug that friendlier languages simply don't have, and the defining feature of those bugs is that they're quiet. They don't announce themselves. They corrupt something and let you carry on.

Which is why your bench has a sanitizer and a debugger on it, and why you installed both before writing a single real program. Those two tools exist to make quiet bugs loud.

## One idea about algorithms

An **algorithm** is a procedure precise enough that something extremely literal could follow it without asking questions. That's all the word means. It isn't a mathematical object and there's nothing intimidating about it.

Here's the only algorithmic idea you need before Chapter 1.

You've got a printed phone book, a thousand pages, and you want to find one name.

**One approach.** Open page 1, check. Open page 2, check. Keep going. Worst case, where the name is on the last page or isn't there at all, you turn a thousand pages.

**Another approach.** Open to the middle. If the name you want comes alphabetically before the names on that page, throw away the entire second half without looking at it. Open to the middle of what's left. Throw half of that away. Repeat.

A thousand pages becomes 500, then 250, then 125, then 63, and you're finished in about ten steps rather than a thousand.

Now double the phone book to two thousand pages. The first approach doubles to two thousand steps. The second needs eleven.

I've used a phone book here rather than something more modern, and I'd normally distrust an analogy that old. This one stays because Chapter 3 comes back and measures the same two approaches on two million lines of real data. The phone book is the version you can picture and the measurement is the version you can trust. You need both, and most analogies never earn the second half.

The gap between ten steps and a thousand isn't efficiency in the abstract. It's the difference between a program that finishes while you wait and a program you assume has hung. In Chapter 3 you'll write both, time them yourself, and watch the numbers separate. Only after that will I introduce the notation people use to talk about the difference.

You'll have felt the thing before anybody gives it a name. That order is deliberate and it's how the whole book works.

One more thing about the second approach, because it's easy to miss. It only works because the phone book is sorted. Take that away and it collapses on the spot, since you can no longer throw half away with any confidence. That's why sorting turns out to matter so much, and why Chapter 3 spends real time on it.

## What to carry into Chapter 1

Six things. If you remember nothing else from this section, remember these.

1. **Everything in memory is a number.** Letters, colours, prices, images. What a number *means* is an agreement applied from outside rather than a property of the bytes.
2. **`'A'` is 65.** Characters are small integers and C treats them that way, which makes some surprising things possible.
3. **Whole numbers are exact and fractions aren't.** Binary can't represent 0.1 precisely, the error is tiny, and tiny errors accumulate into money that's visibly gone missing.
4. **A compiler translates your C into instructions the processor runs.** It's a program, not magic, and it works in four stages you'll take apart by hand in Chapter 2.
5. **C checks nothing you didn't ask it to check.** The speed and the honesty both come from that, and so does an entire family of quiet bugs, which is why there's a sanitizer on your bench.
6. **How you go about a task can matter more than how fast the machine is.** Halving beats scanning, and it beats it by more as the data grows.

## Now, Chapter 1

A bakery is short a few pennies most days. The owner has counted the till three times, checked the CCTV, and quietly started wondering about her staff. Nobody is stealing from her. The money is being lost by the program that prints the receipts, at a rate of a fraction of a penny per line, four hundred times a day.

You're going to write that program, watch it eat the money, and then fix it properly.

**Next:** [`ch01-the-till/`](../ch01-the-till/README.md)
