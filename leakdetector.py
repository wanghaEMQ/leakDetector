from ipcqueue import posixmq

lq = posixmq.Queue('/leakdetector') # leakage info queue
ms = set() # memory address info set

try:
    while True:
        t = lq.get()
        print(t[0])
        print(t[1])
        if t[1] == 1:
            ms.add(t[0])
        elif t[1] == 0:
            try:
                ms.remove(t[0])
            except KeyError:
                print("Invalid Address [0x%X]: ", end='')
                print("Dangling pointer OR Heap use after free.")
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
            print("0x%X, " %(e), end='')
        print("")
    lq.close()
    lq.unlink()

