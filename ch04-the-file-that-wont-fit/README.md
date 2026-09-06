# Chapter 4: The file that won't fit

*CS50x Week 4*

> **Status: not written yet.** This file exists so the links in the rest of the
> book work, and so you can see where things are going. The scenario below is
> settled; the text is not.

## The scenario

Your log reader has worked perfectly for weeks. Then a request with a 4,000 character URL arrives, and the program corrupts its own memory and dies. The fixed-size buffer that was fine on day one is the bug.

## What you will learn

Hexadecimal. Pointers, properly and slowly, with pictures and with `gdb`. Pointer arithmetic. The stack and the heap and what lives where. `malloc`, `realloc`, and `free`. Memory leaks and use-after-free. Valgrind and AddressSanitizer. File input and output.

---

**Back to:** [the map](../README.md#the-map)
