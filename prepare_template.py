#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 dal22 <dal22@fenrir.ess.washington.edu>
#
# Distributed under terms of the MIT license.

"""

"""
import sys

lambdav = sys.argv[1]

template_fn = 'template_inversion.sif'
out_fn = 'inversion_{:s}.sif'.format(lambdav)

subs = {'LAMBDA': lambdav}
with open(template_fn, 'r') as fin:
    with open(out_fn, 'w') as fout:
        for line in fin:
            for sub in subs:
                if '{%s}' % sub in line:
                    line = line.format(**subs)
                    break
            fout.write(line)
