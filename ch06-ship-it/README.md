# Chapter 6: Ship it

*Capstone*

> **Status: not written yet.** This file exists so the links in the rest of the
> book work, and so you can see where things are going. The scenario below is
> settled; the text is not.

## The scenario

No new syntax. This chapter is about turning code that works on your machine into a product that works on someone else's.

## What you will learn

You write the specification first, then assemble `logtool` from parts you already built: argument parsing with real validation, error handling that never fails silently, streaming input that handles a file bigger than your memory, the hash table from Chapter 5, the top-N logic from Chapter 3, a `--help` that reads like a proper manual page, a Makefile with debug and release targets, a shell test suite, a clean Valgrind run, and a tagged release on GitHub.

Then you hand it to a friend and watch them break it in ninety seconds.

---

**Back to:** [the map](../README.md#the-map)
