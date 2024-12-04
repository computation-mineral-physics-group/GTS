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
from gibbs_surf import *
import sys


def generate_derived_surface(phase='solid', nV='nV', nT='nT'):
    """
    Generate derived surface data for a given phase.

    Parameters:
    phase (str): The phase for which to generate the surface data ('solid' or 'liquid').
    nV (str): Number of volume data points.
    nT (str): Number of temperature data points.
    """

    try:
        # Load data files
        dat_abc = np.genfromtxt(f'{phase}_dat_abc.txt')
        dat_eos = np.genfromtxt(f'{phase}_dat_eos.txt')
        data = np.genfromtxt(f'{phase}_input.txt')

        # Extract temperature data and compute min and max values
        temperatures = data[:, 3]
        T_max = np.max(temperatures) * 1e-3
        T_min = np.min(temperatures) * 1e-3

        # Extract volume data and compute min and max values
        volumes = dat_abc[:, 0]
        V_min = min(volumes)
        V_max = max(volumes)

        # Open output file
        with open(f'data_{phase}.txt', 'w') as f:
            # Generate volume and temperature data points
            V_data = np.linspace(V_min, V_max, int(nV))
            T_data = np.linspace(float(T_min), float(T_max), int(nT))

            # Calculate properties for each combination of V and T
            for V in V_data:
                for T in T_data:
                    V, S, P, T, E, A, H, G = potential_A(T, V, dat_abc, dat_eos)
                    f.write(f"{V:10.6f} {S:10.6f} {P:10.6f} {T:10.6f} {E:10.6f} {A:10.6f} {H:10.6f} {G:10.6f}\n")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
