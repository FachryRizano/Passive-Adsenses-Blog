from setuptools import setup, find_packages
import shutil, os
setup(name = 'Article', packages = find_packages())
# setup(name = 'Article', packages = find_packages())
# setup(name = 'Article', packages = find_packages())
for folder in os.listdir():
    if folder.endswith('egg-info') or folder == 'build' or folder =='dist':
        shutil.rmtree(folder)