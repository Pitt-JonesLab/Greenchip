__author__ = 'Donald Kline, Jr'

from plugins.shared.Utils import *
from plugins.shared.GreenChip import *
import plugins.shared.Config as settingsConfig
#import SimVis
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from idlelib.tooltip import Hovertip


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
        return False

    def verify_input(self, *args):
        config1 = {}
        config2 = {}

        try:
            config1['chipArea'] = float(self.chipArea1.get())
            config2['chipArea'] = float(self.chipArea2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Chip Area!")
            return None, None

        try:
            config1['dynamicPower'] = float(self.dynPower1.get())
            config2['dynamicPower'] = float(self.dynPower2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Dynamic Power!")
            return None, None

        try:
            config1['staticPower'] = float(self.staticPower1.get())
            config2['staticPower'] = float(self.staticPower2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Static Power!")
            return None, None

        try:
            config1['dynamicMemory'] = float(self.dynMemPower1.get())
            config2['dynamicMemory'] = float(self.dynMemPower2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Memory Dynamic Power!")
            return None, None

        try:
            config1['staticMemory'] = float(self.staticMemPower1.get())
            config2['staticMemory'] = float(self.staticMemPower2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Memory Static Power!")
            return None, None

        try:
            config1['IPC'] = float(self.ipc1.get())
            config2['IPC'] = float(self.ipc2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid IPC!")
            return None, None

        #try:
        #    config1['cycles'] = int(self.cycles1.get())
        #    config2['cycles'] = int(self.cycles2.get())
        #except (ValueError):
        #    messagebox.showinfo("Warning: Illegal Argument", "Invalid Cycles!")
        #    return

        config1['layers'] = int(1)
        config2['layers'] = int(1)

        try:
            config1['processSize'] = int(self.techNode1.get())
            config2['processSize'] = int(self.techNode2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Technology Node!")
            return None, None

        return config1, config2

    def plot_indifference(self,*args):
        config1, config2 = self.verify_input(*args)
        if config1 is None:
            return
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        res = chip_breakeven_IPC(config_dicts)['chipVsChipBreakevenInDays']
        utils.make_single_plot(self, config1, config2, self.title1.get(), self.title2.get(), res)



    def plot_breakeven(self, *args):
        config1, config2 = self.verify_input(*args)
        if config1 is None:
            return
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        res = chip_breakeven_IPC(config_dicts)['upgradeDays']
        utils.make_single_plot(self, config1, config2, self.title1.get(), self.title2.get(), res)

    def plot_breakeven_colors(self, *args):
        config1, config2 = self.verify_input(*args)
        if config1 is None:
            return
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        res = chip_breakeven_IPC(config_dicts)['upgradeDays']
        utils.make_single_plot_colors(self, config1, config2, self.title1.get(), self.title2.get(), res)
        
    def export_indifference(self, *args):

        config1, config2 = self.verify_input()
        if config1 is None:
            return
        breakeven_export_name = filedialog.asksaveasfilename(defaultextension=".csv")
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        res = chip_breakeven_IPC(config_dicts)['chipVsChipBreakevenInDays']

        arr = utils.perform_greenchip_analysis(res)
        print(arr[3][4])
        with open(breakeven_export_name, "w") as indiff_writer:
            indiff_writer.write("GreenChip SimVis Tool Version " + str(settingsConfig.version) + " Output\n-\n")

            indiff_writer.write("Input Parameters:\n")
            indiff_writer.write("Category, System1, System2\n")
            indiff_writer.write("Chip Area (mm^2),"+str(config1['chipArea'])+","+str(config2['chipArea'])+"\n")
            indiff_writer.write("Dyn. Power (Processor+Caches)(W)," +
                                str(config1['dynamicPower'])+","+str(config2['dynamicPower'])+"\n")
            indiff_writer.write("Static Power (Processor+Caches)(W)," +
                                str(config1['staticPower'])+","+str(config2['staticPower'])+"\n")
            indiff_writer.write("Dyn. Memory Power (W)," +
                                str(config1['dynamicMemory'])+","+str(config2['dynamicMemory'])+"\n")
            indiff_writer.write("Static Memory Power (W)," +
                                str(config1['staticMemory'])+","+str(config2['staticMemory'])+"\n")
            indiff_writer.write("Instructions-Per-Cycle,"+str(config1['IPC'])+","+str(config2['IPC'])+"\n")
            indiff_writer.write("Technology Node (nm),"+str(config1['processSize'])+","+str(config2['processSize'])+"\n")

            indiff_writer.write("-\nIndifference Time (Days):\n")
            indiff_writer.write("Note: Infinite indifference times are represented with the value '-42': \n\n")
            indiff_writer.write("Active Percent, Sleep Percent, Indifference Days\n")

            for a in range(0, len(arr)):
                for b in range(0, len(arr[0])):
                    indiff_writer.write(str(a)+","+str(b)+","+str(arr[a][b])+"\n")


    def export_breakeven(self, *args):

        config1, config2 = self.verify_input()
        if config1 is None:
            return
        breakeven_export_name = filedialog.asksaveasfilename(defaultextension=".csv")
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        res = chip_breakeven_IPC(config_dicts)['upgradeDays']

        arr = utils.perform_greenchip_analysis(res)
        with open(breakeven_export_name, "w") as indiff_writer:
            indiff_writer.write("GreenChip SimVis Tool Version " + str(settingsConfig.version) + " Output\n-\n")

            indiff_writer.write("Input Parameters:\n")
            indiff_writer.write("Category, System1, System2\n")
            indiff_writer.write("Chip Area (mm^2),"+str(config1['chipArea'])+","+str(config2['chipArea'])+"\n")
            indiff_writer.write("Dyn. Power (Processor+Caches)(W)," +
                                str(config1['dynamicPower'])+","+str(config2['dynamicPower'])+"\n")
            indiff_writer.write("Static Power (Processor+Caches)(W)," +
                                str(config1['staticPower'])+","+str(config2['staticPower'])+"\n")
            indiff_writer.write("Dyn. Memory Power (W)," +
                                str(config1['dynamicMemory'])+","+str(config2['dynamicMemory'])+"\n")
            indiff_writer.write("Static Memory Power (W)," +
                                str(config1['staticMemory'])+","+str(config2['staticMemory'])+"\n")
            indiff_writer.write("Instructions-Per-Cycle,"+str(config1['IPC'])+","+str(config2['IPC'])+"\n")
            indiff_writer.write("Technology Node (nm),"+str(config1['processSize'])+","+str(config2['processSize'])+"\n")

            indiff_writer.write("-\nBreakeven Time (Days): \n")
            indiff_writer.write("Active Percent, Sleep Percent, Breakeven Days\n")
            for a in range(0, len(arr)):
                for b in range(0, len(arr[0])):
                    indiff_writer.write(str(a)+","+str(b)+","+str(arr[a][b])+"\n")
                    

    def average_gradient(self, Radius, Sleep, Activity, Orig, Mod):
        numofpoints = 0
        totaldifference = 0
        for x in range(Sleep - Radius, Sleep + Radius + 1):
            for y in range(Activity - Radius, Activity + Radius + 1):
                if ((x + y)<=Radius + Activity + Sleep and (x + y)>=Radius + Activity + Sleep ):
                    numofpoints = numofpoints + 1
                    totaldifference = totaldifference + Orig[x][y] - Mod[x][y]
        averagedifference = totaldifference/numofpoints           
        return averagedifference       

    def total_gradient(self, Orig, Mod):
        numofpoints = 0
        totaldifference = 0
        for x in range(0,100):
            for y in range(0,100):
                if (Orig[x][y]>0):
                    numofpoints = numofpoints + 1
                    totaldifference = totaldifference + Orig[x][y] - Mod[x][y]
        averagedifference = totaldifference/numofpoints           
        return averagedifference      

    def total_average(self, Orig):
        numofpoints = 0
        total = 0
        for x in range(0,100):
            for y in range(0,100):
                if (Orig[x][y]>0):
                    numofpoints = numofpoints + 1
                    total = total + Orig[x][y]
        average = total/numofpoints           
        return average 

    def partial_average(self, Radius, Sleep, Activity, Orig):
        numofpoints = 0
        total = 0
        for x in range(Sleep - Radius, Sleep + Radius + 1):
            for y in range(Activity - Radius, Activity + Radius + 1):
                if ((x + y)<=Radius + Activity + Sleep and (x + y)>=Radius + Activity + Sleep ):
                    numofpoints = numofpoints + 1
                    total = total + Orig[x][y]
        average = total/numofpoints           
        return average    

    def total_analysis(self, *args):
        config1, config2 = self.verify_input(*args)
        if config1 is None:
            return
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)

        difference = [0,0,0,0,0]
        original = chip_breakeven_IPC(config_dicts)['upgradeDays']
        old = config2['chipArea']
        config2['chipArea'] = config2['chipArea'] - (.01 * config2['chipArea'])
        mod = chip_breakeven_IPC(config_dicts)['upgradeDays']
        difference[0] = self.total_gradient(original, mod)
        config2['chipArea'] = old

        old = config2['dynamicPower']
        config2['dynamicPower'] = config2['dynamicPower'] - (.01 * config2['dynamicPower'])
        mod = chip_breakeven_IPC(config_dicts)['upgradeDays']
        difference[1] = self.total_gradient(original, mod)
        config2['dynamicPower'] = old

        old = config2['staticPower']
        config2['staticPower'] = config2['staticPower'] - (.01 * config2['staticPower'])
        mod = chip_breakeven_IPC(config_dicts)['upgradeDays']
        difference[2] = self.total_gradient(original, mod)
        config2['staticPower'] = old

        old = config2['dynamicMemory']
        config2['dynamicMemory'] = config2['dynamicMemory'] - (.01 * config2['dynamicMemory'])
        mod = chip_breakeven_IPC(config_dicts)['upgradeDays']
        difference[3] = self.total_gradient(original, mod)
        config2['dynamicMemory'] = old
        
        old = config2['staticMemory']
        config2['staticMemory'] = config2['staticMemory'] - (.01 * config2['staticMemory'])
        mod = chip_breakeven_IPC(config_dicts)['upgradeDays']
        difference[4] = self.total_gradient(original, mod)
        config2['staticMemory'] = old
        
        total = difference[0] + difference[1] + difference[2] + difference[3] + difference[4]
        difference[0] = 100 * difference[0]/total
        difference[1] = 100 * difference[1]/total
        difference[2] = 100 * difference[2]/total
        difference[3] = 100 * difference[3]/total
        difference[4] = 100 * difference[4]/total

        messagebox.showinfo("Importance", "Chip Area: " + str(round(difference[0],2)) + "%\nDynamic Power(Processor + Cache): "
            + str(round(difference[1],2)) + "%\nStatic Power(Processor + Cache): " + str(round(difference[2],2)) + "%\nDynamic Power(Memory): "
            + str(round(difference[3],2)) + "%\nStatic Power(Memory): " + str(round(difference[4],2)) + "%")         
            

    def average_analysis(self, *args):
        config1, config2 = self.verify_input(*args)
        if config1 is None:
            return
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        Sleep = int(simpledialog.askstring("Sleep","Please enter the Center Sleep Ratio:"))
        Activity = int(simpledialog.askstring("Activity","Please enter the Center Activity Ratio:"))
        Radius = int(simpledialog.askstring("Radius","Please enter the Average Radius:"))
        if ((Radius > Sleep) or (Radius > Activity) or (Radius + Activity >= 100) or (Radius + Sleep >= 100)):
            messagebox.showinfo("Error", "Radius results in out of bounds points.")
            return
        difference = [0,0,0,0,0]
        original = chip_breakeven_IPC(config_dicts)['upgradeDays']
        old = config2['chipArea']
        config2['chipArea'] = config2['chipArea'] - (.01 * config2['chipArea'])
        mod = chip_breakeven_IPC(config_dicts)['upgradeDays']
        difference[0] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['chipArea'] = old

        old = config2['dynamicPower']
        config2['dynamicPower'] = config2['dynamicPower'] - (.01 * config2['dynamicPower'])
        mod = chip_breakeven_IPC(config_dicts)['upgradeDays']
        difference[1] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['dynamicPower'] = old

        old = config2['staticPower']
        config2['staticPower'] = config2['staticPower'] - (.01 * config2['staticPower'])
        mod = chip_breakeven_IPC(config_dicts)['upgradeDays']
        difference[2] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['staticPower'] = old

        old = config2['dynamicMemory']
        config2['dynamicMemory'] = config2['dynamicMemory'] - (.01 * config2['dynamicMemory'])
        mod = chip_breakeven_IPC(config_dicts)['upgradeDays']
        difference[3] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['dynamicMemory'] = old
        
        old = config2['staticMemory']
        config2['staticMemory'] = config2['staticMemory'] - (.01 * config2['staticMemory'])
        mod = chip_breakeven_IPC(config_dicts)['upgradeDays']
        difference[4] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['staticMemory'] = old
        
        total = difference[0] + difference[1] + difference[2] + difference[3] + difference[4]
        difference[0] = 100 * difference[0]/total
        difference[1] = 100 * difference[1]/total
        difference[2] = 100 * difference[2]/total
        difference[3] = 100 * difference[3]/total
        difference[4] = 100 * difference[4]/total

        messagebox.showinfo("Importance", "Current Average Number of Days to Breakeven: " + str(round(self.partial_average(Radius, Sleep, Activity, original),2))
            + "\nChip Area: " + str(round(difference[0],2)) + "%\nDynamic Power(Processor + Cache): "
            + str(round(difference[1],2)) + "%\nStatic Power(Processor + Cache): " + str(round(difference[2],2)) + "%\nDynamic Power(Memory): "
            + str(round(difference[3],2)) + "%\nStatic Power(Memory): " + str(round(difference[4],2)) + "%")

    def single_point_analysis(self, *args):
        config1, config2 = self.verify_input(*args)
        if config1 is None:
            return
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        Sleep = int(simpledialog.askstring("Sleep","Please enter the Sleep Ratio:")) # Prompts user for the sleep ratio at which the point is at
        Activity = int(simpledialog.askstring("Activity","Please enter the Activity Ratio:")) # Prompts user for the activity ratio at which the point is at
        if (Sleep < 0 or Activity < 0 or Sleep>=100 or Activity>=100): # Checks to see if the point is in bounds
            messagebox.showinfo("Error", "The values inputted are out of bounds")
            return
        difference = [0,0,0,0,0]
        orig = chip_breakeven_IPC(config_dicts)['upgradeDays'][Sleep][Activity]
        old = config2['chipArea']
        config2['chipArea'] = config2['chipArea'] - (.01 * config2['chipArea'])
        difference[0] = orig - chip_breakeven_IPC(config_dicts)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['chipArea'] = old

        old = config2['dynamicPower']
        config2['dynamicPower'] = config2['dynamicPower'] - (.01 * config2['dynamicPower'])
        difference[1] = orig - chip_breakeven_IPC(config_dicts)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['dynamicPower'] = old

        old = config2['staticPower']
        config2['staticPower'] = config2['staticPower'] - (.01 * config2['staticPower'])
        difference[2] = orig - chip_breakeven_IPC(config_dicts)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['staticPower'] = old

        old = config2['dynamicMemory']
        config2['dynamicMemory'] = config2['dynamicMemory'] - (.01 * config2['dynamicMemory'])
        difference[3] = orig - chip_breakeven_IPC(config_dicts)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['dynamicMemory'] = old
        
        old = config2['staticMemory']
        config2['staticMemory'] = config2['staticMemory'] - (.01 * config2['staticMemory'])
        difference[4] = orig - chip_breakeven_IPC(config_dicts)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['staticMemory'] = old
        
        total = difference[0] + difference[1] + difference[2] + difference[3] + difference[4]   # Scales gradients to percentages
        difference[0] = 100 * difference[0]/total
        difference[1] = 100 * difference[1]/total
        difference[2] = 100 * difference[2]/total
        difference[3] = 100 * difference[3]/total
        difference[4] = 100 * difference[4]/total

        messagebox.showinfo("Importance", "Current Number of Days to Breakeven: " + str(round(orig,2)) + "\nChip Area: " + str(round(difference[0],2)) + "%\nDynamic Power(Processor + Cache): "
            + str(round(difference[1],2)) + "%\nStatic Power(Processor + Cache): " + str(round(difference[2],2)) + "%\nDynamic Power(Memory): "
            + str(round(difference[3],2)) + "%\nStatic Power(Memory): " + str(round(difference[4],2)) + "%") # Displays a message box showing the percentages                     

    def launch_config(self):

        self.window.geometry('1000x600')
        self.title1 = ttk.Entry(self.window, width=30)
        self.title2 = ttk.Entry(self.window, width=30)
        self.chipArea1 = ttk.Entry(self.window, width=30)
        self.chipArea2 = ttk.Entry(self.window, width=30)
        self.dynPower1 = ttk.Entry(self.window, width=30)
        self.dynPower2 = ttk.Entry(self.window, width=30)
        self.staticPower1 = ttk.Entry(self.window, width=30)
        self.staticPower2 = ttk.Entry(self.window, width=30)
        self.dynMemPower1 = ttk.Entry(self.window, width=30)
        self.dynMemPower2 = ttk.Entry(self.window, width=30)
        self.staticMemPower1 = ttk.Entry(self.window, width=30)
        self.staticMemPower2 = ttk.Entry(self.window, width=30)
        self.ipc1 = ttk.Entry(self.window, width=30)
        self.ipc2 = ttk.Entry(self.window, width=30)
        self.cycles1 = ttk.Entry(self.window, width=30)
        self.cycles2 = ttk.Entry(self.window, width=30)
        self.layers1 = ttk.Entry(self.window, width=30)
        self.layers2 = ttk.Entry(self.window, width=30)

        self.techNode1 = ttk.Combobox(self.window, textvariable=StringVar(), values=list(high_process_energies.keys()))
        self.techNode1.current(0)
        self.techNode2 = ttk.Combobox(self.window, textvariable=StringVar(), values=list(high_process_energies.keys()))
        self.techNode2.current(0)

        #self.title_label = ttk.Label(self.window, text='Labels:')
        #self.title_label.grid(column=0, row=0, sticky=(N, W, E, S))
        #self.title1.grid(column=1, row=0, sticky=(N, W, E, S))
        #self.title2.grid(column=2, row=0, sticky=(N, W, E, S))

        self.chipArea_label = ttk.Label(self.window, text='Chip Area (mm^2):')
        self.chipArea_label.grid(column=0, row=1, sticky=(N, W, E, S))
        self.chipArea1.grid(column=1, row=1, sticky=(N, W, E, S))
        self.chipArea2.grid(column=2, row=1, sticky=(N, W, E, S))
        Hovertip(self.chipArea_label, "Chip Area in mm^2")

        self.dynPower_label = ttk.Label(self.window, text='Dynamic Power (Processor+Caches)(W): ')
        self.dynPower_label.grid(column=0, row=2, sticky=(N, W, E, S))
        self.dynPower1.grid(column=1, row=2, sticky=(N, W, E, S))
        self.dynPower2.grid(column=2, row=2, sticky=(N, W, E, S))
        Hovertip(self.dynPower_label, "Dynamic Power is the major component of the power dissipated in circuits and also contributes to the peak power. \n It is a function of the supply voltage, the switching frequency and the output load. ")

        self.staticPower_label = ttk.Label(self.window, text='Static Power (Processor+Caches)(W): ')
        self.staticPower_label.grid(column=0, row=3, sticky=(N, W, E, S))
        self.staticPower1.grid(column=1, row=3, sticky=(N, W, E, S))
        self.staticPower2.grid(column=2, row=3, sticky=(N, W, E, S))
        Hovertip(self.staticPower_label, "static power is comprised of leakage, or current that flows through the transistor when there is no activity.")

        self.dynMem_label = ttk.Label(self.window, text='Dynamic Power (Memory)(W):')
        self.dynMem_label.grid(column=0, row=4, sticky=(N, W, E, S))
        self.dynMemPower1.grid(column=1, row=4, sticky=(N, W, E, S))
        self.dynMemPower2.grid(column=2, row=4, sticky=(N, W, E, S))
        Hovertip(self.dynMem_label, "tooltip text goes here")

        self.staticMem_label = ttk.Label(self.window, text='Static Power (Memory)(W):')
        self.staticMem_label.grid(column=0, row=5, sticky=(N, W, E, S))
        self.staticMemPower1.grid(column=1, row=5, sticky=(N, W, E, S))
        self.staticMemPower2 .grid(column=2, row=5, sticky=(N, W, E, S))
        Hovertip(self.staticMem_label, "tooltip text goes here")

        self.ipc_label = ttk.Label(self.window, text='IPC :')
        self.ipc_label.grid(column=0, row=6, sticky=(N, W, E, S))
        self.ipc1.grid(column=1, row=6, sticky=(N, W, E, S))
        self.ipc2.grid(column=2, row=6, sticky=(N, W, E, S))
        Hovertip(self.ipc_label, "IPC stands for instructions per cycle/clock. This tells you how many things a CPU can do in one cycle.")
        #Hovertip(self.ipc1.grid, "Tooltip text on grid")

        #self.cycles_label = ttk.Label(self.window, text='Cycles per simulation instance:')
        #self.cycles_label.grid(column=0, row=7, sticky=(N, W, E, S))
        #self.cycles1.grid(column=1, row=7, sticky=(N, W, E, S))
        #self.cycles2.grid(column=2, row=7, sticky=(N, W, E, S))

       # self.layers_label = ttk.Label(self.window, text='Number of Systems:')
        #self.layers_label.grid(column=0, row=8, sticky=(N, W, E, S))
        #self.layers1.
        #self.layers1.grid(column=1, row=8, sticky=(N, W, E, S))
        #self.layers2.current(1)
        #self.layers2.grid(column=2, row=8, sticky=(N, W, E, S))

        self.techNode_label = ttk.Label(self.window, text='Technology Node (nm): ')
        self.techNode_label.grid(column=0, row=9, sticky=(N, W, E, S))
        self.techNode1.grid(column=1, row=9, sticky=(N, W, E, S))
        self.techNode2.grid(column=2, row=9, sticky=(N, W, E, S))
        Hovertip(self.techNode_label, "The technology node (also process node, process technology or simply node) \n refers to a specific semiconductor manufacturing process and its design rules. \n Different nodes often imply different circuit generations and architectures.")

        self.plotButton1 = ttk.Button(self.window, text="Create Indifference Plot", command=self.plot_indifference)
        self.plotButton1.grid(column=1, row=11, sticky=(W))

        self.plotButton2 = ttk.Button(self.window, text="Create Breakeven Plot (Left Upgrading to Right)", command=self.plot_breakeven)
        self.plotButton2.grid(column=1, row=13, sticky=(W))

        self.plotButton3 = ttk.Button(self.window, text="Export Indifference to .csv", command=self.export_indifference)
        self.plotButton3.grid(column=1, row=15, sticky=(W))

        self.plotButton4 = ttk.Button(self.window, text="Export Breakeven to .csv", command=self.export_breakeven)
        self.plotButton4.grid(column=1, row=16, sticky=(W))
        
        self.plotButton5 = ttk.Button(self.window, text="Find Importance (Single Point Analysis)", command=self.single_point_analysis) # Creates button for single point analysis
        self.plotButton5.grid(column=2, row=11, sticky=(W))

        self.plotButton6 = ttk.Button(self.window, text="Find Importance (Average Analysis)", command=self.average_analysis) # Creates button for average point analysis
        self.plotButton6.grid(column=2, row=13, sticky=(W))

        self.plotButton7 = ttk.Button(self.window, text="Find Importance (All Point Analysis)", command=self.total_analysis) # Creates button for all point analysis
        self.plotButton7.grid(column=2, row=15, sticky=(W))
