#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring

import os.path
import numpy as np
from pytest import approx, raises
from h5py import File

from lisagwresponse import Response, ResponseFromStrain, GalacticBinary
from lisagwresponse import VerificationBinary, ReadResponse


def test_abstract_classes():
    """Check that abstract base classes cannot be instantiated."""
    # pylint: disable=abstract-class-instantiated

    with raises(TypeError):
        Response(orbits='tests/orbits/keplerian-orbits.h5')
    with raises(TypeError):
        ResponseFromStrain(0, 0, orbits='tests/orbits/keplerian-orbits.h5')


def test_readgwresponse():
    """Test that we can read response with `ReadResponse` objects."""

    orbits = 'tests/keplerian-orbits-2-0.h5'
    with File(orbits) as orbitf:
        t0 = orbitf.attrs['t0']

    dt = 0.1
    t = t0 + np.arange(100) * dt
    y_12 = np.random.normal(size=100)
    y_23 = np.random.normal(size=100)
    y_31 = np.random.normal(size=100)
    y_13 = np.random.normal(size=100)
    y_32 = np.random.normal(size=100)
    y_21 = np.random.normal(size=100)

    response = ReadResponse(
        t, y_12, y_23, y_31, y_13, y_32, y_21,
        orbits=orbits, interp_order=1, dt=dt, t0=t0, size=len(t))

    assert response.dt == dt
    assert response.t == approx(t)

    # One point in time
    assert response.compute_gw_response([t0], [12])[0, 0] == approx(y_12[0])
    assert response.compute_gw_response([t0], [23])[0, 0] == approx(y_23[0])
    assert response.compute_gw_response([t0], [31])[0, 0] == approx(y_31[0])
    assert response.compute_gw_response([t0], [13])[0, 0] == approx(y_13[0])
    assert response.compute_gw_response([t0], [32])[0, 0] == approx(y_32[0])
    assert response.compute_gw_response([t0], [21])[0, 0] == approx(y_21[0])

    # The entire time array
    assert response.compute_gw_response(t, [12])[:, 0] == approx(y_12)
    assert response.compute_gw_response(t, [23])[:, 0] == approx(y_23)
    assert response.compute_gw_response(t, [31])[:, 0] == approx(y_31)
    assert response.compute_gw_response(t, [13])[:, 0] == approx(y_13)
    assert response.compute_gw_response(t, [32])[:, 0] == approx(y_32)
    assert response.compute_gw_response(t, [21])[:, 0] == approx(y_21)

    # With some resampling involved
    assert response.compute_gw_response([t0 + 1.05], [12])[0, 0] == approx(np.average(y_12[10:12]))
    assert response.compute_gw_response([t0 + 1.05], [23])[0, 0] == approx(np.average(y_23[10:12]))
    assert response.compute_gw_response([t0 + 1.05], [31])[0, 0] == approx(np.average(y_31[10:12]))
    assert response.compute_gw_response([t0 + 1.05], [13])[0, 0] == approx(np.average(y_13[10:12]))
    assert response.compute_gw_response([t0 + 1.05], [32])[0, 0] == approx(np.average(y_32[10:12]))
    assert response.compute_gw_response([t0 + 1.05], [21])[0, 0] == approx(np.average(y_21[10:12]))

    # With multiple links
    assert response.compute_gw_response(t, [12, 13]) == approx(np.stack([y_12, y_13], axis=-1))
    assert response.compute_gw_response(t, [13, 32, 12]) == approx(np.stack([y_13, y_32, y_12], axis=-1))
    assert response.compute_gw_response(t, response.LINKS) \
        == approx(np.stack([y_12, y_23, y_31, y_13, y_32, y_21], axis=-1))

    # Test writing
    response.write('gws.h5', mode='w')
    assert os.path.isfile('gws.h5')


def test_galactic_binary():
    """Test GalacticBinary class."""

    orbits = 'tests/keplerian-orbits-2-0.h5'
    with File(orbits) as orbitf:
        t0 = orbitf.attrs['t0']

    galbin = GalacticBinary(
        A=1E-21, f=2E-3, df=1E-9,
        gw_beta=0, gw_lambda=0,
        orbits=orbits,
        size=100, t0=t0 + 10.0, dt=1.0)

    assert galbin.A == 1E-21
    assert galbin.f == 2E-3
    assert galbin.df == 1E-9
    assert galbin.orbits_path == orbits
    assert galbin.size == 100
    assert galbin.t0 == t0 + 10.0
    assert galbin.dt == 1.0
    assert galbin.t == approx(np.arange(t0 + 10.0, t0 + 110.0, 1.0))

    links = [12, 21]
    times = np.arange(t0 + 100, t0 + 150, 10)
    response = galbin.compute_gw_response(times, links)
    assert response.shape == (len(times), len(links))

    links = [12, 21, 31]
    times = np.arange(t0 + 100, t0 + 150, 5)
    response = galbin.compute_gw_response(times, links)
    assert response.shape == (len(times), len(links))

    response = galbin.compute_gw_response(galbin.t, galbin.LINKS)
    assert response.shape == (100, 6)

def test_verification_binary():
    """Test VerificationBinary class."""

    orbits = 'tests/keplerian-orbits-2-0.h5'
    with File(orbits) as orbitf:
        t0 = orbitf.attrs['t0']

    galbin = VerificationBinary(
        period=569.4,
        distance=2089,
        masses=(0.8, 0.117),
        glong=57.7281,
        glat=6.4006,
        iota=60 * (np.pi / 180),
        orbits=orbits,
        size=100, t0=t0 + 10.0, dt=1.0
    )

    assert galbin.period == 569.4
    assert galbin.distance == 2089
    assert galbin.masses[0] == 0.8
    assert galbin.masses[1] == 0.117
    assert galbin.glong == 57.7281
    assert galbin.glat == 6.4006

    assert galbin.A == approx(6.333424477822074E-23)
    assert galbin.f == approx(3.5124692658939235E-3)
    assert galbin.df == approx(5.591334254143374E-17)
    assert galbin.gw_beta == approx(0.8165220844186913)
    assert galbin.gw_lambda == approx(5.1485583542879)
    assert galbin.orbits_path == orbits
    assert galbin.size == 100
    assert galbin.t0 == t0 + 10.0
    assert galbin.dt == 1.0
    assert galbin.t == approx(np.arange(t0 + 10.0, t0 + 110.0, 1.0))

    links = [12, 21]
    times = np.arange(t0 + 100, t0 + 150, 10)
    response = galbin.compute_gw_response(times, links)
    assert response.shape == (len(times), len(links))

    links = [12, 21, 31]
    times = np.arange(t0 + 100, t0 + 150, 5)
    response = galbin.compute_gw_response(times, links)
    assert response.shape == (len(times), len(links))

    response = galbin.compute_gw_response(galbin.t, galbin.LINKS)
    assert response.shape == (100, 6)
