import os
from setuptools import setup, find_packages
from typing import List

REQUIEMENTS_FILE_PATH = 'requirements.txt'
PROJECT_NAME = "customer-analysis"
VERSION = '0.0.1'
DESC = "This is classification problem on Customer Segmentation"
AUTHOR_NAME = 'Utkarsh Tewari'

def get_requirments_packages():
    if os.path.exists(REQUIEMENTS_FILE_PATH):
        packages=[]
        with open(REQUIEMENTS_FILE_PATH, 'r') as req:
            for p in req.readlines():
                packages.append(p.replace('\n',''))
        return packages[:-1]

    else:
        print("Requirements file does not exist")

print(get_requirments_packages())

setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR_NAME,
    description=DESC,
    packages=find_packages(),
    install_requires=get_requirments_packages(),
    
)