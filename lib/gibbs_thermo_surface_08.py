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

import json
import numpy as np
from gibbs_surf import potential_G
from scipy import constants
import sys


def print_internal(data, name):
    """
    Print internal thermodynamic properties for solid and liquid phases.

    Parameters:
    data (str): Path to the data file containing melting pressure and temperature.
    name (str): Name of the material, used to load the corresponding JSON file.
    """

    try:
        with open(data, 'r') as file:
            lines = file.readlines()

        # Extract the melting pressure and temperature
        temp_pressure_line = lines[1].strip().split()
        pressure_melting = float(temp_pressure_line[0])
        temp_melting = float(temp_pressure_line[1])  # Convert to K

        properties = ['G', 'A', 'H', 'U', 'S', 'V']
        units = ['1.0e-19 J/atom', '1.0e-19 J/atom', '1.0e-19 J/atom',
                 '1.0e-19 J/atom', r'1.0e-22 J/K/atom', '1.0e-29 m**3/atom']

        print(f"melting_pressure {'=':>4} {pressure_melting:.3f} GPa")
        print(f"melting_temperature {'=':>1} {temp_melting * 1.0e+3:.1f} K")
        # print(f"##{properties[0]}:{units[0]}, {properties[1]}:{units[1]}, {properties[2]}:{units[2]}##\n"
        #       f"##{properties[3]}:{units[3]}, {properties[4]}:{units[4]}, {properties[5]}:{units[5]}##")
        print(f"{'####':^6} {'#solid#':^9}{'#liquid#':^10}{'#units#':^16}")

        # start to print thermodynamic potential
        with open('%s' % str(name) + '.json', 'r') as jsonfile:
            material = json.load(jsonfile)
        [V, S, p, T, U, A, H, G] = potential_G(temp_melting, pressure_melting * 1.0e-1, np.array(material['solid']['abc']),
                                               np.array(material['solid']['eos']))
        G_sol = G
        A_sol = A
        H_sol = H
        U_sol = U
        S_sol = S
        V_sol = V

        [V, S, p, T, U, A, H, G] = potential_G(temp_melting, pressure_melting * 1.0e-1, np.array(material['liquid']['abc']),
                                               np.array(material['liquid']['eos']))
        G_liq = G
        A_liq = A
        H_liq = H
        U_liq = U
        S_liq = S
        V_liq = V

        print(f"{properties[0]:^5}{G_sol:>9.3f}{G_liq:>10.3f}{units[0]:^20}")
        print(f"{properties[1]:^5}{A_sol:>9.3f}{A_liq:>10.3f}{units[1]:^20}")
        print(f"{properties[2]:^5}{H_sol:>9.3f}{H_liq:>10.3f}{units[2]:^20}")
        print(f"{properties[3]:^5}{U_sol:>9.3f}{U_liq:>10.3f}{units[3]:^20}")
        print(f"{properties[4]:^5}{S_sol:>9.3f}{S_liq:>10.3f}{units[4]:^20}")
        print(f"{properties[5]:^5}{V_sol:>9.3f}{V_liq:>10.3f}{units[5]:^20}")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)


# convert units to VASP standard
def print_vasp_type(data, name):
    """
    Print thermodynamic properties in VASP units for solid and liquid phases.

    Parameters:
    data (str): Path to the data file containing melting pressure and temperature.
    name (str): Name of the material, used to load the corresponding JSON file.
    """

    eV = constants.e

    try:
        with open(data, 'r') as file:
            lines = file.readlines()

        # Extract the melting pressure and temperature
        temp_pressure_line = lines[1].strip().split()
        pressure_melting = float(temp_pressure_line[0])
        temp_melting = float(temp_pressure_line[1])

        properties = ['G', 'A', 'H', 'U', 'S', 'V']
        units = ['eV/atom', 'eV/atom', 'eV/atom',
                 'eV/atom', 'eV/K/atom', 'A**3/atom']

        print(f"melting_pressure {'=':>4} {pressure_melting:.3f} GPa")
        print(f"melting_temperature {'=':>1} {temp_melting * 1.0e+3:.1f} K")
        # print(f"##{properties[0]}:{units[0]}, {properties[1]}:{units[1]}, {properties[2]}:{units[2]}##\n"
        #       f"##{properties[3]}:{units[3]}, {properties[4]}:{units[4]}, {properties[5]}:{units[5]}##")
        print(f"{'####':^6} {'#solid#':^9}{'#liquid#':^10}{'#units#':^16}")

        # start to print thermodynamic potential
        with open('%s' % str(name) + '.json', 'r') as jsonfile:
            material = json.load(jsonfile)
        [V, S, p, T, U, A, H, G] = potential_G(temp_melting, pressure_melting * 1.0e-1, np.array(material['solid']['abc']),
                                               np.array(material['solid']['eos']))
        G_sol = float(G) / (eV * 1.0e+19)
        A_sol = float(A) / (eV * 1.0e+19)
        H_sol = float(H) / (eV * 1.0e+19)
        U_sol = float(U) / (eV * 1.0e+19)
        S_sol = float(S) * 1.0e-3 / (eV * 1.0e+19)
        V_sol = float(V) * 1.0e+1

        [V, S, p, T, U, A, H, G] = potential_G(temp_melting, pressure_melting * 1.0e-1, np.array(material['liquid']['abc']),
                                               np.array(material['liquid']['eos']))
        G_liq = float(G) / (eV * 1.0e+19)
        A_liq = float(A) / (eV * 1.0e+19)
        H_liq = float(H) / (eV * 1.0e+19)
        U_liq = float(U) / (eV * 1.0e+19)
        S_liq = float(S) * 1.0e-3 / (eV * 1.0e+19)
        V_liq = float(V) * 1.0e+1

        # Print the properties
        print(f"{properties[0]:^5}{G_sol:>9.3f}{G_liq:>10.3f}{units[0]:^20}")
        print(f"{properties[1]:^5}{A_sol:>9.3f}{A_liq:>10.3f}{units[1]:^20}")
        print(f"{properties[2]:^5}{H_sol:>9.3f}{H_liq:>10.3f}{units[2]:^20}")
        print(f"{properties[3]:^5}{U_sol:>9.3f}{U_liq:>10.3f}{units[3]:^20}")
        print(f"{properties[4]:^5}{S_sol:>9.6f}{S_liq:>10.6f}{units[4]:^20}")
        print(f"{properties[5]:^5}{V_sol:>9.3f}{V_liq:>10.3f}{units[5]:^20}")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
