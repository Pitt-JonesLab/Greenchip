__author__ = 'Donald Kline, Jr'

from plugins.shared.Utils import *
from plugins.shared.GreenChip import *
import plugins.shared.Config as settingsConfig
#import SimVis
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
import Pmw
import csv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import re
import os

class config(object):

    def __init__(self, root, DB, outdir, increment1, increment2, mindays, maxdays, minyears, maxyears, gridMixSettingsFilename = 'EnergyGridMix.csv'):
        self.DB = DB
        self.root = root
        self.path_to_output_directory = outdir
        self.path_to_sniper_directory1 = ''
        self.path_to_sniper_directory2 = ''
        self.increment1 = increment1
        self.increment2 = increment2
        self.mindays = mindays
        self.maxdays = maxdays
        self.minyears = minyears
        self.maxyears = maxyears
        self.window = Toplevel(self.root)
        self.window.title('Raw Data Entry Sliders')
        self.window.protocol("WM_DELETE_WINDOW", self.window_exit)
        self.balloon = Pmw.Balloon(self.root)
        lblballoon = self.balloon.component('label')
        lblballoon.config(background='white')
        #self.window.iconbitmap(r'Assets/greenchipicon.ico')
        self.window.geometry("500x100+0+0")
        self.energyData=[]
        filename=os.path.normpath(gridMixSettingsFilename)
        with open(filename, 'r') as file:
            reader=csv.reader(file)
            for row in reader:
               if row[0]!='Country': self.energyData.append(row)
        self.isOpen = True
        self.launch_config()

    def browse_sniper_input1(self):
        

        f = open(os.path.join(os.path.dirname(os.path.realpath('__file__')),'defaultFolders.txt'), "r+")
        defaults = f.readlines()
        filename1 = None
        if defaults[1]=='\n':
            filename1 = filedialog.askdirectory()
        else:
            filename1 = filedialog.askdirectory(initialdir = os.path.normpath(defaults[1].strip()))

        if (filename1 is None or filename1==""):
            return

        defaults[1] = filename1 + "\n"
        f.seek(0)
        f.truncate(0)
        f.writelines(defaults)
        f.close()
        
        self.path_to_sniper_directory1 = filename1
        self.get_sniper_inputs1()

    def browse_sniper_input2(self):
        
        f = open(os.path.join(os.path.dirname(os.path.realpath('__file__')),'defaultFolders.txt'), "r+")
        defaults = f.readlines()
        filename2 = None
        if defaults[2]=='\n':
            filename2 = filedialog.askdirectory()
        else:
            filename2 = filedialog.askdirectory(initialdir = os.path.normpath(defaults[2].strip()))

        if (filename2 is None or filename2==""):
            return

        defaults[2] = filename2 + "\n"
        f.seek(0)
        f.truncate(0)
        f.writelines(defaults)
        f.close()
        
        self.path_to_sniper_directory2 = filename2
        self.get_sniper_inputs2()

    @staticmethod
    def needs_DB():
        return False

    def window_exit(self):
        self.isOpen = False
        self.window.destroy()
                
    def remove_source(self, tech_node):
        i = 0
        while i<len(tech_node) and tech_node[i]!='(':
            i += 1
        return tech_node[0:(i-1)]

    def calculateCarbon(self, row):
        sum = 0
        index = 2
        while index < 12:
            source =  int(row[index]) * float(row[index+10])
            sum += source
            index += 1
        return round(sum/100)

    def verify_input(self, *args):
        config1 = {}
        config2 = {}

        try:
            config1['chipArea'] = float(self.chipArea1.get())
            config2['chipArea'] = float(self.chipArea2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid CPU Chip Area!")
            return None, None
        
        if self.varD.get()==1:
            try:
                config1['chipAreaDram'] = float(self.dramArea1.get())
                config2['chipAreaDram'] = float(self.dramArea2.get())
            except (ValueError):
                messagebox.showinfo("Warning: Illegal Argument", "Invalid DRAM Chip Area!")
                return None, None
            
            try:
                techNode3 = self.remove_source(self.techNode3.get())
                techNode4 = self.remove_source(self.techNode4.get())
                config1['processSizeDram'] = str(techNode3)    
                config2['processSizeDram'] = str(techNode4)
            except (ValueError):
                messagebox.showinfo("Warning: Illegal Argument", "Invalid DRAM Technology Node!")
                return None, None
            try:
                techNode3Num = self.techNode3.get().split(' ')[0]
                techNode4Num = self.techNode4.get().split(' ')[0]
                config1['processSizeDramNum'] = int (techNode3Num)    
                config2['processSizeDramNum'] = int (techNode4Num)
            except (ValueError):
                messagebox.showinfo("Warning: Illegal Argument", "Invalid DRAM Technology Node!")
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
        else:
            config1['chipAreaDram'] = 0.0
            config2['chipAreaDram'] = 0.0
            techNode3 = '55'
            techNode4 = '55'
            config1['processSizeDram'] = str(techNode3)    
            config2['processSizeDram'] = str(techNode4)
            techNode3Num = '55'
            techNode4Num = '55'
            config1['processSizeDramNum'] = int (techNode3Num)    
            config2['processSizeDramNum'] = int (techNode4Num)        
            config1['dynamicMemory'] = 0.0
            config2['dynamicMemory'] = 0.0
            config1['staticMemory'] = 0.0
            config2['staticMemory'] =  0.0
    
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
            config1['IPC'] = float(self.ipc1.get())
            config2['IPC'] = float(self.ipc2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid IPC!")
            return None, None

        try:
            config1['FREQ'] = float(self.freq1.get())
            config2['FREQ'] = float(self.freq2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Frequency!")
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
            techNode1 = self.remove_source(self.techNode1.get())
            techNode2 = self.remove_source(self.techNode2.get())
            config1['processSize'] = techNode1
            config2['processSize'] = techNode2
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Technology Node!")
            return None, None

        try:
            config1['LocationManu CPU'] = self.locCPU1.get()
            for row in self.energyData:
                if row[2] == '':
                    continue
                if row[0] == self.locCPU1.get():
                    config1['CPU Carbon Value'] = self.calculateCarbon(row)
                    break
                if row[1] == self.locCPU1.get():
                    config1['CPU Carbon Value'] = self.calculateCarbon(row)
                    break    
            config2['LocationManu CPU'] = self.locCPU2.get()
            for row in self.energyData:
                if row[2] == '':
                    continue
                if row[0] == self.locCPU2.get():
                    config2['CPU Carbon Value'] = self.calculateCarbon(row)
                    break
                if row[1] == self.locCPU2.get():
                    config2['CPU Carbon Value'] = self.calculateCarbon(row)
                    break        
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Energy Grid Mix Location for CPU!")
            return None, None       
        
        if self.varD.get()==1:
            try:
                config1['LocationManu DRAM'] = self.locDRAM1.get()
                for row in self.energyData:
                    if row[2] == '':
                        continue
                    if row[0] == self.locDRAM1.get():
                        config1['DRAM Carbon Value'] = self.calculateCarbon(row)
                        break
                    if row[1] == self.locDRAM1.get():
                        config1['DRAM Carbon Value'] = self.calculateCarbon(row)
                        break     
                config2['LocationManu DRAM'] = self.locDRAM2.get()
                for row in self.energyData:
                    if row[2] == '':
                        continue
                    if row[0] == self.locDRAM2.get():
                        config2['DRAM Carbon Value'] = self.calculateCarbon(row)
                        break
                    if row[1] == self.locDRAM2.get():
                        config2['DRAM Carbon Value'] = self.calculateCarbon(row)
                        break

            except (ValueError):
                messagebox.showinfo("Warning: Illegal Argument", "Invalid Energy Grid Mix Location for DRAM!")
                return None, None
        else:
            config1['LocationManu DRAM'] = self.locCPU1.get()
            config1['DRAM Carbon Value'] = 0
            config2['LocationManu DRAM'] = self.locCPU2.get()
            config2['DRAM Carbon Value'] = 0
            

        try:
            config1['Carbon Use Phase Loc'] = (self.locUse1.get())
            for row in self.energyData:
                if row[2] == '':
                    continue
                if row[0] == self.locUse1.get():
                    config1['UsePh Carbon Value'] = self.calculateCarbon(row)
                    break
                if row[1] == self.locUse1.get():
                    config1['UsePh Carbon Value'] = self.calculateCarbon(row)
                    break        
            config2['Carbon Use Phase Loc'] = (self.locUse2.get())
            for row in self.energyData:
                if row[2] == '':
                    continue
                if row[0] == self.locUse2.get():
                    config2['UsePh Carbon Value'] = self.calculateCarbon(row)
                    break
                if row[1] == self.locUse2.get():
                    config2['UsePh Carbon Value'] = self.calculateCarbon(row)
                    break
                    
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Energy Grid Mix Location for Use Phase!")
            return None, None

        ''' Add energy (Joules) manufacturing CPU '''
        config1['CPU Energy'] = high_process_energies[techNode1]['energy']
        config2['CPU Energy'] = high_process_energies[techNode2]['energy']
            
        config1['Total CPU Energy'] = simple_manufacturing(config1['CPU Energy'], config1['chipArea'], config1['layers'])
        config2['Total CPU Energy'] = simple_manufacturing(config2['CPU Energy'], config2['chipArea'], config2['layers'])
        config1['Total CPU Carbon'] = config1['Total CPU Energy'] /3600000 * config1['CPU Carbon Value']
        config2['Total CPU Carbon'] = config2['Total CPU Energy'] /3600000 * config2['CPU Carbon Value']
        
        ''' Add energy (Joules) manufacturing DRAM '''
        config1['DRAM Energy'] = high_process_energies_DRAM[techNode3]['energy']
        config2['DRAM Energy'] = high_process_energies_DRAM[techNode4]['energy']
            
        config1['Total DRAM Energy'] = simple_manufacturing(config1['DRAM Energy'], config1['chipAreaDram'], config1['layers'])
        config2['Total DRAM Energy'] = simple_manufacturing(config2['DRAM Energy'], config2['chipAreaDram'], config2['layers'])
        config1['Total DRAM Carbon'] = config1['Total DRAM Energy'] /3600000 * config1['DRAM Carbon Value']
        config2['Total DRAM Carbon'] = config2['Total DRAM Energy'] /3600000 * config2['DRAM Carbon Value']
        
        # 
        CPUWattHours = config1['dynamicPower'] + config1['staticPower'] #Power in Watts
        CPUKWattHours = CPUWattHours/1000
        config1['CPU Hourly Usage Carbon'] = CPUKWattHours * config1['CPU Carbon Value']
        
        CPUWattHours = config2['dynamicPower'] + config2['staticPower'] #Power in Watts
        CPUKWattHours = CPUWattHours/1000
        config2['CPU Hourly Usage Carbon'] = CPUKWattHours * config2['CPU Carbon Value']
                
        DRAMWattHours = config1['dynamicMemory'] + config1['staticMemory']
        DRAMKWattHours = DRAMWattHours/1000
        config1['DRAM Hourly Usage Carbon'] = DRAMKWattHours * config1['DRAM Carbon Value']
        
        DRAMWattHours = config2['dynamicMemory'] + config2['staticMemory']
        DRAMKWattHours = DRAMWattHours/1000
        config2['DRAM Hourly Usage Carbon'] = DRAMKWattHours * config2['DRAM Carbon Value']

        return config1, config2

    def plot_indifference(self,*args):
        config1, config2 = self.verify_input(*args)
        if config1 is None:
            return
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        if self.varE.get()==1:
            res = chip_breakeven_IPC(config_dicts, False, self.increment1)['chipVsChipBreakevenInDays']
            utils.make_single_plot(self, config1, config2, self.title1.get(), self.title2.get(), res, 'Indifference Plot Energy', self.increment1, self.mindays, self.maxdays, self.minyears, self.maxyears)
        if self.varC.get()==1:
            if (config2['LocationManu DRAM'] == '' or config2['LocationManu CPU'] == '' or config2['Carbon Use Phase Loc'] == '' 
            or config1['LocationManu DRAM'] == '' or config1['LocationManu CPU'] == '' or config1['Carbon Use Phase Loc'] == ''):
                messagebox.showerror('Empty Grid Mix','Could not generate carbon plot due to empty Grid Mix(es)! Be sure to fill in all values.')
                return
            res = chip_breakeven_IPC(config_dicts, True, self.increment1)['chipVsChipBreakevenInDays']
            utils.make_single_plot(self, config1, config2, self.title1.get(), self.title2.get(), res, 'Indifference Plot Carbon', self.increment1, self.mindays, self.maxdays, self.minyears, self.maxyears)        


    def plot_breakeven(self, *args):
        config1, config2 = self.verify_input(*args)
        if config1 is None:
            return
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        if self.varE.get()==1:
            res = chip_breakeven_IPC(config_dicts, False, self.increment1)['upgradeDays']
            utils.make_single_plot(self, config1, config2, self.title1.get(), self.title2.get(), res, 'Breakeven Plot Energy', self.increment1, self.mindays, self.maxdays, self.minyears, self.maxyears)
        if self.varC.get()==1:
            if (config2['LocationManu DRAM'] == '' or config2['LocationManu CPU'] == '' or config2['Carbon Use Phase Loc'] == '' 
            or config1['LocationManu DRAM'] == '' or config1['LocationManu CPU'] == '' or config1['Carbon Use Phase Loc'] == ''):
                messagebox.showerror('Empty Grid Mix','Could not generate carbon plot due to empty Grid Mix(es)! Be sure to fill in all values.')
                return
            res = chip_breakeven_IPC(config_dicts, True, self.increment1)['upgradeDays']
            utils.make_single_plot(self, config1, config2, self.title1.get(), self.title2.get(), res, 'Breakeven Plot Carbon', self.increment1, self.mindays, self.maxdays, self.minyears, self.maxyears)
    
    def updateDropdown(self, event):
        utils.changeOptionsLoc(event, self.energyData)
        if event.widget.get() != '':
            self.plot_mini()
        
    def plot_mini(self, *args):
        self.plot_mini_breakeven(*args)
        self.plot_mini_indifference(*args)

    def plot_mini_breakeven(self, *args):
        config1, config2 = self.verify_input(*args)
        if self.varD.get()==1:
            if ((config2['chipArea'] == 0 and config2['chipAreaDram'] == 0)
             or config1['dynamicMemory'] == 0 or config2['dynamicMemory'] == 0 or config1['staticMemory'] == 0 or config2['staticMemory'] == 0
             or config1['dynamicPower'] == 0 or config2['dynamicPower'] == 0 or config1['staticPower'] == 0 or config2['staticPower'] == 0
             or config1['IPC'] == 0 or config2['IPC'] == 0 or config1['FREQ'] == 0 or config2['FREQ'] == 0):
                if hasattr(self, 'breakeven_preview'):
                    self.breakeven_preview.grid_remove()
                    self.breakevenplt_label.grid_remove()
                return
        else:
            if ((config2['chipArea'] == 0) or config1['dynamicPower'] == 0 or config2['dynamicPower'] == 0 or config1['staticPower'] == 0 or config2['staticPower'] == 0
             or config1['IPC'] == 0 or config2['IPC'] == 0 or config1['FREQ'] == 0 or config2['FREQ'] == 0):
                if hasattr(self, 'breakeven_preview'):
                    self.breakeven_preview.grid_remove()
                    self.breakevenplt_label.grid_remove()
                return
        if self.recentlychecked == 'C':
            if (config2['LocationManu DRAM'] == '' or config2['LocationManu CPU'] == '' or config2['Carbon Use Phase Loc'] == '' 
            or config1['LocationManu DRAM'] == '' or config1['LocationManu CPU'] == '' or config1['Carbon Use Phase Loc'] == ''):
                if hasattr(self, 'breakeven_preview'):
                    self.breakeven_preview.grid_remove()
                    self.breakevenplt_label.grid_remove()
                return
        if config1 is None:
            if hasattr(self, 'breakeven_preview'):
                self.breakeven_preview.grid_remove()
                self.breakevebplt_label.grid_remove()
            return
        self.breakevenplt_label.grid(column=3, row=0, sticky=(N))
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        
        carbon = False
        if self.recentlychecked=='C':
            self.bplt.set("Breakeven Plot (Carbon)")
            carbon = True

        if self.recentlychecked=='E':
            self.bplt.set("Breakeven Plot (Energy)")


        res = chip_breakeven_IPC(config_dicts, carbon, self.increment2)['upgradeDays']
        self.mini_viewer(config1, config2, self.title1.get(), self.title2.get(), res, self.increment2, self.mindays, self.maxdays, self.minyears, self.maxyears)



    def plot_mini_indifference(self, *args):
        config1, config2 = self.verify_input(*args)
        if self.varD.get()==1:
            if ((config2['chipArea'] == 0 and config2['chipAreaDram'] == 0) or (config1['chipArea'] == 0 and config1['chipAreaDram'] == 0)
             or config1['dynamicMemory'] == 0
             or config2['dynamicMemory'] == 0 or config1['staticMemory'] == 0 or config2['staticMemory'] == 0
             or config1['dynamicPower'] == 0 or config2['dynamicPower'] == 0 or config1['staticPower'] == 0 or config2['staticPower'] == 0
             or config1['IPC'] == 0 or config2['IPC'] == 0 or config1['FREQ'] == 0 or config2['FREQ'] == 0):
                if hasattr(self, 'indifference_preview'):
                    self.indifference_preview.grid_remove()
                    self.indifferenceplt_label.grid_remove()
                return
        else:
            if (config2['chipArea'] == 0 or config1['chipArea'] == 0  or config1['dynamicPower'] == 0 or config2['dynamicPower'] == 0
             or config1['staticPower'] == 0 or config2['staticPower'] == 0 or config1['IPC'] == 0 or config2['IPC'] == 0 
             or config1['FREQ'] == 0 or config2['FREQ'] == 0):
                if hasattr(self, 'indifference_preview'):
                    self.indifference_preview.grid_remove()
                    self.indifferenceplt_label.grid_remove()
                return
        if self.recentlychecked == 'C':
            if (config2['LocationManu DRAM'] == '' or config2['LocationManu CPU'] == '' or config2['Carbon Use Phase Loc'] == '' 
            or config1['LocationManu DRAM'] == '' or config1['LocationManu CPU'] == '' or config1['Carbon Use Phase Loc'] == ''):
                if hasattr(self, 'indifference_preview'):
                    self.indifference_preview.grid_remove()
                    self.indifferenceplt_label.grid_remove()
                return
        if config1 is None:
            return
        self.indifferenceplt_label.grid(column=3, row=self.indiffRow, sticky=(N))
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        
        carbon = False
        if self.recentlychecked=='C':
            if (config2['LocationManu DRAM'] == '' or config2['LocationManu CPU'] == '' or config2['Carbon Use Phase Loc'] == '' 
            or config1['LocationManu DRAM'] == '' or config1['LocationManu CPU'] == '' or config1['Carbon Use Phase Loc'] == ''):
                if hasattr(self, 'indifference_preview'):
                    self.indifference_preview.grid_remove()
                    self.indifferenceplt_label.remove()
                return
            self.iplt.set("Indifference Plot (Carbon)")
            carbon = True

        if self.recentlychecked=='E':
            self.iplt.set("Indifference Plot (Energy)")
            
        res = chip_breakeven_IPC(config_dicts, carbon, self.increment2)['chipVsChipBreakevenInDays']
        self.mini_viewer_indifference(config1, config2, self.title1.get(), self.title2.get(), res, self.increment2, self.mindays, self.maxdays, self.minyears, self.maxyears)


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
        original = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays']
        old = config2['chipArea']
        config2['chipArea'] = config2['chipArea'] - (.01 * config2['chipArea'])
        mod = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays']
        difference[0] = self.total_gradient(original, mod)
        config2['chipArea'] = old

        old = config2['dynamicPower']
        config2['dynamicPower'] = config2['dynamicPower'] - (.01 * config2['dynamicPower'])
        mod = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays']
        difference[1] = self.total_gradient(original, mod)
        config2['dynamicPower'] = old

        old = config2['staticPower']
        config2['staticPower'] = config2['staticPower'] - (.01 * config2['staticPower'])
        mod = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays']
        difference[2] = self.total_gradient(original, mod)
        config2['staticPower'] = old

        old = config2['dynamicMemory']
        config2['dynamicMemory'] = config2['dynamicMemory'] - (.01 * config2['dynamicMemory'])
        mod = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays']
        difference[3] = self.total_gradient(original, mod)
        config2['dynamicMemory'] = old
        
        old = config2['staticMemory']
        config2['staticMemory'] = config2['staticMemory'] - (.01 * config2['staticMemory'])
        mod = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays']
        difference[4] = self.total_gradient(original, mod)
        config2['staticMemory'] = old
        
        total = difference[0] + difference[1] + difference[2] + difference[3] + difference[4]
        difference[0] = 100 * difference[0]/total
        difference[1] = 100 * difference[1]/total
        difference[2] = 100 * difference[2]/total
        difference[3] = 100 * difference[3]/total
        difference[4] = 100 * difference[4]/total
        
        if (total==0):
            messagebox.showerror("Bad Plot", "The entire plot is infinite. Maybe you switched the systems? Please try again.")
            return

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
        original = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays']
        old = config2['chipArea']
        config2['chipArea'] = config2['chipArea'] - (.01 * config2['chipArea'])
        mod = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays']
        difference[0] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['chipArea'] = old

        old = config2['dynamicPower']
        config2['dynamicPower'] = config2['dynamicPower'] - (.01 * config2['dynamicPower'])
        mod = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays']
        difference[1] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['dynamicPower'] = old

        old = config2['staticPower']
        config2['staticPower'] = config2['staticPower'] - (.01 * config2['staticPower'])
        mod = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays']
        difference[2] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['staticPower'] = old

        old = config2['dynamicMemory']
        config2['dynamicMemory'] = config2['dynamicMemory'] - (.01 * config2['dynamicMemory'])
        mod = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays']
        difference[3] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['dynamicMemory'] = old
        
        old = config2['staticMemory']
        config2['staticMemory'] = config2['staticMemory'] - (.01 * config2['staticMemory'])
        mod = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays']
        difference[4] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['staticMemory'] = old
        
        total = difference[0] + difference[1] + difference[2] + difference[3] + difference[4]

        if (total==0):
            messagebox.showerror("Bad Input", "All your inputs take an infinite amount of time to breakeven. Please try again.")
            return
        
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
        orig = chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays'][Sleep][Activity]
        old = config2['chipArea']
        config2['chipArea'] = config2['chipArea'] - (.01 * config2['chipArea'])
        difference[0] = orig - chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['chipArea'] = old

        old = config2['dynamicPower']
        config2['dynamicPower'] = config2['dynamicPower'] - (.01 * config2['dynamicPower'])
        difference[1] = orig - chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['dynamicPower'] = old

        old = config2['staticPower']
        config2['staticPower'] = config2['staticPower'] - (.01 * config2['staticPower'])
        difference[2] = orig - chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['staticPower'] = old

        old = config2['dynamicMemory']
        config2['dynamicMemory'] = config2['dynamicMemory'] - (.01 * config2['dynamicMemory'])
        difference[3] = orig - chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['dynamicMemory'] = old
        
        old = config2['staticMemory']
        config2['staticMemory'] = config2['staticMemory'] - (.01 * config2['staticMemory'])
        difference[4] = orig - chip_breakeven_IPC(config_dicts, False, 1)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['staticMemory'] = old
        
        total = difference[0] + difference[1] + difference[2] + difference[3] + difference[4]   # Scales gradients to percentages
        
        if (total==0):
            messagebox.showerror("Bad Input", "Your input takes an infinite amount of time to breakeven. Please try again.")
            return
        
        difference[0] = 100 * difference[0]/total
        difference[1] = 100 * difference[1]/total
        difference[2] = 100 * difference[2]/total
        difference[3] = 100 * difference[3]/total
        difference[4] = 100 * difference[4]/total

        messagebox.showinfo("Importance", "Current Number of Days to Breakeven: " + str(round(orig,2)) + "\nChip Area: " + str(round(difference[0],2)) + "%\nDynamic Power(Processor + Cache): "
            + str(round(difference[1],2)) + "%\nStatic Power(Processor + Cache): " + str(round(difference[2],2)) + "%\nDynamic Power(Memory): "
            + str(round(difference[3],2)) + "%\nStatic Power(Memory): " + str(round(difference[4],2)) + "%") # Displays a message box showing the percentages    

    def mini_viewer(self, first_entry, second_entry, title1, title2, res, increment, mindays, maxdays, minyears, maxyears):
        if settingsConfig.nativePlotting:



            if first_entry is None or second_entry is None:
                return

            settingsFile = settingsConfig.advancedSettingsFile
            arr = utils.perform_greenchip_analysis(res)

            fig = Figure(figsize=(2.75,2.75), dpi = 100)
            ax = fig.add_subplot(111)

           # fig, ax = plt.subplots()

            cdict2 = OurConstants.get_cdict2()

            cdict1 = OurConstants.get_cdict1()

            customgray = LinearSegmentedColormap('customgray', cdict1)
            customspectrum = LinearSegmentedColormap('customspectrum', cdict2)
            c = (0, 0, 0, 0)
            my_cmap = plt.get_cmap(customspectrum)
            my_cmap.set_under(color='white')
            second_cmap = plt.get_cmap(customgray)
            second_cmap.set_under(color=c)

            heatmap = ax.pcolormesh(arr, cmap=my_cmap, vmax=maxdays, vmin=mindays)
            heatbar = heatmap
            heatmap = ax.pcolormesh(arr, cmap=second_cmap, vmax=maxyears*365, vmin=minyears*365)
            heatbar2 = heatmap
            

           # def Clicked(event, int sleep, int activity):
            #    print(sleep)

            
            # want a more natural, table-like display
            ax.invert_yaxis()
            ax.xaxis.tick_top()
            ax.axis('tight')

            ax.set_xticks(np.array([0.5,20/increment + 0.5,40/increment + 0.5,60/increment + 0.5,80/increment + 0.5,(100/increment)+0.5]), [0,20,40,60,80,100])
            ax.set_yticks(np.array([0.5,20/increment + 0.5,40/increment + 0.5,60/increment + 0.5,80/increment + 0.5,(100/increment)+0.5]), [0,20,40,60,80,100])

            # l = arr.shape[0]
            
            # if arr[0,0]<0:
                # i = int(100/(increment*2))
                # shifter = int(i/2)
                # while i>0 and i<l-1 and (arr[i,0]>0 or arr[i+1,0]<0):
                    # if arr[i,0]<0: i+=shifter
                    # else: i-=shifter
                    # if shifter!=1: shifter = int(shifter/2)
                # if i<0: i=0
                # if i>=l: i=l-1
                # ax.add_patch(Rectangle((0,0), l, i+1, fc = 'w', hatch = '///', ec = 'black'))

            # elif arr[l-1,0]<0:
                # i = int(100/(increment*2))
                # shifter = int(i/2)
                # while i>0 and i<l-1 and (arr[i,0]>0 or arr[i-1,0]<0):
                    # if arr[i,0]<0: i-=shifter
                    # else: i+=shifter
                    # if shifter!=1: shifter = int(shifter/2)
                # if i<0: i=0
                # if i>=l: i=l-1
                # ax.add_patch(Rectangle((0,i), l, l-i+1, fc = 'w', hatch = '///', ec = 'black'))

            # plt.title(''.join([utils.rename(self.entry1, False), ' vs. ', utils.rename(self.entry2, False)]), y=1.08)

            #image_file_name = path_to_output_directory + title1 + "_vs_" + title2 + ".pdf"

            self.canvasP = FigureCanvasTkAgg(fig, master=self.window)
            if hasattr(self, 'breakeven_preview'): self.breakeven_preview.grid_remove()
            self.breakeven_preview = self.canvasP.get_tk_widget()
            self.breakeven_preview.grid(column=3, row=1, rowspan = 9, sticky=(E))
            self.canvasP.draw()
           # figcanvas.get_tk_widget().grid()
            #plt.savefig(image_file_name, bbox_inches='tight')
            #plt.clf()
            #plt.close()
        elif sys.platform.startswith("win"):
            try:
                breakeven_export_name = filedialog.asksaveasfilename(defaultextension=".csv")
                with open(breakeven_export_name, "w") as indiff_writer:
                    for a in range(0, len(res)):
                        for b in range(0, len(res[0])):
                            indiff_writer.write(str(a)+","+str(b)+","+str(res[a][b])+"\n")
                #Assumes matlab is in the current directory
                dir_path = os.path.dirname(os.path.realpath(__file__))
                subprocess.call('matlab -nodesktop -nosplash /r "addpath '+str(dir_path)+';greenchip_plotter(\''+str(breakeven_export_name)+'\');"', shell = True)
            except:
                messagebox.showinfo("Library Missing!", "Missing matplotlib, and no matlab found to take its place!")
                for bbb in range(0, len(sys.exc_info())):
                    print(sys.exc_info()[bbb])
                #print(sys.exc_info()[0])
        else:
            messagebox.showinfo("Library Missing!", "Missing matplotlib, cannot plot natively in python!")

    def mini_viewer_indifference(self, first_entry, second_entry, title1, title2, res, increment, mindays, maxdays, minyears, maxyears):
        if settingsConfig.nativePlotting:



            if first_entry is None or second_entry is None:
                return

            settingsFile = settingsConfig.advancedSettingsFile
            arr = utils.perform_greenchip_analysis(res)

            fig = Figure(figsize=(2.75,2.75), dpi = 100)
            ax = fig.add_subplot(111)

           # fig, ax = plt.subplots()

            cdict2 = OurConstants.get_cdict2()

            cdict1 = OurConstants.get_cdict1()

            customgray = LinearSegmentedColormap('customgray', cdict1)
            customspectrum = LinearSegmentedColormap('customspectrum', cdict2)
            c = (0, 0, 0, 0)
            my_cmap = plt.get_cmap(customspectrum)
            my_cmap.set_under(color='white')
            second_cmap = plt.get_cmap(customgray)
            second_cmap.set_under(color=c)

            heatmap = ax.pcolormesh(arr, cmap=my_cmap, vmax=maxdays, vmin=mindays)
            heatbar = heatmap
            heatmap = ax.pcolormesh(arr, cmap=second_cmap, vmax=maxyears*365, vmin=minyears*365)
            heatbar2 = heatmap
            

           # def Clicked(event, int sleep, int activity):
            #    print(sleep)

            
            # want a more natural, table-like display
            ax.invert_yaxis()
            ax.xaxis.tick_top()
            ax.axis('tight')

            ax.set_xticks(np.array([0,20/increment,40/increment,60/increment,80/increment,(100/increment)+1]), [0,20,40,60,80,100])
            ax.set_yticks(np.array([0,20/increment,40/increment,60/increment,80/increment,(100/increment)+1]), [0,20,40,60,80,100])

            # l = arr.shape[0]
            
            # if arr[0,0]<0:
                # i = int(100/(increment*2))
                # shifter = int(i/2)
                # while i>0 and i<l-1 and (arr[i,0]>0 or arr[i+1,0]<0):
                    # if arr[i,0]<0: i+=shifter
                    # else: i-=shifter
                    # if shifter!=1: shifter = int(shifter/2)
                # if i<0: i=0
                # if i>=l: i=l-1
                # ax.add_patch(Rectangle((0,0), l, i+1, fc = 'w', hatch = '///', ec = 'black'))

            # elif arr[l-1,0]<0:
                # i = int(100/(increment*2))
                # shifter = int(i/2)
                # while i>0 and i<l-1 and (arr[i,0]>0 or arr[i-1,0]<0):
                    # if arr[i,0]<0: i-=shifter
                    # else: i+=shifter
                    # if shifter!=1: shifter = int(shifter/2)
                # if i<0: i=0
                # if i>=l: i=l-1
                # ax.add_patch(Rectangle((0,i), l, l-i+1, fc = 'w', hatch = '///', ec = 'black'))

            # plt.title(''.join([utils.rename(self.entry1, False), ' vs. ', utils.rename(self.entry2, False)]), y=1.08)

            #image_file_name = path_to_output_directory + title1 + "_vs_" + title2 + ".pdf"

            self.canvasP = FigureCanvasTkAgg(fig, master=self.window)
            if hasattr(self, 'indifference_preview'): self.indifference_preview.grid_remove()
            self.indifference_preview = self.canvasP.get_tk_widget()
            self.indifference_preview.grid(column=3, row=11, rowspan=20, sticky=(W))
            self.canvasP.draw()
           # figcanvas.get_tk_widget().grid()
            #plt.savefig(image_file_name, bbox_inches='tight')
            #plt.clf()
            #plt.close()
        elif sys.platform.startswith("win"):
            try:
                breakeven_export_name = filedialog.asksaveasfilename(defaultextension=".csv")
                with open(breakeven_export_name, "w") as indiff_writer:
                    for a in range(0, len(res)):
                        for b in range(0, len(res[0])):
                            indiff_writer.write(str(a)+","+str(b)+","+str(res[a][b])+"\n")
                #Assumes matlab is in the current directory
                dir_path = os.path.dirname(os.path.realpath(__file__))
                subprocess.call('matlab -nodesktop -nosplash /r "addpath '+str(dir_path)+';greenchip_plotter(\''+str(breakeven_export_name)+'\');"', shell = True)
            except:
                messagebox.showinfo("Library Missing!", "Missing matplotlib, and no matlab found to take its place!")
                for bbb in range(0, len(sys.exc_info())):
                    print(sys.exc_info()[bbb])
                #print(sys.exc_info()[0])
        else:
            messagebox.showinfo("Library Missing!", "Missing matplotlib, cannot plot natively in python!")

    def get_sniper_inputs1(self):
        if not self.path_to_sniper_directory1:
            messagebox.showinfo("Error","Sniper Directory is empty!")
            return
        f = open(self.path_to_sniper_directory1  + "/power.txt", "r")
        l = f.readline()
        while (l[0:12] != "  Technology"):
            l = f.readline()
        numbers = re.findall(r'\d+', l)
        self.techNode1.set(numbers[0])
        for tech in high_process_energies_with_sources:
            if numbers[0] + " " in tech or numbers[0]==tech:
                self.techNode1.set(tech)
                break
        while (l[0:22] != "  Core clock Rate(MHz)"):
            l = f.readline()
        numbers = re.findall(r'\d+', l)
        self.freq1.set(float(numbers[0])/1000.0)
        while (l[0:6] != "  Area"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        self.chipArea1.set(float(numbers[0]))
        while (l[0:40] != "  Subthreshold Leakage with power gating"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        self.staticPower1.set(float(numbers[0]))
        while (l[0:14] != "  Gate Leakage"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        self.staticPower1.set(self.staticPower1.get() + float(numbers[0]))
        while (l[0:17] != "  Runtime Dynamic"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        self.dynPower1.set(float(numbers[0]))
        f = open(self.path_to_sniper_directory1  + "/power.py", "r")
        while (l[0:25] != "          'Gate Leakage':"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        numbers2 = re.findall(r'\d+', l)
        if len(numbers2) != 1: 
            self.staticMemPower1.set(float(numbers[0]))
        else:
            self.staticMemPower1.set(float(numbers2[0]))
        while (l[0:28] != "          'Runtime Dynamic':"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        self.dynMemPower1.set(float(numbers[0]))
        while (l[0:51] != "          'Subthreshold Leakage with power gating':"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        self.staticMemPower1.set(self.staticMemPower1.get() + float(numbers[0]))
        f = open(self.path_to_sniper_directory1  + "/sim.out", "r")
        while (l[0:5] != "  IPC"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        total = 0
        for i in range(len(numbers)):
            total = total + float(numbers[i])
        self.ipc1.set(float(total))
		
        if os.path.exists(os.path.join(self.path_to_sniper_directory1,"Greenchip.txt")):
            f = open(os.path.join(self.path_to_sniper_directory1,"Greenchip.txt"), "r")
            l = f.readlines()
            for i in range(len(l)):
                l[i] = l[i].split('//')[0].strip()

            self.dramArea1.set(float(l[0]))
            for i in self.comboboxEntriesDram:
                if l[1]==self.remove_source(i):
                    self.techNode3.set(i)
                    break
                    
            locTemp = utils.returnListLoc(l[2], self.energyData)
            if locTemp is not None:
                self.locCPU1['values'] = locTemp
                self.locCPU1.set(l[2])
            locTemp = utils.returnListLoc(l[3], self.energyData)
            if locTemp is not None:
                self.locDRAM1['values'] = locTemp
                self.locDRAM1.set(l[3])
            locTemp = utils.returnListLoc(l[4], self.energyData)
            if locTemp is not None:
                self.locUse1['values'] = locTemp
                self.locUse1.set(l[4])

        self.plot_mini()

    def get_sniper_inputs2(self):
        if not self.path_to_sniper_directory2:
            messagebox.showinfo("Error","Sniper Directory is empty!")
            return
        f = open(self.path_to_sniper_directory2  + "/power.txt", "r")
        l = f.readline()
        while (l[0:12] != "  Technology"):
            l = f.readline()
        numbers = re.findall(r'\d+', l)
        self.techNode2.set(numbers[0])
        for tech in high_process_energies_with_sources:
            if numbers[0] + " " in tech or numbers[0]==tech:
                self.techNode2.set(tech)
                break
        while (l[0:22] != "  Core clock Rate(MHz)"):
            l = f.readline()
        numbers = re.findall(r'\d+', l)
        self.freq2.set(float(numbers[0])/1000.0)
        while (l[0:6] != "  Area"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        self.chipArea2.set(float(numbers[0]))
        while (l[0:40] != "  Subthreshold Leakage with power gating"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        self.staticPower2.set(float(numbers[0]))
        while (l[0:14] != "  Gate Leakage"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        self.staticPower2.set(self.staticPower2.get() + float(numbers[0]))
        while (l[0:17] != "  Runtime Dynamic"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        self.dynPower2.set(float(numbers[0]))
        f = open(self.path_to_sniper_directory2  + "/power.py", "r")
        while (l[0:25] != "          'Gate Leakage':"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        numbers2 = re.findall(r'\d+', l)
        if len(numbers2) != 1: 
            self.staticMemPower2.set(float(numbers[0]))
        else:
            self.staticMemPower2.set(float(numbers2[0]))
        while (l[0:28] != "          'Runtime Dynamic':"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        self.dynMemPower2.set(float(numbers[0]))
        while (l[0:51] != "          'Subthreshold Leakage with power gating':"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        self.staticMemPower2.set(self.staticMemPower2.get() + float(numbers[0]))
        f = open(self.path_to_sniper_directory2  + "/sim.out", "r")
        while (l[0:5] != "  IPC"):
            l = f.readline()
        numbers = re.findall(r'\d+\.\d*', l)
        total = 0
        for i in range(len(numbers)):
            total = total + float(numbers[i])
        self.ipc2.set(float(total))
        
        if os.path.exists(os.path.join(self.path_to_sniper_directory1,"Greenchip.txt")):
            f = open(os.path.join(self.path_to_sniper_directory1,"Greenchip.txt"), "r")
            l = f.readlines()
            for i in range(len(l)):
                l[i] = l[i].split('//')[0].strip()

            self.dramArea2.set(float(l[0]))
            for i in self.comboboxEntriesDram:
                if l[1]==self.remove_source(i):
                    self.techNode4.set(i)
                    break
                    
            locTemp = utils.returnListLoc(l[2], self.energyData)
            if locTemp is not None:
                self.locCPU2['values'] = locTemp
                self.locCPU2.set(l[2])
            locTemp = utils.returnListLoc(l[3], self.energyData)
            if locTemp is not None:
                self.locDRAM2['values'] = locTemp
                self.locDRAM2.set(l[3])
            locTemp = utils.returnListLoc(l[4], self.energyData)
            if locTemp is not None:
                self.locUse2['values'] = locTemp
                self.locUse2.set(l[4])

        self.plot_mini()

    def export_indifference(self, *args):

        config1, config2 = self.verify_input()
        if config1 is None:
            return
        breakeven_export_name = filedialog.asksaveasfilename(defaultextension=".csv")
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        resE = chip_breakeven_IPC(config_dicts, False, self.increment1)['chipVsChipBreakevenInDays']
        resC = chip_breakeven_IPC(config_dicts, True, self.increment1)['chipVsChipBreakevenInDays']

        arrE = utils.perform_greenchip_analysis(resE)
        arrC = utils.perform_greenchip_analysis(resC)
        with open(breakeven_export_name, "w") as indiff_writer:
            indiff_writer.write("GreenChip SimVis Tool Version " + str(settingsConfig.version) + " Output\n-\n")

            indiff_writer.write("Input Parameters:\n")
            indiff_writer.write("Category, System1, System2\n")
            indiff_writer.write("Chip Area (mm^2),"+str(config1['chipArea'])+","+str(config2['chipArea'])+"\n")
            indiff_writer.write("Dyn. Power (Processor+Caches)(W)," +
                                str(config1['dynamicPower'])+","+str(config2['dynamicPower'])+"\n")
            indiff_writer.write("Static Power (Processor+Caches)(W)," +
                                str(config1['staticPower'])+","+str(config2['staticPower'])+"\n")
            indiff_writer.write("Instructions-Per-Cycle,"+str(config1['IPC'])+","+str(config2['IPC'])+"\n")
            indiff_writer.write("Technology Node (nm),"+str(config1['processSize'])+","+str(config2['processSize'])+"\n")
            
            indiff_writer.write("Chip Area (mm^2),"+str(config1['chipAreaDram'])+","+str(config2['chipAreaDram'])+"\n")           
            indiff_writer.write("Dyn. Memory Power (W)," +
                                str(config1['dynamicMemory'])+","+str(config2['dynamicMemory'])+"\n")
            indiff_writer.write("Static Memory Power (W)," +
                                str(config1['staticMemory'])+","+str(config2['staticMemory'])+"\n")
            indiff_writer.write("Technology Node (nm),"+str(config1['processSizeDram'])+","+str(config2['processSizeDram'])+"\n")

            if self.varC.get()==1:
                indiff_writer.write("CPU Manufacturing Location,"+str(config1['LocationManu CPU'])+","+str(config2['LocationManu CPU'])+"\n")
                indiff_writer.write("DRAM Manufacturing Location,"+str(config1['LocationManu DRAM'])+","+str(config2['LocationManu DRAM'])+"\n")
                indiff_writer.write("Use Phase Location,"+str(config1['Carbon Use Phase Loc'])+","+str(config2['Carbon Use Phase Loc'])+"\n")                
                
            indiff_writer.write("Note: Infinite indifference times are represented with the value '-42': \n\n")
            
            if self.varE.get()==1:
                if self.varC.get()==1:
                    indiff_writer.write("-\Indifference Time (Days): \n")
                    indiff_writer.write("Active Percent, Sleep Percent, Indifference Days (Energy), Indifference Days (Carbon)\n")
                    for a in range(0, len(arrC)):
                        for b in range(0, len(arrC[0])):
                            indiff_writer.write(str(a*self.increment1)+","+str(b*self.increment1)+","+str(arrE[a][b])+","+str(arrC[a][b])+"\n")
                if self.varC.get()==0:
                    indiff_writer.write("-\Indifference Time (Days): \n")
                    indiff_writer.write("Active Percent, Sleep Percent, Indifference Days (Energy)\n")
                    for a in range(0, len(arrE)):
                        for b in range(0, len(arrE[0])):
                            indiff_writer.write(str(a*self.increment1)+","+str(b*self.increment1)+","+str(arrE[a][b])+"\n")
            else:
                indiff_writer.write("-\Indifference Time (Days): \n")
                indiff_writer.write("Active Percent, Sleep Percent, Indifference Days (Carbon)\n")
                for a in range(0, len(arrC)):
                    for b in range(0, len(arrC[0])):
                        indiff_writer.write(str(a*self.increment1)+","+str(b*self.increment1)+","+str(arrC[a][b])+"\n")

        messagebox.showinfo("Done", "The exportation process has completed.")


    def export_breakeven(self, *args):

        config1, config2 = self.verify_input()
        if config1 is None:
            return
        breakeven_export_name = filedialog.asksaveasfilename(defaultextension=".csv")
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        resE = chip_breakeven_IPC(config_dicts, False, self.increment1)['upgradeDays']
        resC = chip_breakeven_IPC(config_dicts, True, self.increment1)['upgradeDays']

        arrE = utils.perform_greenchip_analysis(resE)
        arrC = utils.perform_greenchip_analysis(resC)
        with open(breakeven_export_name, "w") as indiff_writer:
            indiff_writer.write("GreenChip SimVis Tool Version " + str(settingsConfig.version) + " Output\n-\n")

            indiff_writer.write("Input Parameters:\n")
            indiff_writer.write("Category, System1, System2\n")
            indiff_writer.write("Chip Area (mm^2),"+str(config1['chipArea'])+","+str(config2['chipArea'])+"\n")
            indiff_writer.write("Dyn. Power (Processor+Caches)(W)," +
                                str(config1['dynamicPower'])+","+str(config2['dynamicPower'])+"\n")
            indiff_writer.write("Static Power (Processor+Caches)(W)," +
                                str(config1['staticPower'])+","+str(config2['staticPower'])+"\n")
            indiff_writer.write("Instructions-Per-Cycle,"+str(config1['IPC'])+","+str(config2['IPC'])+"\n")
            indiff_writer.write("Technology Node (nm),"+str(config1['processSize'])+","+str(config2['processSize'])+"\n")                    
            
            indiff_writer.write("Chip Area (mm^2),"+str(config1['chipAreaDram'])+","+str(config2['chipAreaDram'])+"\n")
            indiff_writer.write("Dyn. Memory Power (W)," +
                                str(config1['dynamicMemory'])+","+str(config2['dynamicMemory'])+"\n")
            indiff_writer.write("Static Memory Power (W)," +
                                str(config1['staticMemory'])+","+str(config2['staticMemory'])+"\n")
            indiff_writer.write("Technology Node (nm),"+str(config1['processSizeDram'])+","+str(config2['processSizeDram'])+"\n")

            if self.varC.get()==1:
                indiff_writer.write("CPU Manufacturing Location,"+str(config1['LocationManu CPU'])+","+str(config2['LocationManu CPU'])+"\n")
                indiff_writer.write("DRAM Manufacturing Location,"+str(config1['LocationManu DRAM'])+","+str(config2['LocationManu DRAM'])+"\n")
                indiff_writer.write("Use Phase Location,"+str(config1['Carbon Use Phase Loc'])+","+str(config2['Carbon Use Phase Loc'])+"\n")                

            indiff_writer.write("Note: Infinite breakeven times are represented with the value '-42': \n\n")
            
            if self.varE.get()==1:
                if self.varC.get()==1:
                    indiff_writer.write("-\Breakeven Time (Days): \n")
                    indiff_writer.write("Active Percent, Sleep Percent, Breakeven Days (Energy), Breakeven Days (Carbon)\n")
                    for a in range(0, len(arrC)):
                        for b in range(0, len(arrC[0])):
                            indiff_writer.write(str(a*self.increment1)+","+str(b*self.increment1)+","+str(arrE[a][b])+","+str(arrC[a][b])+"\n")
                if self.varC.get()==0:
                    indiff_writer.write("-\Breakeven Time (Days): \n")
                    indiff_writer.write("Active Percent, Sleep Percent, Breakeven Days (Energy)\n")
                    for a in range(0, len(arrE)):
                        for b in range(0, len(arrE[0])):
                            indiff_writer.write(str(a*self.increment1)+","+str(b*self.increment1)+","+str(arrE[a][b])+"\n")
            else:
                indiff_writer.write("-\Breakeven Time (Days): \n")
                indiff_writer.write("Active Percent, Sleep Percent, Breakeven Days (Carbon)\n")
                for a in range(0, len(arrC)):
                    for b in range(0, len(arrC[0])):
                        indiff_writer.write(str(a*self.increment1)+","+str(b*self.increment1)+","+str(arrC[a][b])+"\n")
        
        messagebox.showinfo("Done", "The exportation process has completed.")

    def launch_config(self):
		
        slidersFile = settingsConfig.slidersFile
        self.comboboxEntriesDram = ['3 (IMEC/DTCO, CMOS)', '6 (IMEC/DTCO, CMOS)', '7 EUV (IMEC/DTCO, CMOS)', '7 193i (IMEC/DTCO, CMOS)', '8 EUV (IMEC/DTCO, CMOS)', '8 193i (IMEC/DTCO, CMOS)', '10 (IMEC/DTCO, CMOS)', '12 (IMEC/DTCO, CMOS)'
                                    ,'14 (IMEC/DTCO, CMOS)', '20 (IMEC/DTCO, CMOS)', '28 (IMEC/DTCO, CMOS)', '30 (Higgs, CMOS)',
                                     '32 (Boyd, CMOS)', '45 (Boyd, CMOS)', '55 (Boyd, DRAM)', '57 (Boyd, DRAM)', '90 (Boyd, DRAM)', '130 (Boyd, DRAM)', '180 (Boyd, DRAM)', '250 (Boyd, DRAM)'] 
        self.window.geometry('1030x890')
        self.title1 = ttk.Entry(self.window, width=30)
        self.title2 = ttk.Entry(self.window, width=30)
        self.chipArea1 = Scale(self.window, from_=0, to=500, resolution=0.01, length = 250, width = 15, orient = HORIZONTAL)
        self.chipArea2 = Scale(self.window, from_=0, to=500, resolution=0.01, length = 250, width = 15, orient = HORIZONTAL)
        self.dynPower1 = Scale(self.window, from_=0, to=200, resolution=0.01, length = 250, width = 15, orient = HORIZONTAL)
        self.dynPower2 = Scale(self.window, from_=0, to=200, resolution=0.01, length = 250, width = 15, orient = HORIZONTAL)
        self.staticPower1 = Scale(self.window, from_=0, to=100, resolution=0.01, length = 250, width = 15, orient = HORIZONTAL)
        self.staticPower2 = Scale(self.window, from_=0, to=100, resolution=0.01, length = 250, width = 15, orient = HORIZONTAL)
        self.dynMemPower1 = Scale(self.window, from_=0, to=30, resolution=0.01, length = 250, width = 15, orient = HORIZONTAL)
        self.dynMemPower2 = Scale(self.window, from_=0, to=30, resolution=0.01, length = 250, width = 15, orient = HORIZONTAL)
        self.staticMemPower1 = Scale(self.window, from_=0, to=30, resolution=0.01, length = 250, width = 15, orient = HORIZONTAL)
        self.staticMemPower2 = Scale(self.window, from_=0, to=30, resolution=0.01, length = 250, width = 15, orient = HORIZONTAL)
        self.ipc1 = Scale(self.window, from_=0, to=20, resolution=0.01, width = 15, length = 250, orient = HORIZONTAL)
        self.ipc2 = Scale(self.window, from_=0, to=20, resolution=0.01, width = 15, length = 250, orient = HORIZONTAL)
        self.freq1 = Scale(self.window, from_=0, to=5, resolution=0.01, width = 15, length = 250, orient = HORIZONTAL)
        self.freq2 = Scale(self.window, from_=0, to=5, resolution=0.01, width = 15, length = 250, orient = HORIZONTAL)
        self.cycles1 = ttk.Entry(self.window, width=30)
        self.cycles2 = ttk.Entry(self.window, width=30)
        self.layers1 = ttk.Entry(self.window, width=30)
        self.layers2 = ttk.Entry(self.window, width=30)
        self.dramArea1 = Scale(self.window, from_=0, to=200, resolution=0.01, length = 250, width = 15, orient = HORIZONTAL)
        self.dramArea2 = Scale(self.window, from_=0, to=200, resolution=0.01, length = 250, width = 15, orient = HORIZONTAL)

        if slidersFile is not None:
            with open(slidersFile, "r") as settingsObject:
                for line in settingsObject:
                    linevars = line.split(" ")
                    if (linevars[0][0]=='#'):
                        continue;
                    if (len(linevars[0].strip())==0):
                        continue;   
                    if (len(linevars)!=4):
                         messagebox.showerror("Error", "Incorrect number of variables!")
                    if (linevars[0].upper()=="CHIPAREA1"):
                        self.chipArea1 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="CHIPAREA2"):
                        self.chipArea2 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="DYNAMICPOWER1"):
                        self.dynPower1 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="DYNAMICPOWER2"):
                        self.dynPower2 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="STATICPOWER1"):
                        self.staticPower1 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="STATICPOWER2"):
                        self.staticPower2 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="DYNAMICMEMORYPOWER1"):
                        self.dynMemPower1 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="DYNAMICMEMORYPOWER2"):
                        self.dynMemPower2 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="STATICMEMORYPOWER1"):
                        self.staticMemPower1 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="STATICMEMORYPOWER2"):
                        self.staticMemPower1 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="IPC1"):
                        self.ipc1 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="IPC2"):
                        self.ipc2 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="FREQUENCY1"):
                        self.freq1 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="FREQUENCY2"):
                        self.freq2 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="DRAMCHIPAREA1"):
                        self.dramArea1 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
                    if (linevars[0].upper()=="DRAMCHIPAREA2"):
                        self.dramArea2 = Scale(self.window, from_=linevars[1], to=linevars[2], resolution=linevars[3], length = 250, width = 20, orient = HORIZONTAL)
        
        self.techNode1 = ttk.Combobox(self.window, textvariable=StringVar(), values=high_process_energies_with_sources)
        self.techNode1.current(0)
        self.techNode2 = ttk.Combobox(self.window, textvariable=StringVar(), values=high_process_energies_with_sources)
        self.techNode2.current(0)
        self.techNode3 = ttk.Combobox(self.window, textvariable=StringVar(), values=self.comboboxEntriesDram)
        self.techNode3.current(14)
        self.techNode4 = ttk.Combobox(self.window, textvariable=StringVar(), values=self.comboboxEntriesDram)
        self.techNode4.current(14)
        
        countryOptions = []
        for row in self.energyData:
            if row[0] != '':
                countryOptions.append(row[0])
            
        self.locCPU1 = ttk.Combobox(self.window, textvariable=StringVar(), values=countryOptions)
        self.locCPU1.bind("<<ComboboxSelected>>", self.updateDropdown)
        self.locCPU2 = ttk.Combobox(self.window, textvariable=StringVar(), values=countryOptions)
        self.locCPU2.bind("<<ComboboxSelected>>", self.updateDropdown)

        self.locDRAM1 = ttk.Combobox(self.window, textvariable=StringVar(), values=countryOptions)
        self.locDRAM1.bind("<<ComboboxSelected>>", self.updateDropdown)
        self.locDRAM2 = ttk.Combobox(self.window, textvariable=StringVar(), values=countryOptions)
        self.locDRAM2.bind("<<ComboboxSelected>>", self.updateDropdown)

        self.locUse1 = ttk.Combobox(self.window, textvariable=StringVar(), values=countryOptions)
        self.locUse1.bind("<<ComboboxSelected>>", self.updateDropdown)
        self.locUse2 = ttk.Combobox(self.window, textvariable=StringVar(), values=countryOptions)
        self.locUse2.bind("<<ComboboxSelected>>", self.updateDropdown)

        #self.title_label = ttk.Label(self.window, text='Labels:')
        #self.title_label.grid(column=0, row=0, sticky=(N, W, E, S))
        #self.title1.grid(column=1, row=0, sticky=(N, W, E, S))
        #self.title2.grid(column=2, row=0, sticky=(N, W, E, S))

        
        self.system1_label = ttk.Label(self.window, text='System 1', font='Helvetica 15 bold underline')
        self.system1_label.grid(column=1, row=0, sticky=(N))
        
        self.system2_label = ttk.Label(self.window, text='System 2', font='Helvetica 15 bold underline')
        self.system2_label.grid(column=2, row=0, sticky=(N))
        
        self.bplt = StringVar()
        self.iplt = StringVar()
        
        self.breakevenplt_label = ttk.Label(self.window, textvariable=self.bplt, font='Helvetica 15 bold underline')
        self.indifferenceplt_label = ttk.Label(self.window, textvariable=self.iplt, font='Helvetica 15 bold underline')
        
        self.processor_label = ttk.Label(self.window, text='Processors:', font='Helvetica 13 bold')
        self.processor_label.grid(column=0, row=1, sticky=(NW))
        
        self.chipArea_label = ttk.Label(self.window, text='Chip Area (mm^2):')
        self.chipArea_label.grid(column=0, row=2, sticky=(SW))
        self.chipArea1.grid(column=1, row=2, sticky=(SW))
        self.chipArea2.grid(column=2, row=2, sticky=(SW))
        self.balloon.bind(self.chipArea_label, "Area of the processor die in mm^2")

        self.dynPower_label = ttk.Label(self.window, text='Dynamic Power (Including Caches)(W): ')
        self.dynPower_label.grid(column=0, row=3, sticky=(SW))
        self.dynPower1.grid(column=1, row=3, sticky=(SW))
        self.dynPower2.grid(column=2, row=3, sticky=(SW))
        self.balloon.bind(self.dynPower_label, "Dynamic Power is the major component of the power dissipated in circuits and also contributes to the peak power. \n It is a function of the supply voltage, the switching frequency and the output load. ")

        self.staticPower_label = ttk.Label(self.window, text='Static Power (Including Caches)(W): ')
        self.staticPower_label.grid(column=0, row=4, sticky=(SW))
        self.staticPower1.grid(column=1, row=4, sticky=(SW))
        self.staticPower2.grid(column=2, row=4, sticky=(SW))
        self.balloon.bind(self.staticPower_label, "Static Power is comprised of leakage, or current that flows through the transistor when there is no activity.")

        self.ipc_label = ttk.Label(self.window, text='IPC :')
        self.ipc_label.grid(column=0, row=5, sticky=(SW))
        self.ipc1.grid(column=1, row=5, sticky=(SW))
        self.ipc2.grid(column=2, row=5, sticky=(SW))
        self.balloon.bind(self.ipc_label, "IPC stands for instructions per cycle/clock. This tells you how many things a CPU can do in one cycle.")

        self.freq_label = ttk.Label(self.window, text='Clock Frequency (GHz):')
        self.freq_label.grid(column=0, row=6, sticky=(SW))
        self.freq1.grid(column=1, row=6, sticky=(SW))
        self.freq2.grid(column=2, row=6, sticky=(SW))
        self.balloon.bind(self.freq_label, "This is the frequency of the CPU in gigahertz. This tells you how many cycles the CPU can run in a second.")
        
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
        
        self.empty_label = ttk.Label(self.window, text='')
        self.empty_label.grid(column=0, row=7, sticky=(SW))
        
        self.techNode_label = ttk.Label(self.window, text='Technology Node (nm): ')
        self.techNode_label.grid(column=0, row=8, sticky=(SW))
        self.techNode1.grid(column=1, row=8, sticky=(N, W, E, S))
        self.techNode2.grid(column=2, row=8, sticky=(N, W, E, S))
        self.balloon.bind(self.techNode_label, "The technology node (also process node, process technology or simply node) \n refers to a specific semiconductor manufacturing process and its design rules. \n Different nodes often imply different circuit generations and architectures.")
        
        self.empty_labelD1 = ttk.Label(self.window, text='')
        self.empty_labelD1.grid(column=0, row=9, sticky=(SW))
        
        self.dram_label = ttk.Label(self.window, text='DRAM:', font='Helvetica 13 bold')
        self.dram_label.grid(column=0, row=10, sticky=(NW))
        
        self.dramArea_label = ttk.Label(self.window, text='Chip Area (mm^2):')
        self.dramArea_label.grid(column=0, row=11, sticky=(SW))
        self.dramArea1.grid(column=1, row=11, sticky=(SW))
        self.dramArea2.grid(column=2, row=11, sticky=(SW))
        self.balloon.bind(self.dramArea_label, "Total area of all DRAM die in mm^2")
        
        self.dynMem_label = ttk.Label(self.window, text='Dynamic Power (W):')
        self.dynMem_label.grid(column=0, row=12, sticky=(SW))
        self.dynMemPower1.grid(column=1, row=12, sticky=(SW))
        self.dynMemPower2.grid(column=2, row=12, sticky=(SW))
        self.balloon.bind(self.dynMem_label, "Dynamic Power for DRAM. This is exta power consumed by DRAM when the CPU is active")

        self.staticMem_label = ttk.Label(self.window, text='Static Power (W):')
        self.staticMem_label.grid(column=0, row=13, sticky=(SW))
        self.staticMemPower1.grid(column=1, row=13, sticky=(SW))
        self.staticMemPower2 .grid(column=2, row=13, sticky=(SW))
        self.balloon.bind(self.staticMem_label, "Static Power for DRAM. This is the power consumed by the DRAM when it is on.")
        
        self.empty_labelD2 = ttk.Label(self.window, text='')
        self.empty_labelD2.grid(column=0, row=14, sticky=(SW))
        
        self.techNode_label = ttk.Label(self.window, text='Technology Node (nm): ')
        self.techNode_label.grid(column=0, row=15, sticky=(SW))
        self.techNode3.grid(column=1, row=15, rowspan=1, sticky=(N, W, E, S))
        self.techNode4.grid(column=2, row=15, rowspan=1, sticky=(N, W, E, S))
        self.balloon.bind(self.techNode_label, "The technology node (also process node, process technology or simply node) \n refers to a specific semiconductor manufacturing process and its design rules. \n Different nodes often imply different circuit generations and architectures.")

        self.empty_labelE1 = ttk.Label(self.window, text='')
        self.empty_labelE1.grid(column=0, row=16, sticky=(SW))

        self.GridMix_label = ttk.Label(self.window, text='Grid Mixes:', font='Helvetica 13 bold')
        self.GridMix_label.grid(column=0, row=17, sticky=(NW))
        
        self.empty_labelE2 = ttk.Label(self.window, text='')
        self.empty_labelE2.grid(column=0, row=18, sticky=(SW))

        self.locCPU_label = ttk.Label(self.window, text='Energy Grid Mix By Location for CPU: ')
        self.locCPU_label.grid(column=0, row=19, sticky=(SW))
        
        self.locCPU1.grid(column=1, row=19, sticky=(N, W, E, S))
        self.locCPU2.grid(column=2, row=19, sticky=(N, W, E, S))

        self.locDRAM_label = ttk.Label(self.window, text='Energy Grid Mix By Location for DRAM: ')
        self.locDRAM_label.grid(column=0, row=20, sticky=(SW))

        self.locDRAM1.grid(column=1, row=20, sticky=(N, W, E, S))
        self.locDRAM2.grid(column=2, row=20, sticky=(N, W, E, S))

        self.locUse_label = ttk.Label(self.window, text='Energy Grid Mix By Location for Use Phase: ')
        self.locUse_label.grid(column=0, row=21, sticky=(SW))

        self.locUse1.grid(column=1, row=21, sticky=(N, W, E, S))
        self.locUse2.grid(column=2, row=21, sticky=(N, W, E, S))

        self.empty_labelC1 = ttk.Label(self.window, text='')
        self.empty_labelC2 = ttk.Label(self.window, text='')
        self.empty_labelC3 = ttk.Label(self.window, text='')
        self.empty_labelC4 = ttk.Label(self.window, text='')
        self.empty_labelC5 = ttk.Label(self.window, text='')
        self.empty_labelC6 = ttk.Label(self.window, text='')
        self.empty_labelC7 = ttk.Label(self.window, text='')
        self.empty_labelC8 = ttk.Label(self.window, text='')
        self.empty_labelC9 = ttk.Label(self.window, text='')


        self.empty_labelE3 = ttk.Label(self.window, text='')
        self.empty_labelE3.grid(column=0, row=41, sticky=(SW))

        self.empty_labelE4 = ttk.Label(self.window, text='')
        self.empty_labelE4.grid(column=0, row=42, sticky=(SW))
        
        self.plotbtn_label = ttk.Label(self.window, text='Plot Generators', font='Helvetica 15 bold underline')
        self.plotbtn_label.grid(column=0, row=43, sticky=(N))
        
        self.csvbtn_label = ttk.Label(self.window, text='CSV Generators', font='Helvetica 15 bold underline')
        self.csvbtn_label.grid(column=1, row=43, sticky=(N))
        
        self.importancebtn_label = ttk.Label(self.window, text='Importance Calculators', font='Helvetica 15 bold underline')
        self.importancebtn_label.grid(column=2, row=43, sticky=(N))

        self.plotButton1 = ttk.Button(self.window, text="Create Breakeven Plot(s)", command=self.plot_breakeven)
        self.balloon.bind(self.plotButton1, 'Creates a plot for the breakeven times at different sleep and activity ratios when upgrading from System 1 to System 2.')
        self.plotButton1.grid(column=0, row=45, sticky=(N)) 
        

        self.plotButton2 = ttk.Button(self.window, text="Create Indifference Plot(s)", command=self.plot_indifference)
        self.balloon.bind(self.plotButton2, 'Creates a plot for the indifference times at different sleep and activity ratios for System 1 and System 2.')
        self.plotButton2.grid(column=0, row=46, sticky=(N))
        
        self.recentlychecked = 'E'
        
        self.indiffRow = 10
        
        def energyChecker():
            if self.varE.get()==0 and self.varC.get()==0:
                messagebox.showerror(title = "No Output", message = "Please enable at least one output method.", icon = "error")
                self.varE.set(1)
                return
                
            oldchecked = self.recentlychecked
            
            if self.varE.get()==1: self.recentlychecked = 'E'
            else: self.recentlychecked = 'C'
            
            if oldchecked!=self.recentlychecked: self.plot_mini()

		
        def dramChecker():
            self.plot_mini()
            if self.varD.get()==1:
                if self.varC.get()==1:
                    self.window.geometry("1030x890")
                    self.empty_labelE1.grid(column=0, row=16, sticky=(SW))
                    self.GridMix_label.grid(column=0, row=17, sticky=(NW))                
                    self.empty_labelE2.grid(column=0, row=18, sticky=(SW))

                    self.locCPU_label.grid(column=0, row=19, sticky=(SW))
                    self.locDRAM_label.grid(column=0, row=20, sticky=(SW))
                    self.locUse_label.grid(column=0, row=21, sticky=(SW))
                    
                    self.locCPU1.grid(column=1, row=19, sticky=(N, W, E, S))
                    self.locCPU2.grid(column=2, row=19, sticky=(N, W, E, S))
                    self.locDRAM1.grid(column=1, row=20, sticky=(N, W, E, S))
                    self.locDRAM2.grid(column=2, row=20, sticky=(N, W, E, S))
                    self.locUse1.grid(column=1, row=21, sticky=(N, W, E, S))
                    self.locUse2.grid(column=2, row=21, sticky=(N, W, E, S))
                    
                    self.empty_labelE3.grid(column=0, row=41, sticky=(SW))
                    self.empty_labelE4.grid(column=0, row=42, sticky=(SW))               
                    self.plotbtn_label.grid(column=0, row=43, sticky=(N))                    
                    self.csvbtn_label.grid(column=1, row=43, sticky=(N))
                    self.importancebtn_label.grid(column=2, row=43, sticky=(N))
                    
                    self.plotButton1.grid(column=0, row=45, sticky=(N))                     
                    self.plotButton2.grid(column=0, row=46, sticky=(N))
                    self.plotButton3.grid(column=1, row=45, sticky=(N))
                    self.plotButton4.grid(column=1, row=46, sticky=(N))
                    self.plotButton5.grid(column=2, row=45, sticky=(N))
                    self.plotButton6.grid(column=2, row=46, sticky=(N))
                    self.plotButton7.grid(column=2, row=47, sticky=(N))
                    
                    self.mod_label.grid(column=0, row=50, sticky=(N))        
                    self.dramCheck.grid(column=0, row=51, sticky=(N))
                    self.energyCheck.grid(column=0, row=52, sticky=(N))
                    self.carbonCheck.grid(column=0, row=53, sticky=(N))
                    self.cfg_label.grid(column=1, row=50, sticky=(N))
                    self.plotButton8.grid(column=1, row=51, sticky=(N))
                    self.plotButton9.grid(column=1, row=52, sticky=(N))
                    
                    self.indiffRow = 10
                    if self.indifferenceplt_label in self.window.grid_slaves():
                        self.indifferenceplt_label.grid(column=3, row=self.indiffRow, sticky=(N))
                        
                else:
                    self.window.geometry("1030x760")
                    self.empty_labelE3.grid(column=0, row=20, sticky=(SW))
                    self.empty_labelE4.grid(column=0, row=21, sticky=(SW))               
                    self.plotbtn_label.grid(column=0, row=22, sticky=(N))                    
                    self.csvbtn_label.grid(column=1, row=22, sticky=(N))
                    self.importancebtn_label.grid(column=2, row=22, sticky=(N))
                    
                    self.plotButton1.grid(column=0, row=24, sticky=(N))                     
                    self.plotButton2.grid(column=0, row=25, sticky=(N))
                    self.plotButton3.grid(column=1, row=24, sticky=(N))
                    self.plotButton4.grid(column=1, row=25, sticky=(N))
                    self.plotButton5.grid(column=2, row=24, sticky=(N))
                    self.plotButton6.grid(column=2, row=25, sticky=(N))
                    self.plotButton7.grid(column=2, row=26, sticky=(N))
                    
                    self.mod_label.grid(column=0, row=29, sticky=(N))        
                    self.dramCheck.grid(column=0, row=30, sticky=(N))
                    self.energyCheck.grid(column=0, row=31, sticky=(N))
                    self.carbonCheck.grid(column=0, row=32, sticky=(N))
                    self.cfg_label.grid(column=1, row=29, sticky=(N))
                    self.plotButton8.grid(column=1, row=30, sticky=(N))
                    self.plotButton9.grid(column=1, row=31, sticky=(N))
                    
                    self.indiffRow = 11
                    if self.indifferenceplt_label in self.window.grid_slaves():
                        self.indifferenceplt_label.grid(column=3, row=self.indiffRow, sticky=(N))                       
                
                self.empty_labelD1.grid(column=0, row=9, sticky=(SW))
                self.dram_label.grid(column=0, row=10, sticky=(NW))
                self.dramArea_label.grid(column=0, row=11, sticky=(SW))
                self.dramArea1.grid(column=1, row=11, sticky=(SW))
                self.dramArea2.grid(column=2, row=11, sticky=(SW))                
                self.dynMem_label.grid(column=0, row=12, sticky=(SW))
                self.dynMemPower1.grid(column=1, row=12, sticky=(SW))
                self.dynMemPower2.grid(column=2, row=12, sticky=(SW))
                self.staticMem_label.grid(column=0, row=13, sticky=(SW))
                self.staticMemPower1.grid(column=1, row=13, sticky=(SW))
                self.staticMemPower2 .grid(column=2, row=13, sticky=(SW))                
                self.empty_labelD2.grid(column=0, row=14, sticky=(SW))
                self.techNode_label.grid(column=0, row=15, sticky=(SW))
                self.techNode3.grid(column=1, row=15, rowspan=1, sticky=(N, W, E, S))
                self.techNode4.grid(column=2, row=15, rowspan=1, sticky=(N, W, E, S))
                
            else:
                self.empty_labelD1.grid_remove()
                self.empty_labelD2.grid_remove()
                self.dram_label.grid_remove()
                self.dramArea_label.grid_remove()
                self.dramArea1.grid_remove()
                self.dramArea2.grid_remove()   
                self.dynMem_label.grid_remove()
                self.dynMemPower1.grid_remove()
                self.dynMemPower2.grid_remove()
                self.staticMem_label.grid_remove()
                self.staticMemPower1.grid_remove()
                self.staticMemPower2.grid_remove() 
                self.techNode_label.grid_remove()
                self.techNode3.grid_remove()
                self.techNode4.grid_remove()

                self.locDRAM_label.grid_remove()
                self.locDRAM1.grid_remove()
                self.locDRAM2.grid_remove()
                
                if self.varC.get()==1:
                    self.window.geometry("1030x650")
                    self.empty_labelE1.grid(column=0, row=9, sticky=(SW))
                    self.GridMix_label.grid(column=0, row=10, sticky=(NW))                
                    self.empty_labelE2.grid(column=0, row=11, sticky=(SW))

                    self.locCPU_label.grid(column=0, row=12, sticky=(SW))
                    self.locUse_label.grid(column=0, row=14, sticky=(SW))
                    
                    self.locCPU1.grid(column=1, row=12, sticky=(N, W, E, S))
                    self.locCPU2.grid(column=2, row=12, sticky=(N, W, E, S))
                    self.locUse1.grid(column=1, row=14, sticky=(N, W, E, S))
                    self.locUse2.grid(column=2, row=14, sticky=(N, W, E, S))
                    
                    self.empty_labelE3.grid(column=0, row=18, sticky=(SW))
                    self.empty_labelE4.grid(column=0, row=19, sticky=(SW))               
                    self.plotbtn_label.grid(column=0, row=20, sticky=(N))                    
                    self.csvbtn_label.grid(column=1, row=20, sticky=(N))
                    self.importancebtn_label.grid(column=2, row=20, sticky=(N))
                    
                    self.plotButton1.grid(column=0, row=22, sticky=(N))                     
                    self.plotButton2.grid(column=0, row=23, sticky=(N))
                    self.plotButton3.grid(column=1, row=22, sticky=(N))
                    self.plotButton4.grid(column=1, row=23, sticky=(N))
                    self.plotButton5.grid(column=2, row=22, sticky=(N))
                    self.plotButton6.grid(column=2, row=23, sticky=(N))
                    self.plotButton7.grid(column=2, row=24, sticky=(N))
                    
                    self.mod_label.grid(column=0, row=25, sticky=(N))        
                    self.dramCheck.grid(column=0, row=26, sticky=(N))
                    self.energyCheck.grid(column=0, row=27, sticky=(N))
                    self.carbonCheck.grid(column=0, row=28, sticky=(N))
                    self.cfg_label.grid(column=1, row=25, sticky=(N))
                    self.plotButton8.grid(column=1, row=26, sticky=(N))
                    self.plotButton9.grid(column=1, row=27, sticky=(N))
                    
                    self.indiffRow = 10
                    if self.indifferenceplt_label in self.window.grid_slaves():
                        self.indifferenceplt_label.grid(column=3, row=self.indiffRow, sticky=(N)) 
                
                else:
                    self.window.geometry("1030x630")
                    self.empty_labelE3.grid(column=0, row=9, sticky=(SW))
                    self.empty_labelE4.grid(column=0, row=10, sticky=(SW))               
                    self.plotbtn_label.grid(column=0, row=11, sticky=(N))                    
                    self.csvbtn_label.grid(column=1, row=11, sticky=(N))
                    self.importancebtn_label.grid(column=2, row=11, sticky=(N))
                    
                    self.plotButton1.grid(column=0, row=13, sticky=(N))                     
                    self.plotButton2.grid(column=0, row=14, sticky=(N))
                    self.plotButton3.grid(column=1, row=13, sticky=(N))
                    self.plotButton4.grid(column=1, row=14, sticky=(N))
                    self.plotButton5.grid(column=2, row=13, sticky=(N))
                    self.plotButton6.grid(column=2, row=14, sticky=(N))
                    self.plotButton7.grid(column=2, row=15, sticky=(N))
                    
                    self.mod_label.grid(column=0, row=16, sticky=(N))        
                    self.dramCheck.grid(column=0, row=17, sticky=(N))
                    self.energyCheck.grid(column=0, row=18, sticky=(N))
                    self.carbonCheck.grid(column=0, row=19, sticky=(N))
                    self.cfg_label.grid(column=1, row=16, sticky=(N))
                    self.plotButton8.grid(column=1, row=17, sticky=(N))
                    self.plotButton9.grid(column=1, row=18, sticky=(N))
                    
                    self.indiffRow = 10
                    if self.indifferenceplt_label in self.window.grid_slaves():
                        self.indifferenceplt_label.grid(column=3, row=self.indiffRow, sticky=(N))                   

        def carbonChecker():            
            if self.varE.get()==0 and self.varC.get()==0:
                messagebox.showerror(title = "No Output", message = "Please enable at least one output method.", icon = "error")
                self.varC.set(1)
                return
            elif self.varC.get()==0:
                self.empty_labelE1.grid_remove()
                self.GridMix_label.grid_remove()
                self.empty_labelE2.grid_remove()

                if self.varD.get()==0:
                    self.window.geometry('1030x630')
                    self.empty_labelE3.grid(column=0, row=9, sticky=(SW))
                    self.empty_labelE4.grid(column=0, row=10, sticky=(SW))               
                    self.plotbtn_label.grid(column=0, row=11, sticky=(N))                    
                    self.csvbtn_label.grid(column=1, row=11, sticky=(N))
                    self.importancebtn_label.grid(column=2, row=11, sticky=(N))
                    
                    self.plotButton1.grid(column=0, row=13, sticky=(N))                     
                    self.plotButton2.grid(column=0, row=14, sticky=(N))
                    self.plotButton3.grid(column=1, row=13, sticky=(N))
                    self.plotButton4.grid(column=1, row=14, sticky=(N))
                    self.plotButton5.grid(column=2, row=13, sticky=(N))
                    self.plotButton6.grid(column=2, row=14, sticky=(N))
                    self.plotButton7.grid(column=2, row=15, sticky=(N))
                    
                    self.mod_label.grid(column=0, row=16, sticky=(N))        
                    self.dramCheck.grid(column=0, row=17, sticky=(N))
                    self.energyCheck.grid(column=0, row=18, sticky=(N))
                    self.carbonCheck.grid(column=0, row=19, sticky=(N))
                    self.cfg_label.grid(column=1, row=16, sticky=(N))
                    self.plotButton8.grid(column=1, row=17, sticky=(N))
                    self.plotButton9.grid(column=1, row=18, sticky=(N))
                    
                    self.indiffRow = 10
                    if self.indifferenceplt_label in self.window.grid_slaves():
                        self.indifferenceplt_label.grid(column=3, row=self.indiffRow, sticky=(N))
                    
                else:
                    self.window.geometry('1030x760')
                    self.empty_labelE3.grid(column=0, row=20, sticky=(SW))
                    self.empty_labelE4.grid(column=0, row=21, sticky=(SW))               
                    self.plotbtn_label.grid(column=0, row=22, sticky=(N))                    
                    self.csvbtn_label.grid(column=1, row=22, sticky=(N))
                    self.importancebtn_label.grid(column=2, row=22, sticky=(N))
                    
                    self.plotButton1.grid(column=0, row=24, sticky=(N))                     
                    self.plotButton2.grid(column=0, row=25, sticky=(N))
                    self.plotButton3.grid(column=1, row=24, sticky=(N))
                    self.plotButton4.grid(column=1, row=25, sticky=(N))
                    self.plotButton5.grid(column=2, row=24, sticky=(N))
                    self.plotButton6.grid(column=2, row=25, sticky=(N))
                    self.plotButton7.grid(column=2, row=26, sticky=(N))
                    
                    self.mod_label.grid(column=0, row=29, sticky=(N))        
                    self.dramCheck.grid(column=0, row=30, sticky=(N))
                    self.energyCheck.grid(column=0, row=31, sticky=(N))
                    self.carbonCheck.grid(column=0, row=32, sticky=(N))
                    self.cfg_label.grid(column=1, row=29, sticky=(N))
                    self.plotButton8.grid(column=1, row=30, sticky=(N))
                    self.plotButton9.grid(column=1, row=31, sticky=(N))
                    
                    self.indiffRow = 11
                    if self.indifferenceplt_label in self.window.grid_slaves():
                        self.indifferenceplt_label.grid(column=3, row=self.indiffRow, sticky=(N)) 
                
                self.locCPU_label.grid_remove()
                self.locDRAM_label.grid_remove()
                self.locUse_label.grid_remove()

                self.locCPU1.grid_remove()
                self.locCPU2.grid_remove()
                self.locDRAM1.grid_remove()
                self.locDRAM2.grid_remove()
                self.locUse1.grid_remove()
                self.locUse2.grid_remove()
                
            elif self.varC.get()==1:
                if self.varD.get()==1:
                    self.window.geometry("1030x890")                   
                    self.locDRAM_label.grid(column=0, row=25, sticky=(SW))
                    self.locDRAM1.grid(column=1, row=25, sticky=(N, W, E, S))
                    self.locDRAM2.grid(column=2, row=25, sticky=(N, W, E, S))
                    
                    self.empty_labelE3.grid(column=0, row=41, sticky=(SW))
                    self.empty_labelE4.grid(column=0, row=42, sticky=(SW))               
                    self.plotbtn_label.grid(column=0, row=43, sticky=(N))                    
                    self.csvbtn_label.grid(column=1, row=43, sticky=(N))
                    self.importancebtn_label.grid(column=2, row=43, sticky=(N))
                    
                    self.plotButton1.grid(column=0, row=45, sticky=(N))                     
                    self.plotButton2.grid(column=0, row=46, sticky=(N))
                    self.plotButton3.grid(column=1, row=45, sticky=(N))
                    self.plotButton4.grid(column=1, row=46, sticky=(N))
                    self.plotButton5.grid(column=2, row=45, sticky=(N))
                    self.plotButton6.grid(column=2, row=46, sticky=(N))
                    self.plotButton7.grid(column=2, row=47, sticky=(N))
                    
                    self.mod_label.grid(column=0, row=50, sticky=(N))        
                    self.dramCheck.grid(column=0, row=51, sticky=(N))
                    self.energyCheck.grid(column=0, row=52, sticky=(N))
                    self.carbonCheck.grid(column=0, row=53, sticky=(N))
                    self.cfg_label.grid(column=1, row=50, sticky=(N))
                    self.plotButton8.grid(column=1, row=51, sticky=(N))
                    self.plotButton9.grid(column=1, row=52, sticky=(N))
                    
                    self.indiffRow = 10
                    if self.indifferenceplt_label in self.window.grid_slaves():
                        self.indifferenceplt_label.grid(column=3, row=self.indiffRow, sticky=(N)) 


                    self.empty_labelE1.grid(column=0, row=21, sticky=(SW))
                    self.GridMix_label.grid(column=0, row=22, sticky=(NW))                
                    self.empty_labelE2.grid(column=0, row=23, sticky=(SW))

                    self.locCPU_label.grid(column=0, row=24, sticky=(SW))
                    self.locUse_label.grid(column=0, row=26, sticky=(SW))
                    
                    self.locCPU1.grid(column=1, row=24, sticky=(N, W, E, S))
                    self.locCPU2.grid(column=2, row=24, sticky=(N, W, E, S))
                    self.locUse1.grid(column=1, row=26, sticky=(N, W, E, S))
                    self.locUse2.grid(column=2, row=26, sticky=(N, W, E, S))
                
                else:
                    self.window.geometry("1030x650")
                    self.empty_labelE1.grid(column=0, row=9, sticky=(SW))
                    self.GridMix_label.grid(column=0, row=10, sticky=(NW))                
                    self.empty_labelE2.grid(column=0, row=11, sticky=(SW))

                    self.locCPU_label.grid(column=0, row=12, sticky=(SW))
                    self.locUse_label.grid(column=0, row=14, sticky=(SW))
                    
                    self.locCPU1.grid(column=1, row=12, sticky=(N, W, E, S))
                    self.locCPU2.grid(column=2, row=12, sticky=(N, W, E, S))
                    self.locUse1.grid(column=1, row=14, sticky=(N, W, E, S))
                    self.locUse2.grid(column=2, row=14, sticky=(N, W, E, S))
                    
                    self.empty_labelE3.grid(column=0, row=18, sticky=(SW))
                    self.empty_labelE4.grid(column=0, row=19, sticky=(SW))               
                    self.plotbtn_label.grid(column=0, row=20, sticky=(N))                    
                    self.csvbtn_label.grid(column=1, row=20, sticky=(N))
                    self.importancebtn_label.grid(column=2, row=20, sticky=(N))
                    
                    self.plotButton1.grid(column=0, row=22, sticky=(N))                     
                    self.plotButton2.grid(column=0, row=23, sticky=(N))
                    self.plotButton3.grid(column=1, row=22, sticky=(N))
                    self.plotButton4.grid(column=1, row=23, sticky=(N))
                    self.plotButton5.grid(column=2, row=22, sticky=(N))
                    self.plotButton6.grid(column=2, row=23, sticky=(N))
                    self.plotButton7.grid(column=2, row=24, sticky=(N))
                    
                    self.mod_label.grid(column=0, row=25, sticky=(N))        
                    self.dramCheck.grid(column=0, row=26, sticky=(N))
                    self.energyCheck.grid(column=0, row=27, sticky=(N))
                    self.carbonCheck.grid(column=0, row=28, sticky=(N))
                    self.cfg_label.grid(column=1, row=25, sticky=(N))
                    self.plotButton8.grid(column=1, row=26, sticky=(N))
                    self.plotButton9.grid(column=1, row=27, sticky=(N))
                    
                    self.indiffRow = 10
                    if self.indifferenceplt_label in self.window.grid_slaves():
                        self.indifferenceplt_label.grid(column=3, row=self.indiffRow, sticky=(N))                     
                               
            
            oldchecked = self.recentlychecked
            
            if self.varC.get()==1: self.recentlychecked = 'C'
            else: self.recentlychecked = 'E'
            
            if oldchecked!=self.recentlychecked: self.plot_mini()

        self.plotButton3 = ttk.Button(self.window, text="Export Indifference to .csv", command=self.export_indifference)
        self.balloon.bind(self.plotButton3, 'Exports the indifference data into a .csv file.')
        self.plotButton3.grid(column=1, row=45, sticky=(N))

        self.plotButton4 = ttk.Button(self.window, text="Export Breakeven to .csv", command=self.export_breakeven)
        self.balloon.bind(self.plotButton4, 'Exports the breakeven data into a .csv file.')
        self.plotButton4.grid(column=1, row=46, sticky=(N))

        self.plotButton5 = ttk.Button(self.window, text="Find Importance (Single Point Analysis)", command=self.single_point_analysis) # Creates button for single point analysis
        self.balloon.bind(self.plotButton5, 'Determines which variables have the highest impact on the breakeven time at a specified sleep and activity ratio.')
        self.plotButton5.grid(column=2, row=45, sticky=(N))

        self.plotButton6 = ttk.Button(self.window, text="Find Importance (Average Analysis)", command=self.average_analysis) # Creates button for average point analysis
        self.balloon.bind(self.plotButton6, 'Determines the relative impact of each variable on the breakeven time for a user specified region of sleep and activity ratios.')
        self.plotButton6.grid(column=2, row=46, sticky=(N))

        self.plotButton7 = ttk.Button(self.window, text="Find Importance (All Point Analysis)", command=self.total_analysis) # Creates button for all point analysis
        self.balloon.bind(self.plotButton7, 'Determines the relative impact of each variable on the breakeven time for all sleep and activity ratios.')
        self.plotButton7.grid(column=2, row=47, sticky=(N))

        self.mod_label = ttk.Label(self.window, text='Modifiers', font='Helvetica 15 bold underline')
        self.mod_label.grid(column=0, row=50, sticky=(N))        

        self.varD = IntVar()
        self.varD.set(True)
        self.dramCheck = ttk.Checkbutton(self.window, text="Enable DRAM", variable=self.varD, onvalue=1, offvalue=0, command=dramChecker)
        self.dramCheck.grid(column=0, row=51, sticky=(N))
        self.balloon.bind(self.dramCheck, 'If checked, DRAM settings will be provided, and will be included in all subsequent calculations')
        
        self.varE = IntVar()
        self.varE.set(True)
        self.energyCheck = ttk.Checkbutton(self.window, text="Enable Energy Outputs", variable=self.varE, onvalue=1, offvalue=0, command=energyChecker)
        self.energyCheck.grid(column=0, row=52, sticky=(N))
        self.balloon.bind(self.energyCheck, 'If checked, energy plots will be generated when you click "Create Breakeven Plot(s)" or "Create Indifference Plot(s)",\nand energy data will be included in any generated CSV files.')

        self.varC = IntVar()
        self.varC.set(True)
        self.carbonCheck = ttk.Checkbutton(self.window, text="Enable Carbons Outputs/Settings", variable=self.varC, onvalue=1, offvalue=0, command=carbonChecker)
        self.carbonCheck.grid(column=0, row=53, sticky=(N))
        self.balloon.bind(self.carbonCheck, 'If checked, carbon plots will be generated when you click "Create Breakeven Plot(s)" or "Create Indifference Plot(s)",\nand carbon data will be included in any generated CSV files.')
        
        self.cfg_label = ttk.Label(self.window, text='Sniper Inputs', font='Helvetica 15 bold underline')
        self.cfg_label.grid(column=1, row=50, sticky=(N))
        
        self.plotButton8 = ttk.Button(self.window, text="Select Sniper Data for System 1", command=self.browse_sniper_input1) # Creates button for sniper to inputs
        self.balloon.bind(self.plotButton8, 'This allows the user to specify an output directory for a sniper and mcpat run, and will set the values in System 1 accordingly')
        self.plotButton8.grid(column=1, row=51, sticky=(N))

        self.plotButton9 = ttk.Button(self.window, text="Select Sniper Data for System 2", command=self.browse_sniper_input2) # Creates button for sniper to inputs
        self.balloon.bind(self.plotButton9, 'This allows the user to specify an output directory for a sniper and mcpat run, and will set the values in System 2 accordingly')
        self.plotButton9.grid(column=1, row=52, sticky=(N))

        self.chipArea1.bind("<ButtonRelease-1>", self.plot_mini_indifference)
        self.chipArea2.bind("<ButtonRelease-1>", self.plot_mini)
        self.dynPower1.bind("<ButtonRelease-1>", self.plot_mini)
        self.dynPower2.bind("<ButtonRelease-1>", self.plot_mini)
        self.staticPower1.bind("<ButtonRelease-1>", self.plot_mini)
        self.staticPower2.bind("<ButtonRelease-1>", self.plot_mini)
        self.dynMemPower1.bind("<ButtonRelease-1>", self.plot_mini)
        self.dynMemPower2.bind("<ButtonRelease-1>", self.plot_mini)
        self.staticMemPower1.bind("<ButtonRelease-1>", self.plot_mini)
        self.staticMemPower2.bind("<ButtonRelease-1>", self.plot_mini)
        self.ipc1.bind("<ButtonRelease-1>", self.plot_mini)
        self.ipc2.bind("<ButtonRelease-1>", self.plot_mini)
        self.freq1.bind("<ButtonRelease-1>", self.plot_mini)
        self.freq2.bind("<ButtonRelease-1>", self.plot_mini)
        self.dramArea1.bind("<ButtonRelease-1>", self.plot_mini_indifference)
        self.dramArea2.bind("<ButtonRelease-1>", self.plot_mini)
        self.techNode1.bind("<<ComboboxSelected>>", self.plot_mini)
        self.techNode2.bind("<<ComboboxSelected>>", self.plot_mini)
        self.techNode3.bind("<<ComboboxSelected>>", self.plot_mini)
        self.techNode4.bind("<<ComboboxSelected>>", self.plot_mini)      

