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


def fit_linear_functions():
    """Fit linear functions U(T)=a*T+b and p(T)=d*T+e for data in V*.txt files."""

    volumes = np.genfromtxt('V.txt')  # Read the volumes from V.txt

    file_out = 'abde.txt'

    with open(file_out, 'w') as f:
        for i in range(len(volumes)):
            file_tup = f'V{i + 1}.txt'

            dat = np.genfromtxt(file_tup)

            T = dat[:, 0]
            U = dat[:, 1]
            p = dat[:, 2]
            [a, b] = np.polyfit(T, U, 1)
            [d, e] = np.polyfit(T, p, 1)
            f.write(f"{a:.6f} {b:.6f} {d:.6f} {e:.6f}\n")
