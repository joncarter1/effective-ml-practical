import ray
import sys
import time

MAX_PARALLEL = 100


@ray.remote
def my_slow_func():
    """Some slow function e.g. pre-processing a file in our dataset."""
    time.sleep(5)
    return 1


def main():
    if len(sys.argv) != 2:
        print("Usage: python cpu_example.py <num_tasks>")
        sys.exit(1)
    num_tasks = min(int(sys.argv[1]), MAX_PARALLEL)
    ray.init()
    result_refs = []  # References to remote results.
    # Launch 10 tasks in parallel.
    for _ in range(num_tasks):
        result_refs.append(my_slow_func.remote())
    # Block until all tasks have completed.
    result = ray.get(result_refs)
    print(result)


if __name__ == "__main__":
    main()
