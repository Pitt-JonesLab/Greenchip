__author__ = 'nbp3'

import math

import numpy as np

#NOTE NOTE: The 20 energy is for PCM. Higher energy for non-PCM
# If new entries are added , go to combobox to change the Combobox entries to match the source
high_process_energies = {'3': {'energy': 118080, 'gwp': 0.042}, '5': {'energy': 102600, 'gwp': 0.042}, '6': {'energy': 99360, 'gwp': 0.042}, '7 EUV': {'energy': 74800, 'gwp': 0.042},
                         '7 193i': {'energy': 75960, 'gwp': 0.042}, '8 EUV': {'energy': 58680, 'gwp': 0.042}, '8 193i': {'energy': 60480, 'gwp': 0.042}, '10': {'energy': 52200, 'gwp': 0.042},
                         '12': {'energy': 45142, 'gwp': 0.042}, '14': {'energy': 40680, 'gwp': 0.042}, 
                         '20': {'energy': 41040, 'gwp': 1.6},
                         '28': {'energy': 33480, 'gwp': 0.5}, '30': {'energy': 42397, 'gwp': 0.042},
                         '32': {'energy': 73937, 'gwp': 0.042}, '45': {'energy': 73427, 'gwp': 0.055}, 
                         '65': {'energy': 61699, 'gwp': 0.042}, '90': {'energy': 51501, 'gwp': 0.042}, '130': {'energy': 53541, 'gwp': 0.042},
                         '180': {'energy': 48951, 'gwp': 0.042}, '250': {'energy': 49971, 'gwp': 0.042}, '350': {'energy': 56090, 'gwp': 0.042}
                        }
                        
high_process_energies_with_sources = ['3 (IMEC/DTCO)', '6 (IMEC/DTCO)', '7 EUV (IMEC/DTCO)', '7 193i (IMEC/DTCO)', '8 EUV (IMEC/DTCO)', '8 193i (IMEC/DTCO)', '10 (IMEC/DTCO)', '12 (IMEC/DTCO)', '14 (IMEC/DTCO)', '20 (IMEC/DTCO)', '28 (IMEC/DTCO)', 
                                      '30 (Higgs)',
                                      '32 (Boyd)', '45 (Boyd)', '65 (Boyd)', '130 (Boyd)','180 (Boyd)', '250 (Boyd)', '350 (Boyd)']

#Change the values and match with Raw_Data_Entry line 654
high_process_energies_DRAM = {'3': {'energy': 118080, 'gwp': 0.042}, '5': {'energy': 102600, 'gwp': 0.042}, '6': {'energy': 99360, 'gwp': 0.042}, '7 EUV': {'energy': 74800, 'gwp': 0.042},
                              '7 193i': {'energy': 75960, 'gwp': 0.042}, '8 EUV': {'energy': 58680, 'gwp': 0.042}, '8 193i': {'energy': 60480, 'gwp': 0.042}, '10': {'energy': 52200, 'gwp': 0.042},
                              '12': {'energy': 45142, 'gwp': 0.042}, '14': {'energy': 40680, 'gwp': 0.042}, 
                              '20': {'energy': 41040, 'gwp': 1.6}, 
                              '28': {'energy': 334800, 'gwp': 0.5}, '30': {'energy': 42397, 'gwp': 0.042}, 
                              '32': {'energy': 73937, 'gwp': 0.042}, '45': {'energy': 73427, 'gwp': 0.055},
                              '55': {'energy': 979726, 'gwp': 0.042}, '57': {'energy': 600000, 'gwp': 0.042}, '90': {'energy': 53031, 'gwp': 0.042}, '130': {'energy': 54560, 'gwp': 0.042},
                              '180': {'energy': 45892, 'gwp': 0.042}, '250': {'energy': 48442, 'gwp': 0.042}, 
                             } 

                        


def get_workload_power(dynamic, static, active_percent, sleep_percent):
    return (1 - sleep_percent) * (active_percent * (dynamic + static) + static * (1 - active_percent)) + sleep_percent * 0.2 #0 before seb change


