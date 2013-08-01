import yaml

def get_tupa_data():
    config_file = open('officeboy.config', 'r')
    config = yaml.load(config_file)
    config_file.close()
    log_file = open(config['qstat_log'], 'r')
    log_text = log_file.readlines()
    log_file.close()
    return log_text

def get_restart_list(fancy_name):
    config_file = open('officeboy.config', 'r')
    config = yaml.load(config_file)
    config_file.close()
    fancy_filename = config['restart_list_template'].format(fancy_name)
    restart_file = open(fancy_filename, 'r')
    restart_list = restart_file.readlines()
    restart_file.close()
    return restart_list
