"""
  GTS -- Gibbs Thermodynamic Surface: an automated toolkit to obtain high-pressure melting data

  Copyright (C) 2024-2025 by Kun Yin and Xuan Zhao

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
import matplotlib.pyplot as plt
import sys



def get_range(name):
    data_melting_points = np.genfromtxt(f'cross_point_{name}.txt')
    pressure_range = data_melting_points[:, 0] * 1.0e-1 # GPa => 1e+10 Pa
    temperature_range = data_melting_points[:, 1] # 1e+3 K
    return pressure_range, temperature_range

def a_fit_V_S(ax, name):
    # Get pressure and temperature of melting points
    pressure_range = get_range(name)[0]
    temperature_range = get_range(name)[1]

    # Arrays for volumes and entropies at solid and liquid melting points
    volume_solid_range = np.empty(len(pressure_range))
    volume_liquid_range = np.empty(len(pressure_range))
    entropy_solid_range = np.empty(len(pressure_range))
    entropy_liquid_range = np.empty(len(pressure_range))

    # Get volume and entropy for each melting points
    for i in range(len(pressure_range)):
        temperature_i = temperature_range[i]
        pressure_i = pressure_range[i]
        with open('%s' % str(name) + '.json', 'r') as jsonfile:
            material = json.load(jsonfile)

        [V1, S1, p, T, U, A, H, G] = potential_G(temperature_i, pressure_i, np.array(material['solid']['abc']),
                                               np.array(material['solid']['eos']))

        [V2, S2, p, T, U, A, H, G] = potential_G(temperature_i, pressure_i, np.array(material['liquid']['abc']),
                                               np.array(material['liquid']['eos']))

        volume_solid_range[i] = round(V1, 4)
        entropy_solid_range[i] = round(S1, 4)
        volume_liquid_range[i] = round(V2, 4)
        entropy_liquid_range[i] = round(S2, 4)

        # Plot coexistence lines between solid and liquid states
        ax.plot([V1 * 10, V2 * 10], [S1, S2], '--', color='black', zorder=9)

    # Fit the curve for solid phase and liquid phase
    coefficient_solid = np.polyfit(volume_solid_range * 10, entropy_solid_range, 2)
    coefficient_liquid = np.polyfit(volume_liquid_range * 10, entropy_liquid_range, 2)

    # The boundary of the plot
    lower_boundary_solid = min(volume_solid_range * 10) * (1 - 0.05)
    upper_boundary_solid = max(volume_solid_range * 10) * (1 + 0.05)

    lower_boundary_liquid = min(volume_liquid_range * 10) * (1 - 0.05)
    upper_boundary_liquid = max(volume_liquid_range * 10) * (1 + 0.05)

    # The value of curve for solid phase and liquid phase
    volume_solid_curve = np.linspace(lower_boundary_solid, upper_boundary_solid, 50)
    volume_liquid_curve = np.linspace(lower_boundary_liquid, upper_boundary_liquid, 50)

    entropy_solid_curve = np.polyval(coefficient_solid, volume_solid_curve)
    entropy_liquid_curve = np.polyval(coefficient_liquid, volume_liquid_curve)

    # plot the curve for solid phase and liquid phase
    ax.plot(volume_solid_curve, entropy_solid_curve, 'r-')
    ax.plot(volume_liquid_curve, entropy_liquid_curve, 'g-')

    left_solid_point = (volume_solid_curve[0], entropy_solid_curve[0])
    left_liquid_point = (volume_liquid_curve[0], entropy_liquid_curve[0])

    right_solid_point = (volume_solid_curve[-1], entropy_solid_curve[-1])
    right_liquid_point = (volume_liquid_curve[-1], entropy_liquid_curve[-1])

    # Create a complete closed path for shaded coexistence area
    volume_path = np.concatenate([
        volume_solid_curve,
        [right_liquid_point[0]],
        volume_liquid_curve[::-1],
        [left_solid_point[0]]
    ])

    entropy_path = np.concatenate([
        entropy_solid_curve,
        [right_liquid_point[1]],
        entropy_liquid_curve[::-1],
        [left_solid_point[1]]
    ])

    ax.fill(volume_path, entropy_path, color='#89B8F6', edgecolor='none', alpha=0.8)

    # Plot melting points on each state(solid and liquid)
    ax.scatter(volume_solid_range * 10, entropy_solid_range, marker='s', s=30,edgecolor='black', facecolor='red', zorder=10)
    ax.scatter(volume_liquid_range * 10, entropy_liquid_range, marker='^', s=40,edgecolor='black', facecolor='green', zorder=10)

    # Settings for plot
    ax.set_xlabel(r'Volume ($\mathrm{\AA}^3$/atom)')
    ax.set_ylabel(r'Entropy ($\times 10^{-22}$ J/(K$\cdot$atom))')
    ax.set_title('Volume-Entropy diagram', fontsize=10)

    y_min = min(min(entropy_solid_curve), min(entropy_liquid_curve))
    y_max = max(max(entropy_solid_curve), max(entropy_liquid_curve))
    padding = 0.3 * (y_max - y_min)
    ax.set_ylim(y_min - padding, y_max + padding)

    ax.text(-0.18, 1.0, '(a)', fontsize=15, color='black', zorder=5,
            horizontalalignment='left', verticalalignment='top', transform=ax.transAxes
            )
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
    ax.minorticks_on()
    # ax.legend(frameon=False, loc='best', fontsize='10')

def b_fit_p_S(ax, name):
    # Get pressure and temperature of melting points
    pressure_range = np.array(get_range(name)[0])
    temperature_range = np.array(get_range(name)[1])

    # Arrays for volumes and entropies at solid and liquid melting points
    volume_solid_range = np.empty(len(pressure_range))
    volume_liquid_range = np.empty(len(pressure_range))
    entropy_solid_range = np.empty(len(pressure_range))
    entropy_liquid_range = np.empty(len(pressure_range))

    # Get volume and entropy for each melting points
    for i in range(len(pressure_range)):
        temperature_i = temperature_range[i]
        pressure_i = pressure_range[i]
        with open('%s' % str(name) + '.json', 'r') as jsonfile:
            material = json.load(jsonfile)

        [V1, S1, p, T, U, A, H, G] = potential_G(temperature_i, pressure_i, np.array(material['solid']['abc']),
                                               np.array(material['solid']['eos']))

        [V2, S2, p, T, U, A, H, G] = potential_G(temperature_i, pressure_i, np.array(material['liquid']['abc']),
                                               np.array(material['liquid']['eos']))

        volume_solid_range[i] = round(V1, 4)
        entropy_solid_range[i] = round(S1, 4)
        volume_liquid_range[i] = round(V2, 4)
        entropy_liquid_range[i] = round(S2, 4)


        # Plot the coexistence line of solid phase and liquid phase
        ax.plot([pressure_i * 10, pressure_i * 10], [S1, S2], '--', color='black', zorder=9)

    # Ffit the curve for solid phase and liquid phase
    coefficient_solid = np.polyfit(pressure_range * 10, entropy_solid_range, 2)
    coefficient_liquid = np.polyfit(pressure_range * 10, entropy_liquid_range, 2)

    # The boundary of the plot
    lower_boundary_solid = min(pressure_range * 10) * (1 - 0.1)
    upper_boundary_solid = max(pressure_range * 10) * (1 + 0.1)

    lower_boundary_liquid = min(pressure_range * 10) * (1 - 0.1)
    upper_boundary_liquid = max(pressure_range * 10) * (1 + 0.1)

    # The value of curve for solid phase and liquid phase
    pressure_solid_curve = np.linspace(lower_boundary_solid, upper_boundary_solid, 50)
    pressure_liquid_curve = np.linspace(lower_boundary_liquid, upper_boundary_liquid, 50)

    entropy_solid_curve = np.polyval(coefficient_solid, pressure_solid_curve)
    entropy_liquid_curve = np.polyval(coefficient_liquid, pressure_liquid_curve)

    # Plot the curve for solid phase and liquid phase
    ax.plot(pressure_solid_curve, entropy_solid_curve, 'r-')
    ax.plot(pressure_liquid_curve, entropy_liquid_curve, 'g-')

    # Plot the shaded coexistence area
    pressure_common = np.linspace(
        max(lower_boundary_solid, lower_boundary_liquid),
        min(upper_boundary_solid, upper_boundary_liquid),
        200
    )
    entropy_solid_common = np.polyval(coefficient_solid, pressure_common)
    entropy_liquid_common = np.polyval(coefficient_liquid, pressure_common)
    ax.fill_between(pressure_common, entropy_solid_common, entropy_liquid_common,
                    where=entropy_liquid_common > entropy_solid_common,
                    interpolate=True, color='#89B8F6', edgecolor='none', alpha=0.8)

    # Plot melting points on each state(solid and liquid)
    ax.scatter(pressure_range * 10, entropy_solid_range, marker='s', s=30, edgecolor='black', facecolor='red', zorder=10)
    ax.scatter(pressure_range * 10, entropy_liquid_range, marker='^', s=40, edgecolor='black', facecolor='green', zorder=10)

    # Settings for plot
    ax.set_xlabel(r'Pressure (GPa)')
    ax.set_ylabel(r'Entropy ($\times 10^{-22}$ J/(K$\cdot$atom))')
    ax.set_title('Pressure-Entropy diagram', fontsize=10)

    y_min = min(min(entropy_solid_curve), min(entropy_liquid_curve))
    y_max = max(max(entropy_solid_curve), max(entropy_liquid_curve))
    padding = 0.3 * (y_max - y_min)
    ax.set_ylim(y_min - padding, y_max + padding)

    ax.text(-0.18, 1.0, '(b)', fontsize=15, color='black', zorder=5,
            horizontalalignment='left', verticalalignment='top', transform=ax.transAxes
            )
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
    ax.minorticks_on()
    # ax.legend(frameon=False, loc='best', fontsize=10)


def c_fit_V_T(ax, name):
    # Get pressure and temperature of melting points
    pressure_range = np.array(get_range(name)[0])
    temperature_range = np.array(get_range(name)[1])

    # Arrays for volumes and entropies at solid and liquid melting points
    volume_solid_range = np.empty(len(pressure_range))
    volume_liquid_range = np.empty(len(pressure_range))
    entropy_solid_range = np.empty(len(pressure_range))
    entropy_liquid_range = np.empty(len(pressure_range))

    # Get volume and entropy for each melting points
    for i in range(len(pressure_range)):
        temperature_i = temperature_range[i]
        pressure_i = pressure_range[i]
        with open('%s' % str(name) + '.json', 'r') as jsonfile:
            material = json.load(jsonfile)

        [V1, S1, p, T, U, A, H, G] = potential_G(temperature_i, pressure_i, np.array(material['solid']['abc']),
                                               np.array(material['solid']['eos']))

        [V2, S2, p, T, U, A, H, G] = potential_G(temperature_i, pressure_i, np.array(material['liquid']['abc']),
                                               np.array(material['liquid']['eos']))
        volume_solid_range[i] = V1
        entropy_solid_range[i] = S1
        volume_liquid_range[i] = V2
        entropy_liquid_range[i] = S2

        # Plot the coexistence line of solid phase and liquid phase
        ax.plot([V1 * 10, V2 * 10], [temperature_i * 1000, temperature_i * 1000], '--', color='black', zorder=9)

    # Fit the curve for solid phase and liquid phase
    coefficient_solid = np.polyfit(volume_solid_range * 10, temperature_range * 1000, 2)
    coefficient_liquid = np.polyfit(volume_liquid_range * 10, temperature_range * 1000, 2)

    # The boundary of the plot
    lower_boundary_solid = min(volume_solid_range * 10) * (1 - 0.05)
    upper_boundary_solid = max(volume_solid_range * 10) * (1 + 0.05)

    lower_boundary_liquid = min(volume_liquid_range * 10) * (1 - 0.05)
    upper_boundary_liquid = max(volume_liquid_range * 10) * (1 + 0.05)

    # The value of curve for solid phase and liquid phase
    volume_solid_curve = np.linspace(lower_boundary_solid, upper_boundary_solid, 50)
    volume_liquid_curve = np.linspace(lower_boundary_liquid, upper_boundary_liquid, 50)

    temperature_solid_curve = np.polyval(coefficient_solid, volume_solid_curve)
    temperature_liquid_curve = np.polyval(coefficient_liquid, volume_liquid_curve)

    # Plot the curve for solid phase and liquid phase
    ax.plot(volume_solid_curve, temperature_solid_curve, 'r-', label='Solid phase boundary')
    ax.plot(volume_liquid_curve, temperature_liquid_curve, 'g-', label='Liquid phase boundary')

    # Create a complete closed path for shaded coexistence area
    left_solid_point = (volume_solid_curve[0], temperature_solid_curve[0])
    left_liquid_point = (volume_liquid_curve[0], temperature_liquid_curve[0])

    right_solid_point = (volume_solid_curve[-1], temperature_solid_curve[-1])
    right_liquid_point = (volume_liquid_curve[-1], temperature_liquid_curve[-1])

    volume_path = np.concatenate([
        volume_solid_curve,
        [right_liquid_point[0]],
        volume_liquid_curve[::-1],
        [left_solid_point[0]]
    ])

    entropy_path = np.concatenate([
        temperature_solid_curve,
        [right_liquid_point[1]],
        temperature_liquid_curve[::-1],
        [left_solid_point[1]]
    ])

    ax.fill(volume_path, entropy_path, color='#89B8F6', edgecolor='none', alpha=0.8, label='Two-phase coexistence region')

    # Plot melting points on each state(solid and liquid)
    ax.scatter(volume_solid_range * 10, temperature_range * 1000, marker='s', s=30, edgecolor='black', facecolor='red',
               zorder=10, label='Melting point (solid phase end)')
    ax.scatter(volume_liquid_range * 10, temperature_range * 1000, marker='^', s=40, edgecolor='black',
               facecolor='green', zorder=10, label='Melting point (liquid phase end)')

    # Settings for plot
    ax.set_xlabel(r'Volume ($\mathrm{\AA}^3$/atom)')
    ax.set_ylabel(r'Temperature (K)')
    ax.set_title('Volume-Temperature diagram', fontsize=10)
    ax.text(-0.18, 1.0, '(c)', fontsize=15, color='black', zorder=5,
            horizontalalignment='left', verticalalignment='top', transform=ax.transAxes
            )
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
    ax.minorticks_on()
    ax.legend(frameon=False, loc='best', fontsize=9)



def d_fit_p_T(ax, name):
    # Get pressure and temperature of melting points
    pressure_range = np.array(get_range(name)[0])
    temperature_range = np.array(get_range(name)[1])

    # Fit the melting curve with a third order polynomial
    coefficient_melting_curve = np.polyfit(pressure_range * 10, temperature_range * 1000, 2)

    # The boundary of the plot
    lower_boundary_pressure = min(pressure_range * 10) * (1 - 0.08)
    upper_boundary_pressure = max(pressure_range * 10) * (1 + 0.08)

    # The value of curve for solid phase and liquid phase
    pressure_melting_curve = np.linspace(lower_boundary_pressure, upper_boundary_pressure, 50)
    temperature_melting_curve = np.polyval(coefficient_melting_curve, pressure_melting_curve)

    # Plot the curve for solid phase and liquid phase
    ax.plot(pressure_melting_curve, temperature_melting_curve, '--', color='black', label='Melting curve')

    # Plot melting points on each state(solid and liquid)
    ax.scatter(pressure_range * 10, temperature_range * 1000, marker='o', edgecolor='black', facecolor='#89B8F6', zorder=10, label='Melting point')

    # Settings for plot
    ax.set_xlabel(r'Pressure (GPa)')
    ax.set_ylabel(r'Temperature (K)')
    ax.set_title('Pressure-Temperature diagram', fontsize=10)
    ax.set_xlim(min(pressure_melting_curve), max(pressure_melting_curve))
    ax.text(-0.18, 1.0, '(d)', fontsize=15, color='black', zorder=5,
            horizontalalignment='left', verticalalignment='top', transform=ax.transAxes
            )
    ax.text(0.7, 0.2, f'{name}', fontsize=15, color='black', zorder=5,
            horizontalalignment='left', verticalalignment='top', transform=ax.transAxes
            )
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
    ax.minorticks_on()
    ax.legend(frameon=False, loc='best')


def plot_for_pressure_range(name,lowerlimit, upperlimit):

    try:
        fig, axs = plt.subplots(2, 2, figsize=(12, 9))

        a_fit_V_S(axs[0, 0], name)
        b_fit_p_S(axs[0, 1], name)
        c_fit_V_T(axs[1, 0], name)
        d_fit_p_T(axs[1, 1], name)

        plt.savefig(f'{name}_{lowerlimit}_{upperlimit}_melting_data.pdf', format='pdf', dpi=300, bbox_inches='tight')

    except Exception as e:
        print(f"An error occurred while generating the plot: {e}", file=sys.stderr)


