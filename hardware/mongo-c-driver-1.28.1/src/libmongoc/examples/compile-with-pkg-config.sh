#!/usr/bin/env bash

# -- sphinx-include-start --
gcc -o hello_mongoc hello_mongoc.c $(pkg-config --libs --cflags libmongoc-1.0)
