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

# get isovalue lines of Gibbs free energy from contour plot
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
import json
import sys


def generate_TGP(phase_type, dictionary):
    """
    Generate temperature, Gibbs free energy, and pressure data for a given phase.

    Parameters:
    phase_type (str): The phase type ('solid' or 'liquid').
    dictionary (dict): The dictionary containing data.

    Returns:
    tuple: Meshgrid arrays for temperature, Gibbs free energy, and interpolated pressure data.
    """
    # Input data
    grid_dat = dictionary[phase_type]['dat']
    dat = np.array(grid_dat)

    # Solid phase or Liquid phase
    X = dat[:, 3]  # Temperature
    Y = dat[:, 7]  # Gibbs free energy
    Z = dat[:, 2]  # Pressure

    # Interpolating data
    xi = np.linspace(X.min(), X.max(), 100)
    yi = np.linspace(Y.min(), Y.max(), 100)
    zi = griddata((X, Y), Z, (xi[None, :], yi[:, None]), method='cubic')
    xig, yig = np.meshgrid(xi, yi)

    return xig, yig, zi


def save_contour_lines(phase, level, dictionary):
    """
    Save contour lines for a given phase at a specified pressure level to a file.

    Parameters:
    phase (str): The phase type ('solid' or 'liquid').
    level (float): The pressure level to generate contour lines for.
    dictionary (dict): The dictionary containing data.
    """
    try:
        xig, yig, zi = generate_TGP(phase, dictionary)
        cset = plt.contour(xig, yig, zi, [level])
        level_value_str = f"{level * 10 :.3f}"
        file_name = f"{phase}_pressure_{level_value_str}.txt"

        path = cset.collections[0].get_paths()[0]
        vert = path.vertices

        with open(file_name, 'w') as f:
            for j in range(vert.shape[0]):
                # f.write(f"{vert[j, 0]:.6f} {vert[j, 1]:.6f}\n")
                f.write(f"{vert[j, 0]} {vert[j, 1]}\n")
    except Exception as e:
        print(f"An error occurred while saving contour lines for {phase}: {e}", file=sys.stderr)


def contour_line(p, n):
    """
    Generate and save contour lines of Gibbs free energy for both solid and liquid phases.

    Parameters:
    p (float): The pressure level.
    n (str): The filename prefix for the input JSON file.
    """
    try:
        with open(f'{n}.json', 'r') as t:
            dictionary = json.load(t)

        # Specify isovalue level of pressure
        level = float(p) * 1.0e-1  # GPa ==> Pa*1e+10

        # Save contour lines for both phases
        save_contour_lines('solid', level, dictionary)
        save_contour_lines('liquid', level, dictionary)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

