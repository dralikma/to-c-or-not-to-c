#!/usr/bin/env bash
#
# Runs every Chapter 2 program and compares its output against the
# matching file here. Silence from diff means a match.
#
#     cd ../code && make test

set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
DATA="$HERE/../data"

# Run from inside code/ and invoke programs by a relative path. This
# matters: argv[0] is whatever was typed to start the program, so
# calling it by an absolute path would change the output of greet and
# status. The chapter makes that point; the test suite has to respect it.
cd "$HERE/../code" || exit 1
BUILD="./build"

pass=0
fail=0

# check <name> <program> [stdin file] [expected exit status] [args...]
check()
{
    name="$1"; prog="$2"; stdin_file="${3:-/dev/null}"; want_status="${4:-0}"
    shift 4 2>/dev/null || shift $#

    if [ ! -x "$prog" ]; then
        printf 'MISSING  %-22s (not built)\n' "$name"; fail=$((fail + 1)); return
    fi

    got="$(mktemp)"
    "$prog" "$@" < "$stdin_file" > "$got" 2>/dev/null
    got_status=$?

    if ! diff -q "$got" "$HERE/$name-expected.txt" > /dev/null 2>&1; then
        printf 'FAIL     %-22s (output differs)\n' "$name"
        diff "$got" "$HERE/$name-expected.txt" | head -8 | sed 's/^/         /'
        fail=$((fail + 1))
    elif [ "$got_status" -ne "$want_status" ]; then
        printf 'FAIL     %-22s (exit %s, wanted %s)\n' "$name" "$got_status" "$want_status"
        fail=$((fail + 1))
    else
        printf 'PASS     %s\n' "$name"; pass=$((pass + 1))
    fi
    rm -f "$got"
}

echo "Part 1: the naive redactor"
check 01-echo        "$BUILD/steps/01-echo"        "$DATA/access.log"
check 02-echo-fixed  "$BUILD/steps/02-echo-fixed"  "$DATA/access.log"
check 03-redact-at   "$BUILD/steps/03-redact-at"   "$DATA/access.log"

echo
echo "Part 2: compilation"
check hello          "$BUILD/hello"
check count          "$BUILD/count"

echo
echo "Part 3: arrays, strings, arguments"
check scores         "$BUILD/scores"
check peek           "$BUILD/peek"
check shout          "$BUILD/shout"
check chars          "$BUILD/chars"
check len            "$BUILD/len"          "$HERE/inputs/david.txt"
check greet          "$BUILD/greet"        /dev/null 0 David Malan
check status-ok      "$BUILD/status"       /dev/null 0 Ali
check status-missing "$BUILD/status"       /dev/null 1
check argv-ok        "$BUILD/argvchars"    /dev/null 0 13
check argv-bad       "$BUILD/argvchars"    /dev/null 1 1x3
check redact         "$BUILD/redact"       "$DATA/access.log"

echo
echo "Part 4: the planted bugs still misbehave as documented"
check bug1           "$BUILD/bugs/bug1"    /dev/null 0 Ali
check bug3           "$BUILD/bugs/bug3"    "$DATA/access.log"
check bug4           "$BUILD/bugs/bug4"    "$DATA/access.log"

echo
echo "The requirements themselves, not just the saved output"

# bug2 has no null terminator, so strlen walks off the end of the array and
# what it finds is whatever the stack happened to hold. Its printed output is
# undefined behaviour and must never be pinned in an expected file: it was
# stable on the machine the chapter was written on and different on Debian.
#
# What IS stable is that AddressSanitizer catches it. Test that instead.
if [ -x "$BUILD/bugs/bug2-asan" ]; then
    if "$BUILD/bugs/bug2-asan" 2>&1 | grep -q "stack-buffer-overflow"; then
        printf 'PASS     %s\n' "bug2 still overruns its array (sanitizer catches it)"; pass=$((pass + 1))
    else
        printf 'FAIL     %s\n' "bug2 no longer overruns its array"; fail=$((fail + 1))
    fi
else
    printf 'MISSING  %s\n' "bug2-asan not built"; fail=$((fail + 1))
fi

if [ "$("$BUILD/redact" < "$DATA/access.log" | grep -c '@')" -eq 0 ]; then
    printf 'PASS     %s\n' "no address survives redaction"; pass=$((pass + 1))
else
    printf 'FAIL     %s\n' "an address survived redaction"; fail=$((fail + 1))
fi

echo
echo "-------------------------------------"
printf '%d passed, %d failed\n' "$pass" "$fail"

# Two programs are deliberately not output-tested, for the same reason:
#   garbage.c reads uninitialised memory
#   bugs/bug2.c reads past the end of an array
# Both have undefined output. Pinning either one in an expected file turns a
# true fact about your machine into a test failure on somebody else's.

[ "$fail" -eq 0 ]
