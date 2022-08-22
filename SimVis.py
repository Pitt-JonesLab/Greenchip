import ast
import sys
import os
import subprocess
from sys import platform
from tkinter import *
from tkinter import ttk
import Pmw
from tkinter import filedialog
from tkinter import messagebox
import plugins.shared.Config as config
import csv
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt



try:
    import matplotlib
    matplotlib.use("TkAgg")
    config.nativePlotting = True
except ImportError:
    config.nativePlotting = False

from Database import flatfileDB
from PluginHandler import import_plugins
from plugins.shared.Utils import OurConstants
from plugins.shared.Utils import utils

global gridMixSettingsFilename
global gridMixSettingsDefaultFilename
gridMixSettingsFilename = os.path.join(os.path.abspath(os.getcwd()), 'EnergyGridMix.csv')
gridMixSettingsDefaultFilename = gridMixSettingsFilename

plugins_dirs = "plugins"
sys.path.extend(plugins_dirs.split(os.pathsep))
import_plugins(plugins_dirs, globals())
plugins = ['Raw Data Entry', 'Raw Data Entry Sliders', 'Breakeven -- Sniper', 'Indifference -- Sniper', 'All Breakeven -- Sniper', 'All Indifference -- Sniper']
windows = {'Raw Data Entry' : None, 'Raw Data Entry Sliders' : None, 'Breakeven -- Sniper' : None, 'Indifference -- Sniper' : None, 'All Breakeven -- Sniper' : None, 'All Indifference -- Sniper' : None, 'Increment' : None}

def path_shortener(path):
    if len(path) > 25:
        return  path[0:25] + '...'  
    else:
        return path

def browse_filename():
    # Allow user to select a directory and store it in global var
    # called folder_path 
    global gridMixSettingsFilename
    filename = filedialog.askopenfile(initialdir = os.path.dirname(gridMixSettingsFilename))
    if (filename is None or filename==""):
        gridMixSettingsFilename = gridMixSettingsDefaultFilename
        balloon.bind(csvPathLbl, gridMixSettingsDefaultFilename)
        return 

    gridMix_file_path.set(path_shortener(filename.name))
    gridMixSettingsFilename = os.path.join(filename.name, '')
    lastchar=gridMixSettingsFilename[-1]
    if lastchar == '/' or lastchar == '\\' :
        gridMixSettingsFilename=gridMixSettingsFilename[:-1]

    balloon.bind(csvPathLbl, gridMixSettingsFilename)

    newEnergyData = []
    filename=os.path.normpath(gridMixSettingsFilename)
    with open(filename, 'r') as file:
        reader=csv.reader(file)
        for row in reader:
            if row[0]!='Country': newEnergyData.append(row)
    
    
    if windows['Raw Data Entry'] is not None:
        windows['Raw Data Entry'].energyData = newEnergyData

    if windows['Raw Data Entry Sliders'] is not None:
        windows['Raw Data Entry Sliders'].energyData = newEnergyData
                
    if windows['Breakeven -- Sniper'] is not None:
        windows['Breakeven -- Sniper'].energyData = newEnergyData

    if windows['Indifference -- Sniper'] is not None:
        windows['Indifference -- Sniper'].energyData = newEnergyData

    if windows['All Breakeven -- Sniper'] is not None:
        windows['All Breakeven -- Sniper'].energyData = newEnergyData

    if windows['All Indifference -- Sniper'] is not None:
        windows['All Indifference -- Sniper'].energyData = newEnergyData

def browse_button_input():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path_in, folder_path_in_actual
    
    f = open("defaultFolders.txt", "r+")
    defaults = f.readlines()
    filename1 = None
    if defaults[0]=='\n':
        filename1 = filedialog.askdirectory()
    else:
        filename1 = filedialog.askdirectory(initialdir = os.path.normpath(defaults[0].strip()))

    if (filename1 is None or filename1==""):
        return

    defaults[0] = filename1 + "\n"
    f.seek(0)
    f.truncate(0)
    f.writelines(defaults)
    f.close()
    
    folder_path_in.set(filename1)
    folder_path_in_actual.set(filename1)
    balloon.bind(lbl1, folder_path_in.get())
    folder_path_in.set(path_shortener(folder_path_in.get()))
    #print(filename)

