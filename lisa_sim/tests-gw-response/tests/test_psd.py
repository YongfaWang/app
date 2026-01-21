#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring

import numpy as np
import pytest
from scipy.signal import welch
from lisagwresponse.psd import white_generator, ifft_generator


@pytest.mark.xfail(reason="statistical tests can fail")
def test_white_generator():
    """Test that white generator generates a white noise."""

    size = 100000

    for fs in [1.0, 0.2, 10.0]:
        for psd in [1.0, 0.1, 12.3, 42.0]:

            generator = white_generator(psd)
            data = generator(fs, size)
            data_psd = welch(data, fs, nperseg=size // 100)[1][5:-5]

            assert np.isclose(np.mean(data), 0.0, atol=0.1)
            assert np.all(np.isclose(data_psd, psd, rtol=0.5))

@pytest.mark.xfail(reason="statistical tests can fail")
def test_ifft_generator_white():
    """Test that IFFT generator can generate a white noise."""

    size = 100000

    for fs in [1.0, 0.2, 10.0]:
        for psd in [1.0, 0.1, 12.3, 42.0]:

            generator = ifft_generator(lambda _: psd) # pylint: disable=cell-var-from-loop
            data = generator(fs, size)
            data_psd = welch(data, fs, nperseg=size // 100)[1][5:-5]

            assert np.isclose(np.mean(data), 0.0, atol=0.1)
            assert np.all(np.isclose(data_psd, psd, rtol=0.5))
