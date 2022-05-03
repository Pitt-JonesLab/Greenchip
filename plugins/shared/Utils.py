import os
from plugins.loaders import *
from tkinter import *
from tkinter import ttk
import plugins.shared.Config as settingsConfig
from plugins.shared.GreenChip import *
from tkinter import messagebox
from tkinter import simpledialog
import subprocess
import math
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition

if settingsConfig.nativePlotting:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib import pyplot as plt
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap



class utils(object):
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
        label = ':'.join([utils.abbreviate(items1[3]), items1[2] + "MB"])
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
    def build_config(database, entry, path_to_output_directory, writeMe = True):
        global_cycle_time = 0.000000000375
        mcpat, mcpat_was_loaded = database.get_item(entry, 'power.py', mcpat_dict_loader)
        if mcpat is None:
            return None
        dramsim, dramsim_was_loaded = database.get_item(entry, 'run_out.txt', dramsim_dict_loader)
        ipc, ipc_was_loaded = database.get_item(entry, 'sim.out', ipc_dict_loader)
        if ipc is None:
            return None

        config = {}
        config['chipArea'] = mcpat['Processor']['Area']
        config['dynamicPower'] = mcpat['Processor']['Runtime Dynamic']
        config['staticPower'] = mcpat['Processor']['Subthreshold Leakage with power gating'] + mcpat['Processor'][
            'Gate Leakage']
        config['staticMemory'] = dramsim['static_memory']
        config['dynamicMemory'] = dramsim['dynamic_memory']
        config['MPKI'] = ipc['mpki']
        config['IPC'] = ipc['ipc']
        config['cycles'] = ipc['cycles']
        config['layers'] = 1
        mcpat_cfg, mcpat_config_was_loaded = database.get_item(entry, 'power.xml', mcpat_cfg_loader)
        config['processSize'] = int(mcpat_cfg[0][14].attrib['value'])

        if mcpat_was_loaded and dramsim_was_loaded:
            entry = utils.rename(entry, False)

            if writeMe:
                with open(path_to_output_directory + "Power.csv", "a") as power_file:
                    power_file.write(entry + "," + str(config['staticMemory']) + "," + str(config['staticPower']) + "," +
                                     str(config['dynamicMemory']) + "," + str(config['dynamicPower']) + "\n")

                with open(path_to_output_directory + "MPKI.csv", "a") as mpki_file:
                    mpki_file.write(entry + "," + str(ipc['mpki']) + "\n")

                with open(path_to_output_directory + "IPC.csv", "a") as ipc_file:
                    ipc_file.write(entry + "," + str(ipc['ipc']) + "\n")

                with open(path_to_output_directory + "Energy.csv", "a") as energy_file:
                    energy_file.write(
                        entry + "," + str(config['staticMemory'] * config['cycles'] * global_cycle_time) +
                        "," + str(config['staticPower'] * config['cycles'] * global_cycle_time) + "," +
                        str(config['dynamicMemory'] * config['cycles'] * global_cycle_time) + "," +
                        str(config['dynamicPower'] * config['cycles'] * global_cycle_time) + "\n")

        return config

    @staticmethod
    def make_plot(first_entry, second_entry, entry1, entry2, res, snapshot_label, path_to_output_directory):
        if settingsConfig.nativePlotting:
            matplotlib.rc('xtick', labelsize=16)
            matplotlib.rc('ytick', labelsize=16)

            if first_entry is None or second_entry is None:
                return

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

            # Desktop
#            plt.plot([77], [17], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
#            plt.plot([77], [17], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")

            # Server
#            plt.plot([5], [30], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
#            plt.plot([5], [30], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")

            # HPC
