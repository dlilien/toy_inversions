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

import glob
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
import simplevtulib


def main():
    vel()


def vel():
    fig, (ax1, ax3) = plt.subplots(2, 1, sharex=True, figsize=(8, 5))
    for lambdav in [0, 10, 14, 18]:
        fns = glob.glob('rectangle/inversion_l1.0e{:d}_t????.vtu'.format(lambdav))
        inds = np.argsort([int(fn[-8:-4]) for fn in fns])
        fn = fns[inds[-1]]
        vtu = simplevtulib.VTU(fn)
        top = vtu.get_geometry_data(103, order='x')
        bottom = vtu.get_geometry_data(101, order='x')

        uniform_x = np.linspace(np.min(top['coordsX']), np.max(top['coordsX']), 1001)
        top_v = interp1d(top['coordsX'], top['velocity'][:, 0], fill_value='extrapolate')(uniform_x)
        top_vin = interp1d(bottom['coordsX'], top['vxin'], fill_value='extrapolate')(uniform_x)
        true_beta = interp1d(bottom['coordsX'], bottom['truebeta'], fill_value='extrapolate')(uniform_x)
        beta = interp1d(bottom['coordsX'], bottom['beta'], fill_value='extrapolate')(uniform_x)
        ax3.plot(uniform_x, beta ** 2.0)
        ax1.plot(uniform_x, top_v, label=r'Inferred $\lambda=10^{%d}$' % lambdav)

    ax1.plot(uniform_x, top_vin, label='True', color='k')
    ax1.set_ylabel(r'Surface speed (m a$^{-1}$)')
    ax1.legend(loc='best', fontsize=8)
    ax3.plot(uniform_x, true_beta ** 2.0, color='k')
    ax3.set_ylabel(r'Stickiness (MPa a m$^{-1}$)')
    ax3.set_xlabel('Distance (m)')
    ax1.set_title(r'Inversion results, 40x2 km slab, 0.2$^o$ incline')

    fig.tight_layout()
    fig.savefig('compare_inversion.png')


if __name__ == '__main__':
    main()
