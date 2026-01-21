import configparser

############# Orbits types #############
global_orbit_type = "readOEMOrbits"
############# OEM Orbits types parameters #############
global_oem_file_1 = "../data/TianQinOrbit_120days_UTC/FullForce100935km_85.7deg-EphemerisFile_SC1-50s.oem"
global_oem_file_2 = "../data/TianQinOrbit_120days_UTC/FullForce100935km_85.7deg-EphemerisFile_SC2-50s.oem"
global_oem_file_3 = "../data/TianQinOrbit_120days_UTC/FullForce100935km_85.7deg-EphemerisFile_SC3-50s.oem"
global_kepler_a = 149597870700.0
global_kepler_L = 1E8
global_kepler_order = 2
global_m_init1 = 0
global_kepler_lambda1 = 0

def get_config(filename_path = './orbits.ini'):
    global global_orbit_type, global_oem_file_1, global_oem_file_2, global_oem_file_3, \
        global_kepler_a, global_kepler_L, global_kepler_order, global_m_init1, global_kepler_lambda1

    conf_class = configparser.ConfigParser()

    conf_class.read(filename_path)
    ############# Orbits types #############
    global_orbit_type = str(conf_class.get("orbits_types", 'orbit_type'))
    ############# "readOEMOrbits" parameters #############
    global_oem_file_1 = str(conf_class.get("orbits_parameters", 'oem_file_1'))
    global_oem_file_2 = str(conf_class.get("orbits_parameters", 'oem_file_2'))
    global_oem_file_3 = str(conf_class.get("orbits_parameters", 'oem_file_3'))
    ############# "static-constellation","keplerian-orbits" parameters #############
    global_kepler_a = float(conf_class.get("orbits_parameters", 'kepler_a'))
    global_kepler_L = float(conf_class.get("orbits_parameters", 'kepler_L'))
    global_kepler_order = int(conf_class.get("orbits_parameters", 'kepler_order'))
    global_m_init1 = float(conf_class.get("orbits_parameters", 'm_init1'))
    global_kepler_lambda1 = float(conf_class.get("orbits_parameters", 'kepler_lambda1'))




if __name__ == '__main__':
    filename_path = 'orbits.ini'
    get_config(filename_path)

