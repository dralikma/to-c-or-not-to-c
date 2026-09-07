# Makefile for all of Chapter 2's programs.
#
# Bigger than the one you type yourself in Part 5, because it builds
# every program in the chapter rather than one. Everything goes into
# build/, which is not in version control.

CC       = gcc
CFLAGS   = -std=c17 -Wall -Wextra -Wpedantic -g
SANFLAGS = -fsanitize=address,undefined

PART1 = build/steps/01-echo build/steps/02-echo-fixed build/steps/03-redact-at
PART2 = build/hello build/count
PART3 = build/scores build/peek build/garbage build/shout build/len \
        build/chars build/greet build/status build/argvchars build/redact
PART4 = build/bugs/bug1 build/bugs/bug2 build/bugs/bug2-asan \
        build/bugs/bug3 build/bugs/bug4

all: $(PART1) $(PART2) $(PART3) $(PART4)

# One rule builds almost everything. $@ is the target, $< is the first
# thing it depends on.
build/%: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -o $@ $<

# bug2 reads past the end of an array, so it needs a sanitizer build
# to show what is actually wrong with it.
build/bugs/bug2-asan: bugs/bug2.c
	@mkdir -p build/bugs
	$(CC) -std=c17 -Wall -Wextra -g -fsanitize=address -o $@ $<

redact-debug: redact.c
	@mkdir -p build
	$(CC) $(CFLAGS) $(SANFLAGS) -o build/redact-debug $<

# The four stages from Part 2, run one at a time so you can read the
# output of each. Leaves hello.i, hello.s and hello.o behind on purpose.
stages: hello.c
	$(CC) -std=c17 -E hello.c > build/hello.i
	$(CC) -std=c17 -S hello.c -o build/hello.s
	$(CC) -std=c17 -c hello.c -o build/hello.o
	$(CC) build/hello.o -o build/hello-linked
	@echo
	@wc -l hello.c build/hello.i build/hello.s

test: all
	@bash ../tests/run-tests.sh

clean:
	rm -rf build

.PHONY: all test clean stages redact-debug