def get_workload_power_with_dram(dynamic, static, active_percent, sleep_percent, mem_dynamic, mem_static):
    return (1 - sleep_percent) * (active_percent * (dynamic + static+mem_dynamic) + static * (1 - active_percent)) +mem_static


def simple_manufacturing(energy, area, layers):
    return energy * (area * layers)


#def manufacturing_energy(config_dict):
#    return simple_manufacturing(
#        high_process_energies[config_dict['processSize']]['energy'],
#        config_dict['chipArea'], config_dict['layers'])


'''def single_chip_stats(config_file):
    results_dict = {}

    with open(config_file, 'r') as f:
        config_dict = json.load(f)

    results_dict['manufacturingEnergy'] = simple_manufacturing(high_process_energies[config_dict['processSize']]['energy'],
                                                               config_dict['chipArea'], config_dict['layers'])

    results_dict['manufacturingVsUseBreakevenInDays'] = {}
    for x in range(0, 11):
        power = get_workload_power(config_dict['dynamicPower'], config_dict['staticPower'], x * 0.1, 0)
        results_dict['manufacturingVsUseBreakevenInDays'][''.join([str(x * 10), '_percentActive'])] = \
            results_dict['manufacturingEnergy'] / power / 3600 / 24

    return results_dict'''


'''def multi_workload(config_files):
    config_dicts = []
    results_dict = {}

    for file in config_files:
        with open(file, 'r') as f:
            config_dicts.append(json.load(f))

    config_dict = config_dicts[0]
    results_dict['manufacturingEnergy'] = simple_manufacturing(high_process_energies[config_dict['processSize']]['energy'],
                                                               config_dict['chipArea'], config_dict['layers'])
    results_dict['manufacturingVsUseBreakevenInDays'] = {}
    for x in range(0, 11):
        non_idle_percent = 1 - x * .1
        workload_percent = non_idle_percent / len(config_dicts)
        dynamic_power = 0
        for workload in config_dicts:
            dynamic_power += workload_percent * (workload['dynamicPower'] + workload['staticPower'])
        power = config_dicts[0]['staticPower'] * (x * .1) + dynamic_power
        results_dict['manufacturingVsUseBreakevenInDays'][''.join([str(x * 10), '_percentActive'])] = \
            results_dict['manufacturingEnergy'] / power / 3600 / 24

    return results_dict'''


'''def chip_breakeven_IPC_file(config_files):
    config_dicts = []

    for file in config_files:
        with open(file, 'r') as f:
            config_dicts.append(json.load(f))

    return chip_breakeven_IPC(config_dicts)'''

