__author__ = 'nbp3'

import json

#NOTE NOTE: The 20 energy is for PCM. Higher energy for non-PCM
# If new entries are added , go to combobox to change the Combobox entries to match the source
high_process_energies = {'3': {'energy': 118080, 'gwp': 0.042}, '5': {'energy': 102600, 'gwp': 0.042}, '6': {'energy': 99360, 'gwp': 0.042}, '7 EUV': {'energy': 74800, 'gwp': 0.042},
                         '7 193i': {'energy': 75960, 'gwp': 0.042}, '8 EUV': {'energy': 58680, 'gwp': 0.042}, '8 193i': {'energy': 60480, 'gwp': 0.042}, '10': {'energy': 52200, 'gwp': 0.042},
                         '12': {'energy': 45142, 'gwp': 0.042}, '14': {'energy': 40680, 'gwp': 0.042}, 
                         '20': {'energy': 41040, 'gwp': 1.6}, 
                         '28': {'energy': 334800, 'gwp': 0.5}, '30': {'energy': 42397, 'gwp': 0.042}, 
                         '32': {'energy': 73937, 'gwp': 0.042}, '45': {'energy': 73427, 'gwp': 0.055}, 
                         '65': {'energy': 61699, 'gwp': 0.042}, '90': {'energy': 51501, 'gwp': 0.042}, '130': {'energy': 53541, 'gwp': 0.042},
                         '180': {'energy': 48951, 'gwp': 0.042}, '250': {'energy': 49971, 'gwp': 0.042}, '350': {'energy': 56090, 'gwp': 0.042}
                        }
                        
high_process_energies_with_sources = ['3 (IMEC/DTCO)', '6 (IMEC/DTCO)', '7 193i (IMEC/DTCO)', '8 193i (IMEC/DTCO)', '10 (IMEC/DTCO)', '12 (IMEC/DTCO)', '14 (IMEC/DTCO)', '20 (IMEC/DTCO)', '28 (IMEC/DTCO)', 
                                      '30 (Higgs)',
                                      '32 (Boyd)', '45 (Boyd)', '65 (Boyd)', '130 (Boyd)','180 (Boyd)', '250 (Boyd)', '350 (Boyd)']

