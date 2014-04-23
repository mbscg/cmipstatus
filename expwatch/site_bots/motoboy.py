import yaml
import subprocess
import glob
import shutil

motoboy_config = yaml.load(open('motoboy.config','r'))

def get_data_from_tupa():
    subprocess.call(motoboy_config['wget'].split())
    for fig in glob.glob(motoboy_config['fetched_figures']):
        shutil.copy(fig, motoboy_config['static'])

    # Let this here, for future figs
    """
    for old_dir in glob.glob('../../media/cmp*'):
        subprocess.call(['rm', '-rf', old_dir])
    for cmpdir in glob.glob('fetched_data/cmip_evalutation/cmp*'):
        subprocess.call(['mv', cmpdir, '../../media'])
    subprocess.call(['rm', '-rf', '../../media/exp_analysis_figures'])
    subprocess.call(['cp', '-r', 'fetched_data/cmip_evaluation/exp_analysis_figures','../../media'])
    """


if __name__ == "__main__":
    get_data_from_tupa()
