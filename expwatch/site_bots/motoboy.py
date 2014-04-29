import yaml
import subprocess
import glob
import shutil
import os

motoboy_config = yaml.load(open('motoboy.config','r'))

def get_data_from_tupa():
    subprocess.call(motoboy_config['wget'].split())
    for folder in glob.glob(motoboy_config['fig_folders']):
        if "html" in folder:
            continue
        folder_name = os.path.basename(folder)
        media_destino = motoboy_config['media']
        media_folder = os.path.join(media_destino, folder_name)
        if os.path.exists(media_folder):
            shutil.rmtree(media_folder)
        shutil.move(folder, media_destino)


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
