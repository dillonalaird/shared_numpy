import multiprocessing as mp
import shared_numpy as snp
import numpy as np
import time


def f_mp(q):
    for i in range(10):
        frame = np.ndarray((3000, 3000), dtype=np.float32)
        frame[0, 0] = i
        q.put(frame)

    q.put(None)


def f_snp(q):
    for i in range(10):
        frame = snp.ndarray((3000, 3000), dtype=np.float32)
        frame[0, 0] = i
        q.put(frame)
        frame.close()

    q.put(None)


def run(q, f):
    p = mp.Process(target=f, args=(q,))
    p.start()
    out = True
    start = time.time()
    while out is not None:
        out = q.get()
        if out is not None:
            # print(f"obtained array {out[0, 0]}")
            if f.__name__ == "f_snp":
                out.close()
                out.unlink()

    p.join()
    end = time.time()
    total = end - start
    print(f"total time: {total}")


if __name__ == "__main__":
    print("not shared")
    q = mp.Queue()
    run(q, f_mp)
    print("shared")
    q = snp.Queue()
    run(q, f_snp)
