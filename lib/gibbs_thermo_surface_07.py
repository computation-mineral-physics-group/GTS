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

# find intersection of G-T curves at constant P

import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from scipy import constants
from gibbs_surf import potential_G
import json
import sys

eV = constants.eV


def get_cross_point(level_str, cp, x_label, y_label, y_label_vasp, n):
    """
    Find the intersection point of Gibbs free energy curves for solid and liquid phases.

    Parameters:
    level_str (str): The pressure level as a string.
    cp (file object): The file object to write the melting point.
    x_label (str): Label for the x-axis of the plot.
    y_label (str): Label for the y-axis of the plot.
    n (str): The filename prefix for the plot.

    Returns:
    float: The melting temperature.
    """
    try:
        dat_solid = np.genfromtxt(f'solid_pressure_{level_str}.txt')
        dat_liquid = np.genfromtxt(f'liquid_pressure_{level_str}.txt')
        order = 3

        # Solid phase data
        x_solid = dat_solid[:, 0]
        y_solid = dat_solid[:, 1]
        Ga = np.polyfit(x_solid, y_solid, order)
        plt.clf()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.plot(x_solid, y_solid, 'r+', label='Solid phase')

        # Liquid phase data
        x_liquid = dat_liquid[:, 0]
        y_liquid = dat_liquid[:, 1]
        Gb = np.polyfit(x_liquid, y_liquid, order)
        plt.plot(x_liquid, y_liquid, 'gx', label='Liquid phase')

        # Look for intersection
        lower_bound = max(min(x_solid), min(x_liquid))
        upper_bound = min(max(x_solid), max(x_liquid))
        xs = np.linspace(lower_bound, upper_bound, 100)
        ys_solid = np.polyval(Ga, xs)
        ys_liquid = np.polyval(Gb, xs)
        guess = 0.5 * (lower_bound + upper_bound)
        f = np.poly1d(Ga - Gb)
        root = fsolve(f, guess)
        temperature = root[0]
        gibbsenergy = 0.5 * (np.polyval(Ga, temperature) + np.polyval(Gb, temperature))
        cp.write(f"{level_str} {temperature:.3f}\n")

        plt.plot(temperature, gibbsenergy, 'bo', label='Melting point', zorder=5)
        plt.plot(xs, ys_solid, 'r-', label='Solid fit')
        plt.plot(xs, ys_liquid, 'g-', label='Liquid fit')
        plt.tick_params(axis='both', which='both', direction='in', top=True, right=True)
        plt.minorticks_on()
        plt.legend(frameon=False)
        plt.savefig(f'{n}_pressure_{level_str}_internal.pdf', format='pdf')  # save image with internal units

        # convert units from internal to vasp type
        y_solid_ev = y_solid / (eV * 1.0e+19)
        y_liquid_ev = y_liquid / (eV * 1.0e+19)
        ys_solid_ev = ys_solid / (eV * 1.0e+19)
        ys_liquid_ev = ys_liquid / (eV * 1.0e+19)
        gibbsenergy_ev = gibbsenergy / (eV * 1.0e+19)

        plt.clf()
        plt.xlabel(x_label)
        plt.ylabel(y_label_vasp)
        plt.plot(x_solid, y_solid_ev, 'r+', label='Solid phase')
        plt.plot(x_liquid, y_liquid_ev, 'gx', label='Liquid phase')
        plt.plot(temperature, gibbsenergy_ev, 'bo', label='Melting point', zorder=5)
        plt.plot(xs, ys_solid_ev, 'r-', label='Solid fit')
        plt.plot(xs, ys_liquid_ev, 'g-', label='Liquid fit')
        plt.tick_params(axis='both', which='both', direction='in', top=True, right=True)
        plt.minorticks_on()
        plt.legend(frameon=False)
        plt.savefig(f'{n}_pressure_{level_str}_vasp.pdf', format='pdf')

        return temperature
    except Exception as e:
        print(f"An error occurred while finding the cross point: {e}", file=sys.stderr)
        return None


def get_melting_data(p, n):
    """
    Generate and save melting data for given pressure.

    Parameters:
    p (float): The pressure level.
    n (str): The filename prefix for the input JSON file.
    """
    try:
        level = float(p) * 1.0e-1  # GPa ==> Pa*1e+10
        level_str_c = f"{float(p):.3f}"
        x_label = r'Temperature ($\times 10^{3}$ K)'
        y_label = r'Gibbs free energy ($\times 10^{-19}$ J/atom)'
        y_label_vasp = r'Gibbs free energy (eV/atom)'

        with open(f'cross_point_{level_str_c}.txt', 'w') as cp:
            cp.write("# P(* GPa), T(*1e+3 K)\n")
            get_cross_point(level_str_c, cp, x_label, y_label, y_label_vasp, n)
    except Exception as e:
        print(f"An error occurred while getting the melting data: {e}", file=sys.stderr)

