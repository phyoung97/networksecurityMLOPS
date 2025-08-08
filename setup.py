'''

The setup.py file is an essential part of packaging and distributing Python projects.
 It is used by setuptools (or distutils in older python versions) to define the configuration of your project,
 such as its metadata, dependencies and more

'''

from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """

    This function will return the list of requirements

    """
    requirements_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            #Read line from file
            lines=file.readlines()
            #Porcess each line
            for line in lines:
                requirement=line.strip()
                ## ignore empty lines and -e.
                if requirement and requirement != '-e.':
                    requirements_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
    
    return requirements_lst


setup(
    name="Network Security",
    version = "0.0.1",
    author="Phil Young",
    author_email="Payoung97@outlook.com",
    packages=find_packages(),
    install_requires=get_requirements()
)

            