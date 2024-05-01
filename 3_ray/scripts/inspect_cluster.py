"""Simple script to print out the resources of a live Ray cluster."""
import ray


def main():
    ray.init()
    resources = ray.cluster_resources()
    print(resources)
    print(" ")
    total_cpus = resources["CPU"]
    total_gpus = resources.get("GPU", 0)
    total_tpu_chips = resources.get("TPU", 0)
    total_memory_gb = resources["memory"] / (1024**3)
    print(f"Total CPUs: {total_cpus}")
    print(f"Total RAM: {total_memory_gb:.0f} GB")
    print(f"Total GPUs: {total_gpus}")
    print(f"Total TPU chips: {total_tpu_chips}")


if __name__ == "__main__":
    main()
