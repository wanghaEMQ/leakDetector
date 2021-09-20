# leakDetect

A simple tool to check memery leak.

## Requires

+ ipcqueue

Install requires by command as follows.

```
pip3 install ipcqueue
```

## Usage

```
python3 leakdetector.py
```

## How it works?

Using liblm we provide. When you call malloc or free function,
it will send a msg to channel("/leakdetector"). Actually, this
channel is posix msg queue provided by kernel.

A server will receive msgs from the channel, do something like
statistics.

