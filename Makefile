# Copyright (c) 2023-2024, NVIDIA CORPORATION. All rights reserved.

all:
	nvcc -gencode arch=compute_89,code=lto_89 -rdc true -dc test.cu