#            plt.plot([5], [95], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
#            plt.plot([5], [95], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")

            # Cell Phone
 #           plt.plot([92], [90], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
 #           plt.plot([92], [90], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")

            # Make sure this comparison makes sense (i.e., different process nodes)
            # Get Names
            if snapshot_label is not None and utils.snapshot_reasonable(entry1, entry2):
                filename, label = utils.snapshot_gather(entry1, entry2)
                if not os.path.exists(path_to_output_directory + "Snapshots"):
                    os.makedirs(path_to_output_directory + "Snapshots")

                with open(path_to_output_directory + "Snapshots/"+snapshot_label+"_Desktop_" + filename + ".csv", "a") as desktop_file:
                    desktop_value = arr[17][77]
                    desktop_file.write(label + "," + str(desktop_value) + "\n")
                with open(path_to_output_directory + "Snapshots/"+snapshot_label+"_Server_" + filename + ".csv", "a") as server_file:
                    server_value = arr[30][5]
                    server_file.write(label + "," + str(server_value) + "\n")
                with open(path_to_output_directory + "Snapshots/"+snapshot_label+"_HPC_" + filename + ".csv", "a") as hpc_file:
                    hpc_value = arr[95][5]
                    hpc_file.write(label + "," + str(hpc_value) + "\n")
                with open(path_to_output_directory + "Snapshots/"+snapshot_label+"_Mobile_" + filename + ".csv", "a") as mobile_file:
                    mobile_value = arr[90][92]
                    mobile_file.write(label + "," + str(mobile_value) + "\n")

            # want a more natural, table-like display
            ax.invert_yaxis()
            ax.xaxis.tick_top()
            ax.axis('tight')

            first_ipc = "{0:.2f}".format(first_entry['IPC'])
            second_ipc = "{0:.2f}".format(second_entry['IPC'])

            first_mpki = "{0:.2f}".format(first_entry['MPKI'])
            second_mpki = "{0:.2f}".format(second_entry['MPKI'])

            fig.text(0.95, 0.01, 'IPC: ' + first_ipc + ',' + second_ipc,
                     verticalalignment='bottom', horizontalalignment='left',
                     color='brown', fontsize=15)

            fig.text(0.95, 0.01, 'MPKI: ' + first_mpki + ',' + second_mpki + '\t',
                     verticalalignment='top', horizontalalignment='right',
                     color='brown', fontsize=15)

            # ax.set_xticklabels(column_labels, minor=False)
            # ax.set_yticklabels(row_labels, minor=False)
            # plt.colorbar(heatbar2)
            cbar = plt.colorbar(heatbar2, pad=0.05)
            cbar.ax.set_yticklabels(['11', '22', '33', '44', '55', '66', '77', '88', '99'])
            cbar.ax.tick_params(labelsize=16)
            cbar.set_label('years', rotation=360, size=20, labelpad=-30, y=1.08)
            # plt.colorbar(heatbar)
            cbar2 = plt.colorbar(heatbar)
            cbar2.ax.tick_params(labelsize=16)
            # cbar.ax.set_yticklabels(labelsize=10)
            cbar2.set_label('days', rotation=360, size=20, labelpad=-37.5, y=1.08)
            plt.xlabel('xlabel', fontsize=18)
            plt.ylabel('ylabel', fontsize=18)
            # plt.xlabel('Percent Sleep')
            ax.set_xlabel('Percent Sleep')
            ax.xaxis.set_label_position('top')
            plt.ylabel('Activity Ratio')
            # plt.title(''.join([utils.rename(self.entry1, False), ' vs. ', utils.rename(self.entry2, False)]), y=1.08)

            image_file_name = path_to_output_directory + utils.rename(entry1, True) + "_vs_" + utils.rename(
                entry2, True) + ".pdf"

            plt.savefig(image_file_name, bbox_inches='tight')

            plt.clf()
            plt.close()

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

    @staticmethod
    def make_single_plot(first_entry, second_entry, title1, title2, res):
        if settingsConfig.nativePlotting:
            matplotlib.rc('xtick', labelsize=16)
            matplotlib.rc('ytick', labelsize=16)


            if first_entry is None or second_entry is None:
                return

            settingsFile = settingsConfig.advancedSettingsFile
            arr = utils.perform_greenchip_analysis(res)

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


            if settingsFile is None:
                seb=1
                # Desktop
#                plt.plot([77], [17], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
#                plt.plot([77], [17], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
#                plt.annotate('Desktop',[77+5,17+5])

                # Server
#                plt.plot([5], [30], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
#                plt.plot([5], [30], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
#                plt.annotate('Server',[5+5,30+5])

                # HPC
#                plt.plot([5], [95], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
#                plt.plot([5], [95], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
#                plt.annotate('HPC',[5+5,95+5])

                # Cell Phone
#                plt.plot([92], [90], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
#                plt.plot([92], [90], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
#                plt.annotate('Cellular',[92+5,90+5])

            else:

                with open(settingsFile, "r") as settingsObject:
                    for line in settingsObject:
                        if "point" in line or "Point" in line:
                            tmp = line.split(":")[1].strip()
                            active = int(tmp.split(",")[0].strip())
                            sleep = int(tmp.split(",")[1].strip())
                            plt.plot([active], [sleep], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
                            plt.plot([active], [sleep], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")

            # want a more natural, table-like display
            ax.invert_yaxis()
            ax.xaxis.tick_top()
            ax.axis('tight')

            first_ipc = "{0:.2f}".format(first_entry['IPC'])
            second_ipc = "{0:.2f}".format(second_entry['IPC'])

            fig.text(0.95, 0.01, 'IPC: ' + first_ipc + ',' + second_ipc,
                     verticalalignment='bottom', horizontalalignment='left',
                     color='brown', fontsize=15)

            # ax.set_xticklabels(column_labels, minor=False)
            # ax.set_yticklabels(row_labels, minor=False)
            # plt.colorbar(heatbar2)
            cbar = plt.colorbar(heatbar2, pad=0.05)
            cbar.ax.set_yticklabels(['11', '22', '33', '44', '55', '66', '77', '88', '99'])
            cbar.ax.tick_params(labelsize=16)
            cbar.set_label('years', rotation=360, size=20, labelpad=-30, y=1.08)
            # plt.colorbar(heatbar)
            cbar2 = plt.colorbar(heatbar)
            cbar2.ax.tick_params(labelsize=16)
            # cbar.ax.set_yticklabels(labelsize=10)
            cbar2.set_label('days', rotation=360, size=20, labelpad=-37.5, y=1.08)
            plt.xlabel('xlabel', fontsize=18)
            plt.ylabel('ylabel', fontsize=18)
            # plt.xlabel('Percent Sleep')
            ax.set_xlabel('Percent Sleep')
            ax.xaxis.set_label_position('top')
            plt.ylabel('Activity Ratio')
            # plt.title(''.join([utils.rename(self.entry1, False), ' vs. ', utils.rename(self.entry2, False)]), y=1.08)

            #image_file_name = path_to_output_directory + title1 + "_vs_" + title2 + ".pdf"

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
