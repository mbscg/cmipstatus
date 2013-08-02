from settings import officeboy_configs as config

def get_tupa_data():
    log_file = open(config['qstat_log'], 'r')
    log_text = log_file.readlines()
    log_file.close()
    return log_text

def get_restart_list(fancy_name):
    fancy_filename = config['restart_list_template'].format(fancy_name)
    restart_file = open(fancy_filename, 'r')
    restart_list = restart_file.readlines()
    restart_file.close()
    return restart_list