def browse_button_settings():
    # Allow user to select a directory and store it in global var
    # called folder_path
    f = open("defaultFolders.txt", "r+")
    defaults = f.readlines()
    filename_settings = None
    if defaults[4]=='\n':
        filename_settings = filedialog.askopenfile()
    else:
        filename_settings = filedialog.askopenfile(initialdir = os.path.normpath(defaults[4].strip()))

    if (filename_settings is None or filename_settings==""):
        return

    defaults[4] = os.path.dirname(filename_settings.name) + "\n"
    f.seek(0)
    f.truncate(0)
    f.writelines(defaults)
    f.close()
    
    
    folder_path_settings.set(filename_settings.name)
    folder_path_settings_actual.set(filename_settings.name)
    balloon.bind(settingslbl1, folder_path_settings.get())
    if (len(folder_path_settings.get()) > 2):
        config.advancedSettingsFile = folder_path_settings.get()
    else:
        config.advancedSettingsFile = None
    folder_path_settings.set(path_shortener(folder_path_settings.get()))

def browse_button_sliders():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path_in2
    
    f = open("defaultFolders.txt", "r+")
    defaults = f.readlines()
    filename_sliders = None
    if defaults[5]=='\n':
        filename_sliders = filedialog.askopenfile()
    else:
        filename_sliders = filedialog.askopenfile(initialdir = os.path.normpath(defaults[5].strip()))

    if (filename_sliders is None or filename_sliders==""):
        return

    defaults[5] = os.path.dirname(filename_sliders.name) + "\n"
    f.seek(0)
    f.truncate(0)
    f.writelines(defaults)
    f.close()
    
    folder_path_sliders.set(filename_sliders.name)
    balloon.bind(sliderslbl1, folder_path_sliders.get())
    if (len(folder_path_sliders.get()) > 2):
        config.slidersFile = folder_path_sliders.get()
    else:
        config.slidersFile = None
    folder_path_sliders.set(path_shortener(folder_path_sliders.get()))

def browse_button_output():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path_out
    
    f = open("defaultFolders.txt", "r+")
    defaults = f.readlines()
    filename2 = None
    if defaults[3]=='\n':
        filename2 = filedialog.askdirectory()
    else:
        filename2 = filedialog.askdirectory(initialdir = os.path.normpath(defaults[3].strip()))
    
    if (filename2 is None or filename2==""):
        return
    
    defaults[3] = filename2 + "\n"
    f.seek(0)
    f.truncate(0)
    f.writelines(defaults)
    f.close()
    
    folder_path_out.set(filename2)
    folder_path_out_actual.set(filename2)
    balloon.bind(lbl2, folder_path_out.get())
    folder_path_out.set(path_shortener(folder_path_out.get()))

def plot_carbon():
    #print ('Plot goes here')
    carbonValues=[]
    locations=[]
    fileDir=os.path.dirname(os.path.realpath('__file__'))
    filename=os.path.join(fileDir,'EnergyGridMix.csv')
    with open(filename, 'r') as file:
        reader=csv.reader(file)
        for row in reader:
            locations.append(row[0])
            carbonValues.append(int(row[1]))
    print(locations)
    print(carbonValues)
    '''fig=plt.figure()
    ax=fig.add_axes([0,0,1,1])
    ax.bar(locations, carbonValues)
    '''
    plt.rcParams["figure.figsize"] = (8,5)
    plt.bar(locations,carbonValues)
    plt.xticks(rotation=90, fontsize=10)
    plt.xlabel('Locations')
    plt.ylabel('Carbon Emission in gCo2eq/kWh')
    plt.title('Carbon Emissions by location')
    plt.show()
    