def chip_breakeven_IPC(config_dicts, calc_Carbon, increment = 0.50, norm_large = False):
    results_dict = {}
    if norm_large:
        if calc_Carbon:
            results_dict['chipVsChipBreakevenInDays'] = {}
            results_dict['upgradeDays'] = {}
            chip1IPC = config_dicts[0]['IPC']
            chip2IPC = config_dicts[1]['IPC']
            chip1freq = config_dicts[0]['FREQ']
            chip2freq = config_dicts[1]['FREQ']
            p1Factor = 0
            p2Factor = 0
            for y in np.arange(0.0, 100.0 + increment, increment):
                results_dict['chipVsChipBreakevenInDays'][y] = {}
                results_dict['upgradeDays'][y] = {}
                for x in np.arange(0.0, 100.0 + increment, increment):
                    mult = (config_dicts[0]['IPC'] * (1-(0.01 * y))*(0.01 * x)/config_dicts[1]['IPC'])
                    if mult == 0.0:
                        x_ceil = 1
                    else:
                        x_ceil = math.ceil(mult)

                    dict_num = 0
                    for config_dict in config_dicts:
                        if dict_num == 0:
                            results_dict[''.join(['manufacturingCarbon', str(dict_num)])] = \
                                config_dicts[dict_num]['Total CPU Carbon'] + config_dicts[dict_num]['Total DRAM Carbon']
                        else:
                            results_dict[''.join(['manufacturingCarbon', str(dict_num), str(y), str(x)])] = \
                                config_dicts[dict_num]['Total CPU Carbon']*x_ceil + config_dicts[dict_num]['Total DRAM Carbon']
                        dict_num += 1

                    chip2IPC = config_dicts[1]['IPC'] * x_ceil

                    if (chip1IPC*chip1freq) < (chip2IPC*chip2freq):
                        p1Factor = 1
                        p2Factor = (chip1IPC*chip1freq) / (chip2IPC*chip2freq)
                    else:
                        p2Factor = 1
                        p1Factor = (chip2IPC*chip2freq) / (chip1IPC*chip1freq)

                    awake_1 = mult/x_ceil

                    power1 = get_workload_power_with_dram(config_dicts[0]['dynamicPower'],
                                                          config_dicts[0]['staticPower'],
                                                          x * 0.01 * p1Factor,
                                                          y * 0.01,
                                                          config_dicts[0]['dynamicMemory'],
                                                          config_dicts[0]['staticMemory'])
                    power2 = get_workload_power_with_dram(config_dicts[1]['dynamicPower']*x_ceil,
                                                          config_dicts[1]['staticPower']*x_ceil,
                                                          1 * p2Factor,
                                                          1-awake_1,
                                                          config_dicts[1]['dynamicMemory'],
                                                          config_dicts[1]['staticMemory'])
                    carbon1 = (power1/3600000) * config_dicts[0] ['UsePh Carbon Value']
                    carbon2 = (power2/3600000) * config_dicts[1] ['UsePh Carbon Value']
                    manufacturingCarbon_diff = results_dict['manufacturingCarbon0'] - results_dict[''.join(['manufacturingCarbon', str(1), str(y), str(x)])]
                    useCarbon_diff = carbon2 - carbon1

                    # print(energy_diff)
                    # print(power_diff)
                    # print(x)
                    # print(y)

                    if useCarbon_diff != 0:
                            results_dict['chipVsChipBreakevenInDays'][y][x] = \
                                (manufacturingCarbon_diff / useCarbon_diff) / 3600 / 24

                            results_dict['upgradeDays'][y][x] = (results_dict[''.join(['manufacturingCarbon', str(1), str(y), str(x)])] / (
                            carbon1 - carbon2)) / 3600 / 24

                            if results_dict['chipVsChipBreakevenInDays'][y][x] < 0:
                                results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                            if results_dict['upgradeDays'][y][x] < 0:
                                results_dict['upgradeDays'][y][x] = -42
                    else:
                        results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                        results_dict['upgradeDays'][y][x] = -42

        else:
            results_dict['chipVsChipBreakevenInDays'] = {}
            results_dict['upgradeDays'] = {}
            chip1IPC = config_dicts[0]['IPC']
            chip2IPC = config_dicts[1]['IPC']
            chip1freq = config_dicts[0]['FREQ']
            chip2freq = config_dicts[1]['FREQ']
            p1Factor = 0
            p2Factor = 0
            for y in np.arange(0.0, 100.0 + increment, increment):

                results_dict['chipVsChipBreakevenInDays'][y] = {}
                results_dict['upgradeDays'][y] = {}

                for x in np.arange(0.0, 100.0 + increment, increment):
                    mult = (config_dicts[0]['IPC'] * (1-(0.01 * y))*(0.01 * x)/config_dicts[1]['IPC'])
                    if mult == 0.0:
                        x_ceil = 1
                    else:
                        x_ceil = math.ceil(mult)
                    dict_num = 0
                    for config_dict in config_dicts:
                        if dict_num == 0:
                            results_dict[''.join(['manufacturingEnergy', str(dict_num)])] = \
                                simple_manufacturing(high_process_energies[str(config_dict['processSize'])]['energy'], config_dict['chipArea'],
                                config_dict['layers']) + \
                                simple_manufacturing(high_process_energies_DRAM[str(config_dict['processSizeDram'])]['energy'], config_dict['chipAreaDram'],
                                config_dict['layers'])  + \
                                config_dict['Total Added Energy']
                        else:
                            results_dict[''.join(['manufacturingEnergy', str(dict_num),str(y), str(x)])] = \
                                simple_manufacturing(high_process_energies[str(config_dict['processSize'])]['energy'], config_dict['chipArea']  * x_ceil,
                                config_dict['layers']) + \
                                simple_manufacturing(high_process_energies_DRAM[str(config_dict['processSizeDram'])]['energy'], config_dict['chipAreaDram'],
                                config_dict['layers'])  + \
                                config_dict['Total Added Energy']

                        dict_num += 1

                    chip2IPC = config_dicts[1]['IPC'] * x_ceil

                    if (chip1IPC*chip1freq) < (chip2IPC*chip2freq):
                        p1Factor = 1
                        p2Factor = (chip1IPC * chip1freq) / (chip2IPC * chip2freq)
                    else:
                        p2Factor = 1
                        p1Factor = (chip2IPC * chip2freq) / (chip1IPC * chip1freq)

                    awake_1 = mult/x_ceil
                    power1 = get_workload_power_with_dram(config_dicts[0]['dynamicPower'],
                                                          config_dicts[0]['staticPower'],
                                                          x * 0.01 * p1Factor,
                                                          y * 0.01,
                                                          config_dicts[0]['dynamicMemory'],
                                                          config_dicts[0]['staticMemory'])
                    power2 = get_workload_power_with_dram(config_dicts[1]['dynamicPower'] * x_ceil,
                                                          config_dicts[1]['staticPower'] * x_ceil,
                                                          1 * p2Factor,
                                                          1-awake_1,
                                                          config_dicts[1]['dynamicMemory'],
                                                          config_dicts[1]['staticMemory'])

                    energy_diff = results_dict['manufacturingEnergy0'] - results_dict[''.join(['manufacturingEnergy', str(1), str(y), str(x)])]

                    power_diff = power2 - power1

                    if power_diff != 0:

                        results_dict['chipVsChipBreakevenInDays'][y][x] = \
                            (energy_diff / power_diff) / 3600 / 24

                        results_dict['upgradeDays'][y][x] = (results_dict[''.join(['manufacturingEnergy', str(1), str(y), str(x)])] / (
                        power1 - power2)) / 3600 / 24

                        if results_dict['chipVsChipBreakevenInDays'][y][x] < 0:
                            results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                        if results_dict['upgradeDays'][y][x] < 0:
                            results_dict['upgradeDays'][y][x] = -42
                    else:
                        results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                        results_dict['upgradeDays'][y][x] = -42

                #results_dict['upgradeDays'][y][x] = (results_dict['manufacturingEnergy1'] / (power1 - power2)) / 3600 / 24
    else:
        if calc_Carbon:
            dict_num = 0
            for config_dict in config_dicts:
                results_dict[''.join(['manufacturingCarbon', str(dict_num)])] = \
                    config_dicts[dict_num]['Total CPU Carbon'] + config_dicts[dict_num]['Total DRAM Carbon']
                dict_num += 1

            results_dict['chipVsChipBreakevenInDays'] = {}
            results_dict['upgradeDays'] = {}
            chip1IPC = config_dicts[0]['IPC']
            chip2IPC = config_dicts[1]['IPC']
            chip1freq = config_dicts[0]['FREQ']
            chip2freq = config_dicts[1]['FREQ']
            p1Factor = 0
            p2Factor = 0
            if (chip1IPC * chip1freq) < (chip2IPC * chip2freq):
                p1Factor = 1
                p2Factor = (chip1IPC * chip1freq) / (chip2IPC * chip2freq)
            else:
                p2Factor = 1
                p1Factor = (chip2IPC * chip2freq) / (chip1IPC * chip1freq)
            for y in np.arange(0.0, 100.0 + increment, increment):
                results_dict['chipVsChipBreakevenInDays'][y] = {}
                results_dict['upgradeDays'][y] = {}
                for x in np.arange(0.0, 100.0 + increment, increment):
                    power1 = get_workload_power_with_dram(config_dicts[0]['dynamicPower'],
                                                          config_dicts[0]['staticPower'],
                                                          x * 0.01 * p1Factor,
                                                          y * 0.01,
                                                          config_dicts[0]['dynamicMemory'],
                                                          config_dicts[0]['staticMemory'])
                    power2 = get_workload_power_with_dram(config_dicts[1]['dynamicPower'],
                                                          config_dicts[1]['staticPower'],
                                                          x * 0.01 * p2Factor,
                                                          y * 0.01,
                                                          config_dicts[1]['dynamicMemory'],
                                                          config_dicts[1]['staticMemory'])
                    carbon1 = (power1 / 3600000) * config_dicts[0]['UsePh Carbon Value']
                    carbon2 = (power2 / 3600000) * config_dicts[1]['UsePh Carbon Value']
                    manufacturingCarbon_diff = results_dict['manufacturingCarbon0'] - results_dict[
                        'manufacturingCarbon1']
                    useCarbon_diff = carbon2 - carbon1

                    # print(energy_diff)
                    # print(power_diff)
                    # print(x)
                    # print(y)

                    if useCarbon_diff != 0:
                        results_dict['chipVsChipBreakevenInDays'][y][x] = \
                            (manufacturingCarbon_diff / useCarbon_diff) / 3600 / 24

                        results_dict['upgradeDays'][y][x] = (results_dict['manufacturingCarbon1'] / (
                                carbon1 - carbon2)) / 3600 / 24

                        if results_dict['chipVsChipBreakevenInDays'][y][x] < 0:
                            results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                        if results_dict['upgradeDays'][y][x] < 0:
                            results_dict['upgradeDays'][y][x] = -42
                    else:
                        results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                        results_dict['upgradeDays'][y][x] = -42

        else:
            dict_num = 0
            for config_dict in config_dicts:
                results_dict[''.join(['manufacturingEnergy', str(dict_num)])] = \
                    simple_manufacturing(high_process_energies[str(config_dict['processSize'])]['energy'],
                                         config_dict['chipArea'],
                                         config_dict['layers']) + \
                    simple_manufacturing(high_process_energies_DRAM[str(config_dict['processSizeDram'])]['energy'],
                                         config_dict['chipAreaDram'],
                                         config_dict['layers'])  + \
                    config_dict['Total Added Energy']

                dict_num += 1

            results_dict['chipVsChipBreakevenInDays'] = {}
            results_dict['upgradeDays'] = {}
            chip1IPC = config_dicts[0]['IPC']
            chip2IPC = config_dicts[1]['IPC']
            chip1freq = config_dicts[0]['FREQ']
            chip2freq = config_dicts[1]['FREQ']
            p1Factor = 0
            p2Factor = 0
            if (chip1IPC * chip1freq) < (chip2IPC * chip2freq):
                p1Factor = 1
                p2Factor = (chip1IPC * chip1freq) / (chip2IPC * chip2freq)
            else:
                p2Factor = 1
                p1Factor = (chip2IPC * chip2freq) / (chip1IPC * chip1freq)
            for y in np.arange(0.0, 100.0 + increment, increment):
                results_dict['chipVsChipBreakevenInDays'][y] = {}
                results_dict['upgradeDays'][y] = {}
                for x in np.arange(0.0, 100.0 + increment, increment):
                    power1 = get_workload_power_with_dram(config_dicts[0]['dynamicPower'],
                                                          config_dicts[0]['staticPower'],
                                                          x * 0.01 * p1Factor,
                                                          y * 0.01,
                                                          config_dicts[0]['dynamicMemory'],
                                                          config_dicts[0]['staticMemory'])
                    power2 = get_workload_power_with_dram(config_dicts[1]['dynamicPower'],
                                                          config_dicts[1]['staticPower'],
                                                          x * 0.01 * p2Factor,
                                                          y * 0.01,
                                                          config_dicts[1]['dynamicMemory'],
                                                          config_dicts[1]['staticMemory'])

                    energy_diff = results_dict['manufacturingEnergy0'] - results_dict['manufacturingEnergy1']
                    power_diff = power2 - power1

                    # print(energy_diff)
                    # print(power_diff)
                    # print(x)
                    # print(y)

                    if power_diff != 0:

                        results_dict['chipVsChipBreakevenInDays'][y][x] = \
                            (energy_diff / power_diff) / 3600 / 24

                        results_dict['upgradeDays'][y][x] = (results_dict['manufacturingEnergy1'] / (
                                power1 - power2)) / 3600 / 24

                        if results_dict['chipVsChipBreakevenInDays'][y][x] < 0:
                            results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                        if results_dict['upgradeDays'][y][x] < 0:
                            results_dict['upgradeDays'][y][x] = -42
                    else:
                        results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                        results_dict['upgradeDays'][y][x] = -42

                # results_dict['upgradeDays'][y][x] = (results_dict['manufacturingEnergy1'] / (power1 - power2)) / 3600 / 24

    return results_dict


