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

plugins_dirs = "plugins"
sys.path.extend(plugins_dirs.split(os.pathsep))
import_plugins(plugins_dirs, globals())
plugins = ['Raw Data Entry', 'Raw Data Entry Sliders', 'Breakeven -- Sniper', 'Indifference -- Sniper', 'All Breakeven -- Sniper', 'All Indifference -- Sniper']

def browse_button_input():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path_in
    filename1 = filedialog.askdirectory()
    folder_path_in.set(filename1)
    #print(filename)

def browse_sniper_input1():
    # Allow user to select a directory and store it in global var
    # called sfolder_path1
    global sfolder_path_in1
    filename1 = filedialog.askdirectory()
    sfolder_path_in1.set(filename1)

def browse_sniper_input2():
    # Allow user to select a directory and store it in global var
    # called sfolder_path2
    global sfolder_path_in2
    filename2 = filedialog.askdirectory()
    sfolder_path_in2.set(filename2)

def browse_button_settings():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path_in
    filename_settings = filedialog.askopenfile()
    if (filename_settings is None):
        folder_path_settings.set("")
    else:
        folder_path_settings.set(filename_settings.name)

    if (len(folder_path_settings.get()) > 2):
        config.advancedSettingsFile = folder_path_settings.get()
    else:
        config.advancedSettingsFile = None

def browse_button_sliders():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path_in2
    filename_sliders = filedialog.askopenfile()
    if (filename_sliders is None):
        folder_path_sliders.set("")
    else:
        folder_path_sliders.set(filename_sliders.name)

    if (len(folder_path_sliders.get()) > 2):
        config.slidersFile = folder_path_sliders.get()
    else:
        config.slidersFile = None

def browse_button_output():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path_out
    filename2 = filedialog.askdirectory()
    folder_path_out.set(filename2)

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
    plt.bar(locations,carbonValues)
    plt.xlabel('Locations')
    plt.ylabel('Carbon Emission in gCo2eq/kWh')
    plt.title('Carbon Emissions by location')
    plt.show()

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
    sniper_text1 = " "
    sniper_text2 = " "
    entry_text =folder_path_in.get()
    outy_text = folder_path_out.get()
    sniper_text1 = sfolder_path_in1.get()
    sniper_text2 = sfolder_path_in2.get()
    settings_text = folder_path_settings.get()
    if (str(pluginvar.get()) != "Raw Data Entry"  and str(pluginvar.get()) != "Raw Data Entry Sliders") and (not os.path.isdir(entry_text)):
        messagebox.showinfo("Warning: Illegal Argument", "Please specify a legal input path!")
        print('Please specify a legal input path!')
        return

    if (str(pluginvar.get()) == "All Indifference -- Sniper" or str(pluginvar.get()) == "All Breakeven -- Sniper") and (not os.path.isdir(outy_text)):
        messagebox.showinfo("Warning: Illegal Argument", "Please specify a legal output path!")
        print('Please specify a legal output path!')
        return


    
    if str(pluginvar.get()) != "Raw Data Entry" and str(pluginvar.get()) != "Raw Data Entry Sliders":
        DB = flatfileDB(entry_text)
        plugin = globals()[pluginvar.get().replace(" ", "_")].config(root, DB, outy_text+"/")
    elif str(pluginvar.get()) == "Raw Data Entry Sliders":
        plugin = globals()[pluginvar.get().replace(' ', '_')].config(root, None, outy_text+"/",sniper_text1,sniper_text2)
    else:
        plugin = globals()[pluginvar.get().replace(' ', '_')].config(root, None, outy_text+"/")


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
folder_path_in = StringVar()
folder_path_in2 = StringVar()
sfolder_path_in1 = StringVar()
sfolder_path_in2 = StringVar()
folder_path_settings = StringVar()
folder_path_sliders = StringVar()



#INPUT

inpath = ttk.Label(mainframe, text='Input Directory:')
lbl1 = Label(mainframe, textvariable=folder_path_in)
balloon.bind(inpath, "Top level directory used to find all desired sniper output directories.\n For All Breakeven/All Indifference, refer to the file format specified in the Import format of the readme.")

button2 = Button(mainframe, text="Browse", command=browse_button_input)

sinpath1 = ttk.Label(mainframe, text='System 1 Sniper Input Directory (Optional):')

slbl1 = Label(mainframe, textvariable=sfolder_path_in1)
balloon.bind(sinpath1, "Sniper output directory whose data the user would want to set the sliders values to automatically.\n Refer to the Sliders section of the readme for more information.")
sbutton1 = Button(mainframe, text="Browse", command=browse_sniper_input1)

