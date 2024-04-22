# Copyright (c) 2023-2024, NVIDIA CORPORATION. All rights reserved.

from ctypes import (byref, c_char_p, c_int, c_size_t, c_void_p, CDLL, POINTER)
import sys

NVFATBIN_SUCCESS = 0
NVFATBIN_ERROR_INTERNAL = 1
NVFATBIN_ERROR_ELF_ARCH_MISMATCH = 2
NVFATBIN_ERROR_ELF_SIZE_MISMATCH = 3
NVFATBIN_ERROR_MISSING_PTX_VERSION = 4
NVFATBIN_ERROR_NULL_POINTER = 5
NVFATBIN_ERROR_COMPRESSION_FAILED = 6
NVFATBIN_ERROR_COMPRESSED_SIZE_EXCEEDED = 7
NVFATBIN_ERROR_UNRECOGNIZED_OPTION = 8
NVFATBIN_ERROR_INVALID_ARCH = 9
NVFATBIN_ERROR_INVALID_NVVM = 10
NVFATBIN_ERROR_EMPTY_INPUT = 11

nvFatbinResult = c_int
nvFatbinHandle = c_void_p

nvfatbin = CDLL('/usr/local/cuda-12.4/targets/x86_64-linux/lib/libnvfatbin.so')

nvfatbin.nvFatbinCreate.argtypes = [POINTER(nvFatbinHandle),
                                    POINTER(c_char_p),
                                    c_size_t]
nvfatbin.nvFatbinCreate.restype = nvFatbinResult

nvfatbin.nvFatbinAddLTOIR.argtypes = [nvFatbinHandle, c_void_p, c_size_t,
                                      c_char_p, c_char_p, c_char_p]
nvfatbin.nvFatbinAddLTOIR.restype = nvFatbinResult

nvfatbin.nvFatbinAddPTX.argtypes = [nvFatbinHandle, c_void_p, c_size_t,
                                    c_char_p, c_char_p, c_char_p]
nvfatbin.nvFatbinAddPTX.restype = nvFatbinResult

nvfatbin.nvFatbinSize.argtypes = [nvFatbinHandle, POINTER(c_size_t)]
nvfatbin.nvFatbinSize.restype = nvFatbinResult

nvfatbin.nvFatbinGet.argtypes = [nvFatbinHandle, c_void_p]
nvfatbin.nvFatbinGet.restype = nvFatbinResult

nvfatbin.nvFatbinDestroy.argtypes = [POINTER(nvFatbinHandle)]
nvfatbin.nvFatbinDestroy.restype = nvFatbinResult


def check(result):
    if result != NVFATBIN_SUCCESS:
        print(f"Error: {result}", file=sys.stderr)
        sys.exit(1)


handle = nvFatbinHandle()


options = []

n_options = len(options)
encoded_options = [opt.encode() for opt in options]
option_pointers = [c_char_p(opt) for opt in encoded_options]
c_options_type = (c_char_p * len(options))
c_options = c_options_type(*option_pointers)


result = nvfatbin.nvFatbinCreate(byref(handle), c_options, n_options)
check(result)

args = b"-ftz=0 -prec_div=1 -prec_sqrt=1 -fmad=1"

with open('add.ltoir', 'rb') as f:
    ltoir = f.read()

result = nvfatbin.nvFatbinAddLTOIR(handle, ltoir, len(ltoir), b"89",
                                   b"add.ltoir", args)
check(result)

with open('add.ptx', 'rb') as f:
    ptx = f.read()

result = nvfatbin.nvFatbinAddPTX(handle, ptx, len(ptx), b"89",
                                 b"add.ptx", args)
check(result)

size = c_size_t()
result = nvfatbin.nvFatbinSize(handle, byref(size))
check(result)

fatbin = b' ' * size.value
result = nvfatbin.nvFatbinGet(handle, fatbin)
check(result)

with open('add.fatbin', 'wb') as f:
    f.write(fatbin)

result = nvfatbin.nvFatbinDestroy(byref(handle))
check(result)
