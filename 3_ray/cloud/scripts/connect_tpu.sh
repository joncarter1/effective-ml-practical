#!/bin/bash

# This script runs on the local machine.
# It copies install scripts to the compute nodes and executes them remotely over SSH.
# head_node_internal_ip="10.130.0.36"
tpu_name=${1}
head_node_internal_ip=${2}

# Copy install scripts
gcloud compute tpus tpu-vm scp envs/ ${tpu_name}: --recurse
gcloud compute tpus tpu-vm scp cloud/scripts ${tpu_name}: --recurse

# Set-up environment
gcloud compute tpus tpu-vm ssh ${tpu_name} --command "./scripts/setup_machine.sh"

# Start Ray on the TPU, connecting it to the head node.
gcloud compute tpus tpu-vm ssh ${tpu_name} --command "./scripts/start_ray_tpu.sh ${head_node_internal_ip}"