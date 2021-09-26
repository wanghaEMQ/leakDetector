from ipcqueue import posixmq
from ipcqueue.serializers import RawSerializer

lq = posixmq.Queue('/leakdetector', serializer=RawSerializer) 

lq.put(bytes('0x2342,1', 'ascii'))
lq.put(bytes('0x2343,1', 'ascii'))
lq.put(bytes('0x2344,1', 'ascii'))

lq.put(bytes('0x2342,0', 'ascii'))
lq.put(bytes('0x2344,0', 'ascii'))