def chip_breakeven_ACT(config_dicts, calc_Carbon = True, increment = 0.50):
    dict_num = 0
    results_dict = {}
    for config_dict in config_dicts:
        results_dict[''.join(['manufacturingCarbon', str(dict_num)])] = \
            config_dicts[dict_num]['Total Carbon']
        dict_num += 1

    results_dict['chipVsChipBreakevenInDays'] = {}
    results_dict['upgradeDays'] = {}
    chip1IPC = config_dicts[0]['IPC']
    chip2IPC = config_dicts[1]['IPC']
    chip1freq = config_dicts[0]['FREQ']
    chip2freq = config_dicts[1]['FREQ']
    p1Factor = 0
    p2Factor = 0
    if (chip1IPC * chip1freq) < (chip2IPC * chip2freq):
        p1Factor = 1
        p2Factor = (chip1IPC * chip1freq) / (chip2IPC * chip2freq)
    else:
        p2Factor = 1
        p1Factor = (chip2IPC * chip2freq) / (chip1IPC * chip1freq)
    for y in np.arange(0.0, 100.0 + increment, increment):
        results_dict['chipVsChipBreakevenInDays'][y] = {}
        results_dict['upgradeDays'][y] = {}
        for x in np.arange(0.0, 100.0 + increment, increment):
            power1 = get_workload_power_with_dram(config_dicts[0]['dynamicPower'],
                                                  config_dicts[0]['staticPower'],
                                                  x * 0.01 * p1Factor,
                                                  y * 0.01,
                                                  config_dicts[0]['dynamicMemory'],
                                                  config_dicts[0]['staticMemory'])
            power2 = get_workload_power_with_dram(config_dicts[1]['dynamicPower'],
                                                  config_dicts[1]['staticPower'],
                                                  x * 0.01 * p2Factor,
                                                  y * 0.01,
                                                  config_dicts[1]['dynamicMemory'],
                                                  config_dicts[1]['staticMemory'])
            carbon1 = (power1 / 3600000) * config_dicts[0]['UsePh Carbon Value']
            carbon2 = (power2 / 3600000) * config_dicts[1]['UsePh Carbon Value']
            manufacturingCarbon_diff = results_dict['manufacturingCarbon0'] - results_dict[
                'manufacturingCarbon1']
            useCarbon_diff = carbon2 - carbon1

            # print(energy_diff)
            # print(power_diff)
            # print(x)
            # print(y)

            if useCarbon_diff != 0:
                results_dict['chipVsChipBreakevenInDays'][y][x] = \
                    (manufacturingCarbon_diff / useCarbon_diff) / 3600 / 24

                results_dict['upgradeDays'][y][x] = (results_dict['manufacturingCarbon1'] / (
                        carbon1 - carbon2)) / 3600 / 24

                if results_dict['chipVsChipBreakevenInDays'][y][x] < 0:
                    results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                if results_dict['upgradeDays'][y][x] < 0:
                    results_dict['upgradeDays'][y][x] = -42
            else:
                results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                results_dict['upgradeDays'][y][x] = -42

    return results_dict