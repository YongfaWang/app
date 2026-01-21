import configparser


# Sampling parameters
global_size=1200
global_dt=1/4
global_t0='orbits'
# Physics simulation sampling and filtering
global_physics_upsampling=4
global_aafilter=('kaiser', 240, 1.1, 2.9)
# Telemetry sampling
global_telemetry_downsampling=86400 * 4
global_initial_telemetry_size=0
# Inter-spacecraft propagation
global_orbits='static'
global_orbit_dataset='tps/ppr'
global_gws=None
global_interpolation=('lagrange', 31)
# Artifacts
global_glitches=None
# Laser locking and frequency plan
global_lock='N1-12'
global_fplan='static'
global_laser_asds=30
global_laser_shape='white+infrared'
global_central_freq=2.816E14
global_offset_freqs='default'
# Laser phase modulation
global_modulation_asds='default'
global_modulation_freqs='default'
global_tdir_modulations=None
# Clocks
global_clock_asds=6.32E-14
global_clock_offsets=0
global_clock_freqoffsets='default'
global_clock_freqlindrifts='default'
global_clock_freqquaddrifts='default'
# Clock inversion
global_clockinv_tolerance=1E-10
global_clockinv_maxiter=5
# Optical pathlength noises
global_backlink_asds=3E-12
global_global_backlink_fknees=2E-3
global_testmass_asds=2.4E-15
global_testmass_fknees=0.4E-3
global_testmass_fbreak=8E-3
global_testmass_shape='original'
global_testmass_frelax=0.8E-4
global_oms_asds=(6.35E-12, 1.25E-11, 1.42E-12, 3.38E-12, 3.32E-12, 7.90E-12)
global_oms_fknees=2E-3
# MOC time correlation
global_moc_time_correlation_asds=0.42
# Angular jitters
global_mosa_longitudinal_jitter_asds = 2E-9
global_sc_angular_jitter_asds=(5E-9, 5E-9, 5E-9)
global_sc_angular_jitter_fknees=(8E-4, 8E-4, 8E-4)
global_mosa_angular_jitter_asds=(5E-9, 1e-9)
global_mosa_angular_jitter_fknees=(8E-4, 8E-4)
global_mosa_angles='default'
# Tilt-to-length (TTL)
global_ttl_coeffs='default'
global_dws_asds=7E-8/335
# Pseudo-ranging
global_ranging_biases=0
global_ranging_asds=3E-9
global_prn_ambiguity=None
# Electronic delays
global_electro_delays=(0, 0, 0)
# Concurrency
global_concurrent=False
# Disable noises
global_keep_noises=None
global_keep_dopplers_noise = True




