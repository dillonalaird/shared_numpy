from distutils.core import setup, Extension

import sys
import platform


linux_module = Extension(
    "shared_numpy/_posixshmem",
    define_macros=[
        ("HAVE_SHM_OPEN", "1"),
        ("HAVE_SHM_UNLINK", "1"),
        ("HAVE_SHM_MMAN_H", 1),
    ],
    libraries=["rt"],
    sources=["shared_numpy/posixshmem.c"],
)


darwin_module = Extension(
    "shared_numpy/_posixshmem",
    define_macros=[
        ("HAVE_SHM_OPEN", "1"),
        ("HAVE_SHM_UNLINK", "1"),
        ("HAVE_SHM_MMAN_H", 1),
    ],
    sources=["shared_numpy/posixshmem.c"],
)


setup(
    name="shared-numpy",
    version="1.1.1",
    description="Shared Numpy",
    py_modules=["shared_numpy"],
    ext_modules=[linux_module]
    if platform.system() == "Linux"
    else [darwin_module]
    if platform.system() == "Darwin"
    else [],
)
