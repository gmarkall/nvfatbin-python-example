# nvFatbin Python example

This generates PTX and LTOIR for an add function, and creates a fatbin
containing them both.

A kernel that calls the function in PTX / LTOIR is also created.

Linking them all together with nvjitlink and launching the kernel (e.g. with
`cuda-python`) is for future work.

Numba 0.60rc1 will be required to run this example (not yet available).

Usage in current state:

```
python gen_ltoir.py
python get_fatbin.py
make
```

This should create `add.ltoir`, `add.ptx`, `add.fatbin`, and `test.o`.