def get_config(filename_path = './instrument.ini'):
    global global_size, global_dt, global_t0, global_physics_upsampling, global_aafilter, global_telemetry_downsampling, \
    global_initial_telemetry_size, global_orbits, global_orbit_dataset, global_gws, global_interpolation, global_glitches, \
    global_lock, global_fplan, global_laser_asds, global_laser_shape, global_central_freq, global_offset_freqs, global_modulation_asds, \
    global_modulation_freqs, global_tdir_modulations, global_clock_asds, global_clock_offsets, global_clock_freqoffsets, global_clock_freqlindrifts, \
    global_clock_freqquaddrifts, global_clockinv_tolerance, global_clockinv_maxiter, global_backlink_asds, global_global_backlink_fknees, global_testmass_asds, \
    global_testmass_fknees, global_testmass_fbreak, global_testmass_shape, global_testmass_frelax, global_oms_asds, global_oms_fknees, \
    global_moc_time_correlation_asds, global_sc_angular_jitter_asds, global_sc_angular_jitter_fknees, global_mosa_angular_jitter_asds,global_mosa_angular_jitter_fknees, \
    global_mosa_angles, global_ttl_coeffs, global_dws_asds, global_ranging_biases, global_ranging_asds, global_prn_ambiguity, global_electro_delays, global_concurrent, global_disable_noises, \
    global_keep_dopplers_noise

    conf_class = configparser.ConfigParser()

    conf_class.read(filename_path)
    # Sampling parameters
    global_size = int(conf_class.get('instrument_init', 'size'))
    global_dt = float(conf_class.get('instrument_init', 'dt'))
    global_t0 = str(conf_class.get('instrument_init', 't0'))
    if global_t0 == "None":
        global_t0 = None
    # Physics simulation sampling and filtering
    global_physics_upsampling = float(conf_class.get('instrument_init', 'physics_upsampling'))
    global_aafilter = eval(conf_class.get('instrument_init', 'aafilter'))
    # Telemetry sampling
    global_telemetry_downsampling = float(conf_class.get('instrument_init', 'telemetry_downsampling'))
    global_initial_telemetry_size = int(conf_class.get('instrument_init', 'initial_telemetry_size'))
    # Inter-spacecraft propagation
    global_orbits = str(conf_class.get('instrument_init', 'orbits'))
    if global_orbits == "None":
        global_orbits = None
    global_orbit_dataset = str(conf_class.get('instrument_init', 'orbit_dataset'))
    global_gws = str(conf_class.get('instrument_init', 'gws'))
    if global_gws == "None":
        global_gws = None
    global_interpolation = eval(conf_class.get('instrument_init', 'interpolation'))
    # Artifacts
    global_glitches = str(conf_class.get('instrument_init', 'glitches'))
    if global_glitches == "None":
        global_glitches = None
    # Laser locking and frequency plan
    global_lock = str(conf_class.get('instrument_init', 'lock'))
    global_fplan = str(conf_class.get('instrument_init', 'fplan'))
    global_laser_asds = float(conf_class.get('instrument_init', 'laser_asds'))
    global_laser_shape = str(conf_class.get('instrument_init', 'laser_shape'))
    global_central_freq = float(conf_class.get('instrument_init', 'central_freq'))
    global_offset_freqs = str(conf_class.get('instrument_init', 'offset_freqs'))
    if global_offset_freqs != "default":
        global_offset_freqs = float(conf_class.get('instrument_init', 'offset_freqs'))
    # Laser phase modulation
    global_modulation_asds = str(conf_class.get('instrument_init', 'modulation_asds'))
    global_modulation_freqs = str(conf_class.get('instrument_init', 'modulation_freqs'))
    global_tdir_modulations = str(conf_class.get('instrument_init', 'tdir_modulations'))
    if global_tdir_modulations == "None":
        global_tdir_modulations = None
    # Clocks
    global_clock_asds = float(conf_class.get('instrument_init', 'clock_asds'))
    global_clock_offsets = float(conf_class.get('instrument_init', 'clock_offsets'))
    global_clock_freqoffsets = str(conf_class.get('instrument_init', 'clock_freqoffsets'))
    global_clock_freqlindrifts = str(conf_class.get('instrument_init', 'clock_freqlindrifts'))
    global_clock_freqquaddrifts = str(conf_class.get('instrument_init', 'clock_freqquaddrifts'))
    if global_clock_freqoffsets != "default":
        global_clock_freqoffsets = float(conf_class.get('instrument_init', 'clock_freqoffsets'))
    if global_clock_freqlindrifts != "default":
        global_clock_freqlindrifts = float(conf_class.get('instrument_init', 'clock_freqlindrifts'))
    if global_clock_freqquaddrifts != "default":
        global_clock_freqquaddrifts = float(conf_class.get('instrument_init', 'clock_freqquaddrifts'))
    # Clock inversion
    global_clockinv_tolerance = float(conf_class.get('instrument_init', 'clockinv_tolerance'))
    global_clockinv_maxiter = float(conf_class.get('instrument_init', 'clockinv_maxiter'))
    # Optical pathlength noises
    global_backlink_asds = float(conf_class.get('instrument_init', 'backlink_asds'))
    global_global_backlink_fknees = float(conf_class.get('instrument_init', 'backlink_fknees'))
    global_testmass_asds = float(conf_class.get('instrument_init', 'testmass_asds'))
    global_testmass_fknees = float(conf_class.get('instrument_init', 'testmass_fknees'))
    global_testmass_fbreak = float(conf_class.get('instrument_init', 'testmass_fbreak'))
    global_testmass_shape = str(conf_class.get('instrument_init', 'testmass_shape'))
    global_testmass_frelax = float(conf_class.get('instrument_init', 'testmass_frelax'))
    global_oms_asds = eval(conf_class.get('instrument_init', 'oms_asds'))
    global_oms_fknees = float(conf_class.get('instrument_init', 'oms_fknees'))
    # MOC time correlation
    global_moc_time_correlation_asds = float(conf_class.get('instrument_init', 'moc_time_correlation_asds'))
    # Angular jitters
    global_sc_angular_jitter_asds = eval(conf_class.get('instrument_init', 'sc_angular_jitter_asds'))
    global_sc_angular_jitter_fknees = eval(conf_class.get('instrument_init', 'sc_angular_jitter_fknees'))
    global_mosa_angular_jitter_asds = eval(conf_class.get('instrument_init', 'mosa_angular_jitter_asds'))
    global_mosa_angular_jitter_fknees = eval(conf_class.get('instrument_init', 'mosa_angular_jitter_fknees'))
    global_mosa_angles = str(conf_class.get('instrument_init', 'mosa_angles'))
    # Tilt-to-length (TTL)
    global_ttl_coeffs = str(conf_class.get('instrument_init', 'ttl_coeffs'))
    global_dws_asds = float(conf_class.get('instrument_init', 'dws_asds'))
    if global_ttl_coeffs != "default":
        global_ttl_coeffs = float(conf_class.get('instrument_init', 'ttl_coeffs'))
    if global_mosa_angles != "default":
        global_mosa_angles = float(conf_class.get('instrument_init', 'mosa_angles'))
    # Pseudo-ranging
    global_ranging_biases = float(conf_class.get('instrument_init', 'ranging_biases'))
    global_ranging_asds = float(conf_class.get('instrument_init', 'ranging_asds'))
    global_prn_ambiguity = str(conf_class.get('instrument_init', 'prn_ambiguity'))
    if global_prn_ambiguity == "None":
        global_prn_ambiguity = None
    # Electronic delays
    global_electro_delays = eval(conf_class.get('instrument_init', 'electro_delays'))
    # Concurrency
    global_concurrent = eval(conf_class.get('instrument_init', 'concurrent'))
    # Disable noises
    global_keep_noises = eval(conf_class.get('instrument_init', 'keep_noises'))
    global_keep_dopplers_noise = eval(conf_class.get('instrument_init', 'keep_dopplers_noise'))


if __name__ == '__main__':
    print(global_size)
    filename_path = 'instrument.ini'
    get_config(filename_path)
    print(global_size)