#Change the values and match with Raw_Data_Entry line 654
high_process_energies_DRAM = {'55': {'energy': 979726, 'gwp': 0.042}, '57': {'energy': 600000, 'gwp': 0.042}, '90': {'energy': 53031, 'gwp': 0.042}, '130': {'energy': 54560, 'gwp': 0.042},
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


def chip_breakeven_IPC(config_dicts, calc_Carbon):
    results_dict = {}
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
        if (chip1IPC*chip1freq) < (chip2IPC*chip2freq):
            p1Factor = 1
            p2Factor = (chip1IPC*chip1freq) / (chip2IPC*chip2freq)
        else:
            p2Factor = 1
            p1Factor = (chip2IPC*chip2freq) / (chip1IPC*chip1freq)
        for y in range(0, 100):
            results_dict['chipVsChipBreakevenInDays'][y] = {}
            results_dict['upgradeDays'][y] = {}
            for x in range(0, 101):
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
                carbon1 = (power1/3600000) * config_dicts[0] ['UsePh Carbon Value'] 
                carbon2 = (power2/3600000) * config_dicts[1] ['UsePh Carbon Value']
                manufacturingCarbon_diff = results_dict['manufacturingCarbon0'] - results_dict['manufacturingCarbon1']
                useCarbon_diff = carbon2 - carbon1

                # print(energy_diff)
                # print(power_diff)
                # print(x)
                # print(y)

                if useCarbon_diff != 0:
                        results_dict['chipVsChipBreakevenInDays'][y][x] = \
                            (manufacturingCarbon_diff / useCarbon_diff) / 3600 / 24
                        if results_dict['chipVsChipBreakevenInDays'][y][x] < 0:
                            results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                        results_dict['upgradeDays'][y][x] = (results_dict['manufacturingCarbon1'] / (
                        carbon1 - carbon2)) / 3600 / 24
                else:
                    results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                    results_dict['upgradeDays'][y][x] = -42
            
    else:
        dict_num = 0
        for config_dict in config_dicts:
            results_dict[''.join(['manufacturingEnergy', str(dict_num)])] = \
                simple_manufacturing(high_process_energies[str(config_dict['processSize'])]['energy'], config_dict['chipArea'],
                config_dict['layers']) + \
                simple_manufacturing(high_process_energies_DRAM[str(config_dict['processSizeDram'])]['energy'], config_dict['chipAreaDram'],
                config_dict['layers'])

            dict_num += 1

        results_dict['chipVsChipBreakevenInDays'] = {}
        results_dict['upgradeDays'] = {}
        chip1IPC = config_dicts[0]['IPC']
        chip2IPC = config_dicts[1]['IPC']
        chip1freq = config_dicts[0]['FREQ']
        chip2freq = config_dicts[1]['FREQ']
        p1Factor = 0
        p2Factor = 0
        if (chip1IPC*chip1freq) < (chip2IPC*chip2freq):
            p1Factor = 1
            p2Factor = (chip1IPC*chip1freq) / (chip2IPC*chip2freq)
        else:
            p2Factor = 1
            p1Factor = (chip2IPC*chip2freq) / (chip1IPC*chip1freq)
        for y in range(0, 100):
            results_dict['chipVsChipBreakevenInDays'][y] = {}
            results_dict['upgradeDays'][y] = {}
            for x in range(0, 101):
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
                        if results_dict['chipVsChipBreakevenInDays'][y][x] < 0:
                            results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                        results_dict['upgradeDays'][y][x] = (results_dict['manufacturingEnergy1'] / (
                        power1 - power2)) / 3600 / 24
                else:
                    results_dict['chipVsChipBreakevenInDays'][y][x] = -42
                    results_dict['upgradeDays'][y][x] = -42


            #results_dict['upgradeDays'][y][x] = (results_dict['manufacturingEnergy1'] / (power1 - power2)) / 3600 / 24
    return results_dict


'''def chip_breakeven_Triangle(config_dicts):
    results_dict = {}

    dict_num = 0
    for config_dict in config_dicts:
        results_dict[''.join(['manufacturingEnergy', str(dict_num)])] = \
            simple_manufacturing(high_process_energies[config_dict['processSize']]['energy'], config_dict['chipArea'],
                                 config_dict['layers'])
        dict_num += 1

    results_dict['chipVsChipBreakevenInDays'] = {}
    chip1IPC = config_dicts[0]['IPC']
    chip2IPC = config_dicts[1]['IPC']
    p1Factor = 0
    p2Factor = 0
    if chip1IPC < chip2IPC:
        p1Factor = 1
        p2Factor = chip1IPC / chip2IPC
    else:
        p2Factor = 1
        p1Factor = chip2IPC / chip1IPC
    for y in range(0, 100):
        results_dict['chipVsChipBreakevenInDays'][y] = {}
        for x in range(0, 101 - y):
            if y != 0:
                x = (x * 0.01 / (1 - y * 0.01))
            else:
                x *= 0.01
            power1 = get_workload_power_with_dram(config_dicts[0]['dynamicPower'],
                                                  config_dicts[0]['staticPower'],
                                                  x * p1Factor,
                                                  y * 0.01,
                                                  config_dicts[0]['dynamicMemory'],
                                                  config_dicts[0]['staticMemory'])
            power2 = get_workload_power_with_dram(config_dicts[1]['dynamicPower'],
                                                  config_dicts[1]['staticPower'],
                                                  x * p2Factor,
                                                  y * 0.01,
                                                  config_dicts[1]['dynamicMemory'],
                                                  config_dicts[1]['staticMemory'])
            energy_diff = results_dict['manufacturingEnergy0'] - results_dict['manufacturingEnergy1']
            power_diff = power2 - power1

            if power_diff != 0:
                    results_dict['chipVsChipBreakevenInDays'][y][x] = \
                        (energy_diff / power_diff) / 3600 / 24
                    if results_dict['chipVsChipBreakevenInDays'][y][x] < 0:
                        results_dict['chipVsChipBreakevenInDays'][y][x] = -42
            else:
                results_dict['chipVsChipBreakevenInDays'][y][x] = -42
        for x in range(101 - y, 101):
            results_dict['chipVsChipBreakevenInDays'][y][x] = float('NaN')
    return results_dict'''


'''def chip_breakeven(config_dicts):
    results_dict = {}

    dict_num = 0
    for config_dict in config_dicts:
        results_dict[''.join(['manufacturingEnergy', str(dict_num)])] = \
            simple_manufacturing(high_process_energies[config_dict['processSize']]['energy'], config_dict['chipArea'],
                                 config_dict['layers'])
        dict_num += 1

    results_dict['chipVsChipBreakevenInDays'] = {}
    for y in range(0, 10):
        results_dict['chipVsChipBreakevenInDays'][y] = {}
        for x in range(0, 11):
            power1 = get_workload_power(config_dicts[0]['dynamicPower'], config_dicts[0]['staticPower'], (x * 0.1), y * 0.1)
            power2 = get_workload_power(config_dicts[1]['dynamicPower'], config_dicts[1]['staticPower'], (x * 0.1), y * 0.1)
            energy_diff = results_dict['manufacturingEnergy0'] - results_dict['manufacturingEnergy1']
            power_diff = power2 - power1
            results_dict['chipVsChipBreakevenInDays'][y][x * (1 - float(y) * 0.1)] = \
                (energy_diff / power_diff) / 3600 / 24

    return results_dict'''


'''def chip_breakeven_file(config_files):
    config_dicts = []

    for file in config_files:
        with open(file, 'r') as f:
            config_dicts.append(json.load(f))

    return chip_breakeven(config_dicts)'''


'''def chip_breakeven__MAN_file(config_files, active_percent, sleep_percent, man_min, man_max):
    config_dicts = []

    for file in config_files:
        with open(file, 'r') as f:
            config_dicts.append(json.load(f))

    return chip_breakeven_MAN(config_dicts, active_percent, sleep_percent, man_min, man_max)


def chip_breakeven_MAN(config_dicts, active_percent, sleep_percent, man_min, man_max):
    results_dict = {}

    dict_num = 0
    for config_dict in config_dicts:
        results_dict[''.join(['manufacturingEnergy', str(dict_num)])] = \
            simple_manufacturing(high_process_energies[config_dict['processSize']]['energy'], config_dict['chipArea'],
                                 config_dict['layers'])
        dict_num += 1

    results_dict['chipVsChipBreakevenInDays'] = {}
    chip1IPC = config_dicts[0]['IPC']
    chip2IPC = config_dicts[1]['IPC']
    p1Factor = 0
    p2Factor = 0
    if chip1IPC < chip2IPC:
        p1Factor = 1
        p2Factor = chip1IPC / chip2IPC
    else:
        p2Factor = 1
        p1Factor = chip2IPC / chip1IPC

    # power1 = get_workload_power_with_dram(config_dicts[0]['dynamicPower'],
    #                                       config_dicts[0]['staticPower'],
    #                                       active_percent * 0.01 * p1Factor,
    #                                       sleep_percent * 0.01,
    #                                       config_dicts[0]['dynamicMemory'],
    #                                       config_dicts[0]['staticMemory'])
    # power2 = get_workload_power_with_dram(config_dicts[1]['dynamicPower'],
    #                                       config_dicts[1]['staticPower'],
    #                                       active_percent * 0.01 * p2Factor,
    #                                       sleep_percent * 0.01,
    #                                       config_dicts[0]['dynamicMemory'],
    #                                       config_dicts[0]['staticMemory'])
    power1 = get_workload_power(config_dicts[0]['dynamicPower'],
                                          config_dicts[0]['staticPower'],
                                          active_percent * 0.01 * p1Factor,
                                          sleep_percent * 0.01)
    power2 = get_workload_power(config_dicts[1]['dynamicPower'],
                                          config_dicts[1]['staticPower'],
                                          active_percent * 0.01 * p2Factor,
                                          sleep_percent * 0.01)
    for y in range(man_min, man_max+1):
        results_dict['chipVsChipBreakevenInDays'][y] = {}
        for x in range(man_min, man_max+1):
            energy_diff = results_dict['manufacturingEnergy0'] * (y * 0.01)\
                - results_dict['manufacturingEnergy1'] * (x * 0.01)
            power_diff = power2 - power1

            if power_diff != 0:
                    results_dict['chipVsChipBreakevenInDays'][y][x] = \
                        (energy_diff / power_diff) / 3600 / 24
                    if results_dict['chipVsChipBreakevenInDays'][y][x] < 0:
                        results_dict['chipVsChipBreakevenInDays'][y][x] = -42
            else:
                results_dict['chipVsChipBreakevenInDays'][y][x] = -42

    return results_dict'''

#print("sleep,active,break even")
#print(single_chip_stats("radix45.json"))
#print(single_chip_stats("test4.json"))
#print(multi_workload(['radix45.json', 'test4.json']))
#res = chip_breakeven(['radix45.json', 'radix28.json'])['chipVsChipBreakevenInDays']
#res = chip_breakeven(['radix45.json', 'radix65.json'])['chipVsChipBreakevenInDays']
#res = chip_breakeven(['radix45.json', 'radix90.json'])['chipVsChipBreakevenInDays']
#res = chip_breakeven(['radix90.json', 'radix65.json'])['chipVsChipBreakevenInDays']
#res = chip_breakeven(['radix65.json', 'radix45.json'])['chipVsChipBreakevenInDays']
#res = chip_breakeven(['radix45_64_512_1.json', 'radix28_64_512_1.json'])['chipVsChipBreakevenInDays']
#res = chip_breakeven(['radix45_32_128_1.json', 'radix28_32_128_1.json'])['chipVsChipBreakevenInDays']
#res = chip_breakeven(['radix45_32_256_4.json', 'radix28_32_256_4.json'])['chipVsChipBreakevenInDays']
#res = chip_breakeven_IPC(['bzip_plus_28_4core_4.json', 'bzip_plus_28_4core_1.json'])['chipVsChipBreakevenInDays']
#res = chip_breakeven_IPC(['vips_28_4core_2.json', 'vips_28_4core_1.json'])['chipVsChipBreakevenInDays']
#res = chip_breakeven_IPC(['canneal_28_4core_half.json', 'canneal_28_4core_eigth.json'])['chipVsChipBreakevenInDays']

# res = chip_breakeven__MAN_file(['canneal_28_4core_half.json', 'canneal_28_4core_eigth.json'], 100, 50, 10, 100)['chipVsChipBreakevenInDays']

# # res = chip_breakeven_IPC(['freqmine_45_4core_4.json', 'freqmine_28_4core_4.json'])['chipVsChipBreakevenInDays']
# res_keys = sorted(res.keys())
# for x in range(10, 100):
#     print(',{0}'.format(x * .01), end='')
# print()
# for key in res_keys:
#     innerres = res[key]
#     inner_keys = sorted(innerres.keys())
#     print(key * .01, end="")
#     for inner_key in inner_keys:
#         print(',{0}'.format(innerres[inner_key]), end="")
#     print()
