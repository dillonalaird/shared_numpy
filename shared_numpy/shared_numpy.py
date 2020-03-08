from shared_numpy.shared_memory import SharedMemory
import numpy as np


class SharedNDArray(np.ndarray):
    def set_shm(self, shm):
        self.shm = shm

    def close(self):
        self.shm.close()

    def unlink(self):
        self.shm.unlink()


def from_array(arr):
    shm = SharedMemory(create=True, size=arr.nbytes)
    shm_arr = SharedNDArray(arr.shape, dtype=arr.dtype, buffer=shm.buf)
    shm_arr[:] = arr[:]
    shm_arr.set_shm(shm)
    return shm_arr


def ndarray(obj, *args, **kwargs):
    # TODO: find way to calculate bytes without creating object. Should be something
    # like np.dtype(<dtype>).itemsize * <size>
    nbytes = np.ndarray(obj, *args, **kwargs).nbytes
    shm = SharedMemory(create=True, size=nbytes)
    shm_arr = SharedNDArray(obj, *args, buffer=shm.buf, **kwargs)
    shm_arr.set_shm(shm)
    return shm_arr


def array(obj, *args, **kwargs):
    # TODO: find out way to do this without creating extra array.
    arr = np.array(obj, *args, **kwargs)
    shm = SharedMemory(create=True, size=arr.nbytes)
    nkwargs = {}
    if "offset" in kwargs:
        nkwargs["offset"] = kwargs["offset"]
    if "order" in kwargs:
        nkwargs["order"] = kwargs["order"]
    shm_arr = SharedNDArray(
        arr.shape,
        dtype=arr.dtype,
        buffer=shm.buf,
        strides=arr.strides,
        **nkwargs)
    shm_arr[:] = arr[:]
    shm_arr.set_shm(shm)
    return shm_arr
