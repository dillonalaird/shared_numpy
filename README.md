Shared Numpy
---

This package provides two main items:

1. A light wrapper around numpy arrays and a multiprocessing queue that allows you to
   create numpy arrays with shared memory and efficiently pass them to other processes.
2. A backport of the Python 3.8's shared\_memory module that works for 3.6 and 3.7.


Install
---

To install run `python setup.py build_ext --inplace`.


Examples
---

`shared_numpy` is written as a wrapper around `numpy` so you can use it like any numpy
array. In the example below we create 10 shared numpy arrays using `snp.array(...)` and
add them to a queue. 


```python
imoprt shared_numpy as snp

def f(q):
    for i in range(10):
        a = snp.array([1, 2, 3, 4, 5])
        q.put(a)
        a.close()
    q.put(None)
```

Below we create a shared numpy queue using `snp.Queue()` and pass it to the child
process. Notice we have to call `.close()` in each process when we are done with the
array and finally `.unlink()` when we want to free the shared memory. This is the same
interace as the [shared\_memory](https://docs.python.org/3/library/multiprocessing.shared_memory.html)
module.

```python
import multiprocessing as mp

q = snp.Queue()
p = mp.Process(target=f, args=(q,))
p.start()
while True:
    out = q.get()
    if out is None: break
    out.close()
    out.unlink()
p.join()
```

In addtion to `snp.array()` you can also use `snp.ndarray()`, the same as `np.ndarray()`
or `snp.from_array()` to copy from an existing array.

```python
a = np.zeros((10, 10))
b = snp.from_array(a)
```

You can also access `snp.SharedMemory` and `snp.ShareableList` which are the same as the
ones in Python 3.8's [shared\_memory](https://docs.python.org/3/library/multiprocessing.shared_memory.html)
module.

Timing
---

`examples/timing_comparison.py` runs a timing comparison between normal numpy arrays and
shared numpy arrays. You can run the file to see what kind of speeds up you get on your
machine.
```
not shared
total time: 1.3530828952789307
shared
total time: 0.007848024368286133
```

Clinic
---

The clinic file (that gets generated under `shared_numpy/clinic/posixshmem.c.h`) is a
generated file that gets automatically created when running `setup.py`. You can manually
generate a clinic file for Python 3.6 by running
`python shared_numpy/py36_clinic.py shared_numpy/posixshmem.c`
and one for Python 3.7 by using `py37_clinic.py` instead. More information on clinic
files can be found [here](https://docs.python.org/3/howto/clinic.html)
