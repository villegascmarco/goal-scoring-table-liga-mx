import logging
import subprocess
import os
import glob

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    extract()
    transform()
    load()


def extract():

    subprocess.run(['python', 'main.py'], cwd='./download')

    subprocess.run(['move', r'download\*.csv', r'transform'], shell=True)


def transform():

    for file in glob.glob('transform/*.csv'):
        subprocess.run(
            ['python', 'main.py', file.replace('transform\\', '')], cwd='./transform')
        os.remove(file)
        subprocess.run(['move', r'transform\*.csv', r'upload'],
                       shell=True)


def load():

    for file in glob.glob('upload/*.csv'):
        subprocess.run(
            ['python', 'main.py', file.replace('upload\\', '')], cwd='./upload')
        os.remove(file)


if __name__ == '__main__':
    main()
