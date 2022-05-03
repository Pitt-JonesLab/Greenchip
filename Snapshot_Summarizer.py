#Imports
import os

from plugins.shared.Utils import OurConstants


def summarize_snapshot(summarizing_directory):

    with open(OurConstants.get_path_to_output_dir() + "snapshot_summary.csv", 'w') as sum_handle:
        sum_handle.write("Tag,Average_Break_Even,Special_Case\n")
    for fn in os.listdir(summarizing_directory):
        print("Currently on file "+fn)
        sum_map = dict()
        num_map = dict()
        asterisc_map = dict()
        if fn.lower().endswith('.csv'):
            with open(summarizing_directory + "/" + fn, 'r') as handle:
                for line in handle:
                    line_list = line.split(',')
                    cache_size = line_list[0].split(':')[1]
                    value = float(line_list[1])
                    if cache_size in sum_map:
                        if sum_map[cache_size] < 0 or value < 0:
                            if sum_map[cache_size] > 0 or value > 0:
                                asterisc_map[cache_size] = "*"
                            sum_map[cache_size] = -42
                        else:
                            sum_map[cache_size] += value
                        num_map[cache_size] += 1
                    else:
                        sum_map[cache_size] = value
                        num_map[cache_size] = 1
            if len(sum_map) > 0:
                with open(OurConstants.get_path_to_output_dir() + "snapshot_summary.csv", 'a') as summary_handle:
                    for key in sum_map:
                        name_output = fn[:-4] + ":" + key
                        if sum_map[key] == -42:
                            value_output = -42
                        else:
                            value_output = float(sum_map[key]) / float(num_map[key])
                        if key in asterisc_map:
                            summary_handle.write(name_output + "," + str(value_output) + ",*\n")
                        else:
                            summary_handle.write(name_output + "," + str(value_output) + "\n")

if __name__ == "__main__":

    summarize_snapshot(OurConstants.get_path_to_output_dir()+"Snapshots")







