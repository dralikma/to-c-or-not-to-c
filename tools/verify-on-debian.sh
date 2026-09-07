#!/usr/bin/env bash
#
# verify-on-debian.sh - check the claims that could not be executed while the
# book was being written.
#
# Almost everything in this book was compiled and run before it was written
# down. Four things could not be, because the machine used for writing did not
# have them installed: gdb, valgrind, clang, clang-format, and nano.
#
# The gdb transcripts are the important ones. The book prints about 55 lines of
# gdb session as though they were captured from a real run. The *values* in
# them are safe, because they were worked out from programs that were actually
# executed. The *formatting* around them, meaning the banner, the breakpoint
# addresses, the exact spacing, was written from knowledge rather than from a
# terminal.
#
# So run this on your Debian machine and compare what it prints against what the
# book says. Anything that differs is a bug in the book, and you should fix the
# book rather than your machine.
#
# Usage, from the repository root:
#
#     $ bash tools/verify-on-debian.sh
#
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

hr() { printf '\n%s\n' "------------------------------------------------------------"; }

# ------------------------------------------------------- 1. tools present
hr
echo "1. IS EVERYTHING THE BOOK ASSUMES ACTUALLY INSTALLED?"
echo
missing=0
for t in gcc clang make gdb valgrind git nano python3; do
    if command -v "$t" > /dev/null 2>&1; then
        printf '   %-14s %s\n' "$t" "$("$t" --version 2>&1 | head -1)"
    else
        printf '   %-14s NOT INSTALLED\n' "$t"
        missing=$((missing + 1))
    fi
done

if command -v clang-format > /dev/null 2>&1; then
    printf '   %-14s %s\n' "clang-format" "$(clang-format --version)"
else
    printf '   %-14s NOT INSTALLED (optional, used in Chapter 1 Part 5)\n' "clang-format"
fi

if [ "$missing" -gt 0 ]; then
    echo
    echo "   $missing missing. The Toolbench's apt line should have installed them:"
    echo "   sudo apt install build-essential gdb valgrind clang git man-db manpages-dev"
fi

# --------------------------------------------- 2. man pages, section 3
hr
echo "2. DOES 'man 3 printf' WORK? (needs manpages-dev)"
echo
if man 3 printf > /dev/null 2>&1; then
    echo "   yes. The Toolbench's claim holds."
else
    echo "   NO. Install manpages-dev, or fix the Toolbench's claim."
fi

# ------------------------------------------------- 3. Chapter 1 gdb session
hr
echo "3. THE CHAPTER 1 GDB WALKTHROUGH"
echo
echo "   The chapter claims 'subtotal += part;' is line 38 of receipt.c, and"
echo "   prints a session breaking there. Compare the real output below against"
echo "   the section called 'Under the hood: watch the money move'."
echo

cp -r "$ROOT/ch01-the-till/code" "$WORK/code"
cd "$WORK/code" || exit 1

line=$(grep -n "subtotal += part;" receipt.c | cut -d: -f1)
echo "   receipt.c line $line is: $(sed -n "${line}p" receipt.c | sed 's/^ *//')"
echo

if command -v gdb > /dev/null 2>&1; then
    make build/receipt > /dev/null 2>&1
    echo "   --- real gdb output starts here ---"
    gdb -q -batch \
        -ex "break $line" \
        -ex "run" \
        -ex "print subtotal" \
        -ex "print part" \
        -ex "print i" \
        -ex "next" \
        -ex "print subtotal" \
        -ex "continue" \
        -ex "print i" \
        -ex "print part" \
        -ex "continue" \
        -ex "info locals" \
        ./build/receipt 2>&1 | sed 's/^/   /'
    echo "   --- ends here ---"
    echo
    echo "   The book claims subtotal goes 850, then 1117, and that the three"
    echo "   croissant shares are 267, 267, 266. Check those numbers above."
else
    echo "   gdb not installed, skipping."
fi

# ------------------------------------------- 3b. Chapter 2 gdb session
hr
echo "3b. THE CHAPTER 2 GDB WALKTHROUGH (Bug 3)"
echo
echo "   Chapter 2 breaks on redact_line and then on the left-walk loop."
echo "   Compare the line numbers gdb reports against what the chapter says."
echo

cd "$WORK/code" 2>/dev/null || cd "$ROOT/ch02-scrubbing-the-log/code" || true
if [ -d "$ROOT/ch02-scrubbing-the-log/code" ]; then
    rm -rf "$WORK/ch2" && cp -r "$ROOT/ch02-scrubbing-the-log" "$WORK/ch2"
    cd "$WORK/ch2/code" || exit 1
    walk=$(grep -n "while (start > 0" bugs/bug3.c | cut -d: -f1)
    echo "   bug3.c: redact_line starts at line $(grep -n '^void redact_line(char line\[\])$' bugs/bug3.c | tail -1 | cut -d: -f1)"
    echo "   bug3.c: the left-walk loop is line $walk"
    echo
    if command -v gdb > /dev/null 2>&1; then
        make build/bugs/bug3 > /dev/null 2>&1
        echo "   --- real gdb output starts here ---"
        gdb -q -batch \
            -ex "break redact_line" \
            -ex "break $walk" \
            -ex "run < ../data/access.log" \
            -ex "delete 1" \
            -ex "continue" \
            -ex "print i" \
            -ex "print start" \
            -ex "print line[start]" \
            ./build/bugs/bug3 2>&1 | grep -vE "^\[|libthread" | head -18 | sed 's/^/   /'
        echo "   --- ends here ---"
        echo
        echo "   The chapter claims gdb reports line 43 for redact_line, that the"
        echo "   left-walk loop is line $walk, and that line[start] is 64 '@',"
        echo "   which is the bug: start never moved off the @."
    else
        echo "   gdb not installed, skipping."
    fi
    cd "$WORK" || exit 1