def settingsSetter():
    global root, increment1, increment1_temp, increment2, increment2_temp, increment3, increment3_temp, increment4, increment4_temp
    
    global mindays, maxdays, minyears, maxyears, mindays_temp, maxdays_temp, minyears_temp, maxyears_temp

    if windows['Increment'] is None:
    
        increment1_temp = StringVar()
        increment2_temp = StringVar()
        increment3_temp = StringVar()
        increment4_temp = StringVar()
        
        mindays_temp = StringVar()
        maxdays_temp = StringVar()
        minyears_temp = StringVar()
        maxyears_temp = StringVar()
        
        def window_exit():
            windows['Increment'] = None
            window.destroy()
            
        def save():
            global increment1, increment2, increment3, increment4
            global mindays, maxdays, minyears, maxyears
            global tabIncrement, tabColor, tabControl

            if 100/float(increment1_temp.get())!=int(100/float(increment1_temp.get())):
                messagebox.showerror("Raw Data Increment Error", "The Raw Data Plot Generation Increment does not divide into 100 evenly. Please use an increment that does.")
                window.lift()
                tabControl.select(tabIncrement)
                return
            if 100/float(increment2_temp.get())!=int(100/float(increment2_temp.get())): 
                messagebox.showerror("Breakeven/Indifference Increment Error", "The Breakeven/Indifference Increment does not divide into 100 evenly. Please use an increment that does.")
                window.lift()
                tabControl.select(tabIncrement)
                return
            if 100/float(increment3_temp.get())!=int(100/float(increment3_temp.get())): 
                messagebox.showerror("All Breakeven/All Indifference Increment Error", "The All Breakeven/All Indifference Increment does not divide into 100 evenly. Please use an increment that does.")
                window.lift()
                tabControl.select(tabIncrement)
                return
            if 100/float(increment4_temp.get())!=int(100/float(increment4_temp.get())): 
                messagebox.showerror("Preview Increment Error", "The Raw Data Entry Sliders Preview Increment does not divide into 100 evenly. Please use an increment that does.")
                window.lift()
                tabControl.select(tabIncrement)
                return
                
            if float(mindays_temp.get())>float(maxdays_temp.get()):
                messagebox.showerror("Colobar Settings Error", "The minimum amount of days is greater than the maximum amount of days. Maybe the values are reversed?")
                window.lift()
                tabControl.select(tabColor)
                return

            if float(minyears_temp.get())>float(maxyears_temp.get()):
                messagebox.showerror("Grayscale Settings Error", "The minimum amount of years is greater than the maximum amount of years. Maybe the values are reversed?")
                window.lift()
                tabControl.select(tabColor)
                return

            if (float(minyears_temp.get())*365)<float(maxdays_temp.get()):
                messagebox.showerror("Colorbar/Grayscale Settings Error", "The minimum amount of years is less than the maximum amount of days. Please increase the number of years, decrease the number of days, or both.")
                window.lift()
                tabControl.select(tabColor)
                return

            
            if windows['Raw Data Entry'] is not None:
                windows['Raw Data Entry'].increment = float(increment1_temp.get())
                windows['Raw Data Entry'].mindays = float(mindays_temp.get())
                windows['Raw Data Entry'].maxdays = float(maxdays_temp.get())
                windows['Raw Data Entry'].minyears = float(minyears_temp.get())
                windows['Raw Data Entry'].maxyears = float(maxyears_temp.get())

            if windows['Raw Data Entry Sliders'] is not None:
                windows['Raw Data Entry Sliders'].increment1 = float(increment1_temp.get())
                windows['Raw Data Entry Sliders'].increment2 = float(increment4_temp.get())
                windows['Raw Data Entry Sliders'].mindays = float(mindays_temp.get())
                windows['Raw Data Entry Sliders'].maxdays = float(maxdays_temp.get())
                windows['Raw Data Entry Sliders'].minyears = float(minyears_temp.get())
                windows['Raw Data Entry Sliders'].maxyears = float(maxyears_temp.get())

                if windows['Raw Data Entry Sliders'].isOpen and (increment4!=float(increment4_temp.get()) or round(maxdays,2)!=round(float(maxdays_temp.get()),2) or round(minyears,2)!=round(float(minyears_temp.get()),2) or round(maxyears,2)!=round(float(maxyears_temp.get()),2)): windows['Raw Data Entry Sliders'].plot_mini()
                
            if windows['Breakeven -- Sniper'] is not None:
                windows['Breakeven -- Sniper'].increment = float(increment2_temp.get())
                windows['Breakeven -- Sniper'].mindays = float(mindays_temp.get())
                windows['Breakeven -- Sniper'].maxdays = float(maxdays_temp.get())
                windows['Breakeven -- Sniper'].minyears = float(minyears_temp.get())
                windows['Breakeven -- Sniper'].maxyears = float(maxyears_temp.get())


            if windows['Indifference -- Sniper'] is not None:
                windows['Indifference -- Sniper'].increment = float(increment2_temp.get())
                windows['Indifference -- Sniper'].mindays = float(mindays_temp.get())
                windows['Indifference -- Sniper'].maxdays = float(maxdays_temp.get())
                windows['Indifference -- Sniper'].minyears = float(minyears_temp.get())
                windows['Indifference -- Sniper'].maxyears = float(maxyears_temp.get())

            if windows['All Breakeven -- Sniper'] is not None:
                windows['All Breakeven -- Sniper'].increment = float(increment3_temp.get())
                windows['All Breakeven -- Sniper'].mindays = float(mindays_temp.get())
                windows['All Breakeven -- Sniper'].maxdays = float(maxdays_temp.get())
                windows['All Breakeven -- Sniper'].minyears = float(minyears_temp.get())
                windows['All Breakeven -- Sniper'].maxyears = float(maxyears_temp.get())

            if windows['All Indifference -- Sniper'] is not None:
                windows['All Indifference -- Sniper'].increment = float(increment3_temp.get())
                windows['All Indifference -- Sniper'].mindays = float(mindays_temp.get())
                windows['All Indifference -- Sniper'].maxdays = float(maxdays_temp.get())
                windows['All Indifference -- Sniper'].minyears = float(minyears_temp.get())
                windows['All Indifference -- Sniper'].maxyears = float(maxyears_temp.get())
                
            increment1 = float(increment1_temp.get())
            increment2 = float(increment2_temp.get())
            increment3 = float(increment3_temp.get())
            increment4 = float(increment4_temp.get())
            
            mindays = float(mindays_temp.get())
            maxdays = float(maxdays_temp.get())
            minyears = float(minyears_temp.get())
            maxyears = float(maxyears_temp.get())
            
            window_exit()

        window = Toplevel(root)
        window.title("Increment Modification")
        window.geometry("310x165")
        
        global tabControl, tabIncrement, tabColor
        
        tabControl = ttk.Notebook(window)
        
        tabIncrement = ttk.Frame(tabControl)
        tabColor = ttk.Frame(tabControl)
        tabControl.grid(row=0, column=0, columnspan=2)
        
        tabControl.add(tabIncrement, text = 'Increment Settings')
        tabControl.add(tabColor, text = 'Range Settings')

        window.protocol("WM_DELETE_WINDOW", window_exit)

        windows['Increment'] = window
        
        balloon = Pmw.Balloon(window)
        lblballoon = balloon.component('label')
        lblballoon.config(background='white')
        
        increment1_label = ttk.Label(tabIncrement, text = "Raw Data Plot Generation Increment:")
        increment2_label = ttk.Label(tabIncrement, text = "Breakeven/Indifference Increment:")
        increment3_label = ttk.Label(tabIncrement, text = "All Breakeven/All Indifference Increment:")
        increment4_label = ttk.Label(tabIncrement, text = "Raw Data Entry Sliders Preview Increment:")

        increment1_entry = ttk.Entry(tabIncrement, width=10, textvariable = increment1_temp)
        increment2_entry = ttk.Entry(tabIncrement, width=10, textvariable = increment2_temp)
        increment3_entry = ttk.Entry(tabIncrement, width=10, textvariable = increment3_temp)
        increment4_entry = ttk.Entry(tabIncrement, width=10, textvariable = increment4_temp)

        increment1_entry.delete(0,END)
        increment1_entry.insert(0,increment1)
        increment2_entry.delete(0,END)
        increment2_entry.insert(0,increment2)
        increment3_entry.delete(0,END)
        increment3_entry.insert(0,increment3)
        increment4_entry.delete(0,END)
        increment4_entry.insert(0,increment4)

        mindays_label = ttk.Label(tabColor, text = "Colorbar Minimum Days:")
        maxdays_label = ttk.Label(tabColor, text = "Colorbar Maximum Days:")
        minyears_label = ttk.Label(tabColor, text = "Grayscale Minimum Years:")
        maxyears_label = ttk.Label(tabColor, text = "Grayscale Maximum Years:")

        mindays_entry = ttk.Entry(tabColor, width=10, textvariable = mindays_temp)
        maxdays_entry = ttk.Entry(tabColor, width=10, textvariable = maxdays_temp)
        minyears_entry = ttk.Entry(tabColor, width=10, textvariable = minyears_temp)
        maxyears_entry = ttk.Entry(tabColor, width=10, textvariable = maxyears_temp)

        mindays_entry.delete(0,END)
        mindays_entry.insert(0,round(mindays, 2))
        maxdays_entry.delete(0,END)
        maxdays_entry.insert(0,round(maxdays, 2))
        minyears_entry.delete(0,END)
        minyears_entry.insert(0,round(minyears, 2))
        maxyears_entry.delete(0,END)
        maxyears_entry.insert(0,round(maxyears, 2))

        
        save_button = ttk.Button(window, text = "Save", command=save)
        cancel_button = ttk.Button(window, text = "Cancel", command=window_exit)
        
        balloon.bind(increment1_label, "This setting configures the increment for the plots and CSV files generated by the Raw Data Entry and Raw Data Entry Sliders modes.\nIt must divide 100 evenly.")
        balloon.bind(increment2_label, "This setting configures the increment for the plots and CSV files generated by the Breakeven and Indifference modes.\nIt must divide 100 evenly.")
        balloon.bind(increment3_label, "This setting configures the increment for the PDF files generated by the All Breakeven and All Indifference modes.\nIt must divide 100 evenly.")
        balloon.bind(increment4_label, "This setting configures the increment for the preview located in the Raw Data Entry Sliders mode.\nIt must divide 100 evenly.")
        
        increment1_label.grid(column=0, row=0, sticky=(N, W, E, S), pady=(5,5), padx=(5,0))
        increment2_label.grid(column=0, row=1, sticky=(N, W, E, S), pady=(0,5), padx=(5,0))
        increment3_label.grid(column=0, row=2, sticky=(N, W, E, S), pady=(0,5), padx=(5,0))
        increment4_label.grid(column=0, row=3, sticky=(N, W, E, S), pady=(0,5), padx=(5,0))

        increment1_entry.grid(column=1, row=0, sticky=(N, W, E, S), pady=(5,5), padx=(0,5))
        increment2_entry.grid(column=1, row=1, sticky=(N, W, E, S), pady=(0,5), padx=(0,5))
        increment3_entry.grid(column=1, row=2, sticky=(N, W, E, S), pady=(0,5), padx=(0,5))
        increment4_entry.grid(column=1, row=3, sticky=(N, W, E, S), pady=(0,5), padx=(0,5))

        mindays_label.grid(column=0, row=0, sticky=(N, W, E, S), pady=(5,5), padx=(5,0))
        maxdays_label.grid(column=0, row=1, sticky=(N, W, E, S), pady=(0,5), padx=(5,0))
        minyears_label.grid(column=0, row=2, sticky=(N, W, E, S), pady=(0,5), padx=(5,0))
        maxyears_label.grid(column=0, row=3, sticky=(N, W, E, S), pady=(0,5), padx=(5,0))

        mindays_entry.grid(column=1, row=0, sticky=(N, W, E, S), pady=(5,5), padx=(0,5))
        maxdays_entry.grid(column=1, row=1, sticky=(N, W, E, S), pady=(0,5), padx=(0,5))
        minyears_entry.grid(column=1, row=2, sticky=(N, W, E, S), pady=(0,5), padx=(0,5))
        maxyears_entry.grid(column=1, row=3, sticky=(N, W, E, S), pady=(0,5), padx=(0,5))

        save_button.grid(column=0, row=4, sticky=(N, W, E, S), pady=(0,5), padx=(5,0))
        cancel_button.grid(column=1, row=4, sticky=(N, W, E, S), pady=(0,5), padx=(0,5))
    
    else:
        windows['Increment'].deiconify()
        windows['Increment'].lift()

