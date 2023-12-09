import csv
import glob
import math
import os
import subprocess
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk

import Pmw
import matplotlib as mpl
import matplotlib.backend_bases as bb
import matplotlib.patches as mpatches
import plugins.shared.Config as settingsConfig
from plugins.loaders import *
from plugins.shared.GreenChip import *

global isOpenPower, powerWindow, isOpenCarbon, carbonWindow
isOpenPower = False
powerWindow = None
isOpenCarbon = False
CarbonWindow = None

def colorFader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

if settingsConfig.nativePlotting:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib import pyplot as plt
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.widgets import Button



class utils(object):
    
    @staticmethod
    def calculateCarbon(row):
        sum = 0
        index = 2
        while index < 12:
            source =  int(row[index]) * float(row[index+10])
            sum += source
            index += 1
        return round(sum/100)

    @staticmethod
    def returnListLoc(key, energyData):
        countryOptions = []
        stateOptions = []
        for row in energyData:
            if row[0] != '':
                countryOptions.append(row[0])
                stateOptions.append(['Back...'])
            else:
                stateOptions[len(stateOptions)-1].append(row[1])
        if key in countryOptions:
            return countryOptions
        else:
            for states in stateOptions:
                if key in states:
                    return states
            messagebox.showerror('Invalid Location', 'Invalid location in Greenchip.txt!')
            return None
    
    @staticmethod
    def changeOptionsLoc(event, energyData):
        countryOptions = []
        stateOptions = []
        for row in energyData:
            if row[0] != '':
                countryOptions.append(row[0])
                stateOptions.append(['Back...'])
            else:
                stateOptions[len(stateOptions)-1].append(row[1])
        option=event.widget.get()
        if event.widget['values'][0] == 'Back...':
            if option == 'Back...': 
                event.widget['values'] = countryOptions
                event.widget.set('')
                event.widget.event_generate('<Button-1>', when='tail')
        
        else:
            index = countryOptions.index(option)
            state_list = stateOptions[index]
            if len(state_list) == 1: return
            event.widget['values'] = state_list
            event.widget.set('')
            event.widget.event_generate('<Button-1>', when='tail')
            
    @staticmethod
    def powerPatcherCore(filename, chipAreaDram, technode, locCPU, locDRAM, locUse, YC, NC, YT, NT, Y, N):
        filename = os.path.normpath(filename)
        filename = os.path.join(os.path.dirname(filename),"Greenchip.txt")
        
        varList = None
        
        if (os.path.exists(filename)):
            fileManu = open(filename, "r")
            varList = fileManu.readlines()
            fileManu.close()
            if YC:
                varList[0] = str(chipAreaDram) + ' //DRAM Chip Area\n'
            elif not NC:
                MsgBox = messagebox.askquestion ('Chip Area','A dram chip area of ' + varList[0].split(' ')[0] + ' mm^2 is already specified in ' + filename + '. Do you wish to overwrite this data?' ,icon = 'warning')
                if MsgBox == 'yes':
                    varList[0] = str(chipAreaDram) + ' //DRAM Chip Area\n'
            if YT:
                varList[1] = str(technode) + ' //DRAM Technology Node\n'
            elif not NT:                
                MsgBox = messagebox.askquestion ('Technology Node','A technology node of ' + varList[1].split(' ')[0] + ' nm is already specified in ' + filename + '. Do you wish to overwrite this data?' ,icon = 'warning')
                if MsgBox == 'yes':
                    varList[1] = str(technode) + ' //DRAM Technology Node\n'
            if Y:
                varList[2] = str(locCPU) + ' //CPU Manufacturing Location\n'
                varList[3] = str(locDRAM) + ' //DRAM Manufacturing Location\n'
                varList[4] = str(locUse) + ' //Use Phase Location'
            elif not N:
                MsgBox = messagebox.askquestion ('Locations','Locations for CPU, DRAM, and Use Phase, which are ' + varList[2].split(' ')[0] + ', ' + varList[3].split(' ')[0] + ', and ' + varList[4].split(' ')[0] + ', respectively, are already specified in ' + filename + '. Do you wish to overwrite this data?' ,icon = 'warning')
                if MsgBox == 'yes':
                    varList[2] = str(locCPU) + ' //CPU Manufacturing Location\n'
                    varList[3] = str(locDRAM) + ' //DRAM Manufacturing Location\n'
                    varList[4] = str(locUse) + ' //Use Phase Location'
                
            
        else:
            varList = [str(chipAreaDram) + '\n', str(technode) + '\n', str(locCPU) + '\n', str(locDRAM) + '\n', str(locUse)]
    
        fileManu = open(os.path.join(os.path.dirname(filename),"Greenchip.txt"), "w")
        fileManu.writelines(varList)
        fileManu.close()
    
    @staticmethod
    def powerPatcher(dirname, chipAreaDram, technode, locCPU, locDRAM, locUse, YC, NC, YT, NT, Y, N):
        powerlist = glob.glob(dirname+'/**/power.py', recursive=True)
        for i in powerlist:
            utils.powerPatcherCore(i, chipAreaDram, technode, locCPU, locDRAM, locUse, YC, NC, YT, NT, Y, N)
        messagebox.showinfo('Patch Complete', 'Patch has been completed! You may close this window and run your analysis', icon='info')
    
    @staticmethod
    def powerPrompter(gridMixSettingsFilename):
		
        global isOpenPower,powerWindow
		
        if not isOpenPower:
            window = Toplevel()
            window.title("Specifier Data Entry")
            window.geometry("450x375")

            def window_exit():
                global isOpenPower
                isOpenPower = False
                window.destroy()            

            window.protocol("WM_DELETE_WINDOW", window_exit)
            
        
            powerWindow = window
            isOpenPower = True

            balloon = Pmw.Balloon(window)
            lblballoon = balloon.component('label')
            lblballoon.config(background='white')
            
            Tech_Value = StringVar()
            Patch_Folder = StringVar()
            Patch_Folder_Actual = StringVar()
            CPU_Value = StringVar()
            DRAM_Value = StringVar()
            Use_Value = StringVar()
            varYC = IntVar()
            varNC = IntVar()
            varYT = IntVar()
            varNT = IntVar()
            varY = IntVar()
            varN = IntVar()

            energyData=[]
            filename=os.path.normpath(gridMixSettingsFilename)
            with open(filename, 'r') as file:
                reader=csv.reader(file)
                for row in reader:
                   if row[0]!='Country': energyData.append(row)
            
            countryOptions = []
            for row in energyData:
                if row[0] != '':
                    countryOptions.append(row[0])
                            
            CPU_Label = ttk.Label(window, text="CPU Manufacturing Location:")
            balloon.bind(CPU_Label, "This is the location where each CPU was manufactured.")

            DRAM_Label = ttk.Label(window, text="DRAM Manufacturing Location:")
            balloon.bind(CPU_Label, "This is the location where each DRAM was manufactured.")

            Use_Label = ttk.Label(window, text="Use Phase Location:")
            balloon.bind(CPU_Label, "This is the location where each system operates.")
                        
            
            Patch_Label = ttk.Label(window, text="Directory:")
            balloon.bind(Patch_Label, "The specified information is added to all subdirectories containing sniper output within this directory")
            PatchFolder_Label = ttk.Label(window, textvariable=Patch_Folder)

            Area_Label = ttk.Label(window, text="DRAM Chip Area (mm^2):")
            balloon.bind(Area_Label, "Total area of all DRAM dies in mm^2.")

            Tech_Label = ttk.Label(window, text="DRAM Technology Node (nm):")
            balloon.bind(Tech_Label, "The technology node (also process node, process technology or simply node) \n refers to a specific semiconductor manufacturing process and its design rules. \n Different nodes often imply different circuit generations and architectures.")

            Area_Entry = ttk.Entry(window, width=30)
            
            Empty_Label = ttk.Label(window, text='')

            Tech_Dropdown = ttk.Combobox(window, textvariable=Tech_Value, values=['3 (CMOS)', '6 (CMOS)', '7 EUV (CMOS)', '7 193i (CMOS)', '8 EUV (CMOS)', '8 193i (CMOS)', '10 (CMOS)', '12 (CMOS)','14 (CMOS)', '20 (CMOS)', '28 (CMOS)', '30 (CMOS)', '32 (CMOS)', '45 (CMOS)', '55', '57', '90', '130', '180', '250'], state='readonly')
            Tech_Dropdown.current(12)

            CPU_Dropdown = ttk.Combobox(window, textvariable=CPU_Value, values=countryOptions, state='readonly')
            CPU_Dropdown.bind("<<ComboboxSelected>>", lambda event: utils.changeOptionsLoc(event, energyData))

            DRAM_Dropdown = ttk.Combobox(window, textvariable=DRAM_Value, values=countryOptions, state='readonly')
            DRAM_Dropdown.bind("<<ComboboxSelected>>", lambda event: utils.changeOptionsLoc(event, energyData))

            Use_Dropdown = ttk.Combobox(window, textvariable=Use_Value, values=countryOptions, state='readonly')
            Use_Dropdown.bind("<<ComboboxSelected>>", lambda event: utils.changeOptionsLoc(event, energyData))
            
            Defaults_Label = ttk.Label(window, text='Sample DRAM Modules:')
            balloon.bind(Defaults_Label, "We have provided some sample DRAM Modules. When a module is selected, the DRAM chip area and tech node will jump to the correct values for that module.")
            Defaults_Dropdown = ttk.Combobox(window, textvariable=Use_Value, values=countryOptions, state='readonly')

            def YC_Checker():          
                if varYC.get()==1 and varNC.get()==1:
                    messagebox.showerror(title = "Not Compatible", message = "You can't overwrite everything and never overwrite at the same time. Please select one or the other.", icon = "error")
                    varYC.set(0)

            def NC_Checker():            
                if varYC.get()==1 and varNC.get()==1:
                    messagebox.showerror(title = "Not Compatible", message = "You can't overwrite everything and never overwrite at the same time. Please select one or the other.", icon = "error")
                    varNC.set(0)

            def YT_Checker():            
                if varYT.get()==1 and varNT.get()==1:
                    messagebox.showerror(title = "Not Compatible", message = "You can't overwrite everything and never overwrite at the same time. Please select one or the other.", icon = "error")
                    varYT.set(0)

            def NT_Checker():            
                if varYT.get()==1 and varNT.get()==1:
                    messagebox.showerror(title = "Not Compatible", message = "You can't overwrite everything and never overwrite at the same time. Please select one or the other.", icon = "error")
                    varNT.set(0)

            def Y_Checker():            
                if varY.get()==1 and varN.get()==1:
                    messagebox.showerror(title = "Not Compatible", message = "You can't overwrite everything and never overwrite at the same time. Please select one or the other.", icon = "error")
                    varY.set(0)

            def N_Checker():            
                if varY.get()==1 and varN.get()==1:
                    messagebox.showerror(title = "Not Compatible", message = "You can't overwrite everything and never overwrite at the same time. Please select one or the other.", icon = "error")
                    varN.set(0)


            varY.set(0)
            checkY = ttk.Checkbutton(window, text="Automatically Overwrite\nExisting Grid Mix Data", variable=varY, onvalue=1, offvalue=0, command=Y_Checker)
            balloon.bind(checkY, "If checked, when the tool finds a carbon.txt file,\nit will always overwrite it with the specified values instead of asking the user whether to overwrite data.")

            varN.set(0)
            checkN = ttk.Checkbutton(window, text="Never Overwrite\nExisting Grid Mix Data", variable=varN, onvalue=1, offvalue=0, command=N_Checker)
            balloon.bind(checkN, "If checked, when the tool finds a carbon.txt file,\nit will keep those values instead of asking the user whether to overwrite data.")


            varYC.set(0)
            checkYC = ttk.Checkbutton(window, text="Automatically Overwrite\nExisting Values for\nDRAM Chip Area", variable=varYC, onvalue=1, offvalue=0, command=YC_Checker)
            balloon.bind(checkYC, "If checked, when the patcher finds a file with a non-zero chip area, \ninstead of asking the user whether it should overwrite it, the patcher will automatically overwrite it.")

            varNC.set(0)
            checkNC = ttk.Checkbutton(window, text="Never Overwrite\nExisting Values for\nDRAM Chip Area", variable=varNC, onvalue=1, offvalue=0, command=NC_Checker)
            balloon.bind(checkNC, "If checked, when the patcher finds a file with a non-zero chip area, \ninstead of asking the user whether it should overwrite it, the patcher will keep the current value.")

            varYT.set(0)
            checkYT = ttk.Checkbutton(window, text="Automatically Overwrite\nExisting Values for\nDRAM Technology Node", variable=varYT, onvalue=1, offvalue=0, command=YT_Checker)
            balloon.bind(checkYT, "If checked, when the patcher finds a file with an existing technology node, \ninstead of asking the user whether it should overwrite it, the patcher will automatically overwrite it.")

            varNT.set(0)
            checkNT = ttk.Checkbutton(window, text="Never Overwrite\nExisting Values for\nDRAM Technology Node", variable=varNT, onvalue=1, offvalue=0, command=NT_Checker)
            balloon.bind(checkNT, "If checked, when the patcher finds a file with an existing technology node, \ninstead of asking the user whether it should overwrite it, the patcher will keep the current value.")

            def remove_source(tech_node):
                i = 0
                while i<len(tech_node) and tech_node[i]!='(':
                    i += 1
                if i!=len(tech_node):
                    return tech_node[0:(i-1)]
                else:
                    return tech_node
            
            def path_shortener(path):
                if len(path) > 25:
                    return  path[0:25] + '...'  
                else:
                    return path

            def browse_button_input():
                f = open(os.path.join(os.path.dirname(os.path.realpath('__file__')),'defaultFolders.txt'), "r+")
                defaults = f.readlines()
                filename1 = None
                if defaults[6]=='\n':
                    filename1 = filedialog.askdirectory()
                else:
                    filename1 = filedialog.askdirectory(initialdir = os.path.normpath(defaults[6].strip()))

                if (filename1 is None or filename1==""):
                    return

                defaults[6] = filename1 + "\n"
                f.seek(0)
                f.truncate(0)
                f.writelines(defaults)
                f.close()

                Patch_Folder.set(filename1)
                Patch_Folder_Actual.set(filename1)
                balloon.bind(PatchFolder_Label, Patch_Folder_Actual.get())
                Patch_Folder.set(path_shortener(Patch_Folder.get()))
            
            def call_power_patcher():
                dirname = Patch_Folder_Actual.get()
                chipAreaDram = Area_Entry.get()
                technode = remove_source(Tech_Value.get())
                procLoc = CPU_Value.get()
                dramLoc = DRAM_Value.get()
                useLoc = Use_Value.get()
                
                if dirname is None or dirname=='':
                    messagebox.showerror(title = "Empty Directory", message = "Please specify a directory", icon = "error")
                    return
                if chipAreaDram is None or chipAreaDram=='':
                    messagebox.showerror(title = "No Chip Area Supplied", message = "Please specify the DRAM Chip Area", icon = "error")
                    return
                if technode is None or technode=='':
                    messagebox.showerror(title = "No Tech Node Supplied", message = "Please specify the DRAM Tech Node", icon = "error")
                    return
                if procLoc is None or procLoc=='':
                    messagebox.showerror(title = "No CPU Location Supplied", message = "Please Specify the CPU Manufacturing Location", icon = "error")
                    return
                if dramLoc is None or dramLoc=='':
                    messagebox.showerror(title = "No DRAM Location Supplied", message = "Please Specify the DRAM Manufacturing Location", icon = "error")
                    return
                if useLoc is None or useLoc=='':
                    messagebox.showerror(title = "No Use Phase Location Supplied", message = "Please Specify the Use Phase Location", icon = "error")
                    return
                
                
                utils.powerPatcher(dirname, chipAreaDram, technode, CPU_Value.get(), DRAM_Value.get(), Use_Value.get(), bool(varYC.get()), bool(varNC.get()), bool(varYT.get()), bool(varNT.get()), bool(varY.get()), bool(varN.get()))
                window_exit()

            Browse_Button = ttk.Button(window, text="Browse", command=browse_button_input)
            Patch_Button = ttk.Button(window, text="Begin!",  command=call_power_patcher)
            
            Patch_Label.grid(row=0,column=0, sticky=(N,W,E,S), pady=(5,5))
            PatchFolder_Label.grid(row=0,column=1, sticky=(N,W,E,S), pady=(5,5))
            Browse_Button.grid(row=0, column=2, sticky=(N,W,E,S), pady=(5,5))

            Area_Label.grid(row=1,column=0, sticky=(N,W,E,S), pady=(0,5))
            Area_Entry.grid(row=1,column=1, sticky=(N,W,E,S), pady=(0,5))

            Tech_Label.grid(row=2,column=0, sticky=(N,W,E,S), pady=(0,5))
            Tech_Dropdown.grid(row=2,column=1, sticky=(N,W,E,S), pady=(0,5))
                        
            CPU_Label.grid(row=3,column=0, sticky=(N,W,E,S), pady=(0,5))
            CPU_Dropdown.grid(row=3,column=1, sticky=(N,W,E,S), pady=(0,5))
            
            DRAM_Label.grid(row=4,column=0, sticky=(N,W,E,S), pady=(0,5))
            DRAM_Dropdown.grid(row=4,column=1, sticky=(N,W,E,S), pady=(0,5))
            
            Use_Label.grid(row=5,column=0, sticky=(N,W,E,S), pady=(0,5))
            Use_Dropdown.grid(row=5,column=1, sticky=(N,W,E,S), pady=(0,5))
            
            #Defaults_Dropdown.grid(row=6,column=1, sticky=(N,W,E,S), pady=(0,5))
            #Defaults_Dropdown.grid(row=6,column=1, sticky=(N,W,E,S), pady=(0,5))

            Empty_Label.grid(row=7,column=0, sticky=(N,W,E,S), pady=(0,5))
            
            checkYC.grid(row=8,column=0, sticky=(N,W,E,S), pady=(0,5))
            checkNC.grid(row=8,column=1, sticky=(N,W,E,S), pady=(0,5))
            Patch_Button.grid(row=8,column=2, rowspan=3,sticky=(N,W,E,S), pady=(0,5))

            checkYT.grid(row=9,column=0, sticky=(N,W,E,S), pady=(0,5))
            checkNT.grid(row=9,column=1, sticky=(N,W,E,S), pady=(0,5))
            
            checkY.grid(row=10,column=0, sticky=(N,W,E,S), pady=(0,5))            
            checkN.grid(row=10,column=1, sticky=(N,W,E,S), pady=(0,5))


            window.resizable(width=True, height=True)
        
        else:
            powerWindow.deiconify()
            powerWindow.lift()
        # dirname = filedialog.askdirectory()
        # if dirname == '':
            # return
        # chipAreaDram = simpledialog.askinteger('DRAM Chip Area', 'Please input the desired DRAM chip area for the selected files.')
        # if chipAreaDram is None:
            # return
        # technode = simpledialog.askstring('DRAM Technology Node', 'Please input the desired DRAM technology node for the selected files. The supported tech nodes are ' + "55, 57, 90, 130, 180, and 250.")
        # if technode is None:
            # return
        # while technode not in ['55', '57', '90', '130', '180', '250']:
            # MsgBox = messagebox.askquestion ('DRAM Technology Node','This technology node is not supported. Do you wish to try again?' , icon = 'error')
            # if MsgBox == 'yes':
                # technode = simpledialog.askstring('DRAM Technology Node', 'Please input the desired DRAM technology node for the selected files. The supported tech nodes are ' + "55, 57, 90, 130, 180, and 250.")
            # else:
                # return
        # utils.powerPatcher(dirname, chipAreaDram, technode)
        
    @staticmethod
    def abbreviate(benchmark):
        my_renaming = {'canneal_x264_blackscholes_vips': 'CXBV', 'rtview_fluidanimate_freqmine_bodytrack': 'RFFB',
                       'blackscholes_vips_streamcluster_swaptions': 'BVSS', 'canneal_x264_freqmine_dedup': 'CXFD',
                       'bzip_gobmk_hmmer_libquantum': 'BGHL', 'GemsFDTD_lbm_milc_namd': 'GLMN',
                       'mcf_sjeng_cactusADM_calculix': 'MSCC', 'bzip2_zeusmp_cactusADM_bwaves': 'BZCB',
                       'lbm_perlbench_leslie3d_astar': 'LPLA', 'povray_h264ref_calculix_soplex': 'PHCS',
                       'bzip2_gcc_mcf_zeusmp_cactusADM_GemsFDTD_milc_soplex': 'HIGH8',
                       'lbm_perlbench_calculix_soplex_gobmk_namd_bzip2_gcc': 'MIX8',
                       'gobmk_hmmer_h264ref_gromacs_namd_povray_tonto_libquantum': 'LOW8'}
        if benchmark in my_renaming:
            return my_renaming[benchmark]
        return benchmark
    
    @staticmethod
    def is_adjacent_generation(x, y):
        care_generations = False
        if x == '135':
            if y == '90':
                care_generations = True
        elif x == '90':
            if y == '135' or y == '65':
                care_generations = True
        elif x == '65':
            if y == '90' or y == '45':
                care_generations = True
        elif x == '45':
            if y == '65' or y == '28':
                care_generations = True
        elif x == '28':
            if y == '45' or y == '22':
                care_generations = True
        elif x == '22' and y == '28':
            care_generations = True

        if x == '135nm':
            if y == '90nm':
                care_generations = True
        elif x == '90nm':
            if y == '135nm' or y == '65nm':
                care_generations = True
        elif x == '65nm':
            if y == '90nm' or y == '45nm':
                care_generations = True
        elif x == '45nm':
            if y == '65nm' or y == '28nm':
                care_generations = True
        elif x == '28nm':
            if y == '45nm' or y == '22nm':
                care_generations = True
        elif x == '22nm' and y == '28nm':
            care_generations = True

        return care_generations
        #return True

    @staticmethod
    def is_adjacent_cachesize(x, y):
        care_cachesize = False
        if x == '16':
            if y == '8':
                care_cachesize = True
        elif x == '8':
            if y == '16' or y == '4':
                care_cachesize = True
        elif x == '4':
            if y == '8' or y == '2':
                care_cachesize = True
        elif x == '2':
            if y == '4' or y == '1':
                care_cachesize = True
        elif x == '1':
            if y == '2' or y == 'half':
                care_cachesize = True
        elif x == 'half' and y == '1':
            care_cachesize = True

        return care_cachesize

    @staticmethod
    def snapshot_reasonable(entry1_out, entry2_out):
        entry1_in = entry1_out.replace(',', ':')
        entry2_in = entry2_out.replace(',', ':')
        items1 = entry1_in.split(':')
        items2 = entry2_in.split(':')

        reasonable = utils.is_adjacent_generation(items1[1], items2[1])
        return reasonable

    @staticmethod
    def snapshot_gather(entry1_out, entry2_out):
        entry1_in = entry1_out.replace(',', ':')
        entry2_in = entry2_out.replace(',', ':')

        items1 = entry1_in.split(':')
        items2 = entry2_in.split(':')

        if items1[2] == 'half':
            items1[2] = '0.5'

        filename = '_vs_'.join([items1[1], items2[1]])
        label = ' vs '.join([entry1_in, entry2_in])
        return filename, label

    @staticmethod
    def rename(entry, forTitle):
        entry2 = entry.replace(',', ':')
        items = entry2.split(':')

        items[1] += 'nm'
        if items[2] == 'half':
            items[2] = '0.5'
        items[2] += 'MB'
        items[3] = utils.abbreviate(items[3])

        if forTitle:
            entry2 = ",".join([items[1], items[3], items[2]])
        else:
            entry2 = ':'.join([items[1], items[3], items[2]])
        return entry2

    @staticmethod
    def build_config(database, entry, path_to_output_directory, writeMe = True, configNum = 1, carbonFile = False, useDRAM = True, energyData = None):
        config = {}
        mcpat, mcpat_was_loaded = database.get_item(entry, 'power.py', mcpat_dict_loader)
        if mcpat is None:
            return None
        entries = entry.split(database.delim)
        tmpdict = database.DB[database.DB_name]
        if useDRAM:
            for i in entries:
                tmpdict = tmpdict[i]
            if 'run_out.txt' in tmpdict.keys():    
                dramsim, dramsim_was_loaded = database.get_item(entry, 'run_out.txt', dramsim_dict_loader)
                config['staticMemory'] = dramsim['static_memory']
                config['dynamicMemory'] = dramsim['dynamic_memory']
            else:
               Msgbox = messagebox.askquestion('run_out.txt Missing', 'run_out.txt is missing from ' + entry + '. DRAM Static Power and Dynamic Power will be pulled from Sniper instead. Do you want to proceed?', icon = 'warning')
               if Msgbox == 'yes':
                    config['staticMemory'] = mcpat['DRAM']['Subthreshold Leakage with power gating'] + mcpat['DRAM']['Gate Leakage']
                    config['dynamicMemory'] = mcpat['DRAM']['Runtime Dynamic']
               else:
                    return
        else:
            config['staticMemory'] = 0.0
            config['dynamicMemory'] = 0.0
            
        ipc, ipc_was_loaded = database.get_item(entry, 'sim.out', ipc_dict_loader)
        if ipc is None:
            return None

        config['chipArea'] = mcpat['Processor']['Area']
        if useDRAM: config['chipAreaDram'] = mcpat['DRAM']['Area']
        else: config['chipAreaDram'] = 0.0
        config['dynamicPower'] = mcpat['Processor']['Runtime Dynamic']
        config['staticPower'] = mcpat['Processor']['Subthreshold Leakage with power gating'] + mcpat['Processor'][
            'Gate Leakage']
        config['MPKI'] = ipc['mpki']
        config['IPC'] = ipc['ipc']
        config['cycles'] = ipc['cycles']
        config['layers'] = 1
        mcpat_cfg, mcpat_config_was_loaded = database.get_item(entry, 'power.xml', mcpat_cfg_loader)
        
        processSize = str(mcpat_cfg[0][14].attrib['value'])
        config['processSize'] = processSize

        for tech in high_process_energies.keys():
            if (processSize + " ") in tech or processSize==tech:
                config['processSize'] = tech
                break
        
        if configNum == 3 and not carbonFile and not useDRAM:
            config['chipAreaDram'] = 0.0
            config['processSizeDram'] = '55'

        if configNum == 3 and (carbonFile or useDRAM):
            data_list = database.get_item(entry, 'Greenchip.txt', greenchip_dict_loader)
            
            if data_list is not None:
                config['LocationManu CPU'] = str(data_list[0][2])
                config['Carbon Use Phase Loc'] = str(data_list[0][4])
                if useDRAM:
                    config['chipAreaDram'] = float(data_list[0][0])
                    acceptable_DRAM_nodes = ['3', '6', '7', '8', '10', '12', '14', '20', '28', '30', '32', '45', '55', '57', '90', '130', '180', '250']
                    if str(data_list[0][1]).split(' ')[0].strip() not in acceptable_DRAM_nodes:
                        messagebox.showerror('DRAM Technology Node Error', 'DRAM Technology Node in Greenchip.txt of ' + entry + ' is ' + str(data_list[0][1]) + ', which is not currently compatible with Greenchip. Exiting...')
                        return
                    config['processSizeDram'] = str(data_list[0][1])
                    config['LocationManu DRAM'] = str(data_list[0][3])
                else:
                    config['chipAreaDram'] = 0.0
                    config['processSizeDram'] = '55'
                    config['LocationManu DRAM'] = config['LocationManu CPU']


                for row in energyData:
                    if row[2] == '':
                        continue
                    if row[0] == str(data_list[0][2]):
                        config['CPU Carbon Value'] = utils.calculateCarbon(row)
                    if row[1] == str(data_list[0][2]):
                        config['CPU Carbon Value'] = utils.calculateCarbon(row)
                    if useDRAM:
                        if row[0] == str(data_list[0][3]):
                            config['DRAM Carbon Value'] = utils.calculateCarbon(row)
                        if row[1] == str(data_list[0][3]):
                            config['DRAM Carbon Value'] = utils.calculateCarbon(row)
                    else:
                        config['DRAM Carbon Value'] = 0
                    
                    if row[0] == str(data_list[0][4]):
                        config['UsePh Carbon Value'] = utils.calculateCarbon(row)
                    if row[1] == str(data_list[0][4]):
                        config['UsePh Carbon Value'] = utils.calculateCarbon(row)
            else:
                messagebox.showerror('DRAM Technology Node Error', 'Greenchip.txt for ' + entry + ' is missing. Please run the patcher and try again. Exiting...')
                return
                
        
        if configNum == 3 and carbonFile:
            techNodeCPU = config['processSize']
            techNodeDRAM = config['processSizeDram']
            
            config['CPU Energy'] = high_process_energies[techNodeCPU]['energy']
                
            config['Total CPU Energy'] = simple_manufacturing(config['CPU Energy'], config['chipArea'], config['layers'])
            config['Total CPU Carbon'] = config['Total CPU Energy'] /3600000 * config['CPU Carbon Value']
            
            ''' Add energy (Joules) manufacturing DRAM '''
            config['DRAM Energy'] = high_process_energies_DRAM[techNodeDRAM]['energy']
                
            config['Total DRAM Energy'] = simple_manufacturing(config['DRAM Energy'], config['chipAreaDram'], config['layers'])
            config['Total DRAM Carbon'] = config['Total DRAM Energy'] /3600000 * config['DRAM Carbon Value']
            
        config['FREQ'] = float(mcpat_cfg[0][15].attrib['value'])/1000.0
        cycle_time = 1.0/(config['FREQ']*1000000000)        

        if mcpat_was_loaded:

            if writeMe:
                ProcManuEnergy = simple_manufacturing(high_process_energies[str(config['processSize'])]['energy'], config['chipArea'], config['layers'])
                DramManuEnergy = simple_manufacturing(high_process_energies_DRAM[str(config['processSizeDram'])]['energy'], config['chipAreaDram'], config['layers'])
                entry = utils.rename(entry, False)
                with open(path_to_output_directory + "Power.csv", "a") as power_file:
                    power_file.write(entry + "," + str(config['staticMemory']) + "," + str(config['staticPower']) + "," +
                                     str(config['dynamicMemory']) + "," + str(config['dynamicPower']) + "\n")
                if carbonFile:
                    with open(path_to_output_directory+"CarbonRate.csv", "a") as carbonr_file:
                        carbonr_file.write(entry + "," + str(config['staticMemory']/1000 * config['UsePh Carbon Value']) + "," + str(config['staticPower']/1000 * config['UsePh Carbon Value']) + "," + str(config['dynamicMemory']/1000 * config['UsePh Carbon Value']) + "," + str(config['dynamicPower']/1000 * config['UsePh Carbon Value']) + "\n")

                with open(path_to_output_directory + "MPKI.csv", "a") as mpki_file:
                    mpki_file.write(entry + "," + str(ipc['mpki']) + "\n")

                with open(path_to_output_directory + "IPC.csv", "a") as ipc_file:
                    ipc_file.write(entry + "," + str(ipc['ipc']) + "\n")

                if carbonFile:
                    with open(path_to_output_directory + "Manufacturing.csv", "a") as energy_file:
                        energy_file.write(entry  + "," + str(DramManuEnergy) + "," + str(ProcManuEnergy) + "," + str(config['Total DRAM Carbon']) + "," + str(config['Total CPU Carbon']) + "," + str(config['chipAreaDram']) + "," + str(config['chipArea']) + "\n")
                else:
                    with open(path_to_output_directory + "Manufacturing.csv", "a") as energy_file:
                        energy_file.write(entry  + "," + str(DramManuEnergy) + "," + str(ProcManuEnergy) + "," + str(config['chipAreaDram']) + "," + str(config['chipArea']) + "\n")
                    

                if carbonFile:
                    hours =  config['cycles'] * cycle_time/3600
                    with open(path_to_output_directory+"Carbon.csv", "a") as carbon_file:
                        carbon_file.write(entry + "," + str(config['staticMemory']/1000 * config['UsePh Carbon Value'] * hours) + "," + str(config['staticPower']/1000 * config['UsePh Carbon Value'] * hours) + "," + str(config['dynamicMemory']/1000 * config['UsePh Carbon Value'] * hours) + "," + str(config['dynamicPower']/1000 * config['UsePh Carbon Value'] * hours) + "\n")


                with open(path_to_output_directory + "Energy.csv", "a") as energy_file:
                    energy_file.write(
                        entry + "," + str(config['staticMemory'] * config['cycles'] * cycle_time) +
                        "," + str(config['staticPower'] * config['cycles'] * cycle_time) + "," +
                        str(config['dynamicMemory'] * config['cycles'] * cycle_time) + "," +
                        str(config['dynamicPower'] * config['cycles'] * cycle_time) + "\n")

        return config

    @staticmethod
    def make_plot(first_entry, second_entry, entry1, entry2, res, snapshot_label, path_to_output_directory, increment = 0.5, mindays = 0, maxdays = 3650, minyears = 4000/365, maxyears = 36000/365):
        if settingsConfig.nativePlotting:
			
            fontSize = 13;
            axisLabelSize = 16;
            titleLabelSize = 20

            matplotlib.rc('xtick', labelsize=fontSize)
            matplotlib.rc('ytick', labelsize=fontSize)

            if first_entry is None or second_entry is None:
                return
                
            settingsFile = settingsConfig.advancedSettingsFile

            res_keys = sorted(res.keys())
            #cols = []
            #for x in range(0, 11):
            #    cols.append(round(x * .1, 1))
            data = []
            #rows = []
            for key in res_keys:
                innerres = res[key]
                inner_keys = sorted(innerres.keys())
                #rows.append(round(key * .1, 1))
                inner_data = []
                for inner_key in inner_keys:
                    inner_data.append(innerres[inner_key])
                data.append(np.asarray(inner_data))
            arr = np.asarray(data).T
            #column_labels = cols
            #row_labels = rows
            fig, ax = plt.subplots()

            cdict2 = OurConstants.get_cdict2()

            cdict1 = OurConstants.get_cdict1()

            customgray = LinearSegmentedColormap('customgray', cdict1)
            customspectrum = LinearSegmentedColormap('customspectrum', cdict2)
            c = (0, 0, 0, 0)
            my_cmap = plt.get_cmap(customspectrum)
            my_cmap.set_under(color='white')
            second_cmap = plt.get_cmap(customgray)
            second_cmap.set_under(color=c)

            heatmap = ax.pcolormesh(arr, cmap=my_cmap, vmax=3650, vmin=0)
            heatbar = heatmap
            heatmap = ax.pcolormesh(arr, cmap=second_cmap, vmax=36000, vmin=4000)
            heatbar2 = heatmap

            # [x][y]
            e = np.e
                        
            markerDict = {}
            
            if settingsFile is not None:
                with open(settingsFile, "r") as settingsObject:
                    for line in settingsObject:
                        linevars = line.split(" ");
                        if (linevars[0].upper()=="M"):
                            if len(linevars)==5:
                                Sleep = int(linevars[1])
                                if (Sleep<0 or Sleep>100):
                                    messagebox.showerror("Error", "Sleep Ratio out of bounds!")
                                    break
                                Activity = int(linevars[2])
                                if (Activity<0 or Activity>100):
                                    messagebox.showerror("Error", "Activity Ratio out of bounds!")
                                    break
                                Label = linevars[3]
                                Color = linevars[4].lower().strip();
                                plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                                plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")

                                if Label not in markerDict: markerDict[Label] = [Sleep, Activity, -1]
                                else:
                                    i = 2
                                    while Label+str(i) in markerDict: i += 1
                                    markerDict[Label+str(i)] = [Sleep, Activity, -1]

                                if (Sleep>50):
                                    if (Activity<50):                    
                                        ax.text(Sleep/increment - 4/(math.sqrt(2)*increment) - 0.5/increment,Activity/increment + 4/(math.sqrt(2)*increment) + 0.5/increment, Label, color = Color, verticalalignment = 'top', horizontalalignment = 'right')
                                    else:
                                        ax.text(Sleep/increment - 4/(math.sqrt(2)*increment) - 0.5/increment,Activity/increment - 4/(math.sqrt(2)*increment) - 0.5/increment, Label, color = Color, verticalalignment = 'bottom', horizontalalignment = 'right')
                                else:
                                    if (Activity<50):                    
                                        ax.text(Sleep/increment + 4/(math.sqrt(2)*increment) + 0.5/increment,Activity/increment + 4/(math.sqrt(2)*increment) + 0.5/increment, Label, color = Color, verticalalignment = 'top', horizontalalignment = 'left')
                                    else:
                                        ax.text(Sleep/increment + 4/(math.sqrt(2)*increment) + 0.5/increment,Activity/increment - 4/(math.sqrt(2)*increment) - 0.5/increment, Label, color = Color, verticalalignment = 'bottom', horizontalalignment = 'left')
                            else:
                                Sleep = int(linevars[1])
                                if (Sleep<0 or Sleep>100):
                                    messagebox.showerror("Error", "Sleep Ratio out of bounds!")
                                    break
                                Activity = int(linevars[2])
                                if (Activity<0 or Activity>100):
                                    messagebox.showerror("Error", "Activity Ratio out of bounds!")
                                    break
                                Label = linevars[3].strip()
                                plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                                plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
                                
                                if Label not in markerDict: markerDict[Label] = [Sleep, Activity, -1]
                                else:
                                    i = 2
                                    while Label+str(i) in markerDict: i += 1
                                    markerDict[Label+str(i)] = [Sleep, Activity, -1]

                                if (Sleep>50):
                                    if (Activity<50):                    
                                        ax.text(Sleep/increment - 4/(math.sqrt(2)*increment) - 0.5/increment,Activity/increment + 4/(math.sqrt(2)*increment) + 0.5/increment, Label, verticalalignment = 'top', horizontalalignment = 'right', bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                                    else:
                                        ax.text(Sleep/increment - 4/(math.sqrt(2)*increment) - 0.5/increment,Activity/increment - 4/(math.sqrt(2)*increment) - 0.5/increment, Label, verticalalignment = 'bottom', horizontalalignment = 'right', bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                                else:
                                    if (Activity<50):                    
                                        ax.text(Sleep/increment + 4/(math.sqrt(2)*increment) + 0.5/increment,Activity/increment + 4/(math.sqrt(2)*increment) + 0.5/increment, Label, verticalalignment = 'top', horizontalalignment = 'left', bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                                    else:
                                        ax.text(Sleep/increment + 4/(math.sqrt(2)*increment) + 0.5/increment,Activity/increment - 4/(math.sqrt(2)*increment) - 0.5/increment, Label, verticalalignment = 'bottom', horizontalalignment = 'left', bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                        elif (linevars[0].upper()=="WM"):
                            if len(linevars)==6:
                                Sleep = int(linevars[1])
                                if (Sleep<0 or Sleep>100):
                                    messagebox.showerror("Error", "Sleep Ratio out of bounds!")
                                    break
                                Activity = int(linevars[2])
                                if (Activity<0 or Activity>100):
                                    messagebox.showerror("Error", "Activity Ratio out of bounds!")
                                    break
                                Radius = int(linevars[3])
                                Label = linevars[4]
                                Color = linevars[5].lower().strip();
                                plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=Radius*8.5 + 5, markeredgecolor='black', mew=3, markerfacecolor="None")
                                plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=Radius*8.5, markeredgecolor='white', mew=3, markerfacecolor="None")

                                if Label not in markerDict: markerDict[Label] = [Sleep, Activity, Radius]
                                else:
                                    i = 2
                                    while Label+str(i) in markerDict: i += 1
                                    markerDict[Label+str(i)] = [Sleep, Activity, Radius]
                                    
                                if (Sleep>50):
                                    if (Activity<50):                    
                                        ax.text(Sleep/increment - (Radius*8.5)/(9*math.sqrt(2)*increment) - 1/increment, Activity/increment + (Radius*8.5)/(9*math.sqrt(2)*increment) + 1/increment, Label, color = Color, verticalalignment = 'top', horizontalalignment = 'right')
                                    else:
                                        ax.text(Sleep/increment - (Radius*8.5)/(9*math.sqrt(2)*increment) - 1/increment, Activity/increment - (Radius*8.5)/(9*math.sqrt(2)*increment) - 1/increment, Label, color = Color, verticalalignment = 'bottom', horizontalalignment = 'right')
                                else:
                                    if (Activity<50):                    
                                        ax.text(Sleep/increment + (Radius*8.5)/(9*math.sqrt(2)*increment) + 1/increment, Activity/increment + (Radius*8.5)/(9*math.sqrt(2)*increment) + 1/increment, Label, color = Color, verticalalignment = 'top', horizontalalignment = 'left')
                                    else:
                                        ax.text(Sleep/increment + (Radius*8.5)/(9*math.sqrt(2)*increment) + 1/increment, Activity/increment - (Radius*8.5)/(9*math.sqrt(2)*increment) - 1/increment, Label, color = Color, verticalalignment = 'bottom', horizontalalignment = 'left')
                            else:
                                Sleep = int(linevars[1])
                                if (Sleep<0 or Sleep>100):
                                    messagebox.showerror("Error", "Sleep Ratio out of bounds!")
                                    break
                                Activity = int(linevars[2])
                                if (Activity<0 or Activity>100):
                                    messagebox.showerror("Error", "Activity Ratio out of bounds!")
                                    break
                                Radius = int(linevars[3])
                                Label = linevars[4].strip()
                                plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=Radius*8.5 + 5, markeredgecolor='black', mew=3, markerfacecolor="None")
                                plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=Radius*8.5, markeredgecolor='white', mew=3, markerfacecolor="None")

                                if Label not in markerDict: markerDict[Label] = [Sleep, Activity, Radius]
                                else:
                                    i = 2
                                    while Label+str(i) in markerDict: i += 1
                                    markerDict[Label+str(i)] = [Sleep, Activity, Radius]

                                if (Sleep>50):
                                    if (Activity<50):                    
                                        ax.text(Sleep/increment - (Radius*8.5)/(9*math.sqrt(2)*increment) - 1/increment, Activity/increment + (Radius*8.5)/(9*math.sqrt(2)*increment) + 1/increment, Label, color = Color, verticalalignment = 'top', horizontalalignment = 'right')
                                    else:
                                        ax.text(Sleep/increment - (Radius*8.5)/(9*math.sqrt(2)*increment) - 1/increment, Activity/increment - (Radius*8.5)/(9*math.sqrt(2)*increment) - 1/increment, Label, color = Color, verticalalignment = 'bottom', horizontalalignment = 'right')
                                else:
                                    if (Activity<50):                    
                                        ax.text(Sleep/increment + (Radius*8.5)/(9*math.sqrt(2)*increment) + 1/increment, Activity/increment + (Radius*8.5)/(9*math.sqrt(2)*increment) + 1/increment, Label, color = Color, verticalalignment = 'top', horizontalalignment = 'left')
                                    else:
                                        ax.text(Sleep/increment + (Radius*8.5)/(9*math.sqrt(2)*increment) + 1/increment, Activity/increment - (Radius*8.5)/(9*math.sqrt(2)*increment) - 1/increment, Label, color = Color, verticalalignment = 'bottom', horizontalalignment = 'left')
                        elif (linevars[0][0]=="#"):
                            continue;
                        elif (len(linevars[0].strip())==0):
                            continue;
                        else:
                            messagebox.showerror("Error", "Marker specifier incorrect!")

            # Make sure this comparison makes sense (i.e., different process nodes)
            # Get Names
            if snapshot_label is not None:
                filename, label = utils.snapshot_gather(entry1, entry2)
                if not os.path.exists(path_to_output_directory + "Snapshots"):
                    os.makedirs(path_to_output_directory + "Snapshots")

                for key in markerDict.keys():
                    value = markerDict[key]
                    with open(path_to_output_directory + "Snapshots/"+snapshot_label.split(' ')[0] + '_' + snapshot_label.split(' ')[2] + '_' + key + '_' + filename + ".csv", "a") as snapshot_file:
                        if int(value[2])==-1: snapshot_file.write(label + "," + str(arr[int(value[1]/increment)][int(value[0]/increment)]) + "\n")
                        else:
                            val = 0
                            num = 0
                            for x in range(int(float(value[0])/increment-float(value[2])/increment),int(float(value[0])/increment+float(value[2])/increment)):
                                for y in range(int(float(value[1])/increment-float(value[2])/increment),int(float(value[1])/increment+float(value[2])/increment)):
                                    if (float(value[0])/increment-x)*(float(value[0])/increment-x)+(float(value[1])/increment-y)*(float(value[1])/increment-y)<(float(value[2])/increment)*(float(value[2])/increment):
                                        val += arr[y][x]
                                        num += 1
                                        
                            snapshot_file.write(label + "," + str(val/num) + "\n")
                        snapshot_file.close()


            # want a more natural, table-like display
            ax.invert_yaxis()
            ax.xaxis.tick_top()
            ax.axis('tight')
            plt.xticks(np.array([0.5,20/increment + 0.5,40/increment + 0.5,60/increment + 0.5,80/increment + 0.5,100/increment + 0.5]), [0,20,40,60,80,100])
            plt.yticks(np.array([0.5,20/increment + 0.5,40/increment + 0.5,60/increment + 0.5,80/increment + 0.5,100/increment + 0.5]), [0,20,40,60,80,100])

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

            first_ipc = "{0:.2f}".format(first_entry['IPC'])
            second_ipc = "{0:.2f}".format(second_entry['IPC'])

            first_mpki = "{0:.2f}".format(first_entry['MPKI'])
            second_mpki = "{0:.2f}".format(second_entry['MPKI'])

            fig.text(0.95, 0.01, 'IPC: ' + first_ipc + ',' + second_ipc,
                     verticalalignment='bottom', horizontalalignment='left',
                     color='brown', fontsize=15)

            fig.text(0.95, 0.01, 'MPKI: ' + first_mpki + ',' + second_mpki,
                     verticalalignment='top', horizontalalignment='right',
                     color='brown', fontsize=15)

            # ax.set_xticklabels(column_labels, minor=False)
            # ax.set_yticklabels(row_labels, minor=False)
            # plt.colorbar(heatbar2)

            yearlabels = utils.axisListMaker(minyears, maxyears)
            yearints = []
            yearlabels = list(yearlabels)
            yearints.insert(0, minyears*365 + 0.0001)
            yearlabels.insert(0,str(round(minyears, 1)))

            for i in range(1,len(yearlabels)):
                yearlabels[i] = int(yearlabels[i])
                yearints.append(yearlabels[i]*365)
                yearlabels[i] = str(yearlabels[i])

            yearlabels.append(round(maxyears,1))
            yearints.append(maxyears*365 - 0.0001)

            cbar = plt.colorbar(heatbar2, pad=0.05, ticks=yearints)
            cbar.ax.set_yticklabels(yearlabels)
            cbar.ax.tick_params(labelsize=fontSize)
            cbar.set_label('Years', rotation=360, size=axisLabelSize, labelpad=-30, y=1.08)
            
            # plt.colorbar(heatbar)
            cbar2 = plt.colorbar(heatbar, pad = 0.1)
            cbar2.ax.tick_params(labelsize=fontSize)
            # cbar.ax.set_yticklabels(labelsize=10)
            cbar2.set_label('Days', rotation=360, size=axisLabelSize, labelpad=-37.5, y=1.08)
            plt.xlabel('xlabel', fontsize=axisLabelSize)
            plt.ylabel('ylabel', fontsize=axisLabelSize)
            ax.set_xlabel('Percent Sleep')
            ax.xaxis.set_label_position('top')
            ax.xaxis.labelpad = 16;
            ax.set_title(label=snapshot_label, fontsize=titleLabelSize, pad=12)
            plt.ylabel('Activity Ratio')

            ax.set_aspect('equal', adjustable = None)

            # plt.title(''.join([utils.rename(self.entry1, False), ' vs. ', utils.rename(self.entry2, False)]), y=1.08)

            image_file_name = path_to_output_directory + utils.rename(entry1, True) + "_vs_" + utils.rename(
                entry2, True) + "_" + snapshot_label.split(' ')[0] + "_" + snapshot_label.split(' ')[2] + ".pdf"
            
            plt.savefig(image_file_name, bbox_inches='tight')
            
            ax.cla()
            fig.clf()
            plt.close("all")

        else:
            messagebox.showinfo("Library Missing!", "Missing matplotlib, cannot plot in python!")

    @staticmethod
    def perform_greenchip_analysis(res):
        if settingsConfig.nativePlotting:
            res_keys = sorted(res.keys())

            data = []
            for key in res_keys:
                innerres = res[key]
                inner_keys = sorted(innerres.keys())
                inner_data = []
                for inner_key in inner_keys:
                    inner_data.append(innerres[inner_key])
                data.append(np.asarray(inner_data))
            arr = np.asarray(data).T
            return arr
        else: #Much less efficient to not use numpy, so only do it if it is not installed
            res_keys = sorted(res.keys())

            Matrix = []
            for x in range(0, len(res[1].keys())):
                Matrix.append([])
                for y in range(0, len(res_keys)):
                    Matrix[x].append(0)

            for key in res_keys:
                innerres = res[key]
                inner_keys = sorted(innerres.keys())
                for inner_key in inner_keys:
                    Matrix[inner_key][key] = innerres[inner_key]

            return Matrix

    @staticmethod
    def export_single_data(first_entry, second_entry, res, exportFile):
        if first_entry is None or second_entry is None:
            return
        arr = utils.perform_greenchip_analysis(res)

        with open(exportFile, "a") as out_file:
            for a in arr:
                for b in a[0]:
                    out_file.write(str(a)+","+str(b)+","+","+str(arr[a][b])+"\n")

    def average_gradient(Radius, Sleep, Activity, Orig, Mod):
        numofpoints = 0
        totaldifference = 0
        for x in range(Sleep/increment - Radius, Sleep/increment + Radius + 1):
            for y in range(Activity/increment - Radius, Activity/increment + Radius + 1):
                if ((x + y)<=Radius + Activity/increment + Sleep and (x + y)>=Radius + Activity/increment + Sleep ):
                    numofpoints = numofpoints + 1
                    totaldifference = totaldifference + Orig[x][y] - Mod[x][y]
        averagedifference = totaldifference/numofpoints           
        return averagedifference


    
    def partial_average(Radius, Sleep, Activity, Orig):
        numofpoints = 0
        total = 0
        for x in range(Sleep/increment - Radius, Sleep/increment + Radius + 1):
            for y in range(Activity/increment - Radius, Activity/increment + Radius + 1):
                if ((x + y)<=Radius + Activity/increment + Sleep and (x + y)>=Radius + Activity/increment + Sleep ):
                    numofpoints = numofpoints + 1
                    total = total + Orig[x][y]
        average = total/numofpoints           
        return average      

    def average_analysis(self, config1, config2, Sleep, Activity, Radius):
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2) 
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
    

    def single_point_analysis(config1, config2, Sleep, Activity):
        config_dicts = []
        config_dicts.append(config1)
        config_dicts.append(config2) 
        if (Sleep < 0 or Activity < 0 or Sleep>=100 or Activity>=100): # Checks to see if the point is in bounds
            messagebox.showinfo("Error", "The values inputted are out of bounds")
            return
        difference = [0,0,0,0,0]
        orig = chip_breakeven_IPC(config_dicts, False)['upgradeDays'][Sleep/increment][Activity/increment]
        old = config2['chipArea']
        config2['chipArea'] = config2['chipArea'] - (.01 * config2['chipArea'])
        difference[0] = orig - chip_breakeven_IPC(config_dicts, False)['upgradeDays'][Sleep/increment][Activity/increment] # Measures gradient by using a 1% shift
        config2['chipArea'] = old

        old = config2['dynamicPower']
        config2['dynamicPower'] = config2['dynamicPower'] - (.01 * config2['dynamicPower'])
        difference[1] = orig - chip_breakeven_IPC(config_dicts, False)['upgradeDays'][Sleep/increment][Activity/increment] # Measures gradient by using a 1% shift
        config2['dynamicPower'] = old

        old = config2['staticPower']
        config2['staticPower'] = config2['staticPower'] - (.01 * config2['staticPower'])
        difference[2] = orig - chip_breakeven_IPC(config_dicts, False)['upgradeDays'][Sleep/increment][Activity/increment] # Measures gradient by using a 1% shift
        config2['staticPower'] = old

        old = config2['dynamicMemory']
        config2['dynamicMemory'] = config2['dynamicMemory'] - (.01 * config2['dynamicMemory'])
        difference[3] = orig - chip_breakeven_IPC(config_dicts, False)['upgradeDays'][Sleep/increment][Activity/increment] # Measures gradient by using a 1% shift
        config2['dynamicMemory'] = old
        
        old = config2['staticMemory']
        config2['staticMemory'] = config2['staticMemory'] - (.01 * config2['staticMemory'])
        difference[4] = orig - chip_breakeven_IPC(config_dicts, False)['upgradeDays'][Sleep/increment][Activity/increment] # Measures gradient by using a 1% shift
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

    @staticmethod
    def axisListMaker(minval, maxval):
        increment = 1
        while ((maxval-minval)/increment>10): increment += 1
        
        mid = round((minval+maxval)/2)
        
        l = [mid]
        
        temp = mid + increment
        while temp<(maxval-increment/2):
            l.append(temp)
            temp += increment

        temp = mid - increment
        while temp>(minval+increment/2):
            l.insert(0, temp)
            temp -= increment
        
        return l

    @staticmethod
    def make_single_plot(self, first_entry, second_entry, title1, title2, res, plot_title, increment = 0.2, mindays = 0, maxdays = 3650, minyears = 4000/365, maxyears = 36000/365):
        if settingsConfig.nativePlotting:

            initialFontSize = 13
            initialAxisLabelSize = 16
            initialTitleLabelSize = 20

            matplotlib.rc('xtick', labelsize=initialFontSize)
            matplotlib.rc('ytick', labelsize=initialFontSize)

            if first_entry is None or second_entry is None:
                return

            settingsFile = settingsConfig.advancedSettingsFile
            arr = utils.perform_greenchip_analysis(res)

            fig, ax = plt.subplots(figsize=(8,6.25))

            cdict2 = OurConstants.get_cdict2()

            cdict1 = OurConstants.get_cdict1()           

            numMarkers = 20

            markers = [None]*numMarkers*2
            markerSizes = [None]*numMarkers*2
            
            annotations = [None]*numMarkers
            xPosition = [None]*numMarkers
            yPosition = [None]*numMarkers

            marker_number = 0
            annotation_number = 0

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
            
            listarr = []
            for i in range(arr.shape[0]):
                listarrtemp = []
                for j in range(arr.shape[0]):
                    listarrtemp.append(arr[i,j])
                listarr.append(listarrtemp)
                
            def _mouse_event_to_message(self, event):
                if event.inaxes and event.inaxes.get_navigate():
                    try:
                        s = event.inaxes.format_coord(event.xdata, event.ydata)
                    except (ValueError, OverflowError):
                        pass
                    return s

            bb.NavigationToolbar2._mouse_event_to_message = _mouse_event_to_message
                
            def format_coord(x, y):
                col = int(x)
                row = int(y)
                x = col*increment
                y = row*increment
                if col>=0 and col<=100/increment and row>=0 and row<=100/increment:
                    z = arr[row,col]
                    if (z<0):
                        return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: Infinite'%(x, y)
                    elif (z<5):
                        if int(z)==0: return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2.4f Hours'%(x, y, (z-int(z))*24)
                        if int(z)==1: return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Day , %2.4f Hours'%(x, y, int(z), (z-int(z))*24)
                        return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Days, %2.4f Hours'%(x, y, int(z), (z-int(z))*24)
                    elif (z<365/12):
                        return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Days'%(x, y, int(z))
                    elif (z<365):
                        if (int(z*12/365)==1 and int(z-int(z*12/365)*365/12+0.5)==1): return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Month , %2d Day '%(x, y, int(z*12/365), int(z-int(z*12/365)*365/12+0.5))
                        if (int(z-int(z*12/365)*365/12+0.5)==1): return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Months, %2d Day '%(x, y, int(z*12/365), int(z-int(z*12/365)*365/12+0.5))
                        if (int(z*12/365)==1): return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Month , %2d Days'%(x, y, int(z*12/365), int(z-int(z*12/365)*365/12+0.5))
                        return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Months, %2d Days'%(x, y, int(z*12/365), int(z-int(z*12/365)*365/12+0.5))
                    else:
                        if (int(z/365)==1):
                            if (int((z-int(z/365)*365)*12/365))==1: 
                                if (int(z-int(z*12/365)*365/12+0.5)==1):
                                    return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Year , %2d Month , %2d Day '%(x, y, int(z/365), int((z-int(z/365)*365)*12/365), int(z-int(z*12/365)*365/12+0.5)) 
                                return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Year , %2d Month , %2d Days'%(x, y, int(z/365), int((z-int(z/365)*365)*12/365), int(z-int(z*12/365)*365/12+0.5))
                            if (int(z-int(z*12/365)*365/12+0.5)==1):
                                return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Year , %2d Months, %2d Day '%(x, y, int(z/365), int((z-int(z/365)*365)*12/365), int(z-int(z*12/365)*365/12+0.5)) 
                            return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Year , %2d Months, %2d Days'%(x, y, int(z/365), int((z-int(z/365)*365)*12/365), int(z-int(z*12/365)*365/12+0.5))  
                        
                        if (int((z-int(z/365)*365)*12/365))==1: 
                            if (int(z-int(z*12/365)*365/12+0.5)==1):
                                return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Years, %2d Month , %2d Day '%(x, y, int(z/365), int((z-int(z/365)*365)*12/365), int(z-int(z*12/365)*365/12+0.5))  
                            return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Years, %2d Month , %2d Days'%(x, y, int(z/365), int((z-int(z/365)*365)*12/365), int(z-int(z*12/365)*365/12+0.5))  
                        if (int(z-int(z*12/365)*365/12+0.5)==1):
                            return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Years, %2d Months, %2d Day '%(x, y, int(z/365), int((z-int(z/365)*365)*12/365), int(z-int(z*12/365)*365/12+0.5))                         
                        return 'Sleep Percentage=%1.2f%%, Activity Ratio=%1.2f%%: %2d Years, %2d Months, %2d Days'%(x, y, int(z/365), int((z-int(z/365)*365)*12/365), int(z-int(z*12/365)*365/12+0.5))  
                else:
                    return 'Sleep Percentage=%1.4f, y=%1.4f'%(x, y)
            
            ax.format_coord = format_coord

           # def Clicked(event, int sleep, int activity):
            #    print(sleep)

            if settingsFile is None:
                marker_number = 0
                # Desktop
                #markers[0] = plt.plot([77], [17], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                #markers[1] = plt.plot([77], [17], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
                #markerSizes[0] = 35.0
                #markerSizes[1] = 30.0
                #annotations[0] = plt.annotate('Desktop',[77+5,17+5], bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                #xPosition[0] = 77
                #yPosition[0] = 17

                # Server
                #markers[2] = plt.plot([5], [30], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                #markers[3] = plt.plot([5], [30], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
                #markerSizes[2] = 35.0
                #markerSizes[3] = 30.0
                #annotations[1] = plt.annotate('Server',[5+5,30+5], bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                #xPosition[1] = 5
                #yPosition[1] = 30
				
                # HPC
                #markers[4] = plt.plot([5], [95], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                #markers[5] = plt.plot([5], [95], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
                #markerSizes[4] = 35.0
                #markerSizes[5] = 30.0
                #annotations[2] = plt.annotate('HPC',[5+5,95+5], bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                #xPosition[2] = 5
                #yPosition[2] = 95
				
                # Cell Phone
                #markers[6] = plt.plot([92], [90], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                #markers[7] = plt.plot([92], [90], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
                #markerSizes[6] = 35.0
                #markerSizes[7] = 30.0
                #annotations[3] = plt.annotate('Cellular',[92+5,90+5], bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                #xPosition[3] = 92
                #yPosition[3] = 90
				
                #marker_number = 8
                #annotation_number = 4
                
            else:

                with open(settingsFile, "r") as settingsObject:
                    for line in settingsObject:
                        linevars = line.split(" ");
                        if (linevars[0].upper()=="M"):
                            if len(linevars)==5:
                                Sleep = int(linevars[1])
                                if (Sleep<0 or Sleep>100):
                                    messagebox.showerror("Error", "Sleep Ratio out of bounds!")
                                    break
                                Activity = int(linevars[2])
                                if (Activity<0 or Activity>100):
                                    messagebox.showerror("Error", "Activity Ratio out of bounds!")
                                    break
                                Label = linevars[3]
                                Color = linevars[4].lower().strip();
                                markers[marker_number] = plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                                markers[marker_number + 1] = plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
                                markerSizes[marker_number] = 35.0;
                                markerSizes[marker_number + 1] = 30.0;
                                marker_number = marker_number + 2;
                                xPosition[annotation_number] = Sleep;
                                yPosition[annotation_number] = Activity;
                                if (Sleep>50):
                                    if (Activity<50):                    
                                        annotations[annotation_number] = ax.text(xPosition[annotation_number]/increment - 4/(math.sqrt(2)*increment) - 0.5/increment,yPosition[annotation_number]/increment + 4/(math.sqrt(2)*increment) + 0.5/increment, Label, color = Color, verticalalignment = 'top', horizontalalignment = 'right')
                                    else:
                                        annotations[annotation_number] = ax.text(xPosition[annotation_number]/increment - 4/(math.sqrt(2)*increment) - 0.5/increment,yPosition[annotation_number]/increment - 4/(math.sqrt(2)*increment) - 0.5/increment, Label, color = Color, verticalalignment = 'bottom', horizontalalignment = 'right')
                                else:
                                    if (Activity<50):                    
                                        annotations[annotation_number] = ax.text(xPosition[annotation_number]/increment + 4/(math.sqrt(2)*increment) + 0.5/increment,yPosition[annotation_number]/increment + 4/(math.sqrt(2)*increment) + 0.5/increment, Label, color = Color, verticalalignment = 'top', horizontalalignment = 'left')
                                    else:
                                        annotations[annotation_number] = ax.text(xPosition[annotation_number]/increment + 4/(math.sqrt(2)*increment) + 0.5/increment,yPosition[annotation_number]/increment - 4/(math.sqrt(2)*increment) - 0.5/increment, Label, color = Color, verticalalignment = 'bottom', horizontalalignment = 'left')
                                annotation_number = annotation_number+1
                            else:
                                Sleep = int(linevars[1])
                                if (Sleep<0 or Sleep>100):
                                    messagebox.showerror("Error", "Sleep Ratio out of bounds!")
                                    break
                                Activity = int(linevars[2])
                                if (Activity<0 or Activity>100):
                                    messagebox.showerror("Error", "Activity Ratio out of bounds!")
                                    break
                                Label = linevars[3].strip()
                                markers[marker_number] = plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                                markers[marker_number + 1] = plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
                                markerSizes[marker_number] = 35.0
                                markerSizes[marker_number + 1] = 30.0
                                marker_number = marker_number + 2
                                xPosition[annotation_number] = Sleep
                                yPosition[annotation_number] = Activity
                                if (Sleep>50):
                                    if (Activity<50):                    
                                        annotations[annotation_number] = ax.text(xPosition[annotation_number]/increment - 4/(math.sqrt(2)*increment) - 0.5/increment,yPosition[annotation_number]/increment + 4/(math.sqrt(2)*increment) + 0.5/increment, Label, verticalalignment = 'top', horizontalalignment = 'right', bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                                    else:
                                        annotations[annotation_number] = ax.text(xPosition[annotation_number]/increment - 4/(math.sqrt(2)*increment) - 0.5/increment,yPosition[annotation_number]/increment - 4/(math.sqrt(2)*increment) - 0.5/increment, Label, verticalalignment = 'bottom', horizontalalignment = 'right', bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                                else:
                                    if (Activity<50):                    
                                        annotations[annotation_number] = ax.text(xPosition[annotation_number]/increment + 4/(math.sqrt(2)*increment) + 0.5/increment,yPosition[annotation_number]/increment + 4/(math.sqrt(2)*increment) + 0.5/increment, Label, verticalalignment = 'top', horizontalalignment = 'left', bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                                    else:
                                        annotations[annotation_number] = ax.text(xPosition[annotation_number]/increment + 4/(math.sqrt(2)*increment) + 0.5/increment,yPosition[annotation_number]/increment - 4/(math.sqrt(2)*increment) - 0.5/increment, Label, verticalalignment = 'bottom', horizontalalignment = 'left', bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                                annotation_number = annotation_number+1
                        elif (linevars[0].upper()=="WM"):
                            if len(linevars)==6:
                                Sleep = int(linevars[1])
                                if (Sleep<0 or Sleep>100):
                                    messagebox.showerror("Error", "Sleep Ratio out of bounds!")
                                    break
                                Activity = int(linevars[2])
                                if (Activity<0 or Activity>100):
                                    messagebox.showerror("Error", "Activity Ratio out of bounds!")
                                    break
                                Radius = int(linevars[3])
                                Label = linevars[4]
                                Color = linevars[5].lower().strip();
                                markers[marker_number] = plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=Radius*8.5 + 5, markeredgecolor='black', mew=3, markerfacecolor="None")
                                markers[marker_number + 1] = plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=Radius*8.5, markeredgecolor='white', mew=3, markerfacecolor="None")
                                markerSizes[marker_number] = Radius*8.5 + 5;
                                markerSizes[marker_number + 1] = Radius*8.5;
                                marker_number = marker_number + 2;
                                if (Sleep>50):
                                    if (Activity<50):                    
                                        annotations[annotation_number] = ax.text(5/increment, 5/increment, Label, color = Color, verticalalignment = 'top', horizontalalignment = 'right')
                                    else:
                                        annotations[annotation_number] = ax.text(5/increment, 5/increment, Label, color = Color, verticalalignment = 'bottom', horizontalalignment = 'right')
                                else:
                                    if (Activity<50):                    
                                        annotations[annotation_number] = ax.text(5/increment, 5/increment, Label, color = Color, verticalalignment = 'top', horizontalalignment = 'left')
                                    else:
                                        annotations[annotation_number] = ax.text(5/increment, 5/increment, Label, color = Color, verticalalignment = 'bottom', horizontalalignment = 'left')
                                xPosition[annotation_number] = Sleep;
                                yPosition[annotation_number] = Activity;
                                annotation_number = annotation_number+1;
                            else:
                                Sleep = int(linevars[1])
                                if (Sleep<0 or Sleep>100):
                                    messagebox.showerror("Error", "Sleep Ratio out of bounds!")
                                    break
                                Activity = int(linevars[2])
                                if (Activity<0 or Activity>100):
                                    messagebox.showerror("Error", "Activity Ratio out of bounds!")
                                    break
                                Radius = int(linevars[3])
                                Label = linevars[4].strip()
                                markers[marker_number] = plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=Radius*8.5 + 5, markeredgecolor='black', mew=3, markerfacecolor="None")
                                markers[marker_number + 1] = plt.plot([Sleep/increment], [Activity/increment], 'k.', markersize=Radius*8.5, markeredgecolor='white', mew=3, markerfacecolor="None")
                                markerSizes[marker_number] = Radius*8.5 + 5;
                                markerSizes[marker_number + 1] = Radius*8.5;
                                marker_number = marker_number + 2;
                                if (Sleep>50):
                                    if (Activity<50):                    
                                        annotations[annotation_number] = ax.text(5/increment, 5/increment, Label, verticalalignment = 'top', horizontalalignment = 'right', bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                                    else:
                                        annotations[annotation_number] = ax.text(5/increment, 5/increment, Label, verticalalignment = 'bottom', horizontalalignment = 'right', bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                                else:
                                    if (Activity<50):                    
                                        annotations[annotation_number] = ax.text(5/increment, 5/increment, Label, verticalalignment = 'top', horizontalalignment = 'left', bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                                    else:
                                        annotations[annotation_number] = ax.text(5/increment, 5/increment, Label, verticalalignment = 'bottom', horizontalalignment = 'left', bbox=dict(boxstyle='round,pad=0.01', fc='white', alpha=0.7))
                                xPosition[annotation_number] = Sleep;
                                yPosition[annotation_number] = Activity;
                                annotation_number = annotation_number+1;
                        elif (linevars[0][0]=="#"):
                            continue;
                        elif (len(linevars[0].strip())==0):
                            continue;
                        else:
                            messagebox.showerror("Error", "Marker specifier incorrect!")
                        
                        #if "point" in line or "Point" in line:
                        #    tmp = line.split(":")[1].strip()
                        #    active = int(tmp.split(",")[0].strip())
                        #    sleep = int(tmp.split(",")[1].strip())
                        #    plt.plot([active], [sleep], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                        #    plt.plot([active], [sleep], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")

            # want a more natural, table-like display
            ax.invert_yaxis()
            ax.xaxis.tick_top()
            ax.axis('tight')
            plt.xticks(np.array([0.5,20/increment + 0.5,40/increment + 0.5,60/increment + 0.5,80/increment + 0.5,100/increment + 0.5]), [0,20,40,60,80,100])
            plt.yticks(np.array([0.5,20/increment + 0.5,40/increment + 0.5,60/increment + 0.5,80/increment + 0.5,100/increment + 0.5]), [0,20,40,60,80,100])

            first_ipc = "{0:.2f}".format(first_entry['IPC'])
            second_ipc = "{0:.2f}".format(second_entry['IPC'])

            ipc = fig.text(0.9, 0.11, 'IPC: ' + first_ipc + ',' + second_ipc,
                     verticalalignment='bottom', horizontalalignment='left',
                     color='brown', fontsize=initialFontSize, rotation = -90)

            # ax.set_xticklabels(column_labels, minor=False)
            # ax.set_yticklabels(row_labels, minor=False)
            # plt.colorbar(heatbar2)
			
            yearlabels = utils.axisListMaker(minyears, maxyears)
            yearints = []
            yearlabels = list(yearlabels)
            yearints.insert(0, minyears*365 + 0.0001)
            yearlabels.insert(0,str(round(minyears, 1)))

            for i in range(1,len(yearlabels)):
                yearlabels[i] = int(yearlabels[i])
                yearints.append(yearlabels[i]*365)
                yearlabels[i] = str(yearlabels[i])

            yearlabels.append(round(maxyears,1))
            yearints.append(maxyears*365 - 0.0001)
            
            cbar = plt.colorbar(heatbar2, pad=0.05, ticks=yearints)
            cbar.ax.set_yticklabels(yearlabels)
            cbar.ax.tick_params(labelsize=initialFontSize)
            cbar.set_label('Years', rotation=360, size=initialAxisLabelSize, labelpad=-30, y=1.08)
            # plt.colorbar(heatbar)
            cbar2 = plt.colorbar(heatbar, pad = 0.1)
            cbar2.ax.tick_params(labelsize=initialFontSize)
            # cbar.ax.set_yticklabels(labelsize=10)
            cbar2.set_label('Days', rotation=360, size=initialAxisLabelSize, labelpad=-37.5, y=1.08)
            plt.xlabel('xlabel', fontsize=initialAxisLabelSize)
            plt.ylabel('ylabel', fontsize=initialAxisLabelSize)
            ax.set_xlabel('Percent Sleep')
            ax.xaxis.set_label_position('top')
            ax.xaxis.labelpad = 16;
            plt.ylabel('Activity Ratio')
            ax.set_title(label=plot_title, fontsize=initialTitleLabelSize, pad=12)
            
            widthScalingFactor = 2
            lengthScalingFactor = 1.3
            initialSize = min(fig.get_size_inches()[0]/widthScalingFactor,fig.get_size_inches()[1]/lengthScalingFactor)
            initialFigWidth = fig.get_size_inches()[0]
            initialFigLength = fig.get_size_inches()[1]

            ax.set_aspect('equal', adjustable = None)
            
            def on_resize(event):
                nonlocal bmarker
                Size = min(fig.get_size_inches()[0]/widthScalingFactor,fig.get_size_inches()[1]/lengthScalingFactor)
                
                # fig.patches[0].set_width(0.03/(fig.get_size_inches()[0]/initialFigWidth)*(fig.get_size_inches()[0]/initialFigWidth)**0.5)
                # fig.patches[0].set_height(0.03/(fig.get_size_inches()[1]/initialFigLength)*(fig.get_size_inches()[0]/initialFigWidth)**0.5)
                
                # fig.patches[0].set_y(0.8505 + 0.03 - 0.03/(fig.get_size_inches()[1]/initialFigLength)*(fig.get_size_inches()[0]/initialFigWidth)**0.5)
                # Inf.set_y(0.918 + 0.03 - 0.03/(fig.get_size_inches()[1]/initialFigLength)*(fig.get_size_inches()[0]/initialFigWidth)**0.5)
                
                #(0.93,0.8505), 0.03, 0.03

                for i in range(marker_number):
                    markers[i][0].set_markersize(markerSizes[i]*Size/initialSize)
                for i in range(annotation_number):
                    if (Size/initialSize<1.5):
                        annotations[i].set_fontsize(10*Size/initialSize)
                    else:
                        annotations[i].set_fontsize(15)
                    if markerSizes[i*2]==35.0:
                        if (xPosition[i]>50):
                            if (yPosition[i]<50):                    
                                annotations[i].set_x(xPosition[i]/increment - 4/(math.sqrt(2)*increment) - 0.5/(Size/initialSize*increment))
                                annotations[i].set_y(yPosition[i]/increment + 4/(math.sqrt(2)*increment) + 0.5/(Size/initialSize*increment))
                            else:
                                annotations[i].set_x(xPosition[i]/increment - 4/(math.sqrt(2)*increment) - 0.5/(Size/initialSize*increment))
                                annotations[i].set_y(yPosition[i]/increment - 4/(math.sqrt(2)*increment) - 0.5/(Size/initialSize*increment))
                        else:
                            if (yPosition[i]<50):                    
                                annotations[i].set_x(xPosition[i]/increment + 4/(math.sqrt(2)*increment) + 0.5/(Size/initialSize*increment))
                                annotations[i].set_y(yPosition[i]/increment + 4/(math.sqrt(2)*increment) + 0.5/(Size/initialSize*increment))
                            else:
                                annotations[i].set_x(xPosition[i]/increment + 4/(math.sqrt(2)*increment) + 0.5/(Size/initialSize*increment))
                                annotations[i].set_y(yPosition[i]/increment - 4/(math.sqrt(2)*increment) - 0.5/(Size/initialSize*increment))
                    else:
                        if (xPosition[i]>50):
                            if (yPosition[i]<50):                    
                                annotations[i].set_x(xPosition[i]/increment - (markerSizes[i*2 + 1])/(9*math.sqrt(2)*increment) - 1/((Size/initialSize)*increment))
                                annotations[i].set_y(yPosition[i]/increment + (markerSizes[i*2 + 1])/(9*math.sqrt(2)*increment) + 1/((Size/initialSize)*increment))
                            else:
                                annotations[i].set_x(xPosition[i]/increment - (markerSizes[i*2 + 1])/(9*math.sqrt(2)*increment) - 1/((Size/initialSize)*increment))
                                annotations[i].set_y(yPosition[i]/increment - (markerSizes[i*2 + 1])/(9*math.sqrt(2)*increment) - 1/((Size/initialSize)*increment))
                        else:
                            if (yPosition[i]<50):                                        
                                annotations[i].set_x(xPosition[i]/increment + (markerSizes[i*2 + 1])/(9*math.sqrt(2)*increment) + 1/((Size/initialSize)*increment))
                                annotations[i].set_y(yPosition[i]/increment + (markerSizes[i*2 + 1])/(9*math.sqrt(2)*increment) + 1/((Size/initialSize)*increment))
                            else:
                                annotations[i].set_x(xPosition[i]/increment + (markerSizes[i*2 + 1])/(9*math.sqrt(2)*increment) + 1/((Size/initialSize)*increment))
                                annotations[i].set_y(yPosition[i]/increment - (markerSizes[i*2 + 1])/(9*math.sqrt(2)*increment) - 1/((Size/initialSize)*increment))

                if (Size<initialSize):
                    # Inf.set_size(initialAxisLabelSize*Size/initialSize)

                    ax.tick_params(axis = 'both', labelsize = initialFontSize*Size/initialSize)
                    ax.xaxis.label.set_size(initialAxisLabelSize*Size/initialSize)
                    ax.yaxis.label.set_size(initialAxisLabelSize*Size/initialSize)
                    ax.xaxis.labelpad = 16*Size/initialSize
                    ax.yaxis.labelpad = 16*Size/initialSize - 8
                    ax.set_title(label=plot_title, fontsize=initialTitleLabelSize*Size/initialSize, pad=12*Size/initialSize)
                    cbar.ax.tick_params(labelsize=initialFontSize*(Size/initialSize)*math.sqrt(Size/initialSize))
                    cbar2.ax.tick_params(labelsize=initialFontSize*Size/initialSize*math.sqrt(Size/initialSize))
                    cbar.set_label('Years', rotation=360, size=initialAxisLabelSize*Size/initialSize, labelpad=-30*Size/initialSize, y=1.08)            
                    cbar2.set_label('Days', rotation=360, size=initialAxisLabelSize*Size/initialSize, labelpad=-37.5*Size/initialSize, y=1.08)
                else:
                    # Inf.set_size(initialAxisLabelSize)
                    # fig.patches[0].set_x((0.93-0.90)/(fig.get_size_inches()[0]/initialFigWidth) + 0.90)
                    ax.tick_params(axis = 'both', labelsize = initialFontSize)
                    ax.xaxis.label.set_size(initialAxisLabelSize)
                    ax.yaxis.label.set_size(initialAxisLabelSize)
                    ax.xaxis.labelpad = 16;
                    ax.yaxis.labelpad = 8;
                    cbar.ax.tick_params(labelsize=initialFontSize)
                    cbar2.ax.tick_params(labelsize=initialFontSize)
                    cbar.set_label('Years', rotation=360, size=initialAxisLabelSize, labelpad=-30, y=1.08)            
                    cbar2.set_label('Days', rotation=360, size=initialAxisLabelSize, labelpad=-37.5, y=1.08)
                    
                bmarker.label.set_fontsize(10*Size/initialSize)
                bigmarker.label.set_fontsize(10*Size/initialSize)
                ipc.set_fontsize(initialFontSize*Size/initialSize)
                    
            
            def PlaceNewMarker(event):
                nonlocal annotation_number
                nonlocal marker_number
                Sleep = int(simpledialog.askstring("Sleep","Please enter the Marker's Sleep Ratio:")) # Prompts user for the sleep ratio at which the point is at
                Activity = int(simpledialog.askstring("Activity","Please enter the Marker's Activity Ratio:")) # Prompts user for the activity ratio at which the point is at
                Label = str(simpledialog.askstring("Label","Please enter the Marker's Label. The next window will ask for the label's color."))
                my_color = colorchooser.askcolor() #Ask the user for a color
                
                Size = min(fig.get_size_inches()[0]/widthScalingFactor,fig.get_size_inches()[1]/lengthScalingFactor)                
                xPosition[annotation_number] = Sleep;
                yPosition[annotation_number] = Activity;
                if (Sleep>50):
                    if (Activity<50):                    
                        annotations[annotation_number] = ax.text(xPosition[annotation_number]/increment - 4/(math.sqrt(2)*increment) - 0.5/(Size/initialSize*increment),yPosition[annotation_number]/increment + 4/(math.sqrt(2)*increment) + 0.5/(Size/initialSize*increment), Label, color = my_color[1], verticalalignment = 'top', horizontalalignment = 'right')
                    else:
                        annotations[annotation_number] = ax.text(xPosition[annotation_number]/increment - 4/(math.sqrt(2)*increment) - 0.5/(Size/initialSize*increment),yPosition[annotation_number]/increment - 4/(math.sqrt(2)*increment) - 0.5/(Size/initialSize*increment), Label, color = my_color[1], verticalalignment = 'bottom', horizontalalignment = 'right')
                else:
                    if (Activity<50):                    
                        annotations[annotation_number] = ax.text(xPosition[annotation_number]/increment + 4/(math.sqrt(2)*increment) + 0.5/(Size/initialSize*increment),yPosition[annotation_number]/increment + 4/(math.sqrt(2)*increment) + 0.5/(Size/initialSize*increment), Label, color = my_color[1], verticalalignment = 'top', horizontalalignment = 'left')
                    else:
                        annotations[annotation_number] = ax.text(xPosition[annotation_number]/increment + 4/(math.sqrt(2)*increment) + 0.5/(Size/initialSize*increment),yPosition[annotation_number]/increment - 4/(math.sqrt(2)*increment) - 0.5/(Size/initialSize*increment), Label, color = my_color[1], verticalalignment = 'bottom', horizontalalignment = 'left')
                
                markerSizes[marker_number] = 35.0;
                markerSizes[marker_number + 1] = 30.0;
                markers[marker_number] = ax.plot([Sleep/increment], [Activity/increment], 'k.', markersize=35.0*Size/initialSize, markeredgecolor='black', mew=3, markerfacecolor="None")
                markers[marker_number + 1] = ax.plot([Sleep/increment], [Activity/increment], 'k.', markersize=30.0*Size/initialSize, markeredgecolor='white', mew=3, markerfacecolor="None")
                marker_number = marker_number + 2
                annotation_number = annotation_number + 1
                if event.inaxes is not None:
                    event.inaxes.figure.canvas.draw_idle()

            def PlaceNewWideMarker(event):
                nonlocal annotation_number
                nonlocal marker_number                
                Sleep = int(simpledialog.askstring("Sleep","Please enter the Marker's Sleep Ratio:")) # Prompts user for the sleep ratio at which the point is at
                Activity = int(simpledialog.askstring("Activity","Please enter the Marker's Activity Ratio:")) # Prompts user for the activity ratio at which the point is at
                Radius = int(simpledialog.askstring("Radius","Please enter the Marker's Radius:"))
                Label = str(simpledialog.askstring("Label","Please enter the Marker's Label. The next window will ask for the label's color."))
                my_color = colorchooser.askcolor() #Ask the user for a color
                
                Size = min(fig.get_size_inches()[0]/widthScalingFactor,fig.get_size_inches()[1]/lengthScalingFactor)
                markerSizes[marker_number] = Radius*8.5 + 5
                markerSizes[marker_number + 1] = Radius*8.5
                markers[marker_number] = ax.plot([Sleep/increment], [Activity/increment], 'k.', markersize=(Radius*8.5 + 5)*Size/initialSize, markeredgecolor='black', mew=3, markerfacecolor="None")
                markers[marker_number + 1] = ax.plot([Sleep/increment], [Activity/increment], 'k.', markersize=(Radius*8.5)*Size/initialSize, markeredgecolor='white', mew=3, markerfacecolor="None")
                                
                xPosition[annotation_number] = Sleep
                yPosition[annotation_number] = Activity

                if (Sleep>50):
                    if (Activity<50):                    
                        annotations[annotation_number] = ax.text(5/increment, 5/increment, Label, color = my_color[1], verticalalignment = 'top', horizontalalignment = 'right')
                        annotations[annotation_number].set_x(xPosition[annotation_number]/increment - (markerSizes[annotation_number*2 + 1])/(9*math.sqrt(2)*increment) - 1/((Size/initialSize)*increment))
                        annotations[annotation_number].set_y(yPosition[annotation_number]/increment + (markerSizes[annotation_number*2 + 1])/(9*math.sqrt(2)*increment) + 1/((Size/initialSize)*increment))
                    else:
                        annotations[annotation_number] = ax.text(5/increment, 5/increment, Label, color = my_color[1], verticalalignment = 'bottom', horizontalalignment = 'right')
                        annotations[annotation_number].set_x(xPosition[annotation_number]/increment - (markerSizes[annotation_number*2 + 1])/(9*math.sqrt(2)*increment) - 1/((Size/initialSize)*increment))
                        annotations[annotation_number].set_y(yPosition[annotation_number]/increment - (markerSizes[annotation_number*2 + 1])/(9*math.sqrt(2)*increment) - 1/((Size/initialSize)*increment))
                else:
                    if (Activity<50):                    
                        annotations[annotation_number] = ax.text(5/increment, 5/increment, Label, color = my_color[1], verticalalignment = 'top', horizontalalignment = 'left')
                        annotations[annotation_number].set_x(xPosition[annotation_number]/increment + (markerSizes[annotation_number*2 + 1])/(9*math.sqrt(2)*increment) + 1/((Size/initialSize)*increment))
                        annotations[annotation_number].set_y(yPosition[annotation_number]/increment + (markerSizes[annotation_number*2 + 1])/(9*math.sqrt(2)*increment) + 1/((Size/initialSize)*increment))
                    else:
                        annotations[annotation_number] = ax.text(5/increment, 5/increment, Label, color = my_color[1], verticalalignment = 'bottom', horizontalalignment = 'left')
                        annotations[annotation_number].set_x(xPosition[annotation_number]/increment + (markerSizes[annotation_number*2 + 1])/(9*math.sqrt(2)*increment) + 1/((Size/initialSize)*increment))
                        annotations[annotation_number].set_y(yPosition[annotation_number]/increment - (markerSizes[annotation_number*2 + 1])/(9*math.sqrt(2)*increment) - 1/((Size/initialSize)*increment))

                        
                marker_number = marker_number + 2
                annotation_number = annotation_number + 1
                if event.inaxes is not None:
                    event.inaxes.figure.canvas.draw_idle()               
            
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
                

            # total_raw_dynamic1 = first_entry['dynamicMemory'] + first_entry['dynamicPower']
            # total_raw_dynamic2 = second_entry['dynamicMemory'] + second_entry['dynamicPower']

            # total_static1 = first_entry['staticMemory'] + first_entry['staticPower']
            # total_static2 = second_entry['staticMemory'] + second_entry['staticPower']
            
            # total_dynamic1 = 
            
            markerax = plt.axes([0.51, .01, 0.3, 0.075])
            bmarker = Button(markerax, 'Place New Marker')
            bmarker.on_clicked(PlaceNewMarker)

            bigmarkerax = plt.axes([0.13, .01, 0.35, 0.075])
            bigmarker = Button(bigmarkerax, 'Place New Wide Marker')
            bigmarker.on_clicked(PlaceNewWideMarker)

            # plt.title(''.join([utils.rename(self.entry1, False), ' vs. ', utils.rename(self.entry2, False)]), y=1.08)

            #image_file_name = path_to_output_directory + title1 + "_vs_" + title2 + ".pdf"

            #Inf = fig.text(0.90, 0.918, "Infinite", fontsize = initialAxisLabelSize)
            #fig.patches.extend([Rectangle((0.93,0.8505), 0.03, 0.03, fc = 'w', hatch = '///', ec = 'black', transform=fig.transFigure, figure=fig)])
            
            fig.canvas.mpl_connect('resize_event', on_resize)
            #fig.tight_layout()
            plt.show(block=False)
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
    
    # The points are done once to determine the maximum x axis location in order to plot the background colors.     
    #For some reason the background color overlay the plot points but they do not overlay the labels     
    #Func is called second time to plot the points over the background of color in order fot the points to be visible 
    @staticmethod
    def make_single_plot_carbon_points(self, first_entry, second_entry):        
        # Plotting location manufacturing phase Carbon for CPU
        sep = 4 # Separation between plotted point and label
        plt.plot([first_entry['Total CPU Carbon']], [first_entry['processSizeNum']], 'b', marker='o', markersize=10.0, markeredgecolor='blue', mew=3, markerfacecolor="blue", alpha=1.0)
        plt.plot([second_entry['Total CPU Carbon']], [second_entry['processSizeNum']], 'w', marker='o', markersize=10.0, markeredgecolor='black', mew=3, markerfacecolor="black", alpha=1.0)
        
        # Plotting location manufacturing phase Carbon for DRAM      
        plt.plot([first_entry['Total DRAM Carbon']], [first_entry['processSizeDramNum']], 'y', marker='o', markersize=10.0, markeredgecolor='yellow', mew=3, markerfacecolor="yellow", alpha=1.0)
        plt.plot([second_entry['Total DRAM Carbon']], [second_entry['processSizeDramNum']], 'm', marker='o', markersize=10.0, markeredgecolor='magenta', mew=3, markerfacecolor="magenta", alpha=1.0)
        
        #Plotting location usage phase Carbon
        plt.plot([first_entry['CPU Hourly Usage Carbon']], [first_entry['processSizeNum']], 'purple', marker='o', markersize=10.0, markeredgecolor='purple', mew=3, markerfacecolor="purple", alpha=1.0)  
        plt.plot([second_entry['CPU Hourly Usage Carbon']], [second_entry['processSizeNum']], 'brown', marker='o', markersize=10.0, markeredgecolor='brown', mew=3, markerfacecolor="brown", alpha=1.0) 
        plt.plot([first_entry['DRAM Hourly Usage Carbon']], [first_entry['processSizeDramNum']], 'orange', marker='o', markersize=10.0, markeredgecolor='orange', mew=3, markerfacecolor="orange", alpha=1.0)
        plt.plot([second_entry['DRAM Hourly Usage Carbon']], [second_entry['processSizeDramNum']], 'cyan', marker='o', markersize=10.0, markeredgecolor='cyan', mew=3, markerfacecolor="cyan", alpha=1.0)
    
    @staticmethod
    def make_single_plot_carbon(self, first_entry, second_entry, title1, title2, res):
        leftColor='lime' #green
        rightColor='red' #red
        
        if settingsConfig.nativePlotting:
            matplotlib.rc('xtick', labelsize=16)
            matplotlib.rc('ytick', labelsize=16)


            if first_entry is None or second_entry is None:
                return

            settingsFile = settingsConfig.advancedSettingsFile
            #arr controls the heatmap coloring
            #arr = utils.perform_greenchip_analysis(res)
        
            fig, ax = plt.subplots()
            
            cdict2 = OurConstants.get_cdict2()

            cdict1 = OurConstants.get_cdict1()

            customgray = LinearSegmentedColormap('customgray', cdict1)
            customspectrum = LinearSegmentedColormap('customspectrum', cdict2)
            c = (0, 0, 0, 0)
            my_cmap = plt.get_cmap(customspectrum)
            my_cmap.set_under(color='white')
            second_cmap = plt.get_cmap(customgray)
            second_cmap.set_under(color=c)
            ''' 
            heatmap = ax.pcolormesh(arr, cmap=my_cmap, vmax=3650, vmin=0)
            heatbar = heatmap
            heatmap = ax.pcolormesh(arr, cmap=second_cmap, vmax=36000, vmin=4000)
            heatbar2 = heatmap
            '''

            if settingsFile is None:
                '''    
                # Desktop
                plt.plot([77], [17], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                plt.plot([77], [17], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
                plt.annotate('Desktop',[77+5,17+5])

                # Server
                plt.plot([5], [30], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                plt.plot([5], [30], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
                plt.annotate('Server',[5+5,30+5])

                # HPC
                plt.plot([5], [95], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                plt.plot([5], [95], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
                plt.annotate('HPC',[5+5,95+5])
                
                # Cell Phone
                plt.plot([92], [90], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                plt.plot([92], [90], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
                plt.annotate('Cellular',[92+5,90+5])
                '''
                utils.make_single_plot_carbon_points(self,first_entry,second_entry)    
                
            else:

                with open(settingsFile, "r") as settingsObject:
                    for line in settingsObject:
                        if "point" in line or "Point" in line:
                            tmp = line.split(":")[1].strip()
                            carbonEm = int(tmp.split(",")[0].strip())
                            techNodenm = int(tmp.split(",")[1].strip())
                            plt.plot([carbonEm], [techNodenm], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                            plt.plot([carbonEm], [techNodenm], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")

            # want a more natural, table-like display
            ax.invert_yaxis()
            ax.xaxis.tick_top()
            ax.axis('tight')

            '''first_ipc = "{0:.2f}".format(first_entry['IPC'])
            second_ipc = "{0:.2f}".format(second_entry['IPC'])

            fig.text(0.95, 0.01, 'IPC: ' + first_ipc + ',' + second_ipc,
                     verticalalignment='bottom', horizontalalignment='left',
                     color='brown', fontsize=15)
                     '''

            # ax.set_xticklabels(column_labels, minor=False)
            # ax.set_yticklabels(row_labels, minor=False)
            # plt.colorbar(heatbar2)
            '''
            cbar = plt.colorbar(heatbar2, pad=0.05)
            cbar.ax.set_yticklabels(['11', '22', '33', '44', '55', '66', '77', '88', '99'])
            cbar.ax.tick_params(labelsize=16)
            cbar.set_label('Carbon Value', rotation=360, size=20, labelpad=-30, y=1.08)
            '''
            # plt.colorbar(heatbar)
            #cbar2 = plt.colorbar(heatbar)
            #cbar2.ax.tick_params(labelsize=16)
            # cbar.ax.set_yticklabels(labelsize=10)
            '''
            cbar2.set_label('days', rotation=360, size=20, labelpad=-37.5, y=1.08)
            '''
            plt.xlabel('xlabel', fontsize=16)
            plt.ylabel('ylabel', fontsize=16)
            plt.title(label='Carbon Generated from Manufacturing and Hourly Usage', fontsize='20', pad='20')
            # plt.xlabel('Percent Sleep')
            ax.set_xlabel('Carbon Emission (gCO2)')
            ax.xaxis.set_label_position('top')
            plt.ylabel('Technology Node (nm)')
            # plt.title(''.join([utils.rename(self.entry1, False), ' vs. ', utils.rename(self.entry2, False)]), y=1.08)

            #image_file_name = path_to_output_directory + title1 + "_vs_" + title2 + ".pdf"
            
            axes = plt.gca()
            n = int(axes.get_xlim()[1])
            
            for x in range(n+1):
                ax.axvline(x, color=colorFader(leftColor, rightColor, x/n), linewidth=6, alpha=1.0) 
            
            utils.make_single_plot_carbon_points(self, first_entry, second_entry)
            blue_patch=mpatches.Patch(color='blue', label='CPU Manufacturing - ' + first_entry['LocationManu CPU'])
            black_patch=mpatches.Patch(color='black', label='CPU Manufacturing - ' + second_entry['LocationManu CPU'])
            yellow_patch=mpatches.Patch(color='yellow', label='DRAM Manufacturing - ' + first_entry['LocationManu DRAM'])
            magenta_patch=mpatches.Patch(color='magenta', label='DRAM Manufacturing - ' + second_entry['LocationManu DRAM'])
            purple_patch=mpatches.Patch(color='purple', label='CPU Use/Hour - ' + first_entry['Carbon Use Phase Loc'])
            brown_patch=mpatches.Patch(color='brown', label='CPU Use/Hour - ' + second_entry['Carbon Use Phase Loc'])
            orange_patch=mpatches.Patch(color='orange', label='DRAM Use/Hour - ' + first_entry['Carbon Use Phase Loc'])
            cyan_patch=mpatches.Patch(color='cyan', label='DRAM Use/Hour - ' + second_entry['Carbon Use Phase Loc'])
            
            plt.legend(handles=[blue_patch, black_patch, yellow_patch, magenta_patch, purple_patch, brown_patch, orange_patch, cyan_patch], loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)
            #plt.figure().subplots_adjust(bottom=0.5)
            fig.tight_layout()       #try if other things are not working   
            
            plt.show()
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

class OurConstants(object):


    @staticmethod
    def get_cdict2():
        return {'red': ((0.0, 0.0, 0.0),  # black
                          (0.13, 1.0, 1.0),  # purple
                          (0.26, 0.0, 0.0),  # blue
                          (0.39, 0.0, 0.0),  #teal
                          (0.52, 0.0, 0.0),  # green
                          (0.65, 1.0, 1.0),  # yellow
                          (0.78, 1.0, 1.0),  # orange
                          (0.9, 1.0, 1.0),  # red
                          (1.0, 0.3, 0.3)),  # gray

                  'green': ((0.0, 0.0, 0.0),
                            (0.13, 0.0, 0.0),  # purple
                            (0.26, 0.0, 0.0),  # blue
                            (0.39, 0.5, 0.5),  #teal
                            (0.52, 1.0, 1.0),  # green
                            (0.65, 1.0, 1.0),  # yellow
                            (0.78, 0.5, 0.5),  # orange
                            (0.9, 0.0, 0.0),  # red
                            (1.0, 0.3, 0.3)),  # gray


                  'blue': ((0.0, 0.0, 0.0),
                           (0.13, 1.0, 1.0),  # purple
                           (0.26, 1.0, 1.0),  # blue
                           (0.39, 0.5, 0.5),  #teal
                           (0.52, 0.0, 0.0),  # green
                           (0.65, 0.0, 0.0),  # yellow
                           (0.78, 0.0, 0.0),  # orange
                           (0.9, 0.0, 0.0),  # red
                           (1.0, 0.3, 0.3)),}  # gray

    @staticmethod
    def get_cdict1():
        return {'red': ((0.0, 0.3, 0.3),
                          (0.05, 0.4, 0.4),
                          (0.1, 0.5, 0.5),
                          (0.2, 0.6, 0.6),
                          (1.0, 1.0, 1.0)),

                  'green': ((0.0, 0.3, 0.3),
                            (0.05, 0.4, 0.4),
                            (0.1, 0.5, 0.5),
                            (0.2, 0.6, 0.6),
                            (1.0, 1.0, 1.0)),

                  'blue': ((0.0, 0.3, 0.3),
                           (0.05, 0.4, 0.4),
                           (0.1, 0.5, 0.5),
                           (0.2, 0.6, 0.6),
                           (1.0, 1.0, 1.0)),}
