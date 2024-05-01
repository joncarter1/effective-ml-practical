#!/bin/bash
# This script runs on the compute node.

# Get head node IP from script passed as argument.
head_node_ip=${1}

# Make sure TPU device is used by XLA library.
export PJRT_DEVICE=TPU

# Initialize Conda
echo "Initializing Conda..."
eval "$($HOME/miniconda/bin/conda shell.bash hook)" && conda init

# Connect the TPU to the Ray cluster head node.
echo "Restarting Ray on TPU..."
ray stop
ray start --address ${head_node_ip}:6379