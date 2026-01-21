import configparser

############# Orbits types #############
global_gws_type = "galactic-binary-TQ3"
global_orbits_file = "../data/readOEMOrbits.h5"


def get_config(filename_path = './gw_response.ini'):
    global global_gws_type, global_orbits_file
    conf_class = configparser.ConfigParser()

    conf_class.read(filename_path)
    ############# gws types #############
    global_gws_type = str(conf_class.get("gws_types", 'gws_type'))
    ############# gws orbits file #############
    global_orbits_file = str(conf_class.get("gws_parameters", 'orbits_file'))


if __name__ == '__main__':
    filename_path = 'gw_response.ini'
    get_config(filename_path)

