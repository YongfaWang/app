#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate figures for various sources.

This script is used by Gitlab-CI to generate example figures for various types of sources
implemented in LISA GW Response.

Authors:
    Jean-Baptiste Bayle <j2b.bayle@gmail.com>
"""

import healpy # not support Windows
from h5py import File
from numpy import pi

import lisagwresponse
import get_my_conf as conf_var
from get_my_conf import *

def main():
    """Main function."""
    # Get configuration
    filename_path = 'gw_response.ini'
    get_config(filename_path)

    select_gws = conf_var.global_gws_type

    if select_gws == "galactic-binary-TQ3":
        gws = galactic_binary_TQ3()
    elif select_gws == "galactic-binary":
        gws = galactic_binary()
    elif select_gws == "stochastic-background":
        gws = stochastic_background()
    elif select_gws == "stochastic-point-source":
        gws = stochastic_point_source()
    else:
        raise ValueError(f"unknown orbit model: '{select_gws}'")

    gws.plot(gws.t, f'../data/pdf/{select_gws}.pdf', select_gws)
    gws.write(f'../data/{select_gws}.h5') # strain or relative frequency shifts [6*1]

def galactic_binary_TQ3():
    """Generate `GalacticBinary` plot."""
    th = get_t0(conf_var.global_orbits_file)
    return lisagwresponse.GalacticBinary(
        A=1E-19, f=1E-3, df=1E-16,
        orbits=conf_var.global_orbits_file,
        gw_beta=pi / 2, gw_lambda=pi / 3,
        t0=th + 10,
        dt=0.25, size=600)

def galactic_binary():
    """Generate `GalacticBinary` plot."""
    th = get_t0('tests/keplerian-orbits-2-0.h5')
    return lisagwresponse.GalacticBinary(
        A=1E-19, f=1E-3, df=1E-16,
        orbits='tests/keplerian-orbits-2-0.h5',
        gw_beta=pi / 2, gw_lambda=pi / 3,
        t0=th + 10,
        dt=10, size=600)


def stochastic_background():
    """Generate `StochasticBackground` plot."""
    skymap = healpy.synfast([1, 0.5, 0.25, 0.125, 1, 0.125], 8)**2
    return lisagwresponse.StochasticBackground(
        skymap,
        generator=lisagwresponse.psd.white_generator(1.0),
        orbits='tests/keplerian-orbits-2-0.h5',
        t0=get_t0('tests/keplerian-orbits-2-0.h5') + 10,
        size=600)


def stochastic_point_source():
    """Generate `StochasticPointSource` plot."""
    spectrum = lambda f: 1E-24 / (f + 1e-5)**2
    generator = lisagwresponse.psd.ifft_generator(spectrum)
    return lisagwresponse.StochasticPointSource(
        generator,
        orbits='tests/keplerian-orbits-2-0.h5',
        gw_beta=pi / 2, gw_lambda=pi / 3,
        t0=get_t0('tests/keplerian-orbits-2-0.h5') + 10,
        size=600)


def get_t0(orbits):
    """Return the initial time ``t0`` of an orbit file.

    Args:
        orbits (str): path to orbit file

    Returns:
        (float) Orbit file's initial time {math}`t_0`.
    """
    with File(orbits) as orbitf:
        return float(orbitf.attrs['t0'])


if __name__ == '__main__':
    main()
