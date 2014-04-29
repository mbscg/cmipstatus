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


if __name__ == "__main__":
    get_data_from_tupa()
