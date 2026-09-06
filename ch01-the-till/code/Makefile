# Makefile for all of Chapter 1's programs.
#
# This is a bigger version of the Makefile you type yourself in Part 5
# of the chapter. That one builds one program; this one builds every
# program in the chapter so the repository can be tested in one go.
#
# Everything is built into build/ so the source directories stay clean.

CC       = gcc
CFLAGS   = -std=c17 -Wall -Wextra -Wpedantic -Wfloat-equal -g
SANFLAGS = -fsanitize=address,undefined

# The programs, grouped the way the chapter is.
PART1 = build/steps/01-till-first build/steps/02-till-money \
        build/steps/03-till-broken build/steps/04-till-debug

PART2 = build/probe build/sizes

PART3 = build/two build/steps/05-receipt-money build/steps/06-receipt-padded \
        build/steps/07-receipt-tax build/feq build/chart build/receipt \
        build/day build/quantity build/confirm build/tax-cases build/loops

PART4 = build/bugs/bug1 build/bugs/bug1-quiet build/bugs/bug2 \
        build/bugs/bug3 build/bugs/bug4

all: $(PART1) $(PART2) $(PART3) $(PART4)

# One rule builds almost everything. In a rule, $@ is the target being
# built and $< is the first thing it depends on, so this says:
# "to make build/anything, compile anything.c into it."
build/%: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -o $@ $<

# Three programs need something different.

# two.c calls round(), which lives in the maths library. -lm goes at
# the END of the command. Leave it off and you get a linker error.
build/two: two.c
	@mkdir -p build
	$(CC) $(CFLAGS) -o $@ $< -lm

# bug1 built with every warning silenced (lowercase -w, the opposite of
# -Wall), so you can see the wrong output the compiler would otherwise
# have saved you from. Debian's gcc checks printf formats by default,
# so -w is what it takes to actually shut it up. Never use this for real.
build/bugs/bug1-quiet: bugs/bug1.c
	@mkdir -p build/bugs
	$(CC) -std=c17 -w -o $@ $<

# The sanitizer build of bug4, which names the overflow.
build/bugs/bug4-ub: bugs/bug4.c
	@mkdir -p build/bugs
	$(CC) -std=c17 -Wall -Wextra -g -fsanitize=undefined -o $@ $<

# feq.c exists to demonstrate -Wfloat-equal, so the default build
# deliberately leaves that flag off. Build feq-warn to see the warning.
build/feq: feq.c
	@mkdir -p build
	$(CC) -std=c17 -Wall -Wextra -Wpedantic -g -o $@ $<

build/feq-warn: feq.c
	@mkdir -p build
	$(CC) $(CFLAGS) -o $@ $<

# The sanitizer build of the finished till, for when something smells.
receipt-debug: receipt.c
	@mkdir -p build
	$(CC) $(CFLAGS) $(SANFLAGS) -o build/receipt-debug $<

test: all
	@bash ../tests/run-tests.sh

clean:
	rm -rf build

.PHONY: all test clean receipt-debug
