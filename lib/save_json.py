import json
import numpy as np


def two_phase(phase):
    p = str(phase)
    # phase_dict = {p: {}}
    phase_dict = {}
    with open('%s' % p + '_dat_abc.txt', 'r') as f1:
        abc_lines = f1.readlines()

    abc_list = []
    for line in abc_lines:
        dat1 = [float(value) for value in line.split()]
        abc_list.append(dat1)

    with open('%s' % p + '_dat_eos.txt', 'r') as f2:
        eos_lines = f2.readlines()

    eos_list = []
    for line in eos_lines:
        dat2 = [float(value) for value in line.split()]
        eos_list.append(dat2)

    with open('data_' + '%s' % p + '.txt', 'r') as f3:
        s_eos_lines = f3.readlines()

    dat_list = []
    for line in s_eos_lines:
        dat3 = [float(value) for value in line.split()]
        dat_list.append(dat3)

    phase_dict["abc"] = abc_list
    phase_dict['eos'] = eos_list
    phase_dict['dat'] = dat_list
    return phase_dict


def save_json(substance_name, phase1, phase2):
    name = str(substance_name)
    dat = {phase1: two_phase(phase1), phase2: two_phase(phase2)}
    with open('%s' % name + '.json', 'w') as json_file:
        json.dump(dat, json_file)
