#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 15:37:57 2023

@author: apschram
"""
from setuptools import setup, find_packages

setup(
    name='pff_physical_metrics_api',
    version='0.1',
    description='PFF Physical Metrics API for Python',
    author='PFF FC',
    author_email='fchelp@pff.com',
    url='https://github.com/pro-football-focus/pff_physical_metrics_api/',
    packages=find_packages(),  # Use find_packages to automatically discover and include all packages
    install_requires=['pandas', 'requests']
)