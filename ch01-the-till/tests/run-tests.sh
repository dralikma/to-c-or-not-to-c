#!/usr/bin/env bash
#
# Runs every Chapter 1 program and compares its output against the
# matching file in this directory. Silence from diff means a match,
# exactly as in the chapter.
#
# Usage, from the code/ directory:   make test
# Or from anywhere:                  ./tests/run-tests.sh

set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
BUILD="$HERE/../code/build"

pass=0
fail=0

# check <name> <program> [stdin file] [expected exit status]
check()
{
    name="$1"
    prog="$2"
    stdin_file="${3:-/dev/null}"
    want_status="${4:-0}"

    if [ ! -x "$prog" ]; then
        printf 'MISSING  %-24s (not built)\n' "$name"
        fail=$((fail + 1))
        return
    fi

    got="$(mktemp)"
    "$prog" < "$stdin_file" > "$got" 2>/dev/null
    got_status=$?

    if ! diff -q "$got" "$HERE/$name-expected.txt" > /dev/null 2>&1; then
        printf 'FAIL     %-24s (output differs)\n' "$name"
        diff "$got" "$HERE/$name-expected.txt" | sed 's/^/         /'
        fail=$((fail + 1))
    elif [ "$got_status" -ne "$want_status" ]; then
        printf 'FAIL     %-24s (exit %s, wanted %s)\n' "$name" "$got_status" "$want_status"
        fail=$((fail + 1))
    else
        printf 'PASS     %s\n' "$name"
        pass=$((pass + 1))
    fi

    rm -f "$got"
}

echo "Part 1: the broken till"
check 01-till-first    "$BUILD/steps/01-till-first"
check 02-till-money    "$BUILD/steps/02-till-money"
check 03-till-broken   "$BUILD/steps/03-till-broken"
check 04-till-debug    "$BUILD/steps/04-till-debug"

echo
echo "Part 2: under the hood"
check probe            "$BUILD/probe"

echo
echo "Part 3: build it properly"
check two              "$BUILD/two"
check 05-receipt-money "$BUILD/steps/05-receipt-money"
check 06-receipt-padded "$BUILD/steps/06-receipt-padded"
check 07-receipt-tax   "$BUILD/steps/07-receipt-tax"
check feq              "$BUILD/feq"
check chart            "$BUILD/chart"
check loops            "$BUILD/loops"
check receipt          "$BUILD/receipt"
check tax-cases        "$BUILD/tax-cases"
check day              "$BUILD/day"
check quantity-good    "$BUILD/quantity" "$HERE/inputs/quantity-good.txt" 0
check quantity-bad     "$BUILD/quantity" "$HERE/inputs/quantity-bad.txt" 1
check confirm-yes      "$BUILD/confirm"  "$HERE/inputs/confirm-yes.txt"  0
check confirm-no       "$BUILD/confirm"  "$HERE/inputs/confirm-no.txt"   0

echo
echo "Part 4: the planted bugs still misbehave as documented"
check bug1-quiet       "$BUILD/bugs/bug1-quiet"
check bug2             "$BUILD/bugs/bug2"
check bug3             "$BUILD/bugs/bug3"
check bug4             "$BUILD/bugs/bug4"

echo
echo "-------------------------------------"
printf '%d passed, %d failed\n' "$pass" "$fail"

# sizes is deliberately not tested: its output depends on the machine,
# which is the entire point of running it.

[ "$fail" -eq 0 ]
