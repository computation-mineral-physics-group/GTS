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
from gibbs_surf import potential_G
from scipy import constants

N_A = constants.N_A


def entropy_calibration(a, b):
    """
    Calibrate the entropy of the liquid phase against the solid phase at reference temperature and pressure.

    Parameters:
    a (float): Reference temperature factor.
    b (float): Reference pressure factor.
    """

    # calibrated state point
    T_ref = float(a) * 1.0e-3   # K ==> K*1e+3
    p_ref = float(b) * 1.0e-1   # GPa ==> Pa*1e+10

    try:
        # solid phase
        dat_abc = np.genfromtxt('solid_dat_abc.txt')
        dat_eos = np.genfromtxt('solid_dat_eos.txt')
        [V, S, p, T, U, F, H, G] = potential_G(T_ref, p_ref, dat_abc, dat_eos)
        G_solid = G

        # liquid phase
        dat_abc = np.genfromtxt('liquid_dat_abc.txt')
        dat_eos = np.genfromtxt('liquid_dat_eos.txt')
        [V, S, p, T, U, F, H, G] = potential_G(T_ref, p_ref, dat_abc, dat_eos)
        V_liquid = V
        S_liquid = S
        p_liquid = p
        T_liquid = T
        U_liquid = U

        S_before_shift = S_liquid
        S_after_shift = (U_liquid + p_liquid * V_liquid - G_solid) / T_liquid
        delta_sx = S_after_shift - S_before_shift

        # Write result to file
        with open('liquid_delta_S.txt', 'w') as f:
            f.write(f"{delta_sx:.6f}")

    except Exception as e:
        print(f"An error occurred: {e}")
