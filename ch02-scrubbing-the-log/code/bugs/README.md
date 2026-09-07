# The four planted bugs

One bug each, one tool each. Read the symptom, work it out, then check the
walkthrough in Part 4 of the chapter.

**These files carry no header comments on purpose.** They are byte-identical to
the listings printed in the chapter, so line numbers match. One extra comment at
the top would shift every line below it.

| File | Symptom | Best tool | The bug |
|---|---|---|---|
| `bug1.c` | Greets everybody, not just Ali | the compiler | `==` on strings compares locations, not contents |
| `bug2.c` | Right answer today, rubbish tomorrow | the sanitizer | no room left for the null terminator |
| `bug3.c` | Looks redacted, still leaks every name | `gdb` | walking left tests the wrong character |
| `bug4.c` | Looks perfect, the parser rejects it | `diff` | the newline `fgets` already gave you |

Bug 3 is the one worth sitting with. It is one character different from correct,
it produces output that looks scrubbed, and every customer's name survives in it.

## Why bug2 is not output-tested

`bug2.c` has no null terminator, so `strlen` walks off the end of the array and
reads whatever is there. That output is **undefined**: it differs between
compiler versions and machines. The test suite checks that AddressSanitizer
still catches the overrun instead of pinning a printed line that was only ever
true on one machine.

## Building them

```
$ cd ..
$ make build/bugs/bug2-asan     # the only build that finds bug 2
$ ./build/bugs/bug3 < ../data/access.log | sed -n '2p;7p'
```

## Checking bug 3 and bug 4

```
$ ./build/bugs/bug3 < ../data/access.log > /tmp/mine.txt
$ diff /tmp/mine.txt ../tests/redact-expected.txt
```
