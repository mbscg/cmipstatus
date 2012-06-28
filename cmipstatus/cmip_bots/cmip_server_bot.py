import yaml
import time
import subprocess

all_info = yaml.load(open('exp_info.yaml', 'r'))

if __name__ == "__main__":
    while True:
        subprocess.call(all_info['scripts']['wget'].split())
        time.sleep(900)
