import ast
import sys
import os
import subprocess
from sys import platform
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import plugins.shared.Config as config


try:
    import matplotlib
    matplotlib.use("TkAgg")
    config.nativePlotting = True
except ImportError:
    config.nativePlotting = False

from Database import flatfileDB
from PluginHandler import import_plugins
from plugins.shared.Utils import OurConstants

plugins_dirs = "plugins"
sys.path.extend(plugins_dirs.split(os.pathsep))
plugins = import_plugins(plugins_dirs, globals())


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

def browse_button_output():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path_out
    filename2 = filedialog.askdirectory()
    folder_path_out.set(filename2)


def About():
    try:
        if sys.platform.startswith('linux'):
            subprocess.call(["xdg-open", "README.txt"])
        elif sys.platform.startswith('win'):
            os.system('start README.txt')
        elif sys.platform.startswith('darwin'):
            os.system('open README.txt')
    except:
        messagebox.showinfo("Automatic opening of README.txt failed, please manually see the provided documentation.")


def plot(*args):
    if (str(pluginvar.get()) == "All_Indifference" or str(pluginvar.get()) == "All_Breakeven") and not config.nativePlotting:
        messagebox.showinfo("Feature is Disabled", "All_Indifference and All_Breakeven have been disabled on these computers, since matplotlib is not installed (and can't be installed) in Benedum 1223.");
        return
    sniper_text1 = " "
    sniper_text2 = " "
    entry_text =folder_path_in.get()
    outy_text = folder_path_out.get()
    sniper_text1 = sfolder_path_in1.get()
    sniper_text2 = sfolder_path_in2.get()
    settings_text = folder_path_settings.get()
    if (str(pluginvar.get()) != "Raw_Data_Entry"  and str(pluginvar.get()) != "Raw_Data_Entry_Sliders") and (not os.path.isdir(entry_text)):
        messagebox.showinfo("Warning: Illegal Argument", "Please specify a legal input path!")
        print('Please specify a legal input path!')
        return

    if str(pluginvar.get()) == "All_Indifference" or str(pluginvar.get()) == "All_Breakeven" and not os.path.isdir(outy_text):
        messagebox.showinfo("Warning: Illegal Argument", "Please specify a legal output path!")
        print('Please specify a legal output path!')
        return


    
    if str(pluginvar.get()) != "Raw_Data_Entry" and str(pluginvar.get()) != "Raw_Data_Entry_Sliders":
        DB = flatfileDB(entry_text)
        plugin = globals()[pluginvar.get()].config(root, DB, outy_text+"/")
    elif str(pluginvar.get()) == "Raw_Data_Entry_Sliders":
        plugin = globals()[pluginvar.get()].config(root, None, outy_text+"/",sniper_text1,sniper_text2)
    else:
        plugin = globals()[pluginvar.get()].config(root, None, outy_text+"/")


# TEST_DIR = '/Users/nbp3/SPEC_SINGLE_RUNS'


def mcpat_dict_loader(file_path):
    item = {}
    with open(file_path, 'r') as f:
        string_dict = f.read()
        item = ast.literal_eval(string_dict[8:])
    return item


root = Tk()
root.title("GreenChip Visualization")

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
sfolder_path_in1 = StringVar()
sfolder_path_in2 = StringVar()
folder_path_settings = StringVar()


#Settings

settingspath = ttk.Label(mainframe, text='Advanced Settings File (Optional):')
settingspath.grid(column=0, row=1, sticky=(N, W, E, S))

settingslbl1 = Label(mainframe, textvariable=folder_path_settings)
settingslbl1.grid(row=1, column=1)
settingsbutton = Button(mainframe, text="Browse", command=browse_button_settings)
settingsbutton.grid(row=1, column=2)


#INPUT

inpath = ttk.Label(mainframe, text='Input Directory (For non-raw input):')
inpath.grid(column=0, row=2, sticky=(N, W, E, S))

lbl1 = Label(mainframe, textvariable=folder_path_in)
lbl1.grid(row=2, column=1)
button2 = Button(mainframe, text="Browse", command=browse_button_input)
button2.grid(row=2, column=2)

sinpath1 = ttk.Label(mainframe, text='Configuration 1 Sniper Input Directory:')
sinpath1.grid(column=0, row=3, sticky=(N, W, E, S))

slbl1 = Label(mainframe, textvariable=folder_path_in)
slbl1.grid(row=3, column=1)
sbutton1 = Button(mainframe, text="Browse", command=browse_sniper_input1)
sbutton1.grid(row=3, column=2)

sinpath2 = ttk.Label(mainframe, text='Configuration 2 Sniper Input Directory:')
sinpath2.grid(column=0, row=4, sticky=(N, W, E, S))

slbl2 = Label(mainframe, textvariable=folder_path_in)
slbl2.grid(row=4, column=1)
sbutton2 = Button(mainframe, text="Browse", command=browse_sniper_input2)
sbutton2.grid(row=4, column=2)


#OUTPUT
outpath = ttk.Label(mainframe, text='Output Directory (For All Breakeven/All Indifference):')
outpath.grid(column=0, row=5, sticky=(N, W, E, S))
lbl2 = Label(mainframe, textvariable=folder_path_out)
lbl2.grid(row=5, column=1)
button3 = Button(mainframe, text="Browse", command=browse_button_output)
button3.grid(row=5, column=2)

#Decision
plugin_box = ttk.Combobox(mainframe, textvariable=pluginvar, values=plugins, state='readonly')
plugin_box.current(0)
plugin_box.grid(column=0, row=6, sticky=(N, W, E, S))
ttk.Button(mainframe, text="Choose Analysis Mode", command=plot).grid(column=1, row=6, sticky=(N, W, E, S))


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

root.bind('<Return>', plot)
root.mainloop()


