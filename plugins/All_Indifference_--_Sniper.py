from plugins.shared.Utils import *
from plugins.shared.GreenChip import *
import tkinter.messagebox


class config(object):

    def __init__(self, root, DB, outdir, increment, mindays, maxdays, minyears, maxyears, gridMixSettingsFilename):
        self.DB = DB
        self.root = root
        self.path_to_output_directory = outdir
        self.increment = increment
        self.mindays = mindays
        self.maxdays = maxdays
        self.minyears = minyears
        self.maxyears = maxyears
        #self.window = Toplevel(self.root)
        #self.window.geometry("500x100+0+0")
        self.energyData=[]
        filename=os.path.normpath(gridMixSettingsFilename)
        with open(filename, 'r') as file:
            reader=csv.reader(file)
            for row in reader:
               if row[0]!='Country': self.energyData.append(row)
        self.launch_config()

    @staticmethod
    def needs_DB():
        return True

    def plot(self, *args):

        first_entry = utils.build_config(self.DB, self.entry1, self.path_to_output_directory, writeMe=True, configNum=3, carbonFile=self.varC.get(), useDRAM = self.varD.get(), energyData = self.energyData)
        if first_entry is None:
            return
        second_entry = utils.build_config(self.DB, self.entry2, self.path_to_output_directory, writeMe=True, configNum=3, carbonFile=self.varC.get(), useDRAM = self.varD.get(), energyData = self.energyData)
        if second_entry is None:
            return
        config_dicts = []
        config_dicts.append(first_entry)
        config_dicts.append(second_entry)        
        if self.varE.get():
            res = chip_breakeven_IPC(config_dicts, False, self.increment)['chipVsChipBreakevenInDays']
            utils.make_plot(first_entry, second_entry, self.entry1, self.entry2, res, "Indifference Plot Energy", self.path_to_output_directory, self.increment, self.mindays, self.maxdays, self.minyears, self.maxyears)
        if self.varC.get():
            res = chip_breakeven_IPC(config_dicts, True, self.increment)['chipVsChipBreakevenInDays']
            utils.make_plot(first_entry, second_entry, self.entry1, self.entry2, res, "Indifference Plot Carbon", self.path_to_output_directory, self.increment, self.mindays, self.maxdays, self.minyears, self.maxyears)

    def window_exit(self):
        self.isOpen = False
        self.window.destroy()

    def launch_config(self):
				
        self.window = Toplevel(self.root)
        self.window.geometry("280x70")
        self.window.title("All Indifference")
        self.window.protocol("WM_DELETE_WINDOW", self.window_exit)
        self.isOpen = True

        self.varC = IntVar()
        self.varD = IntVar()
        self.varE = IntVar()

        def generator():
            self.entries = self.DB.list_entries()
            
            entryset1 = set()
            entryset2 = set()
            entryset3 = set()
            entryset4 = set()
            
            for e in self.entries:
                entries_list = e.split(',')
                if entries_list[0] not in entryset1:
                    entryset1.add(entries_list[0])
                if entries_list[1] not in entryset2:
                    entryset2.add(entries_list[1])
                if entries_list[2] not in entryset3:
                    entryset3.add(entries_list[2])
                if entries_list[3] not in entryset4:
                    entryset4.add(entries_list[3])
            
            sizeList = [len(entryset1), len(entryset2), len(entryset3), len(entryset4)]
            
            E = 0.0
            S = 0
            for i,k in enumerate(sizeList):
                if i!=3 and k!=1:
                    E += 2/k
                    S += 1
            
            Total = (2*S - E)/2
            for k in sizeList:
                Total *= k
            
            self.window.destroy()
            self.isOpen = False
            
            messagebox.showinfo(title="Info", message='To begin the process, click "OK". Progress will be shown in the console.', icon = 'info')

            with open(self.path_to_output_directory+"Power.csv", "w") as power_file:
                power_file.write(",Static_Dram (W),Static_Processor (W),Dynamic_Dram (W),Dynamic_Processor (W)\n")

            if self.varC.get():
                with open(self.path_to_output_directory+"CarbonRate.csv", "w") as carbonr_file:
                    carbonr_file.write(",Static_Dram (gCO2eq/h),Static_Processor (gCO2eq/h),Dynamic_Dram (gCO2eq/h),Dynamic_Processor (gCO2eq/h)\n")

            with open(self.path_to_output_directory+"Energy.csv", "w") as energy_file:
                energy_file.write(",Static_Dram (J),Static_Processor (J),Dynamic_Dram (J),Dynamic_Processor (J)\n")

            if self.varC.get():
                with open(self.path_to_output_directory+"Carbon.csv", "w") as carbon_file:
                    carbon_file.write(",Static_Dram (gCO2eq),Static_Processor (gCO2eq),Dynamic_Dram (gCO2eq),Dynamic_Processor (gCO2eq)\n")

            if self.varC.get():
                with open(self.path_to_output_directory + "Manufacturing.csv", "w") as man_file:
                    man_file.write(",DRAM Manufacturing Energy (J), Processor Manufacturing Energy (J), DRAM Manufacturing Carbon (gCO2eq), Processor Manufacturing Carbon (gCO2eq), DRAM Chip Area (mm^2), Processor Chip Area (mm^2)\n")
            else:
                with open(self.path_to_output_directory + "Manufacturing.csv", "w") as man_file:
                    man_file.write(",DRAM Manufacturing Energy (J), Processor Manufacturing Energy (J), DRAM Chip Area (mm^2), Processor Chip Area (mm^2)\n")

            x_count = 0
            progress = 0.0
            print("Progress: " + "{:.1f}".format(progress) + "%\r", end='')
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
                    if y_count <= x_count:
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
                            if num == len(x)-1:  # No Point in comparing different benchmarks
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
                    #print("X", x_count, x)
                    #print("Y", y_count, y)
                                        
                    self.entry1 = x_str
                    self.entry2 = y_str
                    self.plot()

                    progress += 100/Total
                    print("Progress: " + "{:.1f}".format(progress) + "%\r", end='')                    

                    y_count += 1
                x_count += 1
            print('\ndone')
        
        def energyChecker():            
            if self.varE.get()==0 and self.varC.get()==0:
                messagebox.showerror(title = "No Output", message = "Please enable at least one output method.", icon = "error")
                self.varE.set(1)

        def carbonChecker():            
            if self.varE.get()==0 and self.varC.get()==0:
                messagebox.showerror(title = "No Output", message = "Please enable at least one output method.", icon = "error")
                self.varC.set(1)


        self.varE.set(1)
        self.varD.set(1)
        self.varC.set(1)
        self.ECheck = ttk.Checkbutton(self.window, text="Generate Energy Plots", variable=self.varE, onvalue=1, offvalue=0, command=energyChecker)
        self.CCheck = ttk.Checkbutton(self.window, text="Generate Carbon Plots", variable=self.varC, onvalue=1, offvalue=0, command=carbonChecker)
        self.DCheck = ttk.Checkbutton(self.window, text="Use DRAM values in calculations", variable=self.varD, onvalue=1, offvalue=0)
        self.Start_Button = ttk.Button(self.window, text="Start!", command=generator)


        self.ECheck.grid(row = 0, column = 0, sticky = (N, W, E, S), padx=(0,7))
        self.CCheck.grid(row = 1, column = 0, sticky = (N, W, E, S), padx=(0,7))
        self.DCheck.grid(row = 2, column = 0, sticky = (N, W, E, S), padx=(0,7))
        self.Start_Button.grid(row = 0, column = 1, rowspan = 3, columnspan = 2, sticky = (N, W, E, S))
