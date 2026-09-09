# How this book is written

This is the style guide for *To C or not to C*. It's here because the book is
published under one name and has to read that way: one person, one set of
opinions, from the first page to the last.

If you're writing or editing a chapter, read this first. There's a script that
checks most of it (`tools/check-voice.py`), but the script can only catch the
mechanical failures. The rest is judgment.

## The test

Read the paragraph out loud.

If it sounds like a conference abstract, a press release, or the About page of a
developer tools company, rewrite it until it sounds like somebody explaining
something at a keyboard.

That's the whole guide. Everything below is just the specific ways I've caught
myself failing it.

## Voice

**One author.** Second person for the reader, always. First person singular when
there's an opinion or a war story, and there should be plenty of both. If a
chapter goes 4,000 words without the author appearing, something's wrong.

**Contractions, throughout.** "It's" not "it is." "You'll" not "you will."
"Doesn't" not "does not." The first draft of this book had one contraction in
1,132 opportunities, which is why it read like a manual for a fire alarm.

There's one exception worth keeping: when a sentence needs weight, drop the
contraction. "Do not put that in a test suite" hits harder than "don't." Use it
rarely, or it stops working.

**Varied sentence length.** Long, then short. Some paragraphs are one sentence.

Like that.

**Have opinions and say them.** If a default is bad, say it's bad. `a.out` is a
terrible default name. `scanf` is a trap. GNU style puts a space before the
parenthesis and it looks wrong. A reader can disagree with an opinion. They can't
do anything with mush.

**Admit difficulty.** "Everyone gets this wrong the first time" is worth more
than reassurance, because it's true and because it tells the reader their
confusion is normal rather than a personal failing. When I've made a mistake
myself, say so. Chapter 1's `gdb` walkthrough had the wrong line number for a
week; that's in the book now.

**Let the reader fail on purpose.** "Type this. Run it. It'll break. That's the
point." Every chapter has a First Contact section built on this, and it works
because feeling the problem beats being told about it.

**Concrete, always.** Not "a large file." Forty thousand lines. Not "it's slow."
Four hundred baskets a day at one cent each is $1,248 a year. Name the file, the
error message, the number.

## Never use an em dash

Not the character. Not its disguises either: no spaced hyphen doing the same job,
no semicolon pressed into service as a dramatic pause.

Recast the sentence. Use a comma. Use parentheses. Use a colon. Write two
sentences. There is always another way and it's usually better.

The checker enforces this one absolutely.

## Banned constructions

These are the fingerprints of machine writing. Every one of them appeared in the
first draft of this book.

**"It's not X, it's Y."** Also "not just X but Y." It's a fake reveal. Say the
thing.

**Colon-then-reveal, as a habit.** Fine once in a chapter. Four times is a tic.

**Three-item lists by default.** Sometimes there really are three things. Often
there are two, or four, and the third got invented to fill the rhythm.

**Opening a section by restating its heading.** The heading already said it.

**Closing a section by summarising it.** The reader just read it.

**Rhetorical questions as openers.** "So what's really going on here?" No.

**Template intros.** "By the end of this chapter you will be able to" is a form,
not a sentence. A real opening sets up a problem somebody actually has. Chapters
in this book open with a person losing money or about to leak customer data.

**"Let's dive in," "let's unpack," "buckle up," "this is where the magic
happens."** No.

**These words:** delve, leverage, seamless, robust, crucial, vital, essential,
powerful, elegant, game-changer, journey, landscape, realm, tapestry, testament.

**These phrases:** "it's worth noting," "that said," "at the end of the day,"
"here's the thing."

**Stacked hedges.** "Generally, this typically tends to often work" says nothing.
Pick one hedge or none.

**Bold mid-sentence for emphasis.** Bold is for defined terms on first use and
for box labels. That's it. If a sentence needs emphasis, rewrite it so the
important word lands at the end.

**Praising the reader.** No "Great job!" No "You've come so far!" The reader
knows whether their code compiled.

**Stock analogies.** Git is not save points in a video game. A pointer is not a
house address. A variable is not a box. Every one of those has been used ten
thousand times and none of them survive contact with the real thing.

If an analogy earns its place it has to be specific to this book and it has to do
real work. The phone book in *How the Machine Thinks* stays because Chapter 3
comes back to it and measures it. Most analogies don't clear that bar.

## Boxes

Four kinds, and no others. Bold label, then the content.

> **Under the hood** goes a level deeper than the main text needs. Skippable on
> a first read, worth coming back to.

> **Debian note** is anything specific to Debian 13, a package name, or gcc
> behaviour that differs from what's on the internet.

> **Trap** is the mistake almost everybody makes at that exact line.

> **Parity** connects the chapter to CS50's vocabulary and problem sets.

No emoji, anywhere, including in these.

## Things that are fine

Sentence fragments, when the rhythm calls for it.

Starting a sentence with "And" or "But." Every style guide that bans this is
wrong and every good writer ignores it.

Being funny, if it's actually funny and doesn't cost clarity.

Repeating yourself across chapters. A reader picking up Chapter 4 six months
after Chapter 1 needs the reminder, and one sentence is cheaper than a lookup.

## Checking it

```
$ python3 tools/check-voice.py
```

It reports per file: contraction rate, whether the author appears, banned words
and phrases, em dashes and their disguises, and the constructions above that a
regular expression can spot.

It can't tell you whether a paragraph sounds like a person. Read it aloud.
