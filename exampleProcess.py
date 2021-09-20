from ipcqueue import posixmq

lq = posixmq.Queue('/leakdetector')

lq.put([0x2342, 1])
lq.put([0x2343, 1])
lq.put([0x2344, 1])

lq.put([0x2342, 0])
lq.put([0x2344, 0])