def About():
    try:
        if sys.platform.startswith('linux'):
            subprocess.call(["xdg-open", "README.html"])
        elif sys.platform.startswith('win'):
            os.system('start README.html')
        elif sys.platform.startswith('darwin'):
            os.system('open README.html')
    except:
        messagebox.showinfo("Automatic opening of README.txt failed, please manually see the provided documentation.")


def plot(*args):
    if (str(pluginvar.get()) == "All Indifference -- Sniper" or str(pluginvar.get()) == "All Breakeven -- Sniper") and not config.nativePlotting:
        messagebox.showinfo("Feature is Disabled", "All Indifference and All Breakeven have been disabled on these computers, since matplotlib is not installed (and can't be installed) in Benedum 1223.");
        return
    entry_text =folder_path_in_actual.get()
    outy_text = folder_path_out_actual.get()
    settings_text = folder_path_settings_actual.get()
    if (str(pluginvar.get()) != "Raw Data Entry"  and str(pluginvar.get()) != "Raw Data Entry Sliders") and (not os.path.isdir(entry_text)):
        messagebox.showinfo("Warning: Illegal Argument", "Please specify a legal input path!")
        print('Please specify a legal input path!')
        return

    if (str(pluginvar.get()) == "All Indifference -- Sniper" or str(pluginvar.get()) == "All Breakeven -- Sniper") and (not os.path.isdir(outy_text)):
        messagebox.showinfo("Warning: Illegal Argument", "Please specify a legal output path!")
        print('Please specify a legal output path!')
        return

    global increment1, increment2, increment3, increment4

    if str(pluginvar.get()) == "Breakeven -- Sniper" or str(pluginvar.get()) == "Indifference -- Sniper":
        DB = flatfileDB(entry_text)
        if windows[str(pluginvar.get())] is None or not windows[str(pluginvar.get())].isOpen:
            windows[str(pluginvar.get())] = globals()[pluginvar.get().replace(" ", "_")].config(root, DB, outy_text+"/", increment2, mindays, maxdays, minyears, maxyears, gridMixSettingsFilename)
        else:
            windows[str(pluginvar.get())].window.deiconify()
            windows[str(pluginvar.get())].window.lift()

    elif str(pluginvar.get()) == "All Breakeven -- Sniper" or str(pluginvar.get()) == "All Indifference -- Sniper":
        DB = flatfileDB(entry_text)
        if windows[str(pluginvar.get())] is None or not windows[str(pluginvar.get())].isOpen:
            windows[str(pluginvar.get())] = globals()[pluginvar.get().replace(" ", "_")].config(root, DB, outy_text+"/", increment3, mindays, maxdays, minyears, maxyears, gridMixSettingsFilename)
        else:
            windows[str(pluginvar.get())].window.deiconify()
            windows[str(pluginvar.get())].window.lift()

    elif str(pluginvar.get()) == "Raw Data Entry":
        if windows[str(pluginvar.get())] is None or not windows[str(pluginvar.get())].isOpen:
            windows[str(pluginvar.get())] = globals()[pluginvar.get().replace(' ', '_')].config(root, None, outy_text+"/", increment1, mindays, maxdays, minyears, maxyears, gridMixSettingsFilename)
        else:
            windows[str(pluginvar.get())].window.deiconify()
            windows[str(pluginvar.get())].window.lift()
    elif str(pluginvar.get()) == "Raw Data Entry Sliders":
        if windows[str(pluginvar.get())] is None or not windows[str(pluginvar.get())].isOpen:
            windows[str(pluginvar.get())] = globals()[pluginvar.get().replace(' ', '_')].config(root, None, outy_text+"/", increment1, increment4, mindays, maxdays, minyears, maxyears, gridMixSettingsFilename)
        else:
            windows[str(pluginvar.get())].window.deiconify()
            windows[str(pluginvar.get())].window.lift()


