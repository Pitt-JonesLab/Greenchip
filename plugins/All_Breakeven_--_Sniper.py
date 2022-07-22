from plugins.shared.Utils import *
from plugins.shared.GreenChip import *

global_cycle_time = 0.000000000375

class config(object):

    def __init__(self, root, DB, outdir):
        self.DB = DB
        self.root = root
        self.path_to_output_directory = outdir
        self.window = Toplevel(self.root)
        self.window.geometry("500x100+0+0")
        self.launch_config()

    @staticmethod
    def needs_DB():
        return True

    def plot(self, *args):

        first_entry = utils.build_config(self.DB, self.entry1.get(), self.path_to_output_directory, writeMe=False, configNum=3)
        if first_entry is None:
            return
        second_entry = utils.build_config(self.DB, self.entry2.get(), self.path_to_output_directory, writeMe=False, configNum=3)
        if second_entry is None:
            return
        config_dicts = []
        config_dicts.append(first_entry)
        config_dicts.append(second_entry)
        res = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
        utils.make_plot(first_entry, second_entry, self.entry1, self.entry2, res, "Breakeven Plot Energy", self.path_to_output_directory)

    def launch_config(self):
        self.entries = self.DB.list_entries()

        with open(self.path_to_output_directory+"Power.csv", "w") as power_file:
            power_file.write(",Static_Dram,Static_Processor,Dynamic_Dram,Dynamic_Processor\n")

        with open(self.path_to_output_directory+"Energy.csv", "w") as energy_file:
            energy_file.write(",Static_Dram,Static_Processor,Dynamic_Dram,Dynamic_Processor\n")

        with open(self.path_to_output_directory + "Manufacturing.csv", "w") as man_file:
            man_file.write(",Manufacturing Energy,Chip Area\n")

        x_count = 0
        for x_str in self.entries:
            x = x_str.split(",")
            if len(x) < 4:
                x_count += 1
                continue

            y_count = 0
            valid = True
            for x_elem in x:
                if x_elem.startswith("template"):
                    valid = False
                    break
            if not valid:
                x_count += 1
                continue

            for y_str in self.entries:
                y = y_str.split(",")
                if y_count == x_count:
                    y_count += 1
                    continue

                valid = True
                for y_elem in y:
                    if y_elem.startswith("template"):
                        valid = False
                        break
                if not valid:
                    y_count += 1
                    continue

                if len(x) is not len(y):
                    y_count += 1
                    continue

                num_different = 0
                for num in range(0, len(x)):
                    if x[num] != y[num]:
                        num_different += 1
                        if num == len(x)-1: #No Point in comparing different benchmarks
                            num_different += 10
                        elif num == 1:  # No point in comparing non-adjacent generations
                            care_generations = utils.is_adjacent_generation(x[num], y[num])
                            if not care_generations:
                                num_different += 5
                        elif num == 2:
                            care_cachesizes = utils.is_adjacent_cachesize(x[num], y[num])
                            if not care_cachesizes:
                                num_different += 20

                if num_different > 1:
                    y_count += 1
                    continue
                print("X", x_count, x)
                print("Y", y_count, y)
                self.entry1 = x_str
                self.entry2 = y_str
                self.plot()

                y_count += 1
            x_count += 1
        print('done')
