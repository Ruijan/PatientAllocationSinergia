# -*- coding: utf-8 -*-

from setuptools import setup
setup(name='patient-alloc',
      version='0.1',
      description='Handle database for patient allocation',
      url='https://github.com/Ruijan/PatientAllocationSinergia',
      author='Julien Rechenmann',
      author_email='julien.rechenmann@epfl.ch',
      license='MIT',
      packages=['patientalloc'],
      install_requires=[
          'pyyaml',
          'scipy',
          'appjar'
      ],
      scripts=['bin/patient-alloc'],
      zip_safe=False)
