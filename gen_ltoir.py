# Copyright (c) 2023-2024, NVIDIA CORPORATION. All rights reserved.

from numba import cuda, float32


def add(x, y):
    return x + y


ltoir, resty = cuda.compile(add, (float32, float32), cc=(8, 9),
                            abi_info={'abi_name': 'add'}, output='ltoir')

with open('add.ltoir', 'wb') as f:
    f.write(ltoir)


ptx, resty = cuda.compile(add, (float32, float32), cc=(8, 9),
                          abi_info={'abi_name': 'add'}, output='ptx')

with open('add.ptx', 'w') as f:
    f.write(ptx)