sinpath2 = ttk.Label(mainframe, text='System 2 Sniper Input Directory (Optional):')
balloon.bind(sinpath2, "Sniper output directory whose data the user would want to set the sliders values to automatically.\n Refer to the Sliders section of the readme for more information.")

slbl2 = Label(mainframe, textvariable=sfolder_path_in2)
sbutton2 = Button(mainframe, text="Browse", command=browse_sniper_input2)

#OUTPUT
outpath = ttk.Label(mainframe, text='Output Directory:')
lbl2 = Label(mainframe, textvariable=folder_path_out)
balloon.bind(lbl1, "Directory that all comparison pdf and csv files will be placed.\n Refer to the Getting Charts section of the readme for more information.")
button3 = Button(mainframe, text="Browse", command=browse_button_output)


# Configuration files

settingspath = ttk.Label(mainframe, text='Marker Configuration File (Optional):')
settingspath.grid(column=0, row=7, sticky=(N, W, E, S))
settingslbl1 = Label(mainframe, textvariable=folder_path_settings)
balloon.bind(settingspath, "File used to add markers to any plot automatically. Refer to Markers section of the readme for more information.")
#balloon.bind(settingspath, "File used to add markers to any plot automatically. Refer to Markers section of the readme for more information.")
settingslbl1.grid(row=7, column=1)
settingsbutton = Button(mainframe, text="Browse", command=browse_button_settings)
settingsbutton.grid(row=7, column=2)

sliderspath = ttk.Label(mainframe, text='Slider Configuration File (Optional):')
sliderslbl1 = Label(mainframe, textvariable=folder_path_sliders)
balloon.bind(sliderspath, "File used to adjust the minumum value, maximum value, and resolution of the sliders. \n Refer to Sliders section of the readme for more information.")
slidersbutton = Button(mainframe, text="Browse", command=browse_button_sliders)

# Patches
powerlabel = ttk.Label(mainframe, text='Patch power.py with DRAM information (Required at least once):')
balloon.bind(powerlabel, "Patches every power.py in all subdirectories by adding DRAM specifications given by the user.\n Refer to Power Patcher section of the readme for more information.")
button5 = Button(mainframe, text="Patch", command=utils.powerPrompter)

# Plot Carbon Emission by Location
carbonplot = ttk.Label(mainframe, text='Plot Carbon Emission Data by Location (Auxiliary Information):')
carbonplot.grid(column=0, row=10, sticky=(N, W, E, S))
plotlbl = Label(mainframe, text='')
plotlbl.grid(row=10, column=1)
button4 = Button(mainframe, text="Plot", command=plot_carbon)
button4.grid(row=10, column=2)


def changeOptions(event):
    option=event.widget.get()
    
    inpath.grid_remove()
    lbl1.grid_remove()
    button2.grid_remove()
    outpath.grid_remove()
    lbl2.grid_remove()
    button3.grid_remove()
    sinpath1.grid_remove()
    slbl1.grid_remove()
    sbutton1.grid_remove()
    sinpath2.grid_remove()
    slbl2.grid_remove()
    sbutton2.grid_remove()
    sliderspath.grid_remove()
    sliderslbl1.grid_remove()
    slidersbutton.grid_remove()
    powerlabel.grid_remove()
    button5.grid_remove()
    
    if option == "Raw Data Entry Sliders":
        sinpath1.grid(column=0, row=4, sticky=(N, W, E, S))
        slbl1.grid(row=4, column=1)
        sbutton1.grid(row=4, column=2)
        sinpath2.grid(column=0, row=5, sticky=(N, W, E, S))
        slbl2.grid(row=5, column=1)
        sbutton2.grid(row=5, column=2)
        sliderspath.grid(column=0, row=8, sticky=(N, W, E, S))
        sliderslbl1.grid(row=8, column=1)
        slidersbutton.grid(row=8, column=2)
    if option == "Breakeven -- Sniper" or option == "Indifference -- Sniper":
        inpath.grid(column=0, row=3, sticky=(N, W, E, S))
        lbl1.grid(row=3, column=1)
        button2.grid(row=3, column=2)

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
        balloon.bind(plugin_box, "Plots the indiffernce time for all valid combinations of sniper output directories located in subdirectories following a specific format.\n Refer to the Getting Charts section of the readme for more information.")

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
sinpath1.grid_remove()
slbl1.grid_remove()
sbutton1.grid_remove()
sinpath2.grid_remove()
slbl2.grid_remove()
sbutton2.grid_remove()
sliderspath.grid_remove()
sliderslbl1.grid_remove()
slidersbutton.grid_remove()
powerlabel.grid_remove()
button5.grid_remove()

root.bind('<Return>', plot)
root.mainloop()
