import os
from setuptools import setup, find_packages
from typing import List



# Constants required for setup file
REQUIEMENTS_FILE_PATH = 'requirements.txt'
PROJECT_NAME = "customer-analysis"
VERSION = '0.0.1'
DESC = "This is classification problem on Customer Segmentation"
AUTHOR_NAME = 'Utkarsh Tewari'



def get_requirments_packages() -> List[str]:
    """
    This functions reads the requirements.txt file
    and returns the list of packages mentioned in it.

    Returns
    -------
    list :
        List of all packages mentioned in requirements.txt
    """
    
    try:
        if os.path.exists(REQUIEMENTS_FILE_PATH):
            packages=[]
            with open(REQUIEMENTS_FILE_PATH, 'r') as req:
                for p in req.readlines():
                    if p!=' ' and p!='' and p!='\n':
                        packages.append(p.replace('\n',''))

            return packages[:-1]
        else:
            raise Exception('Requirements file does not exist')
    except Exception as e:
        print("Requirements file does not exist")



setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR_NAME,
    description=DESC,
    packages=find_packages(),
    install_requires=get_requirments_packages(),
    
)