Shared Numpy
---

This package provides two main items:

1. A light wrapper around numpy arrays and a multiprocessing queue that allows you to
   create numpy arrays with shared memory and efficiently pass them to other processes.
2. A backport of the Python 3.8's shared\_memory module that works for 3.6 and 3.7.


`examples/timing_comparison.py` runs a timing comparison between normal numpy arrays and
shared numpy arrays. You can run the file to see what kind of speeds up you get on your
machine.
```
not shared
total time: 1.3530828952789307
shared
total time: 0.007848024368286133
```

Install
---

To install run `python setup.py build_ext --inplace`.

Clinic
---

The clinic file (that gets generated under `shared_numpy/clinic/posixshmem.c.h`) is a
generated file that gets automatically created when running `setup.py`. You can manually
generate a clinic file for Python 3.6 by running
`python shared_numpy/py36_clinic.py shared_numpy/posixshmem.c`
and one for Python 3.7 by using `py37_clinic.py` instead. More information on clinic
files can be found [here](https://docs.python.org/3/howto/clinic.html)
