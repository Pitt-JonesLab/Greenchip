# GreenChip Simulation Visualization (SimVis) Tool

Version 0.1.1 -- 7/22/22


#### Contents:

1) [Installing the simulator](#installing-the-simulator)
    * [Ubuntu/Debian-based Distros Installation](#ubuntudebian-based-distros-installation)
    * [Windows Installation](#windows-installation)
2) [Running the simulator](#running-the-simulator)
    * [Starting](#starting)
        * [Getting Charts](#getting-charts)
        * [Input Format (modes e,f)](#input-format-modes-ef)
    * [Specifier](#specifier)
    * [Importance](#importance)
    * [CSV Output](#csv-output)
3) [Plot Settings](#plot-settings)
4) [Markers File](#markers-file)
5) [Sliders File](#sliders-file)
6) [Publications to cite](#publications)
7) [Authors and Thanks](#authors-and-thanks)


## Installing the Simulator



### Ubuntu/Debian-based Distros Installation

Step 1: First, make sure you have python 3 installed on your machine (Ubuntu 22.04 should have it by default). Next, install python 3's package manager, called pip, which will be used to install other python 3 packages, by using the following command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo apt-get install -y python3-pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 2: Next, install git by using the following command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo apt-get install -y git
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 3: Navigate to your desired directory for Greenchip, and run the following command to download it:

~~~~~~~~~~~~~
git clone https://github.com/Pitt-Jones-Lab/Greenchip.git
~~~~~~~~~~~~~

Step 4: Run "cd Greenchip" to navigate to the downloaded tool's directory, and then run the following command to install some of the needed python 3 packages:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pip3 install -r requirements.txt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 5: Run the following command to install the last necessary python 3 packages.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sudo apt-get install -y python3-tk idle3 python3-pil python3-pil.imagetk
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

### Windows Installation

Step 1: Install python 3 and pip, if you don't have them already. There are many resources available online detailing how to do this.

Step 2: Follow the instructions for windows installation for git from this link:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 3: Navigate to your desired directory for Greenchip, and run the following command to download it:

~~~~~~~~~~~~~
git clone https://github.com/Pitt-Jones-Lab/Greenchip.git
~~~~~~~~~~~~~

Step 4: Run "cd Greenchip" to navigate to the downloaded tool's directory, and then run the following command to install the needed python 3 packages:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pip3 install -r windows-requirements.txt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[Back to Contents](#contents)

## Running the Simulator

### Starting

~~~~~~~~~~~~~~~~~
python3 SimVis.py
~~~~~~~~~~~~~~~~~

#### Getting Charts:

GreenChip SimVis currently has 6 different analysis modes, and an informational plot:

a) Raw Data Entry

This mode allows the user to input the raw data directly into the gui. This avoids requiring the use of a detailed simulator. This mode possess the ability to generate energy and carbon plots.

b) Raw Data Entry Sliders

Similar to Raw Data Entry, except it uses sliders, and it also possesses the ability to push data from single sniper output runs to the sliders, and can generate energy and carbon plots.


c) Indifference

This mode takes an input folder structure, and finds all instances of McPAT and Sniper output in subdirectories, and allows the user to
generate specific indifference comparisons they want to see. It will prompt the user for the DRAM specifications.

d) Breakeven

This mode takes an input folder structure, and finds all instances of McPAT and Sniper output in subdirectories, and allows the user to
generate specific breakeven comparisons they want to see. It will prompt the user for the DRAM specifications.

e) All Indifference

This mode takes a specific input folder structure defined at the bottom of this section, and outputs all valid
indifference comparisons between all data within that folder structure. Runs immediately after hitting "chose analysis
mode".

f) All Breakeven

This mode takes a specific input folder structure defined at the bottom of this section, and outputs all valid
breakeven comparisons between all data within that folder structure. Runs immediately after hitting "chose analysis
mode".

g) Carbon Emissions Plot

This plot shows the grams CO2 equivalent per kilowatt hour to operate/manufacture a system in each state.

#### Input Format (modes e,f)

Currently, All_Indifference, All_Breakeven expect a specific format.

Folder Levels 1 through (N-1): Various Parameters/labels (can be anything)
Folder Level N: Requires Sniper output files, and DramSim2 output files are preferred for greater accuracy for DRAM power values: sim.out, power.xml, power.py, run_out.txt (*)

An example:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Folder level 1- Number of Cores:      4cores       8cores

Folder level 2- Technology Node:      28      45      90

Folder level 3-  Cache size:          1mb   512kb   4mb

Folder level 4- benchmark name:       blackscholes    canneal    x264

Folder level 5- power.py   power.xml  sim.cfg   sim.out    sim.stats.sqlite3   run_out.txt (*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(*) Dram2Sim output, but if it is not found, Greenchip will use the power.py energy specifications for the DRAM power.

### Specifier

As it currently stands, there exists no information about the DRAM technology node or manufacturing and use locations in any of the above files, and while there is a spot for information on the DRAM chip area, it is usually 0. This option allows the user to select a directory, a desired chip area, a desired technology node, and desired locations for manufacturing and usage. A Greenchip.txt file containing this is created and put into each subdirectory containing a power.py (simulator output).

### Importance

Both Raw Data Entry and Raw Data Entry Slider are able to use importance, which involves perturbing certain System 2 configuration parameters by 1%, and seeing how the breakeven time at a specified sleep and activito ratio reacts. From there it normalizes all of the changes such that they add up to 100, and reports the values back to the user. This lets the user know which values that would be the best for tweaking. There are three methods for selecting sleep percentages and activity ratios to calculate over:

a) Single Point Analysis: This prompts the user for a sleep percentage and an activity ratio, and does all calculations at that point.

b) Average Analysis: This prompts the user for a sleep percentage, an activity ratio, and a radius, and averages all of the pertubations for all of the points within the circle.

c) All Point Analysis: This averages over all of the pertubations for all combinations of sleep percentage and activity ratio.

