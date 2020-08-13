#!/usr/bin/python3

import os
import sys
import subprocess
import collections.abc
import json
import glob


def dict_merge(dct, merge_dct):
    """ Recursive dict merge.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for key, value in merge_dct.items():
        if (key in dct and isinstance(dct[key], dict)
                and isinstance(merge_dct[key], collections.abc.Mapping)):
            dict_merge(dct[key], merge_dct[key])
        else:
            dct[key] = merge_dct[key]


if __name__ == '__main__':
    # Remember the dir to get back to in the end
    workdir = os.getcwd()
    # Enter dir with actual script location
    os.chdir(sys.path[0])

    # Directories included into benchmarking suit
    directories = ["docker", "sample"]

    # JSON data, containing all the benchmarking results
    result = {}

    # Run benchmarks for each directory and collect everything into a single JSON
    for directory in directories:
        os.chdir(directory)
        # subprocess.run(["bash", "-x", "run.sh"])
        for bench_result in glob.glob("*benchmark-results.json"):
            with open(bench_result, "r") as file:
                dict_merge(result, json.loads(file.read()))
        os.chdir("..")

    # If running as a Github Action report results into the inital dir
    if os.getenv("CI") == "true":
        os.chdir(os.getenv("GITHUB_WORKSPACE"))

    # Write result into a file
    with open("benchmark-results.json", "w+") as file:
        file.write(json.dumps(result, indent=4, sort_keys=True))
    # Fill Github Action output variable
    abs = os.path.abspath("benchmark-results.json")
    subprocess.run(["echo", f"::set-output name=report::{abs}"])
