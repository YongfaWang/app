import sys
sys.path.append("../libs")
from lisainstrument import Instrument
import importlib_metadata
import get_my_conf as conf_var
from get_my_conf import *

def main(flag = 1):
    # Get configuration
    filename_path = 'instrument.ini'
    get_config(filename_path)

    # Instrument
    instrument = Instrument(
        # Sampling parameters
        size = conf_var.global_size,
        dt = conf_var.global_dt,
        t0 = conf_var.global_t0,
        seed= None,
        # Physics simulation sampling and filtering
        physics_upsampling = conf_var.global_physics_upsampling,
        aafilter = conf_var.global_aafilter,
        # Telemetry sampling
        telemetry_downsampling = conf_var.global_telemetry_downsampling,
        initial_telemetry_size = conf_var.global_initial_telemetry_size,
        # Inter-spacecraft propagation
        orbits = conf_var.global_orbits,
        orbit_dataset = conf_var.global_orbit_dataset,
        gws = conf_var.global_gws,
        interpolation = conf_var.global_interpolation,
        # Artifacts
        glitches = conf_var.global_glitches,
        # Laser locking and frequency plan
        lock = conf_var.global_lock,
        fplan = conf_var.global_fplan,
        laser_asds = conf_var.global_laser_asds,
        laser_shape = conf_var.global_laser_shape,
        central_freq = conf_var.global_central_freq,
        offset_freqs= conf_var.global_offset_freqs,
        # Laser phase modulation
        modulation_asds = conf_var.global_modulation_asds,
        modulation_freqs = conf_var.global_modulation_freqs,
        tdir_modulations = conf_var.global_tdir_modulations,
        # Clocks
        clock_asds = conf_var.global_clock_asds,
        clock_offsets = conf_var.global_clock_offsets,
        clock_freqoffsets = conf_var.global_clock_freqoffsets,
        clock_freqlindrifts = conf_var.global_clock_freqlindrifts,
        clock_freqquaddrifts = conf_var.global_clock_freqquaddrifts,
        # Clock inversion
        clockinv_tolerance = conf_var.global_clockinv_tolerance,
        clockinv_maxiter = conf_var.global_clockinv_maxiter,
        # Backlink noises
        backlink_asds = conf_var.global_backlink_asds,
        backlink_fknees = conf_var.global_global_backlink_fknees,
        # Test-mass noise
        testmass_asds = conf_var.global_testmass_asds,
        testmass_fknees = conf_var.global_testmass_fknees,
        testmass_fbreak = conf_var.global_testmass_fbreak,
        testmass_shape = conf_var.global_testmass_shape,
        testmass_frelax = conf_var.global_testmass_frelax,
        # OMS noise
        oms_asds = conf_var.global_oms_asds,
        oms_fknees = conf_var.global_oms_fknees,
        # MOC time correlation
        moc_time_correlation_asds = conf_var.global_moc_time_correlation_asds,
        # Longitudinal jitters
        mosa_longitudinal_jitter_asds = conf_var.global_mosa_longitudinal_jitter_asds,
        # Angular jitters
        sc_angular_jitter_asds = conf_var.global_sc_angular_jitter_asds,
        sc_angular_jitter_fknees =conf_var.global_sc_angular_jitter_fknees,
        mosa_angular_jitter_asds = conf_var.global_mosa_angular_jitter_asds,
        mosa_angular_jitter_fknees = conf_var.global_mosa_angular_jitter_fknees,
        mosa_angles = conf_var.global_mosa_angles,
        # Tilt-to-length coupling
        ttl_coeffs = conf_var.global_ttl_coeffs,
        dws_asds = conf_var.global_dws_asds,
        # Pseudo-ranging
        ranging_biases = conf_var.global_ranging_biases,
        ranging_asds = conf_var.global_ranging_asds,
        prn_ambiguity = conf_var.global_prn_ambiguity,
        # Electronic delays
        electro_delays = conf_var.global_electro_delays,
        # Concurrency
        concurrent = conf_var.global_concurrent
    )
    ### test by xiaogongwei
    instrument.testXgw()

    ## keep conf_var.global_keep_noises noises
    if conf_var.global_keep_noises not in [None]:
        instrument.disable_all_noises(excluding=conf_var.global_keep_noises)
    ## Keep dopplers
    if not conf_var.global_keep_dopplers_noise:
        instrument.disable_dopplers()
    # Write to a measurement file
    instrument.simulate(keep_all=True)
    instrument.write('../data/instrument.h5', mode= 'w', keep_all=True)
    ## plot to pdf
    instrument.plot_offsets(output='../data/pdf/ISI_RFI_TMI_carrier_offsets.pdf', skip=500)
    instrument.plot_fluctuations(output='../data/pdf/ISI_RFI_TMI_carrier_fluctuations.pdf', skip=500)
    instrument.plot_totals(output='../data/pdf/ISI_RFI_TMI_carrier.pdf', skip=500)
    instrument.plot_mprs(output='../data/pdf/measured_mpprs_dmpprs.pdf', skip=500)
    instrument.plot_dws(output='../data/pdf/isi_dws_phis_etas.pdf', skip=500)

def printVer():
    version = importlib_metadata.version('lisainstrument')
    print_ver = "lisainstrument version: " + str(version)
    print(print_ver)


if __name__ == '__main__':
    print("lisainstrument start!!! ")
    printVer()
    main(0)
    print("lisainstrument have end!!! ")