fi

# ----------------------------------------- 4. Toolbench gdb sessions
hr
echo "4. THE TOOLBENCH GDB SECTIONS"
echo
echo "   The Toolbench uses two programs you type yourself, sum.c and crash.c."
echo "   They are recreated here so the sessions can be checked."
echo

cat > "$WORK/sum.c" << 'CEOF'
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
CEOF

cat > "$WORK/crash.c" << 'CEOF'
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
CEOF

cd "$WORK" || exit 1
gcc -std=c17 -Wall -Wextra -Wpedantic -g -o sum sum.c 2>/dev/null
gcc -std=c17 -Wall -Wextra -Wpedantic -g -o crash crash.c 2>/dev/null

echo "   sum.c should print 45, not 55, because the loop uses < instead of <=:"
echo "     $(./sum)"
echo

if command -v gdb > /dev/null 2>&1; then
    echo "   --- 'no debugging symbols' claim: gdb on a binary built without -g ---"
    gcc -std=c17 -o sum-nodebug sum.c 2>/dev/null
    gdb -q -batch -ex "list" ./sum-nodebug 2>&1 | head -4 | sed 's/^/   /'
    echo
    echo "   --- backtrace after a segfault (crash.c) ---"
    gdb -q -batch -ex "run" -ex "backtrace" ./crash 2>&1 | tail -8 | sed 's/^/   /'
    echo
    echo "   The Toolbench claims the crash reports message=0x0 at crash.c:5,"
    echo "   with main () at crash.c:11 in frame #1. Check that above."
else
    echo "   gdb not installed, skipping."
fi

# ------------------------------------------------------- 5. valgrind
hr
echo "5. VALGRIND"
echo
echo "   The Toolbench only claims valgrind is installed and waiting for"
echo "   Chapter 4. Confirming it runs at all:"
echo
if command -v valgrind > /dev/null 2>&1; then
    valgrind --error-exitcode=0 ./sum 2>&1 | tail -4 | sed 's/^/   /'
else
    echo "   valgrind not installed, skipping."
fi

# ------------------------------------------------------- 6. clang
hr
echo "6. CLANG AS A SECOND OPINION"
echo
echo "   The Toolbench says clang often phrases an error more clearly."
echo "   Same broken file, both compilers:"
echo
cat > bad.c << 'CEOF'
#include <stdio.h>
int main(void)
{
    int count = 3;
    if (count = 0) { printf("empty\n"); }
    return 0;
}
CEOF
echo "   --- gcc ---"
gcc -std=c17 -Wall -o /dev/null bad.c 2>&1 | head -4 | sed 's/^/   /'
if command -v clang > /dev/null 2>&1; then
    echo "   --- clang ---"
    clang -std=c17 -Wall -o /dev/null bad.c 2>&1 | head -4 | sed 's/^/   /'
else
    echo "   clang not installed, skipping."
fi

# ------------------------------------------------- 7. the Makefile tab trap
hr
echo "7. IS THE MAKEFILE TAB TRAP REAL, AND DOES cat -A REVEAL IT?"
echo
printf 'all:\n\techo tab-worked\n' > Makefile.tab
printf 'all:\n    echo spaces-used\n' > Makefile.spaces

echo "   with a real tab:"
make -f Makefile.tab 2>&1 | sed 's/^/     /'
echo
echo "   with four spaces:"
make -f Makefile.spaces 2>&1 | sed 's/^/     /'
echo
echo "   cat -A on the good one (the ^I is the tab the book tells you to look for):"
cat -A Makefile.tab | sed 's/^/     /'

# ------------------------------------------------- 8. clang-format agreement
hr
echo "8. DOES clang-format AGREE WITH THE CODE IN THIS REPOSITORY?"
echo
echo "   Chapter 1 says to hand style to a tool. That is only honest if the tool"
echo "   leaves the book's own code alone. .clang-format at the repository root"
echo "   is meant to make that true for every file."
echo
if command -v clang-format > /dev/null 2>&1; then
    cd "$ROOT" || exit 1
    disagree=0
    total=0
    while IFS= read -r f; do
        total=$((total + 1))
        if ! clang-format --style=file "$f" | diff -q - "$f" > /dev/null 2>&1; then
            disagree=$((disagree + 1))
            echo "   would reformat: ${f#./}"
            clang-format --style=file "$f" | diff "$f" - | head -6 | sed 's/^/       /'
        fi
    done < <(find ch0*/code -name '*.c' | sort)
    echo
    if [ "$disagree" -eq 0 ]; then
        echo "   all $total files already match .clang-format. Nothing to do."
    else
        echo "   $disagree of $total files disagree. Either run"
        echo "     clang-format --style=file -i \$(find ch0*/code -name '*.c')"
        echo "   or adjust .clang-format until it matches what the book prints."
    fi
else
    echo "   clang-format not installed. sudo apt install clang-format"
fi

# ------------------------------------------------ 9. nano toggles, for reference
hr
echo "9. WHAT NANO ACTUALLY CALLS ITS TOGGLES"
echo
echo "   The book no longer tells you to press a key to switch tabs-to-spaces off,"
echo "   because there is no such toggle. It tells you to comment the setting out"
echo "   of ~/.nanorc instead. For reference, here is what your nano documents:"
echo
man nano 2>/dev/null | grep -iE "tabstospaces|tabs to spaces" | head -4 | sed 's/^/     /' \
    || echo "     (no man page for nano installed)"

hr
echo "Done. Anything above that disagrees with the book is a bug in the book."
echo
