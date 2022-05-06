from plugins.shared.Utils import *
from plugins.shared.GreenChip import *

global_cycle_time = 0.000000000375


class config(object):

    def __init__(self, root, DB, outdir):
        self.DB = DB
        self.root = root
        self.path_to_output_directory = outdir
        self.window = Toplevel(self.root)
        self.window.geometry("500x100+0+0")
        self.launch_config()

    @staticmethod
    def needs_DB():
        return True

    def plot(self, *args):

        first_entry = utils.build_config(self.DB, self.entry1.get(), self.path_to_output_directory, writeMe=False)
        second_entry = utils.build_config(self.DB, self.entry2.get(), self.path_to_output_directory, writeMe=False)
        config_dicts = []
        if first_entry is None or second_entry is None:
            return
        config_dicts.append(first_entry)
        config_dicts.append(second_entry)
        res = chip_breakeven_IPC(config_dicts)['upgradeDays']
        utils.make_single_plot(self, first_entry, second_entry, self.entry1.get(), self.entry2.get(), res)

    def launch_config(self):
        self.entries = self.DB.list_entries()
        self.entry1 = StringVar()
        self.entry2 = StringVar()
        self.chip_box0 = ttk.Combobox(self.window, textvariable=self.entry1, values=self.entries, width=30)
        self.chip_box0.current(0)
        self.chip_box0.grid(column=0, row=0, sticky=(N, W, E, S))
        self.chip_box1 = ttk.Combobox(self.window, textvariable=self.entry2, values=self.entries)
        self.chip_box1.current(0)
        self.chip_box1.grid(column=0, row=1, sticky=(N, W, E, S))
        self.plotButton = ttk.Button(self.window, text="Create Plot", command=self.plot)
        self.plotButton.grid(column=1, row=0, rowspan=2, sticky=(N, W, E, S))

        for child in self.window.winfo_children(): child.grid_configure(padx=5, pady=5)
        self.window.resizable(width=True, height=True)
