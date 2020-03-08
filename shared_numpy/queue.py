import io
import pickle
import multiprocessing
import multiprocessing.queues

from multiprocessing.reduction import ForkingPickler


class ConnectionWrapper:
    """Proxy class for _multiprocessing.Connection which uses ForkingPickler to
    serialize objects. Based off of torch and mxnet multiprocessing and dataloader

    https://github.com/pytorch/pytorch/blob/master/torch/multiprocessing/queue.py
    https://github.com/apache/incubator-mxnet/blob/master/python/mxnet/gluon/data/dataloader.py
    """

    def __init__(self, conn):
        self.conn = conn

    def send(self, obj):
        buf = io.BytesIO()
        ForkingPickler(buf, pickle.HIGHEST_PROTOCOL).dump(obj)
        self.send_bytes(buf.getvalue())

    def recv(self):
        buf = self.recv_bytes()
        return pickle.loads(buf)

    def __getattr__(self, name):
        if "conn" in self.__dict__:
            return getattr(self.conn, name)
        raise AttributeError("'{}' object has no attribute '{}'".format(
            type(self).__name__, "conn"))


class Queue(multiprocessing.queues.Queue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, ctx=multiprocessing.get_context(), **kwargs)
        self._reader = ConnectionWrapper(self._reader)
        self._writer = ConnectionWrapper(self._writer)
        self._send = self._writer.send
        self._recv = self._reader.recv
