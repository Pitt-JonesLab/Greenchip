__author__ = 'dek61'


def dramsim_dict_loader(file_path):
    av_power = 0.0
    background_power = 0.0
    refresh_power = 0.0

    with open(file_path, 'r') as f:
        for line in f:
            line=line.strip()
            if line.startswith("Average Power (watts)"):
                x=line.split(":")
                x[1]=x[1].strip()
                av_power=float(x[1])
            elif line.startswith("-Background (watts)"):
                x=line.split(":")
                x[1]=x[1].strip()
                background_power=float(x[1])
            elif line.startswith("-Refresh"):
                x = line.split(":")
                x[1] = x[1].strip()
                refresh_power = float(x[1])
    static_power=refresh_power+background_power
    dynamic_power=av_power-static_power
    my_dict={'static_memory': static_power, 'dynamic_memory': dynamic_power}
    return my_dict
