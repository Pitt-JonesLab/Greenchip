import matplotlib
matplotlib.use("TkAgg")
from plugins.shared.Utils import *


path_to_output_directory = "/Users/donaldklinejr/Downloads/Results_new/"
global_cycle_time = 0.000000000375

def plot(*args):

    matplotlib.rc('xtick', labelsize=16)
    matplotlib.rc('ytick', labelsize=16)
    #TODO Paramaterize this
    #NOTE: Must change this for every run
    first_entry = "swim_65nm_4GB"
    entry1 = first_entry
    second_entry = "swim_55nm_4GB"
    entry2 = second_entry


    #Read in here
    #TODO: Parameterize this. Must read in everytime
    f = open('/Users/donaldklinejr/Downloads/Results_new/swim_65vs55_4GBvs4GB_day.txt', 'r')
    res = []
    for line in f:
        line = line.strip()
        temp = []
        for item in line.split(' '):
            temp.append(item)
        res.append(temp)
    #res = [map(int, line.split(' ')) for line in f]
    #print(res)
    f.close()

    # res = GreenChip.chip_breakeven_IPC(config_dicts)['chipVsChipBreakevenInDays']
    #res = GreenChip.chip_breakeven_IPC(config_dicts)['upgradeDays']

    if type(res) is not list:
        res_keys = sorted(res.keys())
    cols = []
    for x in range(0, 11):
        cols.append(round(x * .1, 1))
    data = []
    rows = []
    if type(res) is not list:
        for key in res_keys:
            innerres = res[key]
            inner_keys = sorted(innerres.keys())
            rows.append(round(key * .1, 1))
            inner_data = []
            for inner_key in inner_keys:
                inner_data.append(innerres[inner_key])
            data.append(np.asarray(inner_data))
    else:
        for item in res:
            data.append(np.asarray(item))

    for item in data:
        print(item)

    arr = np.asarray(data)
    column_labels = cols
    row_labels = rows
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
    plt.plot([77], [17], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
    plt.plot([77], [17], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")

    # Server
    plt.plot([5], [30], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
    plt.plot([5], [30], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")

    # HPC
    plt.plot([5], [95], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
    plt.plot([5], [95], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")

    # Cell Phone
    plt.plot([92], [90], 'k.', markersize=35.0, markeredgecolor='black', mew=3, markerfacecolor="None")
    plt.plot([92], [90], 'k.', markersize=30.0, markeredgecolor='white', mew=3, markerfacecolor="None")
    # put the major ticks at the middle of each cell
    # ax.set_xticks(np.arange(arr.shape[0]) + .5, minor=False)
    # ax.set_yticks(np.arange(arr.shape[1]), minor=False)


    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.axis('tight')


    # ax.set_xticklabels(column_labels, minor=False)
    # ax.set_yticklabels(row_labels, minor=False)
    # plt.colorbar(heatbar2)
    #cbar = plt.colorbar(heatbar2, pad=-0.01)
    cbar = plt.colorbar(heatbar2, pad=0.05)
    cbar.ax.set_yticklabels(['11', '22', '33', '44', '55', '66', '77', '88', '99'])
    cbar.ax.tick_params(labelsize=16)
    cbar.set_label('years', rotation=360, size=20, labelpad=-30, y=1.08) # y=1.05
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
    #plt.title(''.join([entry1, ' vs. ', entry2]), y=1.08)

    image_file_name = path_to_output_directory + entry1 + "_vs_" + entry2 + ".pdf"
    print(image_file_name)
    plt.savefig("/Users/donaldklinejr/Downloads/Results_new/"+entry1+"_vs_"+entry2 + ".pdf", bbox_inches='tight')


    plt.clf()
    plt.close()

if __name__ == "__main__":

    plot()
