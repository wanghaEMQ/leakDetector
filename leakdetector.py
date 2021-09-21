from ipcqueue import posixmq
from ipcqueue.serializers import RawSerializer

# leakage info queue
lq = posixmq.Queue('/leakdetector', maxmsgsize=31, serializer=RawSerializer) 
ms = set() # memory address info set

try:
    while True:
        t = lq.get()
        print(t[-1])
        print(t)
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

