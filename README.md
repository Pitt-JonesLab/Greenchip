###################################################
GreenChip Simulation Visualization (SimVis) Tool

Version 0.1.0 -- May 16, 2022

###################################################


Contents:

1) Installing the simulator
2) Running the simulator
3) Settings File
4) Publications to cite
5) Authors and Thanks


---------------------------------------------------
----       Installing the Simulator          ------
---------------------------------------------------

GreenChip SimVis uses python3, and has two modes of operation, chosen automatically
based on your system

    1) Default/Matplotlib Mode- uses the python3 add-on modules:
        a) matplotlib (for plotting the indifference charts)
        b) numpy (for easy image array manipulation)

    2) Matlab Mode- detects the add-ons above are not present, and tries to use Matlab to plot the charts. 
        - This is currently only implemented for windows
        - This assumes matlab is on the system path, and can be accessed using the batch command "matlab". 


---------------------------------------------------
----         Running the Simulator           ------
---------------------------------------------------

Starting:
~~~~~~~~

python3 SimVis.py

Getting Indifference Charts:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GreenChip SimVis currently has 5 different analysis modes:

a) All_Indifference

This mode takes a specific input folder structure defined at the bottom of this section, and outputs all valid
indifference comparisons between all data within that folder structure. Runs immediately after hitting "chose analysis
mode". This can only be run in matplotlib mode. 

b) All_Breakeven

This mode takes a specific input folder structure defined at the bottom of this section, and outputs all valid
breakeven comparisons between all data within that folder structure. Runs immediately after hitting "chose analysis
mode". This can only be run in matplotlib mode. 

c) Indifference

This mode takes a specific input folder structure defined at the bottom of this section, and allows the user to
generate specific indifference comparisons they want to see. This can run in either matlab plot mode or matplotlib mode. 

d) Breakeven

This mode takes a specific input folder structure defined at the bottom of this section, and allows the user to
generate specific breakeven comparisons they want to see. This can run in either matlab plot mode or matplotlib mode. 

e) Raw_Data_Entry

This mode allows the user to input the raw data directly into the gui. This avoids requiring the Sniper-specific
input format. This can run in either matlab plot mode or matplotlib mode. 

Input Format (modes a-d):
~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, All_Indifference, All_Breakeven, Indifference, and Breakeven expect a specific format.

Folder Levels 1 through (N-1): Various Parameters/labels (can be anything)
Folder Level N: Requires Sniper, DramSim2 output files: sim.out, power.xml, power.py, run_out.txt (DramSim2 output)

An example:

Folder level 1- Number of Cores:      4cores       8cores

Folder level 2- Technology Node:      28      45      90

Folder level 3-  Cache size:          1mb   512kb   4mb

Folder level 4- benchmark name:       blackscholes    canneal    x264

Folder level 5- power.py   power.xml  sim.cfg   sim.out    sim.stats.sqlite3   run_out.txt

---------------------------------------------------
----            Settings File                ------
---------------------------------------------------

Currently the "Advanced Settings File" is parsed looking for the following specific keywords and syntax:

1) Point: x,y

    x and y must be integers, <= 100

    Example: Point: 3,4 will add a circle of 3% active and 4% sleep to all plots. Having at least one point in the
    settings file overwrites the default points. This can be changed after choosing the analysis mode and new plots
    will be updated accordingly.

    The default points on the plot are:
    17, 77 (Typical User Desktop)
    30, 5  (Typical Server, from 2011)
    95, 5  (Typical HPC)
    90, 92 (Cell Phone)

More options might be added over time.


---------------------------------------------------
----             Publications                ------
---------------------------------------------------

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


---------------------------------------------------
----          Authors and Thanks             ------
---------------------------------------------------

Primary Authors, version 0.1:
    Nikolas Parshook

Primary Authors, versions 0.2-0.5:
    Donald Kline, Jr, Nikolas Parshook

Primary Authors, versions 0.6-0.9:
    Donald Kline, Jr
    
Primary Authors, version 0.1.0:
    Ryan Caginalp, Sebastien Ollivier, Stephen Cahoon, Chayanika Choudhuri

Guidance:
    Dr. Alex K. Jones (University of Pittsburgh)
    Dr. Panos Chrysanthis (University of Pittsburgh)

Thanks:
    Eric Cheung, for his work on the indifference plots
