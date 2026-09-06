# The four planted bugs

Each file has exactly one bug, and each is best caught by a different tool.
Work them before reading the walkthroughs in Part 4 of the chapter.

**These files carry no header comments on purpose.** They are byte-identical to
the listings printed in the chapter, so the line numbers in the book's `gdb`
sessions match the files you have here. A single extra comment line at the top
would shift every line below it and quietly break `break 8`.

| File | Symptom | Best tool | The bug |
|---|---|---|---|
| `bug1.c` | Small takings report fine, large ones are nonsense | the compiler | `%d` where `%ld` belongs |
| `bug2.c` | Tax should be about 8% of the bill, reports 0% | `gdb` | dividing before multiplying |
| `bug3.c` | Looks perfect on screen, every total is a cent low | `diff` | a loop counting from 1 instead of 0 |
| `bug4.c` | A year of takings comes out negative | the sanitizer | `int` overflow |

## Building them

`make` from the `code/` directory builds all four, plus two extra versions that
the chapter needs:

```
$ make build/bugs/bug1-quiet   # every warning silenced, to see the wrong output
$ make build/bugs/bug4-ub      # with the undefined behaviour sanitizer
```

`bug1-quiet` uses lowercase `-w`, which is the opposite of `-Wall`. Debian's gcc
checks printf formats by default, so `-w` is what it takes to actually silence
it. Never use that flag on real work.

## Checking bug3

`bug3.c` is `receipt.c` with one line changed. Compare its output against the
known-good file:

```
$ ./build/bugs/bug3 > /tmp/mine.txt
$ diff /tmp/mine.txt ../tests/receipt-expected.txt
```
