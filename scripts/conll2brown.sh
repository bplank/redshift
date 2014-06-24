#!/bin/bash
cat $1 | awk -F'\t' '{ if (NF>0) printf "%s/%s ", $2,$4; else print }' 