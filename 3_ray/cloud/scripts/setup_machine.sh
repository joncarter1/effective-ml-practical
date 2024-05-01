#!/bin/bash
# This script runs on the compute node.

# Install miniconda if shell script not present
if [ ! -f ~/miniconda.sh ]; then
    echo "Miniconda not found, downloading..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
fi
if ! command -v conda &>/dev/null; then
    echo "conda not found, installing..."
    bash ~/miniconda.sh -b -p $HOME/miniconda
    eval "$($HOME/miniconda/bin/conda shell.bash hook)" && conda init
fi

# Create base environment
conda install python=3.10.14 -y
pip install "ray[default]"==2.12.0 git+https://github.com/joncarter1/hydra_ray_job_launcher.git

# Assign random three letter code for hostname
node_idx=$(tr -dc a-z </dev/urandom | head -c 3)
# Install relevant environment for the compute node.
if command -v nvidia-smi >/dev/null 2>&1; then
    echo "nvidia-smi is present, installing GPU environment if not already present..."
    conda env list | grep -q 'aims-ray' || conda env create --file ~/envs/environment_gpu.yaml
    sudo hostnamectl set-hostname aims-gpu-${node_idx}
elif [[ -e /dev/accel3 ]]; then # Check for TPU chip (not foolproof, but works for GCP VMs)
    echo "TPU is present, installing TPU environment if not already present..."
    conda env list | grep -q 'aims-ray' || conda env create --file ~/envs/environment_tpu.yaml
    # Install XLA TPU extensions
    conda activate aims-ray
    pip install torch_xla[tpu]~=2.2.0 -f https://storage.googleapis.com/libtpu-releases/index.html
    sudo hostnamectl set-hostname aims-tpu-${node_idx}
else
    echo "Creating CPU environment if not already present."
    conda env list | grep -q 'aims-ray' || conda env create --file ~/envs/environment_cpu.yaml
    sudo hostnamectl set-hostname aims-cpu-${node_idx}
fi