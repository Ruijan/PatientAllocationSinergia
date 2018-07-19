# Patient Allocator
[![Build Status](https://travis-ci.org/Ruijan/PatientAllocationSinergia.svg?branch=master)](https://travis-ci.org/Ruijan/PatientAllocationSinergia)
[![codecov](https://codecov.io/gh/Ruijan/PatientAllocationSinergia/branch/master/graph/badge.svg)](https://codecov.io/gh/Ruijan/PatientAllocationSinergia)
[![CodeFactor](https://www.codefactor.io/repository/github/ruijan/patientallocationsinergia/badge)](https://www.codefactor.io/repository/github/ruijan/patientallocationsinergia)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5839e54e7307428a8291808e2539c4da)](https://www.codacy.com/app/rechenmann/PatientAllocationSinergia?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Ruijan/PatientAllocationSinergia&amp;utm_campaign=Badge_Grade)

This project aims to sort new patients in different groups in a pseudo-random process and keep non-significant differences between groups.
It allows you to create your database with different fields:
1. Generic field
2. Numeric field
3. List field
4. Hidden field

## Install
First, download the archive from Github: https://github.com/Ruijan/PatientAllocationSinergia. Click on the green icon in the top right corner.
You can also clone the folder with:
```
git clone https://github.com/Ruijan/PatientAllocationSinergia.git
```
You need pip to install the package.
To install the package:

```
pip install .
```

## Launch
To start the allocator for a user open a terminal:
```
patient-alloc
```
or
```
patient-alloc --mode user
```
The user mode allows you to load the database and assign a new patient. The group distribution is hidden and some functionnalities are limited.
To start the allocator for an admin open a terminal:

```
patient-alloc --mode admin
```
The administrator mode gives you the possibility to create a new database and to visualize the distribution of patients.

## Settings
The settings allows you to define if you want to save the database locally or online. To save online the database, you should provide a git url. It can be Github, c4Science, bitbucket or any of the existing server that handles git url. If you use an ssh url, be sure to add the ssh key to your computer before creating the database. 
In order to save the database at the correct place, please provide the folder name where it will be downloaded: pathToFolder + nameOfTheGitFolder. The filename is the filename of the dabase.

## Modify
You are invited to modify the software the way you like it. Remember that coverage tests have been added and you can use them to assess the quality of your modifications. You can run these tests with these commands:
```
pip install .
python3 setup.py tests
```
Please use test-driven development when you apply changes to the code. Check if your modifications don't break previous tests.