# Changelog 
### Version 0.1.2 - 08/22/22
 * Implemented carbon into all modes
 * Added a plot settings option that allows for the customization of plot ranges and the resolution of the plots
 * Updated the patcher to Specifier, which allows the user to add default carbon and DRAM data to simulator output folders via a Greenchip.txt file
 * Updated EnergyGridMix with additional countries and included functionality for states/provinces
 * Updated EnergyGridMix to allow for the customization of usage percentages
 * Added the ability to select custom csv files instead of the default EnergyGridMix
 * Added sniper inputs for Raw Data Entry
 * Added a toggle for the usage of DRAM and carbon to all modes
 * Added a folder memory for each of the folder selection options so that reselecting files is easier on startup
 * Removed the ability to create duplicates of the same window
 * Sniper inputs will pull in DRAM and Carbon data if Greenchip.txt exists
 * Added CMOS tech nodes to DRAM options (for rough estimation)
 * Updated and changed various text to be more descriptive
 * Added a hash to plots in cases where the time is infinite
 * Snapshot files now use the user's marker points rather than default values
 * Fixed bugs with 7 nm and 8 nm tech nodes


### Version 0.1.1 - 07/22/22

 * Added Carbon Emission Breakeven and Indifference plots to Raw Data Entry modes
 * Added Plot Titles for clarity
 * Updated the GUI for Raw Data Entry and Raw Data Entry Sliders
 * Added more tech nodes for CPU manufacturing
 * Added DRAM manufacturing energy estimation
 * Added frequency to all energy calculations 
 * Added a power.py patcher for DRAM manufacturing
 * Changed Breakeven and Indifference to use any input folder format
 * Updated Sliders Indifference and Breakeven to use Runtime Dynamic instead of Peak Dynamic Energy and to use power gating for Static Energy
 * Added more Tooltips and updated older ones
 * Fixed Readme and added HTML Readme to tool
