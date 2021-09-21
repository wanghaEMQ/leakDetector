#!/usr/bin/env python3
# @author wangha

import sys
from ipcqueue import posixmq
from ipcqueue.serializers import RawSerializer

if len(sys.argv) > 1 and (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
    print("USAGE. python3 leakdetector [...]")
    print("-h, --help  show this Usage docs.")
    print("\nThis script help you to check if your process has leak.")
    print("Your process should call the malloc/calloc/realloc/free  ")
    print("function we support in liblm.so. So it will send a msg to")
    print("channel and server will receive msg from channel and do  ")
    print("something like statustics. Actually, this channel is a   ")
    print("msg queue provided by kernel.")
    exit(0)

print("Listening to Channal \"/leakdetector\".")
print("Enter Ctrl-c to check leak.")

# leakage info queue
lq = posixmq.Queue('/leakdetector', maxmsgsize=31, serializer=RawSerializer) 
ms = set() # memory address info set

try:
    while True:
        t = lq.get()
        if t[-1] == 49: # malloc/calloc
            ms.add(t[:-2])
        elif t[-1] == 48: # free
            try:
                ms.remove(t[:-2])
            except KeyError:
                print("Invalid Address [", end='')
                print(t[:-2], end='')
                print("]: Dangling pointer OR Heap use after free.")
                lq.close()
                lq.unlink()
                exit(0)
        elif t[-1] == 50: # realloc
            try:
                ms.remove(t[:14])
                ms.add(t[15:29])
            except KeyError:
                print("Invalid Address [", end='')
                print(t[:14], end='')
                print("]: Dangling pointer OR Heap use after free.")
                lq.close()
                lq.unlink()
                exit(0)

        else:
            print("Message Error.")
except KeyboardInterrupt:
    if len(ms) != 0:
        print("Find [%d] Leaks." %(len(ms)))
        while len(ms):
            e = ms.pop()
            print(e, end='')
        print("")
    lq.close()
    lq.unlink()

