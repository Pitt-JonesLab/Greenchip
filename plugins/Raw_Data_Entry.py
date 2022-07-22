__author__ = 'Donald Kline, Jr'

from plugins.shared.Utils import *
from plugins.shared.GreenChip import *
import plugins.shared.Config as settingsConfig
#import SimVis
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import Pmw
import csv
import os

class config(object):

    def __init__(self, root, DB, outdir):
        self.DB = DB
        self.root = root
        self.path_to_output_directory = outdir
        self.window = Toplevel(self.root)
        self.window.title('Raw Data Entry')
        self.balloon = Pmw.Balloon(self.window)
        lblballoon = self.balloon.component('label')
        lblballoon.config(background='white')
        #self.window.iconbitmap(r'Assets/greenchipicon.ico')
        self.window.geometry("500x100+0+0")
        self.energyData=[]
        fileDir=os.path.dirname(os.path.realpath('__file__'))
        filename=os.path.join(fileDir,'EnergyGridMix.csv')
        with open(filename, 'r') as file:
            reader=csv.reader(file)
            for row in reader:
                self.energyData.append(row)
             
        self.launch_config()
        
        
            
        #for row in self.energyData:
        #    print(row)
        

    @staticmethod
    def needs_DB():
        return False

    def remove_source(self, tech_node):
        i = 0
        while i<len(tech_node) and tech_node[i]!='(':
            i += 1
        if i!=len(tech_node):
            return tech_node[0:(i-1)]
        else:
            return tech_node

    def verify_input(self, *args):
        config1 = {}
        config2 = {}

        config1['layers'] = int(1)
        config2['layers'] = int(1)

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
            config1['IPC'] = float(self.ipc1.get())
            config2['IPC'] = float(self.ipc2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid IPC!")
            return None, None
            
        try:
            config1['Node Source'] = (self.nodeSource.get())
            config2['Node Source'] = (self.nodeSource2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Node Source!")
            return None, None
        
        
        try:
            techNode1 = self.remove_source(self.techNode1.get())
            techNode2 = self.remove_source(self.techNode2.get())
            config1['processSize'] = techNode1
            config2['processSize'] = techNode2
                
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid CPU Technology Node!")
            return None, None
            
        try:
            techNode1Num = self.techNode1.get().split(' ')[0]
            techNode2Num = self.techNode2.get().split(' ')[0]
            config1['processSizeNum'] = int (techNode1Num)
            config2['processSizeNum'] = int (techNode2Num)
            
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid CPU Technology Node!")
            return None, None
        

        try:
            config1['chipAreaDram'] = float(self.chipArea3.get())
            config2['chipAreaDram'] = float(self.chipArea4.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid DRAM Chip Area!")
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
            config1['FREQ'] = float(self.freq1.get())
            config2['FREQ'] = float(self.freq2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid IPC!")
            return None, None

        #try:
        #    config1['cycles'] = int(self.cycles1.get())
        #    config2['cycles'] = int(self.cycles2.get())
        #except (ValueError):
        #    messagebox.showinfo("Warning: Illegal Argument", "Invalid Cycles!")
        #    return

       

        # DRAM process size and energy
        try:
            #techNode1Num = self.techNode1.get().split(' ')[0]
            #techNode2Num = self.techNode2.get().split(' ')[0]
            techNode3Num = self.techNode3.get()
            techNode4Num = self.techNode4.get()
            config1['processSizeDram'] = (techNode3Num)    
            config2['processSizeDram'] = (techNode4Num)
            #config3['processSize'] = (techNode3Num)
            #config4['processSize'] = (techNode4Num)
                                    
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid DRAM Technology Node!")
            return None, None
         
        # DRAM process size
        try:
            #techNode1Num = self.techNode1.get().split(' ')[0]
            #techNode2Num = self.techNode2.get().split(' ')[0]
            techNode3Num = self.techNode3.get().split(' ')[0]
            techNode4Num = self.techNode4.get().split(' ')[0]
            config1['processSizeDramNum'] = int (techNode3Num)    
            config2['processSizeDramNum'] = int (techNode4Num)
            #config3['processSize'] = (techNode3Num)
            #config4['processSize'] = (techNode4Num)
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid DRAM Technology Node!")
            return None, None
                    
        try:
            config1['LocationManu CPU'] = (self.location.get())
            for row in self.energyData:
                if row[0] == self.location.get():
                    config1['CPU Carbon Value'] = int(row[1])
                    break
                    
            config2['LocationManu CPU'] = (self.location2.get())
            for row in self.energyData:
                if row[0] == self.location2.get():
                    config2['CPU Carbon Value'] = int(row[1])
                    break
                    
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Energy Grid Mix Location for CPU!")
            return None, None
                    
        try:
            config1['LocationManu DRAM'] = (self.location3.get())
            for row in self.energyData:
                if row[0] == self.location3.get():
                    config1['DRAM Carbon Value'] = int(row[1])
                    break
                    
            config2['LocationManu DRAM'] = (self.location4.get())
            for row in self.energyData:
                if row[0] == self.location4.get():
                    config2['DRAM Carbon Value'] = int(row[1])
                    break
        
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Energy Grid Mix Location for DRAM!")
            return None, None
        # Calculate total power for the lifetime of device. Comment it out for now. Replaced it by required input for each plot.  
        '''
        try:
            config1['Device Lifetime'] = float(self.lifetime1.get())
            config2['Device Lifetime'] = float(self.lifetime2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Device Lifetime!")
            return None, None
            
        try:
            config1['Usage/Day'] = float(self.usage1.get())
            config2['Usage/Day'] = float(self.usage2.get())
        except (ValueError):
            messagebox.showinfo("Warning: Illegal Argument", "Invalid Usage per day!")
            return None, None
        '''
        try:
            config1['Carbon Use Phase Loc'] = (self.location5.get())
            for row in self.energyData:
                if row[0] == self.location5.get():
                    config1['UsePh Carbon Value'] = int(row[1])
                    break
                    
            config2['Carbon Use Phase Loc'] = (self.location6.get())
            for row in self.energyData:
                if row[0] == self.location6.get():
                    config2['UsePh Carbon Value'] = int(row[1])
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
        config1['DRAM Energy'] = high_process_energies_DRAM[techNode3Num]['energy']
        config2['DRAM Energy'] = high_process_energies_DRAM[techNode4Num]['energy']
            
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
        
        
        #print (config1['LocationManu CPU'])
        #print (config2['LocationManu CPU'])
        #print (config1['LocationManu DRAM'])
        #print (config2['LocationManu DRAM'])
        #print (config1['Carbon Use Phase Loc'])
        #print (config2['Carbon Use Phase Loc'])
        
        return config1, config2

    def plot_indifference(self,*args):
        config1, config2 = self.verify_input(*args)
        if config1 is None:
            return
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        if self.varE.get()==1:
            res = chip_breakeven_IPC(config_dicts, False)['chipVsChipBreakevenInDays']
            utils.make_single_plot(self, config1, config2, self.title1.get(), self.title2.get(), res, 'Indifference Plot Energy')
        if self.varC.get()==1:
            res = chip_breakeven_IPC(config_dicts, True)['chipVsChipBreakevenInDays']
            utils.make_single_plot(self, config1, config2, self.title1.get(), self.title2.get(), res, 'Indifference Plot Carbon')        


    def plot_breakeven(self, *args):
        config1, config2 = self.verify_input(*args)
        if config1 is None:
            return
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        if self.varE.get()==1:
            res = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
            utils.make_single_plot(self, config1, config2, self.title1.get(), self.title2.get(), res, 'Breakeven Plot Energy')
        if self.varC.get()==1:
            res = chip_breakeven_IPC(config_dicts, True)['upgradeDays']
            utils.make_single_plot(self, config1, config2, self.title1.get(), self.title2.get(), res, 'Breakeven Plot Carbon')
        
    def export_indifference(self, *args):

        config1, config2 = self.verify_input()
        if config1 is None:
            return
        breakeven_export_name = filedialog.asksaveasfilename(defaultextension=".csv")
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)
        res = chip_breakeven_IPC(config_dicts, False)['chipVsChipBreakevenInDays']

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
            indiff_writer.write("Instructions-Per-Cycle,"+str(config1['IPC'])+","+str(config2['IPC'])+"\n")
            indiff_writer.write("Node Source,"+str(config1['Node Source'])+","+str(config2['Node Source'])+"\n")
            indiff_writer.write("Technology Node (nm),"+str(config1['processSize'])+","+str(config2['processSize'])+"\n")
            
            indiff_writer.write("Chip Area (mm^2),"+str(config1['chipAreaDram'])+","+str(config2['chipAreaDram'])+"\n")           
            indiff_writer.write("Dyn. Memory Power (W)," +
                                str(config1['dynamicMemory'])+","+str(config2['dynamicMemory'])+"\n")
            indiff_writer.write("Static Memory Power (W)," +
                                str(config1['staticMemory'])+","+str(config2['staticMemory'])+"\n")
            indiff_writer.write("Technology Node (nm),"+str(config1['processSizeDram'])+","+str(config2['processSizeDram'])+"\n")

            indiff_writer.write("Energy Grid Mix By Location,"+str(config1['Energy Grid Mix By Location'])+","+str(config2['Energy Grid Mix By Location'])+"\n")
            
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
        res = chip_breakeven_IPC(config_dicts, False)['upgradeDays']

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
            indiff_writer.write("Instructions-Per-Cycle,"+str(config1['IPC'])+","+str(config2['IPC'])+"\n")
            indiff_writer.write("Node Source,"+str(config1['Node Source'])+","+str(config2['Node Source'])+"\n")
            indiff_writer.write("Technology Node (nm),"+str(config1['processSize'])+","+str(config2['processSize'])+"\n")                    
            
            indiff_writer.write("Chip Area (mm^2),"+str(config1['chipAreaDram'])+","+str(config2['chipAreaDram'])+"\n")
            indiff_writer.write("Dyn. Memory Power (W)," +
                                str(config1['dynamicMemory'])+","+str(config2['dynamicMemory'])+"\n")
            indiff_writer.write("Static Memory Power (W)," +
                                str(config1['staticMemory'])+","+str(config2['staticMemory'])+"\n")
            indiff_writer.write("Technology Node (nm),"+str(config1['processSizeDram'])+","+str(config2['processSizeDram'])+"\n")

            indiff_writer.write("Energy Grid Mix By Location,"+str(config1['Energy Grid Mix By Location'])+","+str(config2['Energy Grid Mix By Location'])+"\n")

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

    def changeOptions(self, event):
        option=event.widget.get()
        # print(option) 
        comboboxTempEntries = list(high_process_energies.keys())
        self.comboboxEntries.clear()
        self.comboboxEntries.append('')
        if option == "All":
            self.comboboxEntries = self.comboboxEntries + high_process_energies_with_sources
        elif option == "Boyd":
            for entry in comboboxTempEntries:
                if entry == '32':
                    self.comboboxEntries.append('32')
                elif entry == '45':
                    self.comboboxEntries.append('45')
                elif entry == '65':
                    self.comboboxEntries.append('65')
                elif entry == '90':
                    self.comboboxEntries.append('90') 
                elif entry == '130':
                    self.comboboxEntries.append('130')
                elif entry == '180':
                    self.comboboxEntries.append('180')
                elif entry == '250':
                    self.comboboxEntries.append('250')
                elif entry == '350':
                    self.comboboxEntries.append('350')
        elif option == "IMEC/DTCO":
            for entry in comboboxTempEntries:
                if entry == '3':
                    self.comboboxEntries.append('3')
                elif entry == '5':
                    self.comboboxEntries.append('5')
                elif entry == '6':
                    self.comboboxEntries.append('6')
                elif entry == '7 EUV':
                    self.comboboxEntries.append('7 EUV')
                elif entry == '7 193i':
                    self.comboboxEntries.append('7 193i')
                elif entry == '8 EUV':
                    self.comboboxEntries.append('8 EUV')
                elif entry == '8 193i':
                    self.comboboxEntries.append('8 193i')
                elif entry == '10':
                    self.comboboxEntries.append('10')
                elif entry == '12':
                    self.comboboxEntries.append('12')
                elif entry == '14':
                    self.comboboxEntries.append('14')
                elif entry == '20':
                    self.comboboxEntries.append('20')
                elif entry == '28':
                    self.comboboxEntries.append('28')
        elif option == "Higgs":
            for entry in comboboxTempEntries:
                if entry == '30':
                    self.comboboxEntries.append('30')
        #elif option == "DRAM":
        #    for entry in comboboxTempEntries:
        #        if entry == '55':
        #            self.comboboxEntries.append('55')
        #       elif entry == '57':
        #           self.comboboxEntries.append('57')
                
        self.techNode1['values'] = self.comboboxEntries 
        self.techNode1.current(0)
        #self.techNode2['values'] = self.comboboxEntries 
        #self.techNode2.current(0)
        #self.techNode3['values'] = self.comboboxEntries2 
        #self.techNode3.current(0)
        #self.techNode4['values'] = self.comboboxEntries2 
        #self.techNode4.current(0)
        
    def changeOptions2(self, event):
        option=event.widget.get()
        # print(option) 
        comboboxTempEntries = list(high_process_energies.keys())
        self.comboboxEntries2.clear()
        self.comboboxEntries2.append('')
        if option == "All":
            self.comboboxEntries2 = self.comboboxEntries2 + high_process_energies_with_sources
        elif option == "Boyd":
            for entry in comboboxTempEntries:
                if entry == '32':
                    self.comboboxEntries2.append('32')
                elif entry == '45':
                    self.comboboxEntries2.append('45')
                elif entry == '65':
                    self.comboboxEntries2.append('65')
                elif entry == '90':
                    self.comboboxEntries2.append('90') 
                elif entry == '130':
                    self.comboboxEntries2.append('130')
                elif entry == '180':
                    self.comboboxEntries2.append('180')
                elif entry == '250':
                    self.comboboxEntries2.append('250')
                elif entry == '350':
                    self.comboboxEntries2.append('350')
        elif option == "IMEC/DTCO":
            for entry in comboboxTempEntries:
                if entry == '3':
                    self.comboboxEntries2.append('3')
                elif entry == '5':
                    self.comboboxEntries2.append('5')
                elif entry == '6':
                    self.comboboxEntries2.append('6')
                elif entry == '7 EUV':
                    self.comboboxEntries2.append('7 EUV')
                elif entry == '7 193i':
                    self.comboboxEntries2.append('7 193i')
                elif entry == '8 EUV':
                    self.comboboxEntries2.append('8 EUV')
                elif entry == '8 193i':
                    self.comboboxEntries2.append('8 193i')
                elif entry == '10':
                    self.comboboxEntries2.append('10')
                elif entry == '12':
                    self.comboboxEntries2.append('12')
                elif entry == '14':
                    self.comboboxEntries2.append('14')
                elif entry == '20':
                    self.comboboxEntries2.append('20')
                elif entry == '28':
                    self.comboboxEntries2.append('28')
        elif option == "Higgs":
            for entry in comboboxTempEntries:
                if entry == '30':
                    self.comboboxEntries2.append('30')
        #elif option == "DRAM":
        #    for entry in comboboxTempEntries:
        #        if entry == '55':
        #            self.comboboxEntries.append('55')
        #       elif entry == '57':
        #           self.comboboxEntries.append('57')
                
        #self.techNode1['values'] = self.comboboxEntries 
        #self.techNode1.current(0)
        self.techNode2['values'] = self.comboboxEntries2 
        self.techNode2.current(0)
        #self.techNode3['values'] = self.comboboxEntries2 
        #self.techNode3.current(0)
        #self.techNode4['values'] = self.comboboxEntries2 
        #self.techNode4.current(0)
    
    def total_analysis(self, *args):
        config1, config2 = self.verify_input(*args)
        if config1 is None:
            return
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2)

        difference = [0,0,0,0,0]
        original = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
        old = config2['chipArea']
        config2['chipArea'] = config2['chipArea'] - (.01 * config2['chipArea'])
        mod = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
        difference[0] = self.total_gradient(original, mod)
        config2['chipArea'] = old

        old = config2['dynamicPower']
        config2['dynamicPower'] = config2['dynamicPower'] - (.01 * config2['dynamicPower'])
        mod = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
        difference[1] = self.total_gradient(original, mod)
        config2['dynamicPower'] = old

        old = config2['staticPower']
        config2['staticPower'] = config2['staticPower'] - (.01 * config2['staticPower'])
        mod = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
        difference[2] = self.total_gradient(original, mod)
        config2['staticPower'] = old

        old = config2['dynamicMemory']
        config2['dynamicMemory'] = config2['dynamicMemory'] - (.01 * config2['dynamicMemory'])
        mod = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
        difference[3] = self.total_gradient(original, mod)
        config2['dynamicMemory'] = old
        
        old = config2['staticMemory']
        config2['staticMemory'] = config2['staticMemory'] - (.01 * config2['staticMemory'])
        mod = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
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
        original = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
        old = config2['chipArea']
        config2['chipArea'] = config2['chipArea'] - (.01 * config2['chipArea'])
        mod = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
        difference[0] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['chipArea'] = old

        old = config2['dynamicPower']
        config2['dynamicPower'] = config2['dynamicPower'] - (.01 * config2['dynamicPower'])
        mod = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
        difference[1] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['dynamicPower'] = old

        old = config2['staticPower']
        config2['staticPower'] = config2['staticPower'] - (.01 * config2['staticPower'])
        mod = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
        difference[2] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['staticPower'] = old

        old = config2['dynamicMemory']
        config2['dynamicMemory'] = config2['dynamicMemory'] - (.01 * config2['dynamicMemory'])
        mod = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
        difference[3] = self.average_gradient(Radius, Sleep, Activity, original, mod)
        config2['dynamicMemory'] = old
        
        old = config2['staticMemory']
        config2['staticMemory'] = config2['staticMemory'] - (.01 * config2['staticMemory'])
        mod = chip_breakeven_IPC(config_dicts, False)['upgradeDays']
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
        orig = chip_breakeven_IPC(config_dicts, False)['upgradeDays'][Sleep][Activity]
        old = config2['chipArea']
        config2['chipArea'] = config2['chipArea'] - (.01 * config2['chipArea'])
        difference[0] = orig - chip_breakeven_IPC(config_dicts, False)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['chipArea'] = old

        old = config2['dynamicPower']
        config2['dynamicPower'] = config2['dynamicPower'] - (.01 * config2['dynamicPower'])
        difference[1] = orig - chip_breakeven_IPC(config_dicts, False)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['dynamicPower'] = old

        old = config2['staticPower']
        config2['staticPower'] = config2['staticPower'] - (.01 * config2['staticPower'])
        difference[2] = orig - chip_breakeven_IPC(config_dicts, False)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['staticPower'] = old

        old = config2['dynamicMemory']
        config2['dynamicMemory'] = config2['dynamicMemory'] - (.01 * config2['dynamicMemory'])
        difference[3] = orig - chip_breakeven_IPC(config_dicts, False)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
        config2['dynamicMemory'] = old
        
        old = config2['staticMemory']
        config2['staticMemory'] = config2['staticMemory'] - (.01 * config2['staticMemory'])
        difference[4] = orig - chip_breakeven_IPC(config_dicts, False)['upgradeDays'][Sleep][Activity] # Measures gradient by using a 1% shift
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

        self.window.geometry('800x600')
        self.title1 = ttk.Entry(self.window, width=30)
        self.title2 = ttk.Entry(self.window, width=30)
        self.chipArea1 = ttk.Entry(self.window, width=30)
        self.chipArea2 = ttk.Entry(self.window, width=30)
        self.dynPower1 = ttk.Entry(self.window, width=30)
        self.dynPower2 = ttk.Entry(self.window, width=30)
        self.staticPower1 = ttk.Entry(self.window, width=30)
        self.staticPower2 = ttk.Entry(self.window, width=30)
        self.ipc1 = ttk.Entry(self.window, width=30)
        self.ipc2 = ttk.Entry(self.window, width=30)
        self.freq1 = ttk.Entry(self.window, width=30)
        self.freq2 = ttk.Entry(self.window, width=30)
        self.layers1 = ttk.Entry(self.window, width=30)
        self.layers2 = ttk.Entry(self.window, width=30)
        self.lifetime1 = ttk.Entry(self.window, width=30)
        self.lifetime2 = ttk.Entry(self.window, width=30)
        self.usage1 = ttk.Entry(self.window, width=30)
        self.usage2 = ttk.Entry(self.window, width=30)
        
        
        sourceOptions = ['All', 'Boyd', 'IMEC/DTCO', 'Higgs']
        self.nodeSource = ttk.Combobox(self.window, textvariable=StringVar(), values=sourceOptions)
        self.nodeSource.current(0)
        self.nodeSource.bind("<<ComboboxSelected>>", self.changeOptions)
        
        self.nodeSource2 = ttk.Combobox(self.window, textvariable=StringVar(), values=sourceOptions)
        self.nodeSource2.current(0)
        self.nodeSource2.bind("<<ComboboxSelected>>", self.changeOptions2)
                
        #self.comboboxEntries = ['32', '45', '55', '65', '90'] 
        self.comboboxEntries = [''] + high_process_energies_with_sources   
        self.comboboxEntries2 = [''] + high_process_energies_with_sources    
        # Change the values and match with high_process_energies_DRAM
        self.comboboxEntriesDram = ['', '55', '57', '90', '130', '180', '250'] 
        

                    
        self.techNode1 = ttk.Combobox(self.window, textvariable=StringVar(), values=self.comboboxEntries)
        self.techNode1.current(0)
        self.techNode2 = ttk.Combobox(self.window, textvariable=StringVar(), values=self.comboboxEntries2)
        self.techNode2.current(0)
        
        self.chipArea3 = ttk.Entry(self.window, width=30)
        self.chipArea4 = ttk.Entry(self.window, width=30)
        self.dynMemPower1 = ttk.Entry(self.window, width=30)
        self.dynMemPower2 = ttk.Entry(self.window, width=30)
        self.staticMemPower1 = ttk.Entry(self.window, width=30)
        self.staticMemPower2 = ttk.Entry(self.window, width=30)
        self.cycles1 = ttk.Entry(self.window, width=30)
        self.cycles2 = ttk.Entry(self.window, width=30)
        
        self.techNode3 = ttk.Combobox(self.window, textvariable=StringVar(), values=self.comboboxEntriesDram)
        self.techNode3.current(0)
        self.techNode4 = ttk.Combobox(self.window, textvariable=StringVar(), values=self.comboboxEntriesDram)
        self.techNode4.current(0)


        locationOptions = ['']
        for row in self.energyData:
            locationOptions.append(row[0])
        self.location = ttk.Combobox(self.window, textvariable=StringVar(), values=locationOptions)
        self.location.current(0)
        self.location2 = ttk.Combobox(self.window, textvariable=StringVar(), values=locationOptions)
        self.location2.current(0)
        
        locationOptions = ['']
        for row in self.energyData:
            locationOptions.append(row[0])
        self.location3 = ttk.Combobox(self.window, textvariable=StringVar(), values=locationOptions)
        self.location3.current(0)
        self.location4 = ttk.Combobox(self.window, textvariable=StringVar(), values=locationOptions)
        self.location4.current(0)
        
        locationOptions = ['']
        for row in self.energyData:
            locationOptions.append(row[0])
        self.location5 = ttk.Combobox(self.window, textvariable=StringVar(), values=locationOptions)
        self.location5.current(0)
        self.location6 = ttk.Combobox(self.window, textvariable=StringVar(), values=locationOptions)
        self.location6.current(0)
        #self.title_label = ttk.Label(self.window, text='Labels:')
        #self.title_label.grid(column=0, row=0, sticky=(N, W, E, S))
        #self.title1.grid(column=1, row=0, sticky=(N, W, E, S))
        #self.title2.grid(column=2, row=0, sticky=(N, W, E, S))
        
        self.system1_label = ttk.Label(self.window, text='System 1', font='Helvetica 15 bold underline')
        self.system1_label.grid(column=1, row=0, sticky=(N))
        
        self.system2_label = ttk.Label(self.window, text='System 2', font='Helvetica 15 bold underline')
        self.system2_label.grid(column=2, row=0, sticky=(N))
        
        self.processor_label = ttk.Label(self.window, text='Processors:', font='Helvetica 13 bold')
        self.processor_label.grid(column=0, row=1, sticky=(NW))

        self.chipArea_label = ttk.Label(self.window, text='Chip Area (mm^2):')
        self.chipArea_label.grid(column=0, row=2, sticky=(N, W, E, S))
        self.chipArea1.grid(column=1, row=2, sticky=(N, W, E, S))
        self.chipArea2.grid(column=2, row=2, sticky=(N, W, E, S))
        self.balloon.bind(self.chipArea_label, "Area of the processor die in mm^2")

        self.dynPower_label = ttk.Label(self.window, text='Dynamic Power (Including Caches)(W): ')
        self.dynPower_label.grid(column=0, row=3, sticky=(N, W, E, S))
        self.dynPower1.grid(column=1, row=3, sticky=(N, W, E, S))
        self.dynPower2.grid(column=2, row=3, sticky=(N, W, E, S))
        self.balloon.bind(self.dynPower_label, "Dynamic Power is the major component of the power dissipated in circuits and also contributes to the peak power. \n It is a function of the supply voltage, the switching frequency and the output load. ")

        self.staticPower_label = ttk.Label(self.window, text='Static Power (Including Caches)(W): ')
        self.staticPower_label.grid(column=0, row=4, sticky=(N, W, E, S))
        self.staticPower1.grid(column=1, row=4, sticky=(N, W, E, S))
        self.staticPower2.grid(column=2, row=4, sticky=(N, W, E, S))
        self.balloon.bind(self.staticPower_label, "Static Power is comprised of leakage, or current that flows through the transistor when there is no activity.")

        self.ipc_label = ttk.Label(self.window, text='IPC :')
        self.ipc_label.grid(column=0, row=5, sticky=(N, W, E, S))
        self.ipc1.grid(column=1, row=5, sticky=(N, W, E, S))
        self.ipc2.grid(column=2, row=5, sticky=(N, W, E, S))
        self.balloon.bind(self.ipc_label, "IPC stands for instructions per cycle/clock. This tells you how many things a CPU can do in one cycle.")
        #self.balloon.bind(self.ipc1.grid, "Tooltip text on grid")
        
        self.freq_label = ttk.Label(self.window, text='CPU Clock Frequency (GHz):')
        self.freq_label.grid(column=0, row=6, sticky=(N, W, E, S))
        self.freq1.grid(column=1, row=6, sticky=(N, W, E, S))
        self.freq2.grid(column=2, row=6, sticky=(N, W, E, S))
        self.balloon.bind(self.freq_label, "This is the frequency of the CPU in gigahertz. This is the frequency of the CPU in gigahertz. This tells you how many cycles the CPU can run in a second.")
        
        self.nodeSource_label = ttk.Label(self.window, text='Node Source: ')
        self.nodeSource_label.grid(column=0, row=7, sticky=(N, W, E, S))
        self.nodeSource.grid(column=1, row=7, sticky=(N, W, E, S))
        self.nodeSource2.grid(column=2, row=7, sticky=(N, W, E, S))
        self.balloon.bind(self.nodeSource_label, "The node source is the location from which data about the manufacuturing energy is pulled from.")
                
        self.techNode_label = ttk.Label(self.window, text='Technology Node (nm): ')
        self.techNode_label.grid(column=0, row=8, sticky=(N, W, E, S))
        self.techNode1.grid(column=1, row=8, sticky=(N, W, E, S))
        self.techNode2.grid(column=2, row=8, sticky=(N, W, E, S))
        self.balloon.bind(self.techNode_label, "The technology node (also process node, process technology or simply node) \n refers to a specific semiconductor manufacturing process and its design rules. \n Different nodes often imply different circuit generations and architectures.")
        
        self.empty_label = ttk.Label(self.window, text='')
        self.empty_label.grid(column=0, row=15, sticky=(SW))
        
        self.dram_label = ttk.Label(self.window, text='DRAM:', font='Helvetica 13 bold')
        self.dram_label.grid(column=0, row=16, sticky=(NW))
        
        self.chipArea2_label = ttk.Label(self.window, text='Chip Area (mm^2):')
        self.chipArea2_label.grid(column=0, row=17, sticky=(N, W, E, S))
        self.chipArea3.grid(column=1, row=17, sticky=(N, W, E, S))
        self.chipArea4.grid(column=2, row=17, sticky=(N, W, E, S))
        self.balloon.bind(self.chipArea2_label, "Total area of all DRAM die in mm^2")
        
        self.dynMem_label = ttk.Label(self.window, text='Dynamic Power (W):')
        self.dynMem_label.grid(column=0, row=18, sticky=(N, W, E, S))
        self.dynMemPower1.grid(column=1, row=18, sticky=(N, W, E, S))
        self.dynMemPower2.grid(column=2, row=18, sticky=(N, W, E, S))
        self.balloon.bind(self.dynMem_label, "Dyanamic Power for DRAM. This is exta power consumed by DRAM when the CPU is active")

        self.staticMem_label = ttk.Label(self.window, text='Static Power (W):')
        self.staticMem_label.grid(column=0, row=19, sticky=(N, W, E, S))
        self.staticMemPower1.grid(column=1, row=19, sticky=(N, W, E, S))
        self.staticMemPower2 .grid(column=2, row=19, sticky=(N, W, E, S))
        self.balloon.bind(self.staticMem_label, "Static Power for DRAM. This is the power consumed by the DRAM when it is on.")

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
        
        self.techNode2_label = ttk.Label(self.window, text='Technology Node (nm): ')
        self.techNode2_label.grid(column=0, row=20, sticky=(N, W, E, S))
        self.techNode3.grid(column=1, row=20, sticky=(N, W, E, S))
        self.techNode4.grid(column=2, row=20, sticky=(N, W, E, S))
        self.balloon.bind(self.techNode2_label, "The technology node (also process node, process technology or simply node) \n refers to a specific semiconductor manufacturing process and its design rules. \n Different nodes often imply different circuit generations and architectures.")
        
        self.empty_labelE = ttk.Label(self.window, text='')
        self.empty_labelE.grid(column=0, row=25, sticky=(N, W, E, S))
        
        self.gridMix_label = ttk.Label(self.window, text='Grid Mixes:', font='Helvetica 13 bold')
        self.gridMix_label.grid(column=0, row=26, sticky=(NW))
        
        # Calculate total power for the lifetime of device. Comment it out for now. Replaced it by required input for each plot.
        '''
        self.lifetime_label = ttk.Label(self.window, text='Lifetime of device (years): ')
        self.lifetime_label.grid(column=0, row=15, sticky=(N, W, E, S))
        self.lifetime1.grid(column=1, row=15, sticky=(N, W, E, S))
        self.lifetime2.grid(column=2, row=15, sticky=(N, W, E, S))
        self.balloon.bind(self.lifetime_label, " Lifetime of different devices in years")
        
        self.usage_label = ttk.Label(self.window, text='Usage per day (hours): ')
        self.usage_label.grid(column=0, row=16, sticky=(N, W, E, S))
        self.usage1.grid(column=1, row=16, sticky=(N, W, E, S))
        self.usage2.grid(column=2, row=16, sticky=(N, W, E, S))
        self.balloon.bind(self.usage_label, " How many hours a day is the device used")
        '''
        self.location_label1 = ttk.Label(self.window, text='Energy Grid Mix By Location for CPU: ')
        self.location_label1.grid(column=0, row=30, sticky=(N, W, E, S))
        self.location.grid(column=1, row=30, sticky=(N, W, E, S))
        self.location2.grid(column=2, row=30, sticky=(N, W, E, S))
        self.balloon.bind(self.location_label1, " Energy Grid Mix by location - 50 US states")
        
        self.location_label2 = ttk.Label(self.window, text='Energy Grid Mix By Location for DRAM: ')
        self.location_label2.grid(column=0, row=31, sticky=(N, W, E, S))
        self.location3.grid(column=1, row=31, sticky=(N, W, E, S))
        self.location4.grid(column=2, row=31, sticky=(N, W, E, S))
        self.balloon.bind(self.location_label2, " Energy Grid Mix by location - 50 US states")
        
        self.location_label3 = ttk.Label(self.window, text='Energy Grid Mix By Location for Use Phase: ')
        self.location_label3.grid(column=0, row=32, sticky=(N, W, E, S))
        self.location5.grid(column=1, row=32, sticky=(N, W, E, S))
        self.location6.grid(column=2, row=32, sticky=(N, W, E, S))
        self.balloon.bind(self.location_label3, " Energy Grid Mix by location - 50 US states")
        
        self.empty_label = ttk.Label(self.window, text='')
        self.empty_label.grid(column=0, row=33, sticky=(N, W, E, S))
        
        self.empty_label = ttk.Label(self.window, text='')
        self.empty_label.grid(column=0, row=34, sticky=(N, W, E, S))
        
        self.plotbtn_label = ttk.Label(self.window, text='Plot Generators', font='Helvetica 15 bold underline')
        self.plotbtn_label.grid(column=0, row=35, sticky=(N))
        
        self.plotButton1 = ttk.Button(self.window, text="Create Indifference Plot(s)", command=self.plot_indifference)
        self.balloon.bind(self.plotButton1, 'Creates a plot for the indifference times at different sleep and activity ratios for System 1 and System 2.')
        self.plotButton1.grid(column=0, row=36, sticky=(N))
        
        self.plotButton2 = ttk.Button(self.window, text="Create Breakeven Plot(s)", command=self.plot_breakeven)
        self.balloon.bind(self.plotButton2, 'Creates a plot for the breakeven times at different sleep and activity ratios when upgrading from System 1 to System 2.')
        self.plotButton2.grid(column=0, row=37, sticky=(N))

        def energyChecker():            
            if self.varE.get()==0 and self.varC.get()==0:
                messagebox.showerror(title = "No Output", message = "Please enable at least one output method.", icon = "error")
                self.varE.set(1)

        def carbonChecker():            
            if self.varE.get()==0 and self.varC.get()==0:
                messagebox.showerror(title = "No Output", message = "Please enable at least one output method.", icon = "error")
                self.varC.set(1)
            elif self.varC.get()==0:
                self.empty_labelE.grid_remove()
                self.gridMix_label.grid_remove()
                
                self.location_label1.grid_remove()
                self.location_label2.grid_remove()
                self.location_label3.grid_remove()

                self.location.grid_remove()
                self.location2.grid_remove()
                self.location3.grid_remove()
                self.location4.grid_remove()
                self.location5.grid_remove()
                self.location6.grid_remove()
                
            elif self.varC.get()==1:
                self.empty_labelE.grid(column=0, row=25, sticky=(N, W, E, S))
                self.gridMix_label.grid(column=0, row=26, sticky=(NW))

                self.location_label1.grid(column=0, row=30, sticky=(N, W, E, S))
                self.location_label2.grid(column=0, row=31, sticky=(N, W, E, S))
                self.location_label3.grid(column=0, row=32, sticky=(N, W, E, S))

                self.location.grid(column=1, row=30, sticky=(N, W, E, S))
                self.location2.grid(column=2, row=30, sticky=(N, W, E, S))
                self.location3.grid(column=1, row=31, sticky=(N, W, E, S))
                self.location4.grid(column=2, row=31, sticky=(N, W, E, S))
                self.location5.grid(column=1, row=32, sticky=(N, W, E, S))
                self.location6.grid(column=2, row=32, sticky=(N, W, E, S))


        self.varE = IntVar()
        self.varE.set(True)
        self.energyCheck = ttk.Checkbutton(self.window, text="Enable Energy Plots", variable=self.varE, onvalue=1, offvalue=0, command=energyChecker)
        self.energyCheck.grid(column=0, row=38, sticky=(N))
        self.balloon.bind(self.energyCheck, 'If checked, energy plots will be generated when you click "Create Breakeven Plot(s)" or "Create Indifference Plot(s)"')

        self.varC = IntVar()
        self.varC.set(True)
        self.carbonCheck = ttk.Checkbutton(self.window, text="Enable Carbons Plots/Settings", variable=self.varC, onvalue=1, offvalue=0, command=carbonChecker)
        self.carbonCheck.grid(column=0, row=39, sticky=(N))
        self.balloon.bind(self.carbonCheck, 'If checked, carbon plots will be generated when you click "Create Breakeven Plot(s)" or "Create Indifference Plot(s)"')
        
        self.csvbtn_label = ttk.Label(self.window, text='CSV Generators', font='Helvetica 15 bold underline')
        self.csvbtn_label.grid(column=1, row=35, sticky=(N))
        
        self.plotButton3 = ttk.Button(self.window, text="Export Indifference to .csv", command=self.export_indifference)
        self.balloon.bind(self.plotButton3, 'Exports the indifference data into a .csv file.')
        self.plotButton3.grid(column=1, row=36, sticky=(N))
        
        self.plotButton4 = ttk.Button(self.window, text="Export Breakeven to .csv", command=self.export_breakeven)
        self.balloon.bind(self.plotButton4, 'Exports the breakeven data into a .csv file.')
        self.plotButton4.grid(column=1, row=37, sticky=(N))
        
        self.importancebtn_label = ttk.Label(self.window, text='Importance Calculators', font='Helvetica 15 bold underline')
        self.importancebtn_label.grid(column=2, row=35, sticky=(N))
        
        self.plotButton5 = ttk.Button(self.window, text="Find Importance (Single Point Analysis)", command=self.single_point_analysis) # Creates button for single point analysis
        self.balloon.bind(self.plotButton5, 'Determines which variables have the highest impact on the breakeven time at a specified sleep and activity ratio.')
        self.plotButton5.grid(column=2, row=36, sticky=(N))
        
        self.plotButton6 = ttk.Button(self.window, text="Find Importance (Average Analysis)", command=self.average_analysis) # Creates button for average point analysis
        self.balloon.bind(self.plotButton6, 'Determines the relative impact of each variable on the breakeven time for a user specified region of sleep and activity ratios.')
        self.plotButton6.grid(column=2, row=37, sticky=(N))
        
        self.plotButton7 = ttk.Button(self.window, text="Find Importance (All Point Analysis)", command=self.total_analysis) # Creates button for all point analysis
        self.balloon.bind(self.plotButton7, 'Determines the relative impact of each variable on the breakeven time for all sleep and activity ratios.')
        self.plotButton7.grid(column=2, row=38, sticky=(N))
