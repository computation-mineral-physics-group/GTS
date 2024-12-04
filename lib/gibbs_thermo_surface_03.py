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
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, leastsq


def eos(V, B0, BP, V0):
    """3rd-order Birch-Murnaghan Equation of State (EoS)."""
    eta = (V0 / V) ** (1. / 3.)
    return 1.5 * B0 * (eta ** 7 - eta ** 5) * (1 + 3. / 4. * (BP - 4) * (eta ** 2 - 1))


def A_without_constant(V, B0, BP, V0):
    """Helmholtz free energy by integration of EoS (without constant A0)."""
    eta = (V0 / V) ** (1. / 3.)
    return 9. * V0 * B0 / 16. * ((eta ** 2 - 1) ** 3 * BP + (eta ** 2 - 1) ** 2 * (6 - 4 * eta ** 2))


def func_ST(T, a, c):
    """Calculate entropy S as a function of T."""
    return a * np.log(a * T / c)


def func_TS(S, a, c):
    """Calculate temperature T as a function of S."""
    return c / a * np.exp(S / a)


def func_UV(V, E0, B0, BP, V0):
    """Calculate internal energy U as a function of V."""
    eta = (V0 / V) ** (1. / 3.)
    return E0 + 9. * B0 * V0 / 16. * ((eta ** 2 - 1) ** 3 * BP + (eta ** 2 - 1) ** 2 * (6 - 4 * eta ** 2))


def bm3(parameters, V):
    """Birch-Murnaghan 3rd-order EoS for optimization."""
    E0, B0, BP, V0 = parameters
    eta = (V0 / V) ** (1. / 3.)
    return E0 + 9. * B0 * V0 / 16. * ((eta ** 2 - 1) ** 3 * BP + (eta ** 2 - 1) ** 2 * (6 - 4 * eta ** 2))


def objective(pars, y, x):
    """Objective function for least squares optimization."""
    return y - bm3(pars, x)


def func_US(S, a, b, c):
    """Calculate internal energy U as a function of entropy S."""
    return c * np.exp(S / a) + b


def parabola(x, a, b, c):
    """Parabolic function for fitting."""
    return a + b * x + c * x ** 2


def read_data(file_path):
    """Read data from a file."""
    return np.genfromtxt(file_path)


def write_data(file_path, data):
    """Write data to a file."""
    try:
        with open(file_path, 'w') as f:
            for line in data:
                f.write(line + '\n')
    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")


