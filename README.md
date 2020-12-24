# leakDetect

A simple tool to find memery leak

## Usage

"""

python3 detectleak.py

python3 -v (verbose)

"""

## How it works?

When you malloc OR free. print a log to file. and this
script will recorder the address of variable.

Type enter trigger the event that print the address
you alloc but not freed in this durations.

