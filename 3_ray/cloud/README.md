# Cloud set-up

This folder documents the configuration and scripts used to provision the cloud cluster used in the practical.

## Initial Cluster Set-up

To start up the initial cluster, I've run:
```bash
envsubst < cluster_template.yaml > cluster.yaml
ray up -y cloud/cluster.yaml
```
where `envsubst` populates values such as `SSH_KEY` in the template file.

This command achieves the following:
- `rsyncs` the local `envs` and `cloud` folders to the cluster nodes to install the dependencies.
- Runs the `scripts/setup_machine.sh` script in this folder which installs `miniconda`, Python, Ray and other useful numerical computing libraries. n.b. exact pins on Python and Ray are required for the cluster to function correctly.
- Starts Ray on the compute nodes. This connects the nodes together to form the Ray cluster and starts up the dashboard, reachable on port 8265 at the head node IP address.

## Adding TPUs
The CPU and GPU compute nodes used in this practical are automatically managed by Ray. However, the TPUs are added manually to the cluster. It is possible to have Ray automatically configure them within the `cluster.yaml` file, but their availability is very patchy, presumably because Google is using them to train Gemini 2.0...

Instead, I made a queued TPU request scheduled for the morning of the practical several weeks ago:
```bash
gcloud alpha compute tpus queued-resources create aims-tpu-v4-$X --node-id aims-tpu-v4-$X --zone=us-central2-b --accelerator-type=v4-8 --runtime-version=tpu-ubuntu2204-base --valid-after-time 2024-05-02T07:00:00Z --valid-until-time 2024-05-02T20:00:00Z
```
for `$X` in {0, ..., 9}.

I've then run `./cloud/connect_tpu.sh aims-tpu-v4-$X HEAD_NODE_IP` for each node.

## Virtual Private Cloud
Adding a firewall to only allow connections from the VPN IP range was very straightforward in Google Cloud console. The Oxford University VPN IP range is publicly listed at: https://help.it.ox.ac.uk/vpn-help

All nodes within the cluster can freely communicate, but external access has to originate from the VPN IP range, and can only access the Ray cluster dashboard at port 8265.

![img](https://cloud.google.com/static/vpc/images/vpc-overview-example.svg)
(Source: https://cloud.google.com/vpc/docs/overview)