# TEST_DIR = '/Users/nbp3/SPEC_SINGLE_RUNS'


def mcpat_dict_loader(file_path):
    item = {}
    with open(file_path, 'r') as f:
        string_dict = f.read()
        item = ast.literal_eval(string_dict[8:])
    return item


root = Tk()
balloon = Pmw.Balloon(root)
lblballoon = balloon.component('label')
lblballoon.config(background='white')
root.title("GreenChip Visualization")
#root.iconbitmap('Assets/greenchipicon.ico')

mainframe = ttk.Frame(root, padding="3 3 12 12", width=10000, height=10000)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

if not os.path.isfile("defaultFolders.txt"):
    f = open("defaultFolders.txt", "w+")
    f.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nCONTAINS DEFAULTS FOR FOLDERS. DO NOT TOUCH.")
    f.close()

#if platform == "darwin":
#    logo = ttk.Label(mainframe)
#    logo_image = ImageTk.PhotoImage(file='Assets/GreenChipLogo.png')
#    logo['image'] = logo_image
#    logo.grid(columnspan=2, row=0, sticky=(N, W, E, S))

#inpath = ttk.Label(mainframe, text='Directory of the simulation results:')
#inpath.grid(column=0, row=1, sticky=(N, W, E, S))

#inpathtext = ttk.Entry(mainframe, width=50)
#inpathtext.grid(column=1, row=1, sticky=(N, W, E, S))

