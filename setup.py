# -*- coding: utf-8 -*-

from setuptools import setup
setup(name='patient-alloc',
      version='0.1',
      description='Handle database for patient allocation',
      url='https://github.com/Ruijan/PatientAllocationSinergia',
      author='Julien Rechenmann',
      author_email='julien.rechenmann@epfl.ch',
      license='MIT',
      packages=['patientalloc', 'patientalloc.src.Database', 'patientalloc.src.GUI'],
      install_requires=[
          'pyyaml',
          'scipy',
          'appjar'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/patient-alloc'],
      include_package_data=True,
      zip_safe=False)
