from settings import officeboy_configs as config
from .tupa_bots.quaco.tests import errorcodes


def get_tupa_data():
    """
    retrieves the running stats
    """
    log_file = open(config['qstat_log'], 'r')
    log_text = log_file.readlines()
    log_file.close()
    return log_text


def get_readme():
    """
    retrieves the readme info
    """
    readme_file = open(config['readme'], 'r')
    readme_text = readme_file.readlines()
    readme_file.close()
    return readme_text


def get_restart_list(fancy_name):
    """
    retrieves the restart list for a given exp/member
    """
    fancy_filename = config['restart_list_template'].format(fancy_name)
    try_again = False
    # special case for unique member with _1
    if '_' not in fancy_name:
        fancy_alt = config['restart_list_template'].format(fancy_name+'_1')
        try_again = True

    try:
        restart_file = open(fancy_filename, 'r')
    except:
        if try_again:
            try:
                restart_file = open(fancy_alt, 'r')
            except:
                raise Exception
        else:
            raise Exception

    restart_list = restart_file.readlines()
    restart_file.close()
    return restart_list


def get_fc_log():
    fc_log = open(config['fc_log'], 'r')
    lines = fc_log.readlines()
    fc_log.close()
    for line in lines:
        columns = line.split(',')
        filename = columns[0]
        error_description = errorcodes.descriptions[int(columns[1])]
        log = {'file': filename, 'error': error_description}
        yield(log)

