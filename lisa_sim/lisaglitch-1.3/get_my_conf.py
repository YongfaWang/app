import configparser

############# Glitches types #############
global_glitch_type = "readOEMOrbits"
global_INJECTION_POINTS = ['tm_12', 'tm_23', 'tm_31', 'tm_13', 'tm_32', 'tm_21']
############# Glitches types parameters #############
global_dataSize = 8000
global_time_t0 = 2032084800.0
global_time_inj = 2032084800.0 + 100


def get_config(filename_path ='./glitches.ini'):
    global global_glitch_type, global_INJECTION_POINTS
    conf_class = configparser.ConfigParser()
    conf_class.read(filename_path)
    ############# Glitches types #############
    global_glitch_type = str(conf_class.get("glitches_types", 'glitch_type'))
    global_INJECTION_POINTS = str(conf_class.get("glitches_types", 'INJECTION_POINTS')).split(',')
    for i in range(len(global_INJECTION_POINTS)):
        global_INJECTION_POINTS[i] = ((global_INJECTION_POINTS[i].replace("\n", "")
                                      .replace("(", "").replace(")", "")
                                      .replace("\r\n", "")).replace("'", "")
                                      .replace(" ", ""))
    ############# Glitches types parameters #############
    global_dataSize = int(conf_class.get("glitches_parameters", 'dataSize'))
    global_time_t0 = float(conf_class.get("glitches_parameters", 'time_t0'))
    global_time_inj = float(conf_class.get("glitches_parameters", 'time_inj'))



if __name__ == '__main__':
    filename_path = 'glitches.ini'
    get_config(filename_path)