#outpathtext = ttk.Entry(mainframe, width=50)
#outpathtext.grid(column=1, row=2, sticky=(N, W, E, S))

pluginvar = StringVar()

folder_path_out = StringVar()
folder_path_out_actual = StringVar()
folder_path_in = StringVar()
folder_path_in_actual = StringVar()
folder_path_in2 = StringVar()
folder_path_in2_actual = StringVar()
folder_path_settings = StringVar()
folder_path_settings_actual = StringVar()
folder_path_sliders = StringVar()
gridMix_file_path = StringVar(mainframe, path_shortener(gridMixSettingsFilename))

increment1 = 0.2
increment2 = 0.2
increment3 = 0.5
increment4 = 0.5

mindays = 0
maxdays = 3650
minyears = 4000/365
maxyears = 36000/365

#INPUT

inpath = ttk.Label(mainframe, text='Input Directory:')
lbl1 = Label(mainframe, textvariable=folder_path_in)
balloon.bind(inpath, "Top level directory used to find all desired sniper output directories.\n For All Breakeven/All Indifference, refer to the file format specified in the Import format of the readme.")

button2 = Button(mainframe, text="Browse", command=browse_button_input)

#OUTPUT
outpath = ttk.Label(mainframe, text='Output Directory:')
lbl2 = Label(mainframe, textvariable=folder_path_out)
balloon.bind(outpath, "Directory that all comparison pdf and csv files will be placed.\n Refer to the Getting Charts section of the readme for more information.")
button3 = Button(mainframe, text="Browse", command=browse_button_output)


