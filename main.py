#!/usr/bin/python

import sys
import subprocess
import time

t_min = 0.2 # second
t_max = 5.0 # second
timeout = 1.0 # second
p = 0.4
verbose = False

def print_v(*args, **kwds):
    if verbose:
        return print(*args, **kwds)

def new_watch(args):
    out = ""
    def check():
        nonlocal out
        try:
            new_out = subprocess.check_output(args, timeout=timeout)
        except subprocess.TimeoutExpired:
            new_out = "run %s timeout"%args
        if new_out != out:
            print(new_out)
            out = new_out
            return True
        return False
    return check

def dyntimer(check, p):
    t_timer = 1.0 # second
    total, positive = 0, 0
    stop = 0
    while True:
        if check():
            positive += 1
        total += 1
        p1 = 1.0*positive/total
        if p1 > p+0.05:
            stop = 1
        elif p1 < p-0.05:
            stop = -1
        else:
            stop = 0

        if total >= 10 and stop != 0:
            if stop > 0 and t_timer > t_min:
                t_timer -= 0.1
            elif t_timer < t_max:
                t_timer += 0.1
            positive = ((total * p) + positive)/2
            if total >= 20:
                total /= 2
                positive /= 2
        print_v("pos,tot=%.2f,%d->%.2f,%d t_timer=%f"%(positive, total, p1, stop, t_timer))
        time.sleep(t_timer)


def watching(args):
    print_v("watching %s -> %.2lf"%(args,p))
    check = new_watch(args)
    dyntimer(check, p)    

def checkargs(fn, args):
    if len(args) == 0:
        print("Usage : %s command_line"%fn)
        sys.exit(1)
    return args

if __name__ == "__main__":
    args = checkargs(sys.argv[0], sys.argv[1:])
    try:
        watching(args)
    except KeyboardInterrupt:
        sys.exit(130)

