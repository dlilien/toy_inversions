#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 David Lilien <dlilien90@gmail.com>
#
# Distributed under terms of the GNU GPL3.0 license.

"""
Get the results of a forward model for input to inversions.
"""

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import simplevtulib


def main():
    vel()


def vel():
    for flid in range(9):
        vtu = simplevtulib.VTU('rectangle/inversion_input_t0001.vtu')
        top = vtu.get_geometry_data(103, order='x')
        bottom = vtu.get_geometry_data(101, order='x')

        uniform_x = np.linspace(np.min(top['coordsX']), np.max(top['coordsX']), 1001)
        top_v = interp1d(top['coordsX'], top['velocity'][:, 0], fill_value='extrapolate')(uniform_x)
        bottom_v = interp1d(bottom['coordsX'], bottom['velocity'][:, 0], fill_value='extrapolate')(uniform_x)
        true_beta = interp1d(bottom['coordsX'], bottom['beta'], fill_value='extrapolate')(uniform_x)

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(8, 5))
        ax1.plot(top['coordsX'], top['velocity'][:, 0])
        ax1.plot(uniform_x, top_v)
        ax1.plot(uniform_x, bottom_v)
        ax1.set_ylabel('Surface vel.\n (m/yr)')
        ax2.plot(uniform_x, np.abs(bottom_v / top_v))
        ax2.set_ylim(0, 1)
        ax2.set_ylabel('Frac. motion\ndue to sliding')
        ax3.plot(uniform_x, true_beta)
        ax3.set_ylabel('True beta')
        fig.savefig('vel_in.png')

        with open('vx.txt', 'w') as fout:
            fout.write('# {:d}\n'.format(len(uniform_x)))
            for i in range(len(uniform_x)):
                fout.write('{:f} {:f}\n'.format(uniform_x[i], top_v[i]))

        with open('true_beta.txt', 'w') as fout:
            fout.write('# {:d}\n'.format(len(uniform_x)))
            for i in range(len(uniform_x)):
                fout.write('{:f} {:f}\n'.format(uniform_x[i], true_beta[i]))


if __name__ == '__main__':
    main()
