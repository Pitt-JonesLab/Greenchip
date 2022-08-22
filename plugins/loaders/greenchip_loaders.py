import os.path


def greenchip_dict_loader(file_path):
    state_list = []
    if not os.path.isfile(file_path):
        return None
    with open(file_path, 'r') as f:
        state_list = f.readlines()
    for i in range(len(state_list)):
        state_list[i] = state_list[i].split("//")[0].strip()
    return state_list
