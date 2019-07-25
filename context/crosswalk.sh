#!/bin/bash

look "$1" "$MRCONSO" | awk -F'|' '$12 == "SNOMEDCT_US" && $17 == "N" {printf "%s\n", $14}' | sort | uniq
