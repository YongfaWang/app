#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate figures for various orbit generators.

This script is used by Gitlab-CI to generate example figures.

Authors:
    Jean-Baptiste Bayle <j2b.bayle@gmail.com>
"""


import lisaorbits
import get_my_conf as conf_var
from get_my_conf import *


def main():
    """Main function."""
    # Get configuration
    filename_path = 'orbits.ini'
    get_config(filename_path)

    select_orbits = conf_var.global_orbit_type

    if select_orbits == "readOEMOrbits":
        orbits = readOEMOrbits()
    elif select_orbits == "static-constellation":
        orbits = static_constellation()
    elif select_orbits == "keplerian-orbits":
        orbits = keplerian_orbits()
    elif select_orbits == "equalarmlength-orbits":
        orbits = equalarmlength_orbits()
    elif select_orbits == "esa-trailing-orbits":
        orbits = esa_trailing_orbits()
    elif select_orbits == "esa-leading-orbits":
        orbits = esa_leading_orbits()
    else:
        raise ValueError(f"unknown orbit model: '{select_orbits}'")

    # Write orbits to HDF5 file and plot figures to pdf
    orbits.write(f'../data/{select_orbits}.h5')
    orbits.plot_spacecraft(1, f'../data/pdf/{select_orbits}-sc1.pdf')
    orbits.plot_spacecraft(2, f'../data/pdf/{select_orbits}-sc2.pdf')
    orbits.plot_spacecraft(3, f'../data/pdf/{select_orbits}-sc3.pdf')
    orbits.plot_links(f'../data/pdf/{select_orbits}-links.pdf')


def static_constellation():
    """Generation `StaticConstellation` plot."""
    keplerian = keplerian_orbits()
    return lisaorbits.StaticConstellation.from_orbits(keplerian)


def keplerian_orbits():
    """Generate `KeplerianOrbits` plot."""
    return lisaorbits.KeplerianOrbits(L=conf_var.global_kepler_L, a=conf_var.global_kepler_a,
                                       lambda1=conf_var.global_kepler_lambda1,
                                       m_init1=conf_var.global_m_init1,
                                       kepler_order=conf_var.global_kepler_order)


def equalarmlength_orbits():
    """Generate `EqualArmlengthOrbits` plot."""
    return lisaorbits.EqualArmlengthOrbits(L = conf_var.global_kepler_L, a=conf_var.global_kepler_a,
                                           lambda1=conf_var.global_kepler_lambda1,
                                           m_init1=conf_var.global_m_init1,
                                           )


def esa_trailing_orbits():
    """Generate `OEMOrbits` plot from trailing ESA orbits."""
    return lisaorbits.OEMOrbits.from_included('esa-trailing')


def esa_leading_orbits():
    """Generate `OEMOrbits` plot from leading ESA orbits."""
    return lisaorbits.OEMOrbits.from_included('esa-leading')

def readOEMOrbits():
    return lisaorbits.OEMOrbits(oem_1= conf_var.global_oem_file_1,
                                oem_2= conf_var.global_oem_file_2,
                                oem_3= conf_var.global_oem_file_3)




if __name__ == '__main__':
    main()
