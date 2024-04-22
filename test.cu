// Copyright (c) 2023-2024, NVIDIA CORPORATION. All rights reserved.

extern "C" __device__ float add(float x, float y);

__global__ void add_kernel(float* xs, float *ys)
{
  add(xs[0], ys[0]);
}
