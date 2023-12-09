import csv

import Pmw
from plugins.loaders import *
from plugins.shared.GreenChip import *
from plugins.shared.Utils import *


class config(object):

    def __init__(self, root, DB, outdir, increment, mindays, maxdays, minyears, maxyears, gridMixSettingsFilename = 'EnergyGridMix.csv'):
        self.DB = DB
        self.root = root
        self.increment = increment
        self.mindays = mindays
        self.maxdays = maxdays
        self.minyears = minyears
        self.maxyears = maxyears
        self.balloon = Pmw.Balloon(self.root)
        lblballoon = self.balloon.component('label')
        lblballoon.config(background='white')
        self.path_to_output_directory = outdir
        self.window = Toplevel(self.root)
        self.window.title('Indifference')
        self.window.protocol("WM_DELETE_WINDOW", self.window_exit)
        #self.window.iconbitmap(r'Assets/greenchipicon.ico')
        self.window.geometry("1275x180+0+0")
        self.energyData=[]
        filename=os.path.normpath(gridMixSettingsFilename)
        with open(filename, 'r') as file:
            reader=csv.reader(file)
            for row in reader:
               if row[0]!='Country': self.energyData.append(row)
        self.isOpen = True
        self.launch_config()

    @staticmethod
    def needs_DB():
        return True

    def window_exit(self):
        self.isOpen = False
        self.window.destroy()

    def calculateCarbon(self, row):
        sum = 0
        index = 2
        while index < 12:
            source =  int(row[index]) * float(row[index+10])
            sum += source
            index += 1
        return round(sum/100)

    def plot(self, *args):

        first_entry = utils.build_config(self.DB, self.entry1.get(), self.path_to_output_directory, writeMe=False, configNum=1)
        if first_entry is None:
            return
        second_entry = utils.build_config(self.DB, self.entry2.get(), self.path_to_output_directory, writeMe=False, configNum=2)
        if second_entry is None:
            return
        if self.varC.get() == 1:            
            try:
                first_entry['LocationManu CPU'] = self.locCPU1.get()
                for row in self.energyData:
                    if row[2] == '':
                        continue
                    if row[0] == self.locCPU1.get():
                        first_entry['CPU Carbon Value'] = self.calculateCarbon(row)
                        break
                    if row[1] == self.locCPU1.get():
                        first_entry['CPU Carbon Value'] = self.calculateCarbon(row)
                        break    
                second_entry['LocationManu CPU'] = self.locCPU2.get()
                for row in self.energyData:
                    if row[2] == '':
                        continue
                    if row[0] == self.locCPU2.get():
                        second_entry['CPU Carbon Value'] = self.calculateCarbon(row)
                        break
                    if row[1] == self.locCPU2.get():
                        second_entry['CPU Carbon Value'] = self.calculateCarbon(row)
                        break        
            except (ValueError):
                messagebox.showinfo("Warning: Illegal Argument", "Invalid Energy Grid Mix Location for CPU!")
                return None, None       
            if self.varD.get()==1:
                try:
                    first_entry['LocationManu DRAM'] = self.locDRAM1.get()
                    for row in self.energyData:
                        if row[2] == '':
                            continue
                        if row[0] == self.locDRAM1.get():
                            first_entry['DRAM Carbon Value'] = self.calculateCarbon(row)
                            break
                        if row[1] == self.locDRAM1.get():
                            first_entry['DRAM Carbon Value'] = self.calculateCarbon(row)
                            break     
                    second_entry['LocationManu DRAM'] = self.locDRAM2.get()
                    for row in self.energyData:
                        if row[2] == '':
                            continue
                        if row[0] == self.locDRAM2.get():
                            second_entry['DRAM Carbon Value'] = self.calculateCarbon(row)
                            break
                        if row[1] == self.locDRAM2.get():
                            second_entry['DRAM Carbon Value'] = self.calculateCarbon(row)
                            break

                except (ValueError):
                    messagebox.showinfo("Warning: Illegal Argument", "Invalid Energy Grid Mix Location for DRAM!")
                    return None, None
            else:
                first_entry['LocationManu DRAM'] = self.locCPU1.get()
                second_entry['LocationManu DRAM'] = self.locCPU2.get()
                first_entry['DRAM Carbon Value'] = 0
                second_entry['DRAM Carbon Value'] = 0

            try:
                first_entry['Carbon Use Phase Loc'] = (self.locUse1.get())
                for row in self.energyData:
                    if row[2] == '':
                        continue
                    if row[0] == self.locUse1.get():
                        first_entry['UsePh Carbon Value'] = self.calculateCarbon(row)
                        break
                    if row[1] == self.locUse1.get():
                        first_entry['UsePh Carbon Value'] = self.calculateCarbon(row)
                        break        
                second_entry['Carbon Use Phase Loc'] = (self.locUse2.get())
                for row in self.energyData:
                    if row[2] == '':
                        continue
                    if row[0] == self.locUse2.get():
                        second_entry['UsePh Carbon Value'] = self.calculateCarbon(row)
                        break
                    if row[1] == self.locUse2.get():
                        second_entry['UsePh Carbon Value'] = self.calculateCarbon(row)
                        break
                        
            except (ValueError):
                messagebox.showinfo("Warning: Illegal Argument", "Invalid Energy Grid Mix Location for Use Phase!")
                return None, None
            
        if self.varD.get()==1:
            if self.area1.get()=='' or self.area1.get() is None:
                messagebox.showerror("Warning: Illegal Argument", "Invalid Chip Area for System 1 DRAM! If you want to ignore DRAM, put an area of 0.")
                return None, None

            if self.area2.get()=='' or self.area2.get() is None:
                messagebox.showerror("Warning: Illegal Argument", "Invalid Chip Area for System 2 DRAM! If you want to ignore DRAM, put an area of 0.")
                return None, None
            

            first_entry['chipAreaDram'] = float(self.area1.get())
            second_entry['chipAreaDram'] = float(self.area2.get())

            def remove_source(tech_node):
                i = 0
                while i<len(tech_node) and tech_node[i]!='(':
                    i += 1
                if i!=len(tech_node):
                    return tech_node[0:(i-1)]
                else:
                    return tech_node
            
            if self.tech1.get()=='' or self.tech1.get() is None:
                if self.area1.get()=='0':
                    first_entry['processSizeDram'] = '55'
                else:
                    messagebox.showerror("Warning: Illegal Argument", "Invalid Technology Node for System 1 DRAM! If you want to ignore DRAM manufacturing, put an area of 0.")            
                    return None, None
            else:
                first_entry['processSizeDram'] = remove_source(self.tech1.get())
                
            if self.tech2.get()=='' or self.tech2.get() is None:
                if self.area2.get()=='0':
                    second_entry['processSizeDram'] = '55'
                else:
                    messagebox.showerror("Warning: Illegal Argument", "Invalid Technology Node for System 2 DRAM! If you want to ignore DRAM manufacturing, put an area of 0.")            
                    return None, None
            else:
                second_entry['processSizeDram'] = remove_source(self.tech2.get())
        
        else:
            first_entry['chipAreaDram'] = 0.0
            second_entry['chipAreaDram'] = 0.0
            first_entry['processSizeDram'] = '55'
            second_entry['processSizeDram'] = '55'
            

        techNode1 = str(first_entry['processSize'])
        techNode2 = str(second_entry['processSize'])
        techNode3Num = first_entry['processSizeDram']
        techNode4Num = second_entry['processSizeDram']
        

        ''' Add energy (Joules) manufacturing CPU '''
        first_entry['CPU Energy'] = high_process_energies[techNode1]['energy']
        second_entry['CPU Energy'] = high_process_energies[techNode2]['energy'] 
        first_entry['Total CPU Energy'] = simple_manufacturing(first_entry['CPU Energy'], first_entry['chipArea'], first_entry['layers'])
        second_entry['Total CPU Energy'] = simple_manufacturing(second_entry['CPU Energy'], second_entry['chipArea'], second_entry['layers'])
        if self.varC.get() == 1:
            first_entry['Total CPU Carbon'] = first_entry['Total CPU Energy'] /3600000 * first_entry['CPU Carbon Value']
            second_entry['Total CPU Carbon'] = second_entry['Total CPU Energy'] /3600000 * second_entry['CPU Carbon Value']
        
        ''' Add energy (Joules) manufacturing DRAM '''
        first_entry['DRAM Energy'] = high_process_energies_DRAM[techNode3Num]['energy']
        second_entry['DRAM Energy'] = high_process_energies_DRAM[techNode4Num]['energy']
            
        first_entry['Total DRAM Energy'] = simple_manufacturing(first_entry['DRAM Energy'], first_entry['chipAreaDram'], first_entry['layers'])
        second_entry['Total DRAM Energy'] = simple_manufacturing(second_entry['DRAM Energy'], second_entry['chipAreaDram'], second_entry['layers'])
        if self.varC.get() == 1: 
            first_entry['Total DRAM Carbon'] = first_entry['Total DRAM Energy'] /3600000 * first_entry['DRAM Carbon Value']
            second_entry['Total DRAM Carbon'] = second_entry['Total DRAM Energy'] /3600000 * second_entry['DRAM Carbon Value']
        
        # 
        if self.varC.get() == 1: 
            CPUWattHours = first_entry['dynamicPower'] + first_entry['staticPower'] #Power in Watts
            CPUKWattHours = CPUWattHours/1000
            first_entry['CPU Hourly Usage Carbon'] = CPUKWattHours * first_entry['CPU Carbon Value']
            
            CPUWattHours = second_entry['dynamicPower'] + second_entry['staticPower'] #Power in Watts
            CPUKWattHours = CPUWattHours/1000
            second_entry['CPU Hourly Usage Carbon'] = CPUKWattHours * second_entry['CPU Carbon Value']
                    
            DRAMWattHours = first_entry['dynamicMemory'] + first_entry['staticMemory']
            DRAMKWattHours = DRAMWattHours/1000
            first_entry['DRAM Hourly Usage Carbon'] = DRAMKWattHours * first_entry['DRAM Carbon Value']
            
            DRAMWattHours = second_entry['dynamicMemory'] + second_entry['staticMemory']
            DRAMKWattHours = DRAMWattHours/1000
            second_entry['DRAM Hourly Usage Carbon'] = DRAMKWattHours * second_entry['DRAM Carbon Value']
        
        config_dicts = []
        config_dicts.append(first_entry)
        config_dicts.append(second_entry)

        if self.varE.get()==1:
            res = chip_breakeven_IPC(config_dicts, False, self.increment)['chipVsChipBreakevenInDays']
            utils.make_single_plot(self, first_entry, second_entry, self.entry1.get(), self.entry2.get(), res, 'Indifference Plot Energy', self.increment, self.mindays, self.maxdays, self.minyears, self.maxyears)
        if self.varC.get()==1:
            if (second_entry['LocationManu DRAM'] == '' or second_entry['LocationManu CPU'] == '' or second_entry['Carbon Use Phase Loc'] == '' 
            or first_entry['LocationManu DRAM'] == '' or first_entry['LocationManu CPU'] == '' or first_entry['Carbon Use Phase Loc'] == ''):
                messagebox.showerror('Empty Grid Mix','Could not generate carbon plot due to empty Grid Mix(es)! Be sure to fill in all values.')
                return
            res = chip_breakeven_IPC(config_dicts, True, self.increment)['chipVsChipBreakevenInDays']
            utils.make_single_plot(self, first_entry, second_entry, self.entry1.get(), self.entry2.get(), res, 'Indifference Plot Carbon', self.increment, self.mindays, self.maxdays, self.minyears, self.maxyears)

    def launch_config(self):
        self.entries = self.DB.list_entries()
        self.entry1 = StringVar()
        self.entry2 = StringVar()
        self.locCPU1 = StringVar()
        self.locCPU2 = StringVar()
        self.locDRAM1 = StringVar()
        self.locDRAM2 = StringVar()
        self.locUse1 = StringVar()
        self.locUse2 = StringVar()
        self.area1 = StringVar()
        self.area2 = StringVar()
        self.tech1 = StringVar()
        self.tech2 = StringVar()

        self.sys1_label = ttk.Label(self.window, text="System 1:")
        self.sys1_label.grid(column=0, row=1)

        self.sys2_label = ttk.Label(self.window, text="System 2:")
        self.sys2_label.grid(column=0, row=2)

        self.file_label = ttk.Label(self.window, text="Input Data")
        self.file_label.grid(column=1, row=0)

        self.area_label = ttk.Label(self.window, text="DRAM Chip Area")
        self.area_label.grid(column=2, row=0)

        self.tech_label = ttk.Label(self.window, text="DRAM Technology Node")
        self.tech_label.grid(column=3, row=0)

        self.cpu_label = ttk.Label(self.window, text="CPU Manufacturing Location")

        self.dram_label = ttk.Label(self.window, text="DRAM Manufacturing Location")

        self.use_label = ttk.Label(self.window, text="Use Phase Location")
        
        self.area1_entry = ttk.Entry(self.window, width=30, textvariable = self.area1)
        self.area2_entry = ttk.Entry(self.window, width=30, textvariable = self.area2)

        self.area1_entry.grid(column=2, row=1)
        self.area2_entry.grid(column=2, row=2)

        self.lastLoadedArea1 = False
        self.lastLoadedArea2 = False
        
        self.lastLoadedTech1 = False
        self.lastLoadedTech2 = False
        
        self.lastLoadedLoc1 = False
        self.lastLoadedLoc2 = False

        countryOptions = []
        for row in self.energyData:
            if row[0] != '':
                countryOptions.append(row[0])
            
        dramOptions = ['3 (IMEC/DTCO, CMOS)', '6 (IMEC/DTCO, CMOS)', '7 EUV (IMEC/DTCO, CMOS)', '7 193i (IMEC/DTCO, CMOS)', '8 EUV (IMEC/DTCO, CMOS)', '8 193i (IMEC/DTCO, CMOS)', '10 (IMEC/DTCO, CMOS)', '12 (IMEC/DTCO, CMOS)'
                                    ,'14 (IMEC/DTCO, CMOS)', '20 (IMEC/DTCO, CMOS)', '28 (IMEC/DTCO, CMOS)', '30 (Higgs, CMOS)',
                                     '32 (Boyd, CMOS)', '45 (Boyd, CMOS)', '55 (Boyd, DRAM)', '57 (Boyd, DRAM)', '90 (Boyd, DRAM)', '130 (Boyd, DRAM)', '180 (Boyd, DRAM)', '250 (Boyd, DRAM)']

        self.Tech_Dropdown1 = ttk.Combobox(self.window, textvariable=self.tech1, values=dramOptions, width=30, state='readonly')
        self.Tech_Dropdown2 = ttk.Combobox(self.window, textvariable=self.tech2, values=dramOptions, width=30, state='readonly')

        self.Tech_Dropdown1.grid(column=3, row=1)
        self.Tech_Dropdown2.grid(column=3, row=2)

        def loadChangeArea1(a, b, c):
            self.lastLoadedArea1 = False

        def loadChangeArea2(a, b, c):
            self.lastLoadedArea2 = False

        def loadChangeTech1(event):
            self.lastLoadedTech1 = False

        def loadChangeTech2(event):
            self.lastLoadedTech2 = False
            
        def loadChangeLoc1(event):
            self.lastLoadedLoc1 = False
            utils.changeOptionsLoc(event, self.energyData)
            
        def loadChangeLoc2(event):
            self.lastLoadedLoc2 = False
            utils.changeOptionsLoc(event, self.energyData)
            
        self.area1.trace_add("write", loadChangeArea1)
        self.area2.trace_add("write", loadChangeArea2)

        self.Tech_Dropdown1.bind("<<ComboboxSelected>>", loadChangeTech1)
        self.Tech_Dropdown2.bind("<<ComboboxSelected>>", loadChangeTech2)
            
        def loader1(event):
            data_list = self.DB.get_item(self.entry1.get(), 'Greenchip.txt', greenchip_dict_loader)
            if data_list[0] is not None:
                self.area1.set(data_list[0][0])

                for i in dramOptions:
                    if i.split(' ')[0]==data_list[0][1] or i.split(' ')[0] + ' ' + i.split(' ')[1]==data_list[0][1]:                        
                        self.lastLoadedTech1 = True
                        self.tech1.set(i)
                        break
                
                locTemp = utils.returnListLoc(data_list[0][2], self.energyData)
                if locTemp is not None:
                    self.chip_box2['values'] = locTemp
                    self.chip_box2.set(data_list[0][2])
                    self.lastLoadedLoc1 = True 
                locTemp = utils.returnListLoc(data_list[0][3], self.energyData)
                if locTemp is not None:
                    self.chip_box4['values'] = locTemp
                    self.chip_box4.set(data_list[0][3])
                    self.lastLoadedLoc1 = True 
                locTemp = utils.returnListLoc(data_list[0][4], self.energyData)
                if locTemp is not None:
                    self.chip_box6['values'] = locTemp
                    self.chip_box6.set(data_list[0][4])
                    self.lastLoadedLoc1 = True 
   
                self.lastLoadedArea1 = True
            else:
                if self.lastLoadedArea1:
                    self.area1.set("")
                if self.lastLoadedTech1:
                    self.tech1.set("")
                if self.lastLoadedLoc1:
                    self.chip_box2['values'] = countryOptions
                    self.chip_box2.set('')
                    self.chip_box4['values'] = countryOptions
                    self.chip_box4.set('')
                    self.chip_box6['values'] = countryOptions
                    self.chip_box6.set('')
                    
                    
        def loader2(event):
            data_list = self.DB.get_item(self.entry2.get(), 'Greenchip.txt', greenchip_dict_loader)
            if data_list[0] is not None:
                self.area2.set(data_list[0][0])

                for i in dramOptions:
                    if i.split(' ')[0]==data_list[0][1] or i.split(' ')[0] + ' ' + i.split(' ')[1]==data_list[0][1]:                        
                        self.lastLoadedTech2 = True
                        self.tech2.set(i)
                        break

                locTemp = utils.returnListLoc(data_list[0][2], self.energyData)
                if locTemp is not None:
                    self.chip_box3['values'] = locTemp
                    self.chip_box3.set(data_list[0][2])
                    self.lastLoadedLoc2 = True 
                locTemp = utils.returnListLoc(data_list[0][3], self.energyData)
                if locTemp is not None:
                    self.chip_box5['values'] = locTemp
                    self.chip_box5.set(data_list[0][3])
                    self.lastLoadedLoc2 = True 
                locTemp = utils.returnListLoc(data_list[0][4], self.energyData)
                if locTemp is not None:
                    self.chip_box7['values'] = locTemp
                    self.chip_box7.set(data_list[0][4])
                    self.lastLoadedLoc2 = True 
   
                self.lastLoadedArea2 = True
            else:
                if self.lastLoadedArea2:
                    self.area2.set("")
                if self.lastLoadedTech2:
                    self.tech2.set("")
                if self.lastLoadedLoc2:
                    self.chip_box3['values'] = countryOptions
                    self.chip_box3.set('')
                    self.chip_box5['values'] = countryOptions
                    self.chip_box5.set('')
                    self.chip_box7['values'] = countryOptions
                    self.chip_box7.set('')

        self.chip_box0 = ttk.Combobox(self.window, textvariable=self.entry1, values=self.entries, width=30)
        self.chip_box0.current(0)
        self.chip_box0.grid(column=1, row=1, sticky=(N, W, E, S), columnspan=1)
        self.chip_box0.bind("<<ComboboxSelected>>", loader1)

        self.chip_box1 = ttk.Combobox(self.window, textvariable=self.entry2, values=self.entries, width=30)
        self.chip_box1.current(0)
        self.chip_box1.grid(column=1, row=2, sticky=(N, W, E, S), columnspan=1)
        self.chip_box1.bind("<<ComboboxSelected>>", loader2)

        self.chip_box2 = ttk.Combobox(self.window, textvariable=self.locCPU1, values=countryOptions)
        self.chip_box2.bind("<<ComboboxSelected>>", loadChangeLoc1)

        self.chip_box3 = ttk.Combobox(self.window, textvariable=self.locCPU2, values=countryOptions)
        self.chip_box3.bind("<<ComboboxSelected>>", loadChangeLoc2)

        self.chip_box4 = ttk.Combobox(self.window, textvariable=self.locDRAM1, values=countryOptions)
        self.chip_box4.bind("<<ComboboxSelected>>", loadChangeLoc1)

        self.chip_box5 = ttk.Combobox(self.window, textvariable=self.locDRAM2, values=countryOptions)
        self.chip_box5.bind("<<ComboboxSelected>>", loadChangeLoc2)

        self.chip_box6 = ttk.Combobox(self.window, textvariable=self.locUse1, values=countryOptions)
        self.chip_box6.bind("<<ComboboxSelected>>", loadChangeLoc1)

        self.chip_box7 = ttk.Combobox(self.window, textvariable=self.locUse2, values=countryOptions)
        self.chip_box7.bind("<<ComboboxSelected>>", loadChangeLoc2)

        self.cpu_label.grid(column=7, row=0)
        self.dram_label.grid(column=8, row=0)
        self.use_label.grid(column=9, row=0)

        self.chip_box2.grid(column=7, row=1, sticky=(N, W, E, S), columnspan=1)
        self.chip_box3.grid(column=7, row=2, sticky=(N, W, E, S), columnspan=1)
        self.chip_box4.grid(column=8, row=1, sticky=(N, W, E, S), columnspan=1)
        self.chip_box5.grid(column=8, row=2, sticky=(N, W, E, S), columnspan=1)
        self.chip_box6.grid(column=9, row=1, sticky=(N, W, E, S), columnspan=1)
        self.chip_box7.grid(column=9, row=2, sticky=(N, W, E, S), columnspan=1)

        loader1(None)
        loader2(None)
                
        self.plotButton = ttk.Button(self.window, text="Create Plot(s)", command=self.plot)
        self.plotButton.grid(column=10, row=1, rowspan=2, sticky=(N, W, E, S))
        
        def energyChecker():            
            if self.varE.get()==0 and self.varC.get()==0:
                messagebox.showerror(title = "No Output", message = "Please enable at least one output method.", icon = "error")
                self.varE.set(1)

        def dramChecker():
            if self.varD.get()==1:
                if self.varC.get()==1:
                    self.dram_label.grid(column=8, row=0)
                    self.chip_box4.grid(column=8, row=1, sticky=(N, W, E, S), columnspan=1)
                    self.chip_box5.grid(column=8, row=2, sticky=(N, W, E, S), columnspan=1)
                    self.window.geometry("1275x180")
                else:
                    self.window.geometry("775x180")

                self.area_label.grid(column=2, row=0)
                self.area1_entry.grid(column=2, row=1)
                self.area2_entry.grid(column=2, row=2)

                self.Tech_Dropdown1.grid(column=3, row=1)
                self.Tech_Dropdown2.grid(column=3, row=2)
                self.tech_label.grid(column=3, row=0)

            else:
                if self.varC.get()==1:
                    self.window.geometry("685x180")
                else:
                    self.window.geometry("365x180")

                self.area_label.grid_remove()
                self.area1_entry.grid_remove()
                self.area2_entry.grid_remove()

                self.Tech_Dropdown1.grid_remove()
                self.Tech_Dropdown2.grid_remove()
                self.tech_label.grid_remove()

                self.dram_label.grid_remove()
                self.chip_box4.grid_remove()
                self.chip_box5.grid_remove()

        def carbonChecker():            
            if self.varE.get()==0 and self.varC.get()==0:
                messagebox.showerror(title = "No Output", message = "Please enable at least one output method.", icon = "error")
                self.varC.set(1)
            if self.varC.get()==1:
                if self.varD.get()==1:
                    self.dram_label.grid(column=8, row=0)
                    self.chip_box4.grid(column=8, row=1, sticky=(N, W, E, S), columnspan=1)
                    self.chip_box5.grid(column=8, row=2, sticky=(N, W, E, S), columnspan=1)
                    self.window.geometry("1275x180")
                else:
                    self.window.geometry("685x180")
                self.cpu_label.grid(column=7, row=0)
                self.use_label.grid(column=9, row=0)

                self.chip_box2.grid(column=7, row=1, sticky=(N, W, E, S), columnspan=1)
                self.chip_box3.grid(column=7, row=2, sticky=(N, W, E, S), columnspan=1)
                self.chip_box6.grid(column=9, row=1, sticky=(N, W, E, S), columnspan=1)
                self.chip_box7.grid(column=9, row=2, sticky=(N, W, E, S), columnspan=1)
            else:
                if self.varD.get()==1:
                    self.window.geometry("775x180")
                else:
                    self.window.geometry("365x180")
                self.cpu_label.grid_remove()
                self.dram_label.grid_remove()
                self.use_label.grid_remove()

                self.chip_box2.grid_remove()
                self.chip_box3.grid_remove()
                self.chip_box4.grid_remove()
                self.chip_box5.grid_remove()
                self.chip_box6.grid_remove()
                self.chip_box7.grid_remove()

        self.varD = IntVar()
        self.varD.set(True)
        self.energyCheck = ttk.Checkbutton(self.window, text="Enable DRAM", variable=self.varD, onvalue=1, offvalue=0, command=dramChecker)
        self.energyCheck.grid(column=1, row=3, sticky=(N))
        self.balloon.bind(self.energyCheck, 'If checked, DRAM power will be factored in when you click "Create Plot(s)"')

        self.varE = IntVar()
        self.varE.set(True)
        self.energyCheck = ttk.Checkbutton(self.window, text="Enable Energy Plots", variable=self.varE, onvalue=1, offvalue=0, command=energyChecker)
        self.energyCheck.grid(column=1, row=4, sticky=(N))
        self.balloon.bind(self.energyCheck, 'If checked, energy plots will be generated when you click "Create Plot(s)"')

        self.varC = IntVar()
        self.varC.set(True)
        self.carbonCheck = ttk.Checkbutton(self.window, text="Enable Carbons Plots/Settings", variable=self.varC, onvalue=1, offvalue=0, command=carbonChecker)
        self.carbonCheck.grid(column=1, row=5, sticky=(N))
        self.balloon.bind(self.carbonCheck, 'If checked, carbon plots will be generated when you click "Create Plot(s)"')

        for child in self.window.winfo_children(): child.grid_configure(padx=5, pady=5)
        self.window.resizable(width=True, height=True)
