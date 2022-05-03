__author__ = 'dek61'

import os.path


def ipc_dict_loader(file_path):
    total_instructions = 0.0
    total_misses = 0.0
    cycles = 0.0
    ready_for_misses = False
    if not os.path.isfile(file_path):
        return None

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("Instructions"):
                x = line.split("|")
                for y in x[1:]:
                    y = y.strip()
                    total_instructions += float(y)
            elif line.startswith("Cycles"):
                x = line.split("|")
                cycles = float(x[1])
            elif line.startswith("Cache L2"):
                ready_for_misses = True
            elif ready_for_misses and line.startswith("num cache misses"):
                x = line.split("|")
                for y in x[1:]:
                    y = y.strip()
                    total_misses += float(y)

    ipc = float(total_instructions / cycles)

    mpki = float(1000 * total_misses / total_instructions)

    my_dict = {'ipc': ipc, 'mpki': mpki, 'cycles': cycles}
    return my_dict
