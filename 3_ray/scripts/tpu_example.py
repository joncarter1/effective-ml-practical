"""Simple example to demonstrate PyTorch on TPU.

Source: https://cloud.google.com/tpu/docs/run-calculation-pytorch
"""
import os
import ray
import socket
import sys
import torch

MAX_PARALLEL = 100


def import_xla():
    try:
        import torch_xla
        import torch_xla.core.xla_model as xm

        return xm
    except ImportError:
        raise ImportError("Please install PyTorch XLA to run this script.")


# This function will run remotely on a TPU chip in the cluster.
@ray.remote(resources={"TPU": 4})
def run_tpu():
    # We import PyTorch XLA within the remote function, because it is not
    # available on the CPU head node where the main function runs.
    print("Running calculation on: ", socket.gethostname())
    xm = import_xla()
    dev = xm.xla_device()
    t1 = torch.randn(1000, 1000, device=dev)
    t2 = torch.randn(1000, 1000, device=dev)
    t3 = t1 @ t2
    # print(t3.sum(), t1.device)
    # Return a CPU object back to the (CPU-only) head node.
    # n.b. avoid sending large objects back to the head node.
    return t3.sum().cpu()


# This function runs on the CPU head node.
def main():
    if len(sys.argv) != 2:
        print("Usage: python tpu_example.py <num_tasks>")
        sys.exit(1)
    num_tasks = min(int(sys.argv[1]), MAX_PARALLEL)
    ray.init()
    result_refs = []
    # Execute function on 10 TPU nodes (in parallel if capacity)
    for _ in range(num_tasks):
        result_refs.append(run_tpu.remote())
    # Sum results from each TPU.
    results = sum(ray.get(result_refs))
    print(results)


if __name__ == "__main__":
    main()
