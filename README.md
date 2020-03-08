Shared Numpy
---

This package provides two main items:

1. A light wrapper around numpy arrays and a multiprocessing queue that allows you to
   create numpy arrays with shared memory and efficiently pass them to other processes.
2. A backport of the Python 3.8's shared\_memory module that works for 3.6.


`examples/timing_comparison.py` runs a timing comparison between normal numpy arrays and
shared numpy arrays. You can run the file to see what kind of speeds up you get on your
machine.
```
not shared
total time: 1.3530828952789307
shared
total time: 0.007848024368286133
```


The clinic file posixshmem.c.h is currently built for Python 3.6. In order to build the
shared\_memory module for other version of Python you can generate a new clinic file.
More information on clinic files can be found [here](https://docs.python.org/3/howto/clinic.html)
```
python clinic.py posixshmem.c
```
which generates the clinic file, `clinic/posixshmem.c.h` and then run
```
python setup.py build_ext --inplace
```
to generate the shared object file.


Issues
---

Does not currently work with Python 3.7, stalls when running
`examples/timing_comparison.py`.
