#!/bin/bash
# This script packages specific XML files into a tar.gz archive.
tar -czvf xml_files.tar.gz \
    ./lisa_sim/lisaglitch-1.3/glitches.xml \
    ./lisa_sim/testsInstrument/instrument.xml \
    ./lisa_sim/testorbits/orbits.xml \
    ./lisa_sim/tests-gw-response/gw_response.xml