# Configuration files

settingspath = ttk.Label(mainframe, text='Marker Configuration File (Optional):')
settingspath.grid(column=0, row=7, sticky=(N, W, E, S))
settingslbl1 = Label(mainframe, textvariable=folder_path_settings, anchor = 'w')
balloon.bind(settingspath, "File used to add markers to any plot automatically. Refer to Markers section of the readme for more information.")
settingslbl1.grid(row=7, column=1)
settingsbutton = Button(mainframe, text="Browse", command=browse_button_settings)
settingsbutton.grid(row=7, column=2)

sliderspath = ttk.Label(mainframe, text='Slider Configuration File (Optional):')
sliderslbl1 = Label(mainframe, textvariable=folder_path_sliders)
balloon.bind(sliderspath, "File used to adjust the minumum value, maximum value, and resolution of the sliders. \n Refer to Sliders section of the readme for more information.")
slidersbutton = Button(mainframe, text="Browse", command=browse_button_sliders)


# Patches
powerlabel = ttk.Label(mainframe, text='Specify DRAM and Carbon Emission information for simulator output (Required at least once):')
balloon.bind(powerlabel, "Creates a Greenchip.txt containing DRAM and carbon specifications given by the user in all subdirectories containing simulator outputs.\n Refer to Power Patcher section of the readme for more information.")
button5 = Button(mainframe, text="Specify", command=lambda:utils.powerPrompter(gridMixSettingsFilename))

powerlabel2 = ttk.Label(mainframe, text='Specify DRAM and Carbon Emission information for simulator output (Optional):')
balloon.bind(powerlabel2, 'Creates a Greenchip.txt containing DRAM and carbon specifications given by the user in all subdirectories containing simulator outputs.\n Refer to the "Power Patcher" and the "Getting Charts" c) and d) sections of the readme for more\n information on the patcher and its effects.')
button6 = Button(mainframe, text="Specify", command=lambda:utils.powerPrompter(gridMixSettingsFilename))

#Global Increment
increment = ttk.Label(mainframe, text='Plot Settings:')
balloon.bind(increment, 'This allows the user to adjust the scale at which the breakeven and indifference plots do their calculations at. Lower values take longer, but provide better-looking graphs.\nThe default is 0.2 for all plots except the previews in Raw Data Entry Sliders and the outputs for All Indifference/All Breakeven, for which it is 0.5. They must divide 100 evenly.')
increment.grid(column=0, row=15, sticky=(N, W, E, S))
button7 = Button(mainframe, text="Modify", command=settingsSetter)
button7.grid(column=2, row=15)


# Plot Carbon Emission by Location
carbonplot = ttk.Label(mainframe, text='Grid Mix Settings File (Optional):')
carbonplot.grid(column=0, row=20, sticky=(N, W, E, S))
csvPathLbl = Label(mainframe,textvariable=gridMix_file_path, anchor = 'w')
csvPathLbl.grid(row=20, column=1)
balloon.bind(csvPathLbl, gridMixSettingsFilename)
button8 = Button(mainframe, text="Browse", command=browse_filename)
button8.grid(row=20, column=2)
balloon.bind(carbonplot, "Choose a grid mix settings file to use instead of the default file EnergyGridMix.csv.")