### CSV Output

Both Raw Data Entry and Raw Data Entry Slider modes can generate CSV output, where every value in the plot (either breakeven or indifference) will be outputted, along with its corresponding sleep percentage and activity ratio, to a CSV file in a directory and filename selected by the user.

[Back to Contents](#contents)

## Plot Settings

The plot settings option contains various settings for customizing the plots generated by the tool. Currently, there are two sections, a Range section for setting the minimum and maximum days and years for the colorbars and an Increment section that allows the user to customize the plot resolution for each of the modes. 

*Note: Increasing the resolution can have a noticable effect on the time it takes to generate a plot.*

[Back to Contents](#contents)

## Markers File

The marker script operates on a line-by-line basis. Each lie is read as a marker command (unless it starts with #, in which case it is assumed to be a comment and thus ignored), and should be structured in the following way

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MarkerSpecifier Sleep Activity Radius Label Color

MarkerSpecifier - This should be either "M" or "WM" (not case sensitive.) "M" specifies a regular marker, and "WM" specifies a wide marker.

Sleep - This should be a number that specifies the marker's sleep ratio (should be between 0 and 100)

Activity - This should be a number that specifies the marker's activity ratio (should be between 0 and 100)

Radius - This is a number tat is only used in the "WM" mode to specify the marker's radius. If you are in the "M" mode, don't put anything here (don't put an extra space either)

Label - This specifies the marker's label

Color(optional) - This specifies the marker's color (not case sensitive). It ports the string directly to matplotlib, so check matplotlib's color list to see which one you want to use. If nothing is specified here, then the label will be black with a white bounding box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some examples are given below:

~~~~~~~~~~~~~~~~~~
M 20 40 Phone2 red
~~~~~~~~~~~~~~~~~~

This creates a marker with sleep ratio of 20, activity ratio of 40, and a red label of Phone2.

~~~~~~~~~~~~~~~~~~~
WM 30 60 15 Tablet
~~~~~~~~~~~~~~~~~~~

This creates a wide marker with sleep ratio of 30, activity ratio of 60, a radius of 15, and a label of Tablet. It uses the default label color scheme of black with a white bounding box

~~~~~~~~~~~~~~
M 30 10 Laptop
~~~~~~~~~~~~~~
This creates a marker with sleep ratio of 30, activity ratio of 10, and a label of Laptop. It again uses the default label color scheme.

[Back to Contents](#contents)

## Sliders File

Each of the sliders that are used in Raw_Data_Entry_Sliders are customizable through a text file that is read line by line. Each slider is adjusted using the following line:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SliderName min max resolution

min - Value at the far left of the slider. Sliders start at this value

max - Value at the far right of the slider.

resolution - The minimum amount the slider can increment. Clicking the slider bar moves it by this amount.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

min, max, and resolution can all be specified as decimals
    
A list of SliderNames is provided below:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CHIPAREA1, CHIPAREA2, DYNAMICPOWER1, DYNAMICPOWER2, STATICPOWER1, STATICPOWER2, DYNAMICMEMORYPOWER1, DYNAMICMEMORYPOWER2, STATICMEMORYPOWER1, STATICMEMORYPOWER2, DRAMCHIPAREA1, DRAMCHIPAREA2, IPC1, IPC2, FREQUENCY1, FREQUENCY2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The names are NOT case sensitive

Each new slider requires a new line and a new command call

Any sliders not specified default the following values:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CHIPAREA1, CHIPAREA2: min: 0, max: 5000, resolution: 0.01

DYNAMICPOWER1, DYNAMICPOWER2: min: 0, max: 200, resolution: 0.01

STATICPOWER1, STATICPOWER2: min: 0, max: 100, resolution: 0.01

DYNAMICMEMORYPOWER1, DYNAMICMEMORYPOWER2: min: 0, max: 30, resolution: 0.01

STATICMEMORYPOWER1, STATICMEMORYPOWER2: min: 0, max: 30, resolution: 0.01

IPC1, IPC2: min: 0, max: 1000, resolution: 0.01

FREQUENCY1, FREQUENCY: min: 0, max: 5, resolution: 0.01
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some examples are given below:

~~~~~~~~~~~~~~~~~~
CHIPAREA1 5 1000 1
~~~~~~~~~~~~~~~~~~

The slider ChipArea1 has a minimum value of 5, max of 1000, and the slider increments by 1

~~~~~~~~~~~~~~~~~~~~~~~~~
DYNAMICPOWER2 200 700 0.1
~~~~~~~~~~~~~~~~~~~~~~~~~

The slider DynamicPower2 has a minimum value of 200, max of 700, and the slider increments by 0.1

[Back to Contents](#contents)

## Publications

If you publish work using GreenChip, please cite:

Donald Kline, Jr., Nikolas Parshook, Xiaoyu Ge, Erik Brunvand, Rami Melhem, Panos K. Chrysanthis, Alex K. Jones,
GreenChip: A Tool for Evaluating Holistic Sustainability of Modern Computing Systems,
In Sustainable Computing: Informatics and Systems, 2017.

http://www.sciencedirect.com/science/article/pii/S2210537917300823


This is an extension to our previous work, in IGSC 2016:

Donald Kline, Jr., Nikolas Parshook, Xiaoyu Ge, Erik Brunvand, Rami Melhem, Panos K. Chrysanthis, Alex K. Jones,
Holistically evaluating the environmental impacts in modern computing systems,
In International Green and Sustainable Computing Conference, 2016.

http://ieeexplore.ieee.org/abstract/document/7892605/

[Back to Contents](#contents)

## Authors and Thanks

Primary Authors, version 0.1:
    Nikolas Parshook

Primary Authors, versions 0.2-0.5:
    Donald Kline, Jr, Nikolas Parshook

Primary Authors, versions 0.6-0.9:
    Donald Kline, Jr
    
Primary Authors, version 0.1.0-Current:
    Ryan Caginalp, Sebastien Ollivier, Stephen Cahoon, Chayanika Choudhuri


Guidance:
    Dr. Alex K. Jones (University of Pittsburgh)
    Dr. Panos Chrysanthis (University of Pittsburgh)

Thanks:
    Eric Cheung, for his work on the indifference plots

[Back to Contents](#contents)
