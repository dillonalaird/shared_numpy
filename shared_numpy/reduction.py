from shared_numpy.shared_memory import SharedMemory
from shared_numpy.shared_numpy import SharedNDArray
from multiprocessing.reduction import ForkingPickler


def rebuild_shared_ndarray(shm, shape, dtype):
    shm = SharedMemory(name=shm)
    shm_arr = SharedNDArray(shape, dtype=dtype, buffer=shm.buf)
    shm_arr.set_shm(shm)
    return shm_arr


def reduce_shared_ndarray(arr):
    return rebuild_shared_ndarray, (arr.shm.name, arr.shape, arr.dtype)


def init_reduction():
    ForkingPickler.register(SharedNDArray, reduce_shared_ndarray)
