#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring

from os.path import isfile
import numpy as np
from h5py import File

from lisagwresponse import ReadResponse, ReadStrain, GalacticBinary


def read_gw_response(orbits):
    """Check with an instance of :class:`ReadResponse`."""

    with File(orbits) as orbitf:
        t0 = 10.0 + orbitf.attrs['t0']

    response = {f'y_{link}': np.random.normal(size=100) for link in ReadResponse.LINKS}
    instance = ReadResponse(
        **response,
        t = t0 + np.arange(100),
        t0=t0, size=100, dt=1.0,
        orbits=orbits,
    )

    instance.compute_gw_response(instance.t, [12, 21])
    instance.write('gws.h5', mode='w')
    assert isfile('gws.h5')
    instance.plot(instance.t, output='figure.png')
    assert isfile('figure.png')


def read_strain(orbits):
    """Check with an instance of :class:`ReadStrain`."""

    with File(orbits) as orbitf:
        t0 = 10.0 + orbitf.attrs['t0']

    instance = ReadStrain(
        hplus=np.random.normal(size=100),
        hcross=np.random.normal(size=100),
        t = t0 + np.arange(100),
        t0=t0, size=100, dt=1.0,
        orbits=orbits,
        gw_beta=0, gw_lambda=0,
    )

    instance.compute_gw_response(instance.t, [12, 21])
    instance.write('gws.h5', mode='w')
    assert isfile('gws.h5')
    instance.plot(instance.t, output='figure.png')


def galactic_binary(orbits):
    """Check with an instance of :class:`GalacticBinary`."""

    with File(orbits) as orbitf:
        t0 = 10.0 + orbitf.attrs['t0']

    instance = GalacticBinary(
        A=1E-21, f=2E-3,
        t0=t0, size=100, dt=1.0,
        orbits=orbits,
        gw_beta=0, gw_lambda=0,
    )

    instance.compute_gw_response(instance.t, [12, 21])
    instance.write('gws.h5', mode='w')
    assert isfile('gws.h5')
    instance.plot(instance.t, output='figure.png')
    assert isfile('figure.png')


def test_keplerian_orbits_1_0_2():
    """Test that simulations can run with Keplerian orbit files v1.0.2."""
    orbits = 'tests/keplerian-orbits-1-0-2.h5'
    read_gw_response(orbits)
    read_strain(orbits)
    galactic_binary(orbits)


def test_esa_orbits_1_0_2():
    """Test that simulations can run with ESA orbit files v1.0.2."""
    orbits = 'tests/esa-orbits-1-0-2.h5'
    read_gw_response(orbits)
    read_strain(orbits)
    galactic_binary(orbits)

def test_keplerian_orbits_2_0():
    """Test that simulations can run with Keplerian orbit files v2.0."""
    orbits = 'tests/keplerian-orbits-2-0.h5'
    read_gw_response(orbits)
    read_strain(orbits)
    galactic_binary(orbits)

def test_esa_trailing_orbits_2_0():
    """Test that simulations can run with ESA trailing orbit files v2.0."""
    orbits = 'tests/esa-trailing-orbits-2-0.h5'
    read_gw_response(orbits)
    read_strain(orbits)
    galactic_binary(orbits)