def surface_03():
    """Main function for Gibbs Thermodynamic Surface analysis."""

    # whether output full information and intermediate graphics to debug
    debug = False

    # load data
    V = read_data('V.txt')
    if V is None:
        return

    nV = len(V)
    dat = read_data('abde.txt')
    if dat is None:
        return

    a, b, d, e = dat[:, 0], dat[:, 1], dat[:, 2], dat[:, 3]

    # set properties at the reference state
    refS = read_data('refS.txt')
    ref_index = int(read_data('ref_index.txt'))
    refV = V[ref_index]
    write_data('refV.txt', [f"{refV:.6f}"])

    refT = read_data('refT.txt')
    refU = a[ref_index] * refT + b[ref_index]

    # get V-p data at the reference T
    p = d * refT + e

    # fit V-p to Equation of State (EoS)
    popt, pcov = curve_fit(eos, V, p, maxfev=1000000)
    B0, BP, V0 = popt

    if debug:
        print('EoS parameters for A_without_constant:')
        print(f'B0 = {B0:.6f}, BP = {BP:.6f}, V0 = {V0:.6f}')
        print(p)

    # derive preliminary coefficient c
    file_out = 'preliminary_c.txt'
    preliminary_c_data = []
    for i in range(nV):
        thisV = V[i]
        thisU = a[i] * refT + b[i]
        thisA = A_without_constant(thisV, B0, BP, V0)
        refA = A_without_constant(refV, B0, BP, V0)
        thisS = ((thisU - refU + refT * refS) - (thisA - refA)) / refT
        c = a[i] * refT / np.exp(thisS / a[i])
        preliminary_c_data.append(f"{c:.6f}")
    write_data(file_out, preliminary_c_data)

    # generate coefficients of U(V) at constant S, i.e., dat_eos.txt
    c = read_data('preliminary_c.txt')
    if c is None:
        return

    S_all = []
    for i in range(nV):
        file_tup = f'V{i + 1}.txt'
        dat = read_data(file_tup)
        if dat is None:
            continue

        T = dat[:, 0]
        for thisT in T:
            thisS = func_ST(thisT, a[i], c[i])
            S_all.append(thisS)

    minS, maxS = min(S_all), max(S_all)

    if debug:
        print(f"Entropy range: minimum = {minS:.6f}, maximum = {maxS:.6f}")
        for i in range(nV):
            mintemp = func_TS(minS, a[i], c[i])
            maxtemp = func_TS(maxS, a[i], c[i])
            print(f"V = {V[i]:.6f}, minimum T = {mintemp:.6f}, maximum T = {maxtemp:.6f}")

    file_out = 'dat_eos.txt'
    dat_eos_data = []
    nS = 10  # number of entropies to sample
    S = np.linspace(minS, maxS, nS)

    fig = plt.figure()
    plt.subplot(111)
    for thisS in S:
        U = np.array([func_US(thisS, a[j], b[j], c[j]) for j in range(nV)])

        # plot figure
        if debug:
            plt.xlabel('V (1.0e-29 m^3/atom)')
            plt.ylabel('U (1.0e-19 J/atom)')
            plt.title(f'Constant S = {thisS:.3f} * 1.0e-22 J/K/atom')
            plt.plot(V, U, 'o')

        # estimate the initial guess
        p0 = [min(U), 1, 1]
        popt, pcov = curve_fit(parabola, V, U, p0, maxfev=1000000)
        a0, b0, c0 = popt
        parabola_vmin = -b0 / (2 * c0)
        E00 = parabola(parabola_vmin, a0, b0, c0)
        B00 = 2 * c0 * parabola_vmin
        BP0 = 4
        initial_guess = [E00, B00, BP0, parabola_vmin]
        guess = initial_guess if 'guess' not in locals() else guess
        plsq = leastsq(objective, guess, args=(U, V), maxfev=1000000)
        popt = plsq[0]
        E0, B0, BP, V0 = popt
        guess = [E0, B0, BP, V0]
        dat_eos_data.append(f"{thisS:.6f} {E0:.6f} {B0:.6f} {BP:.6f} {V0:.6f}")

        if debug:
            print(f"{thisS:.6f} {E0:.6f} {B0:.6f} {BP:.6f} {V0:.6f}")
            nk = 50
            V_s = np.linspace(min(V), max(V), nk)
            U_s = np.array([func_UV(V_s[k], E0, B0, BP, V0) for k in range(nk)])
            plt.plot(V_s, U_s, 'k-')
            plt.show()

    write_data(file_out, dat_eos_data)

    # generate coefficients of U(S) at constant V again, i.e., dat_abc.txt
    dat_abde = read_data('abde.txt')
    if dat_abde is None:
        return

    dat_c = read_data('preliminary_c.txt')
    if dat_c is None:
        return

    guess = [dat_abde[0, 0], dat_abde[0, 1], dat_c[0]]

    file_out = 'dat_abc.txt'
    dat_abc_data = []
    dat_eos = read_data('dat_eos.txt')
    if dat_eos is None:
        return

    S = dat_eos[:, 0]
    nS = dat_eos.shape[0]
    for i in range(nV):
        thisV = V[i]
        U = np.array([func_UV(thisV, dat_eos[j, 1], dat_eos[j, 2], dat_eos[j, 3], dat_eos[j, 4]) for j in range(nS)])
        popt, pcov = curve_fit(func_US, S, U, guess, maxfev=1000000)
        a, b, c = popt
        dat_abc_data.append(f"{thisV:.6f} {a:.6f} {b:.6f} {c:.6f}")
    write_data(file_out, dat_abc_data)



