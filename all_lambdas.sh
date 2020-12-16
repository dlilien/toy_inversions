#! /bin/sh
#
# all_lambdas.sh
# Copyright (C) 2020 dlilien <dlilien@hozideh>
#
# Distributed under terms of the MIT license.
#


for lambda in 1.0e0 1.0e6 1.0e8 1.0e10 1.0e12 1.0e14 1.0e16 1.0e18 1.0e20; do
    ./prepare_template.py $lambda
    rm -f rectangle/inversion_l${lambda}_t????.vtu
    echo Running inversion_${lambda}.sif...
    ElmerSolver inversion_${lambda}.sif > logs/inversion_${lambda}.log
done
