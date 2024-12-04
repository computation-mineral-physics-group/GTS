"""
  GTS -- Gibbs Thermodynamic Surface: an automated toolkit to obtain high-pressure melting data

  Copyright (C) 2024-2024 by Kun Yin and Xuan Zhao

  This program is free software; you can redistribute it and/or modify it under the
  terms of the GNU General Public License as published by the Free Software Foundation
  version 3 of the License.

  This program is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
  PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  E-mail: yinkun@cdut.edu.cn
"""

import numpy as np
from scipy import constants

# Constants for unit conversion
kBar_tO_internal_p = 1e-2  # kBar ==> 1e+10 Pa
eV_tO_internal_U = constants.e * 1e+19  # eV/atom ==> 1e-19 J/atom
K_tO_internal_T = 1e-3  # K ==> 1.0e+3 K
volume_to_internal_V = 1e-1  # A^3/atom ==> 1e-29 m^3/atom
precision = 6  # Number of decimal places to retain


def read_data(input_file):
    """Read data from the input file."""
    dat = np.genfromtxt(input_file)
    return dat


def write_mid_temperature(dat):
    """Calculate and write the middle temperature to mid_T.txt."""
    mid_T = np.mean(dat[:, 3]) * K_tO_internal_T

    with open('mid_T.txt', 'w') as middle_T:
        middle_T.write(f"{mid_T:.{precision}f}\n")


def write_volumes(unique_volumes):
    """Write unique volumes to V.txt."""

    with open('V.txt', 'w') as all_volume:
        all_volume.write("# V(*1e-29 m^3/atom)\n")
        for v in unique_volumes:
            all_volume.write(f"{v * volume_to_internal_V:.{precision}f}\n")


def write_single_volumes(dat, unique_volumes):
    """Write pressure, energy, and temperature for each unique volume."""
    for j, v in enumerate(unique_volumes, start=1):

        with open(f'V{j}.txt', 'w') as single_volume:
            single_volume.write("# T(*1e+3 K), U(*1e-19 J/atom), p(*1e+10 Pa)\n")
            for i in range(dat.shape[0]):
                if v == dat[i, 0]:
                    this_pressure = dat[i, 1] * kBar_tO_internal_p
                    this_energy = dat[i, 2] * eV_tO_internal_U
                    this_temperature = dat[i, 3] * K_tO_internal_T
                    single_volume.write(
                        f"{this_temperature:.{precision}f} "
                        f"{this_energy:.{precision}f} "
                        f"{this_pressure:.{precision}f}\n")


def surface_01():
    """Read input files of two phase and convert units."""
    input_file = 'input.txt'
    dat = read_data(input_file)

    write_mid_temperature(dat)

    unique_volumes = np.unique(dat[:, 0])[::-1]
    write_volumes(unique_volumes)
    write_single_volumes(dat, unique_volumes)
