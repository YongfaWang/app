#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# BSD 3-Clause License
#
# Copyright 2022, by the California Institute of Technology.
# ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged.
# Any commercial use must be negotiated with the Office of Technology Transfer
# at the California Institute of Technology.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# This software may be subject to U.S. export control laws. By accepting this
# software, the user agrees to comply with all applicable U.S. export laws and
# regulations. User has the responsibility to obtain export licenses, or other
# export authority as may be required before exporting such information to
# foreign countries or providing access to foreign persons.
#
"""
Generate figures for various glitch types.

This script is used by Gitlab-CI to generate example figures.

Authors:
    Jean-Baptiste Bayle <j2b.bayle@gmail.com>
"""

import os
import lisaglitch
import get_my_conf as conf_var
from get_my_conf import *


def main():
    """Main function."""
    # Get configuration
    filename_path = 'glitches.ini'
    get_config(filename_path)
    saveH5Path = f'../data/{conf_var.global_glitch_type}.h5'
    savePDFPath = f'../data/pdf/glitches/{conf_var.global_glitch_type}_'
    # remove old file
    try:
        os.remove(saveH5Path)
    except FileNotFoundError:
        print(f"File not Found {saveH5Path}")

    """Glitches types parameters"""
    dataSize = conf_var.global_dataSize
    time_t0 = conf_var.global_time_t0
    time_inj = conf_var.global_time_inj

    """RectangleGlitch, stepGlitch, ShapeletGlitch, IntegratedShapeletGlitch, OneSidedDoubleExpGlitch,
    IntegratedOneSidedDoubleExpGlitch, TwoSidedDoubleExpGlitch, IntegratedTwoSidedDoubleExpGlitch"""
    if conf_var.global_glitch_type == "RectangleGlitch":
        """Generate a rectangle glitch."""
        for inj in conf_var.global_INJECTION_POINTS:
            glitch = lisaglitch.RectangleGlitch(inj_point=inj, width=2, size=dataSize, t0=time_t0, t_inj=time_inj)
            glitch.plot(savePDFPath + inj + '.pdf', title=inj)
            glitch.write(saveH5Path, 'a')
    elif conf_var.global_glitch_type == "stepGlitch":
        """Generate a StepGlitch glitch."""
        for inj in lisaglitch.INJECTION_POINTS:
            glitch = lisaglitch.StepGlitch(inj_point=inj, size=dataSize, t0=time_t0, t_inj=time_inj)
            glitch.plot(savePDFPath + inj + '.pdf', title=inj)
            glitch.write(saveH5Path, 'a')
    elif conf_var.global_glitch_type == "ShapeletGlitch":
        """Generate a shapelet glitch."""
        for inj in lisaglitch.INJECTION_POINTS:
            glitch = lisaglitch.ShapeletGlitch(inj_point=inj, size=dataSize, t0=time_t0, t_inj=time_inj)
            glitch.plot(savePDFPath + inj + '.pdf', title=inj)
            glitch.write(saveH5Path, 'a')
    elif conf_var.global_glitch_type == "IntegratedShapeletGlitch":
        """Generate an integrated shapelet glitch."""
        for inj in lisaglitch.INJECTION_POINTS:
            glitch = lisaglitch.IntegratedShapeletGlitch(inj_point=inj, size=dataSize, t0=time_t0, t_inj=time_inj)
            glitch.plot(savePDFPath + inj + '.pdf', title=inj)
            glitch.write(saveH5Path, 'a')
    elif conf_var.global_glitch_type == "OneSidedDoubleExpGlitch":
        """Generate a one-sided double-exponential glitch."""
        for inj in lisaglitch.INJECTION_POINTS:
            glitch = lisaglitch.OneSidedDoubleExpGlitch(inj_point=inj, t_rise=1, t_fall=2,size=dataSize, t0=time_t0, t_inj=time_inj)
            glitch.plot(savePDFPath + inj + '.pdf', title=inj)
            glitch.write(saveH5Path, 'a')
    elif conf_var.global_glitch_type == "IntegratedOneSidedDoubleExpGlitch":
        """Generate an integrated one-sided double-exponential glitch."""
        for inj in lisaglitch.INJECTION_POINTS:
            glitch = lisaglitch.IntegratedOneSidedDoubleExpGlitch(inj_point=inj, t_rise=1, t_fall=2,size=dataSize, t0=time_t0, t_inj=time_inj)
            glitch.plot(savePDFPath + inj + '.pdf', title=inj)
            glitch.write(saveH5Path, 'a')
    elif conf_var.global_glitch_type == "TwoSidedDoubleExpGlitch":
        """Generate a two-sided double-exponential glitch."""
        for inj in lisaglitch.INJECTION_POINTS:
            glitch = lisaglitch.TwoSidedDoubleExpGlitch(inj_point=inj, t_rise=1, t_fall=2, displacement=10,
                                                        size=dataSize, t0=time_t0, t_inj=time_inj)
            glitch.plot(savePDFPath + inj + '.pdf', title=inj)
            glitch.write(saveH5Path, 'a')
    elif conf_var.global_glitch_type == "IntegratedTwoSidedDoubleExpGlitch":
        """Generate an integrated two-sided double-exponential glitch."""
        for inj in lisaglitch.INJECTION_POINTS:
            glitch = lisaglitch.IntegratedTwoSidedDoubleExpGlitch(inj_point=inj, t_rise=1, t_fall=2, displacement=10,
                                                                  size=dataSize, t0=time_t0, t_inj=time_inj)
            glitch.plot(savePDFPath + inj + '.pdf', title=inj)
            glitch.write(saveH5Path, 'a')

if __name__ == '__main__':
    main()

    # glitch = lisaglitch.HDF5Glitch(path='stepGlitch.h5', inj_point='tm_12')
    # glitch.plot('test.pdf')

    #with h5py.File('stepGlitch.h5', 'r') as f:
    #    print('DataSet in file:')
    #    print(list(f.keys()))
    #    data = f['tm_12'][:]
    #    print("Data in 'dataset_name':")
    #    print(data)
