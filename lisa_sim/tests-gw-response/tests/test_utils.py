#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring

import numpy as np
import pytest
import lisagwresponse.utils


def test_dot():
    """Test that we can compute a dot product on last axis."""
    a = [[2, 3], [1, 1], [4, 5], [0, 3]]
    b = [[5, 3], [2, 4], [0, 5], [1, 2]]
    expected = [19, 6, 25, 6]
    assert lisagwresponse.utils.dot(a, b) == pytest.approx(expected)


def test_norm():
    """Test that we can compute the norm on last axis."""
    a = [[0, 0], [1, 1], [2, -3]]
    expected = [0, np.sqrt(2), np.sqrt(13)]
    assert lisagwresponse.utils.norm(a) == pytest.approx(expected)


def test_arrayindex():
    """Test that we can find array indices of a list of elements."""
    assert lisagwresponse.utils.arrayindex([], []) == pytest.approx([])

    a = [1, 3, 6, 9]
    assert lisagwresponse.utils.arrayindex([], a) == pytest.approx([])
    assert lisagwresponse.utils.arrayindex([3], a) == pytest.approx([1])
    assert lisagwresponse.utils.arrayindex([6, 3, 9], a) == pytest.approx([2, 1, 3])

    with pytest.raises(ValueError):
        lisagwresponse.utils.arrayindex([1], [])
    with pytest.raises(ValueError):
        lisagwresponse.utils.arrayindex([1, 6, 2], a)


def test_atleast_2d():
    """Test that we can resize arrays to 2d on the last axis."""
    assert lisagwresponse.utils.atleast_2d([]).shape == (0, 1)
    assert lisagwresponse.utils.atleast_2d(42).shape == (1, 1)
    assert lisagwresponse.utils.atleast_2d(42) == pytest.approx(np.array([[42]]))
    assert lisagwresponse.utils.atleast_2d([42]).shape == (1, 1)
    assert lisagwresponse.utils.atleast_2d([42]) == pytest.approx(np.array([[42]]))
    assert lisagwresponse.utils.atleast_2d([3, 6, 8]).shape == (3, 1)
    a = np.arange(9).reshape((3, 3))
    assert lisagwresponse.utils.atleast_2d(a) == pytest.approx(a)
    a = np.arange(8).reshape((2, 2, 2))
    assert lisagwresponse.utils.atleast_2d(a) == pytest.approx(a)


def test_emitter():
    """Test that we can get the emitter index."""

    assert lisagwresponse.utils.emitter(12) == 2
    assert lisagwresponse.utils.emitter(31) == 1
    assert lisagwresponse.utils.emitter([31]) == 1
    assert lisagwresponse.utils.emitter([12, 32, 23]) == pytest.approx([2, 2, 3])
    assert lisagwresponse.utils.emitter(np.array([21, 31, 23])) == pytest.approx([1, 1, 3])

    with pytest.raises(ValueError):
        lisagwresponse.utils.emitter(45)
    with pytest.raises(ValueError):
        lisagwresponse.utils.emitter(121)
    with pytest.raises(ValueError):
        lisagwresponse.utils.emitter([12, 34])
    with pytest.raises(ValueError):
        lisagwresponse.utils.emitter(np.array([12, 34]))


def test_receiver():
    """Test that we can get the receiver index."""

    assert lisagwresponse.utils.receiver(12) == 1
    assert lisagwresponse.utils.receiver(31) == 3
    assert lisagwresponse.utils.receiver([31]) == 3
    assert lisagwresponse.utils.receiver([12, 32, 23]) == pytest.approx([1, 3, 2])
    assert lisagwresponse.utils.receiver(np.array([21, 31, 23])) == pytest.approx([2, 3, 2])

    with pytest.raises(ValueError):
        lisagwresponse.utils.receiver(45)
    with pytest.raises(ValueError):
        lisagwresponse.utils.receiver(121)
    with pytest.raises(ValueError):
        lisagwresponse.utils.emitter([12, 34])
    with pytest.raises(ValueError):
        lisagwresponse.utils.emitter(np.array([12, 34]))