def changeOptions(event):
    option=event.widget.get()
    
    inpath.grid_remove()
    lbl1.grid_remove()
    button2.grid_remove()
    outpath.grid_remove()
    lbl2.grid_remove()
    button3.grid_remove()
    sliderspath.grid_remove()
    sliderslbl1.grid_remove()
    slidersbutton.grid_remove()
    powerlabel.grid_remove()
    button5.grid_remove()
    powerlabel2.grid_remove()
    button6.grid_remove()
            
    if option == "Raw Data Entry Sliders":
        sliderspath.grid(column=0, row=8, sticky=(N, W, E, S))
        sliderslbl1.grid(row=8, column=1)
        slidersbutton.grid(row=8, column=2)
    if option == "Breakeven -- Sniper" or option == "Indifference -- Sniper":
        inpath.grid(column=0, row=3, sticky=(N, W, E, S))
        lbl1.grid(row=3, column=1)
        button2.grid(row=3, column=2)
        powerlabel2.grid(row=8, column=0, sticky=(N, W, E, S))
        button6.grid(row=8, column=2)

    if option == "All Breakeven -- Sniper" or option == "All Indifference -- Sniper":
        inpath.grid(column=0, row=3, sticky=(N, W, E, S))
        lbl1.grid(row=3, column=1)
        button2.grid(row=3, column=2)
        outpath.grid(column=0, row=6, sticky=(N, W, E, S))
        lbl2.grid(row=6, column=1)
        button3.grid(row=6, column=2)
        powerlabel.grid(row=9, column=0)
        button5.grid(row=9, column=2)
    if option == 'Raw Data Entry': 
        balloon.bind(plugin_box, "Raw Data Entry allows the user to plot breakeven and indifference times using data entered via textboxes, eliminating the need for output files from a detailed simulator.\n Refer to the Getting Charts section of the readme for more information.")
    if option == 'Raw Data Entry Sliders': 
        balloon.bind(plugin_box, "Raw Data Entry Sliders allows the user to plot breakeven and indifference times using data entered via sliders, eliminating the need for output files from a detailed simulator.\n Refer to the Getting Charts section of the readme for more information.")
    if option == 'Breakeven -- Sniper': 
        balloon.bind(plugin_box, "Plots the breakeven time between data from two sniper output directories located in subdirectories of the input folder.\n Refer to the Getting Charts section of the readme for more information.")
    if option == 'Indifference -- Sniper': 
        balloon.bind(plugin_box, "Plots the indifference time between data from two sniper output directories located in subdirectories of the input folder.\n Refer to the Getting Charts section of the readme for more information.")
    if option == 'All Breakeven -- Sniper': 
        balloon.bind(plugin_box, "Plots the breakeven time for all valid combinations of sniper output directories located in subdirectories following a specific format.\n Refer to the Getting Charts section of the readme for more information.")
    if option == 'All Indifference -- Sniper': 
        balloon.bind(plugin_box, "Plots the indifference time for all valid combinations of sniper output directories located in subdirectories following a specific format.\n Refer to the Getting Charts section of the readme for more information.")

#Decision
plugin_box = ttk.Combobox(mainframe, textvariable=pluginvar, values=plugins, state='readonly')
balloon.bind(plugin_box, "Raw Data entry allows the user to input data of their choosing, eliminating the need for sniper outputs.\n Refer to the Getting Charts section of the readme for more information.")
plugin_box.current(0)
plugin_box.grid(column=0, row=0, sticky=(N, W, E, S))
plugin_box.bind("<<ComboboxSelected>>", changeOptions)
ttk.Button(mainframe, text="Choose Analysis Mode", command=plot).grid(column=2, row=0, sticky=(N, W, E, S))



menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
#filemenu.add_command(label="New", command=NewFile)
#filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

inpath.grid_remove()
lbl1.grid_remove()
button2.grid_remove()
outpath.grid_remove()
lbl2.grid_remove()
button3.grid_remove()
sliderspath.grid_remove()
sliderslbl1.grid_remove()
slidersbutton.grid_remove()
powerlabel.grid_remove()
button5.grid_remove()
powerlabel2.grid_remove()
button6.grid_remove()

root.bind('<Return>', plot)
root.mainloop()
