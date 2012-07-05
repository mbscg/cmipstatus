import yaml
import time
import subprocess
import glob
import os

all_info = yaml.load(open('exp_info.yaml', 'r'))

if __name__ == "__main__":
    while True:
        subprocess.call(all_info['scripts']['wget'].split())
        for old_dir in glob.glob('../../media/cmp*'):
            subprocess.call(['rm', '-rf', old_dir])
        for cmpdir in glob.glob('fetched_data/cmip_evaluation/cmp*'):
            subprocess.call(['mv', cmpdir, '../../media'])
        subprocess.call(['rm', '-rf', '../../media/exp_analysis_figures'])
        subprocess.call(['cp', '-r', 'fetched_data/cmip_evaluation/exp_analysis_figures','../../media'])
        time.sleep(1200)
