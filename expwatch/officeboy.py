import yaml

def get_tupa_data():
    config_file (open('officeboy.config', 'r')
    config = yaml.load(config_file)
    config_file.close()
    log_file = config['qstat_log']
    log_text = log_file.read()
    log_file.close()
    return log_text
    
